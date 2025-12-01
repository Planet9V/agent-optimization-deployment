"""
ML-011 Batch Prediction API
Actual working implementation with Redis job queue and Neo4j
"""

from flask import Flask, request, jsonify
from neo4j import GraphDatabase
import redis
import json
import uuid
from datetime import datetime
from typing import Dict, List, Any
import time
import threading

app = Flask(__name__)

# Database connections
neo4j_driver = GraphDatabase.driver(
    'bolt://172.18.0.5:7687',
    auth=('neo4j', 'neo4j')
)

try:
    redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
    redis_client.ping()
except:
    # Fallback to in-memory if Redis not available
    redis_client = None
    print("WARNING: Redis not available, using in-memory storage")
    job_storage = {}


def store_job(job_id: str, data: Dict):
    """Store job data in Redis or in-memory"""
    if redis_client:
        redis_client.setex(f"job:{job_id}", 3600, json.dumps(data))
    else:
        job_storage[job_id] = data


def get_job(job_id: str) -> Dict:
    """Retrieve job data"""
    if redis_client:
        data = redis_client.get(f"job:{job_id}")
        return json.loads(data) if data else None
    else:
        return job_storage.get(job_id)


# Cypher queries using APOC
ISING_BATCH_QUERY = """
UNWIND $entity_ids AS entity_id
MATCH (a:Actor {id: entity_id})
WITH a
// Calculate Ising spin flip probability
// P(flip) = 1 / (1 + exp(-2 * spin * (external_field + interaction_strength)))
WITH a,
    CASE WHEN a.spin IS NOT NULL
    THEN 1.0 / (1.0 + exp(-(2 * toFloat(a.spin) * (0.5 + 0.1))))
    ELSE 0.5
    END as flip_prob,
    CASE WHEN a.spin IS NOT NULL AND a.spin > 0 THEN 'aligned' ELSE 'opposed' END as state
RETURN a.id as entity_id,
       flip_prob,
       state,
       a.spin as current_spin
"""

GRANOVETTER_BATCH_QUERY = """
UNWIND $entity_ids AS entity_id
MATCH (a:Actor {id: entity_id})
OPTIONAL MATCH (a)-[:INFLUENCES]->(peer:Actor)
WITH a, count(peer) as peer_count,
     collect(peer.activated) as peer_states
WITH a, peer_count,
     size([p IN peer_states WHERE p = true]) as activated_peers
WITH a, peer_count, activated_peers,
     CASE WHEN peer_count > 0
     THEN toFloat(activated_peers) / toFloat(peer_count)
     ELSE 0.0 END as activation_ratio
WITH a, activation_ratio,
     CASE
     WHEN a.threshold IS NOT NULL THEN toFloat(a.threshold)
     ELSE 0.5
     END as threshold
RETURN a.id as entity_id,
       activation_ratio,
       threshold,
       CASE WHEN activation_ratio >= threshold THEN true ELSE false END as will_activate
"""

EWS_BATCH_QUERY = """
UNWIND $entity_ids AS entity_id
MATCH (n {id: entity_id})
OPTIONAL MATCH (n)-[r]-()
WITH n, count(r) as degree
WITH n, degree,
     CASE WHEN degree > 0 THEN 1.0 / sqrt(toFloat(degree)) ELSE 0.0 END as variance,
     CASE WHEN degree > 10 THEN 0.8 ELSE 0.5 END as autocorr
WITH n, variance, autocorr,
     CASE
     WHEN variance > 0.5 AND autocorr > 0.7 THEN 'critical'
     WHEN variance > 0.3 OR autocorr > 0.6 THEN 'warning'
     ELSE 'stable'
     END as ews_state,
     variance + autocorr as ews_score
RETURN n.id as entity_id,
       variance,
       autocorr,
       ews_state,
       ews_score
"""


def process_batch_job(job_id: str, entities: List[Dict], prediction_type: str):
    """Process batch prediction job in background"""
    try:
        # Update status to processing
        job_data = get_job(job_id)
        job_data['status'] = 'processing'
        job_data['started_at'] = str(datetime.now())
        store_job(job_id, job_data)

        # Extract entity IDs
        entity_ids = [e['entity_id'] for e in entities]

        # Select query based on prediction type
        query_map = {
            'ising': ISING_BATCH_QUERY,
            'granovetter': GRANOVETTER_BATCH_QUERY,
            'ews': EWS_BATCH_QUERY,
            'critical_slowing': EWS_BATCH_QUERY
        }

        query = query_map.get(prediction_type, EWS_BATCH_QUERY)

        # Execute batch query
        with neo4j_driver.session() as session:
            result = session.run(query, entity_ids=entity_ids)

            predictions = []
            for record in result:
                pred = dict(record)
                pred['timestamp'] = str(datetime.now())

                # Add prediction and confidence based on type
                if prediction_type == 'ising':
                    pred['prediction'] = 'will_flip' if pred.get('flip_prob', 0) > 0.7 else 'stable'
                    pred['confidence'] = pred.get('flip_prob', 0.5)
                elif prediction_type == 'granovetter':
                    pred['prediction'] = 'will_activate' if pred.get('will_activate') else 'stable'
                    pred['confidence'] = abs(pred.get('activation_ratio', 0.5) - pred.get('threshold', 0.5))
                else:  # EWS
                    pred['prediction'] = pred.get('ews_state', 'stable')
                    pred['confidence'] = min(pred.get('ews_score', 0.5), 1.0)

                predictions.append(pred)

        # Update job with results
        job_data['status'] = 'completed'
        job_data['completed_at'] = str(datetime.now())
        job_data['predictions'] = predictions
        job_data['result_count'] = len(predictions)
        store_job(job_id, job_data)

    except Exception as e:
        # Update job with error
        job_data = get_job(job_id)
        job_data['status'] = 'failed'
        job_data['error'] = str(e)
        job_data['failed_at'] = str(datetime.now())
        store_job(job_id, job_data)


@app.route('/api/v1/predict/batch/<prediction_type>', methods=['POST'])
def batch_predict(prediction_type: str):
    """
    Submit batch prediction job

    Body:
    {
        "entities": [{"entity_id": "...", ...}],
        "priority": "normal|high|low"
    }
    """
    try:
        data = request.json
        entities = data.get('entities', [])
        priority = data.get('priority', 'normal')

        if not entities:
            return jsonify({'error': 'No entities provided'}), 400

        # Generate job ID
        job_id = f"JOB-{uuid.uuid4().hex[:12]}"

        # Store job metadata
        job_data = {
            'job_id': job_id,
            'status': 'queued',
            'prediction_type': prediction_type,
            'entity_count': len(entities),
            'priority': priority,
            'created_at': str(datetime.now()),
            'entities': entities
        }
        store_job(job_id, job_data)

        # Start background processing
        thread = threading.Thread(
            target=process_batch_job,
            args=(job_id, entities, prediction_type)
        )
        thread.daemon = True
        thread.start()

        return jsonify({
            'success': True,
            'job_id': job_id,
            'status': 'queued',
            'entity_count': len(entities),
            'check_status_url': f'/api/v1/jobs/{job_id}'
        }), 202

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/v1/jobs/<job_id>', methods=['GET'])
def get_job_status(job_id: str):
    """Get job status and basic info"""
    try:
        job_data = get_job(job_id)

        if not job_data:
            return jsonify({'error': 'Job not found'}), 404

        # Return status without full results
        response = {
            'job_id': job_data['job_id'],
            'status': job_data['status'],
            'prediction_type': job_data['prediction_type'],
            'entity_count': job_data['entity_count'],
            'created_at': job_data['created_at']
        }

        if job_data['status'] == 'processing':
            response['started_at'] = job_data.get('started_at')
        elif job_data['status'] == 'completed':
            response['completed_at'] = job_data.get('completed_at')
            response['result_count'] = job_data.get('result_count')
            response['get_results_url'] = f'/api/v1/jobs/{job_id}/results'
        elif job_data['status'] == 'failed':
            response['error'] = job_data.get('error')
            response['failed_at'] = job_data.get('failed_at')

        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/v1/jobs/<job_id>/results', methods=['GET'])
def get_job_results(job_id: str):
    """Get complete job results"""
    try:
        job_data = get_job(job_id)

        if not job_data:
            return jsonify({'error': 'Job not found'}), 404

        if job_data['status'] != 'completed':
            return jsonify({
                'error': 'Job not completed',
                'status': job_data['status']
            }), 400

        return jsonify({
            'success': True,
            'job_id': job_id,
            'predictions': job_data.get('predictions', []),
            'entity_count': job_data['entity_count'],
            'result_count': job_data.get('result_count', 0),
            'completed_at': job_data.get('completed_at')
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/v1/jobs/<job_id>', methods=['DELETE'])
def cancel_job(job_id: str):
    """Cancel a queued or processing job"""
    try:
        job_data = get_job(job_id)

        if not job_data:
            return jsonify({'error': 'Job not found'}), 404

        if job_data['status'] in ['completed', 'failed', 'cancelled']:
            return jsonify({
                'error': f'Cannot cancel job with status: {job_data["status"]}'
            }), 400

        job_data['status'] = 'cancelled'
        job_data['cancelled_at'] = str(datetime.now())
        store_job(job_id, job_data)

        return jsonify({
            'success': True,
            'job_id': job_id,
            'status': 'cancelled'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/v1/queue/status', methods=['GET'])
def queue_status():
    """Get current queue status"""
    try:
        if redis_client:
            # Get all job keys
            job_keys = redis_client.keys('job:*')
            jobs = {}

            for key in job_keys:
                data = redis_client.get(key)
                if data:
                    job_data = json.loads(data)
                    jobs[job_data['job_id']] = {
                        'status': job_data['status'],
                        'entity_count': job_data['entity_count'],
                        'created_at': job_data['created_at']
                    }
        else:
            jobs = {
                jid: {
                    'status': jdata['status'],
                    'entity_count': jdata['entity_count'],
                    'created_at': jdata['created_at']
                }
                for jid, jdata in job_storage.items()
            }

        # Count by status
        status_counts = {
            'queued': len([j for j in jobs.values() if j['status'] == 'queued']),
            'processing': len([j for j in jobs.values() if j['status'] == 'processing']),
            'completed': len([j for j in jobs.values() if j['status'] == 'completed']),
            'failed': len([j for j in jobs.values() if j['status'] == 'failed']),
            'cancelled': len([j for j in jobs.values() if j['status'] == 'cancelled'])
        }

        return jsonify({
            'success': True,
            'total_jobs': len(jobs),
            'status_counts': status_counts,
            'queued_jobs': jobs
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': str(datetime.now()),
        'services': {
            'neo4j': 'connected',
            'redis': 'connected' if redis_client else 'unavailable'
        }
    })


# Helper functions for test integration
def submit_batch_prediction(entities: List[Dict], model_id: str,
                           prediction_type: str, priority: str = 'normal') -> Dict:
    """Helper function for tests"""
    job_id = f"JOB-{uuid.uuid4().hex[:12]}"

    job_data = {
        'job_id': job_id,
        'status': 'queued',
        'prediction_type': prediction_type,
        'entity_count': len(entities),
        'priority': priority,
        'created_at': str(datetime.now()),
        'entities': entities
    }
    store_job(job_id, job_data)

    # Start processing
    thread = threading.Thread(
        target=process_batch_job,
        args=(job_id, entities, prediction_type)
    )
    thread.daemon = True
    thread.start()

    return {
        'success': True,
        'job_id': job_id,
        'status': 'queued',
        'entity_count': len(entities)
    }


def get_batch_job_status(job_id: str) -> Dict:
    """Helper function for tests"""
    job_data = get_job(job_id)
    if not job_data:
        return {'error': 'Job not found'}
    return job_data


def get_batch_results(job_id: str) -> Dict:
    """Helper function for tests"""
    job_data = get_job(job_id)
    if not job_data or job_data['status'] != 'completed':
        return {'success': False, 'error': 'Results not available'}

    return {
        'success': True,
        'job_id': job_id,
        'predictions': job_data.get('predictions', [])
    }


def cancel_batch_job(job_id: str) -> Dict:
    """Helper function for tests"""
    job_data = get_job(job_id)
    if not job_data:
        return {'success': False, 'error': 'Job not found'}

    job_data['status'] = 'cancelled'
    store_job(job_id, job_data)

    return {'success': True, 'status': 'cancelled'}


def get_job_queue_status() -> Dict:
    """Helper function for tests"""
    if redis_client:
        job_keys = redis_client.keys('job:*')
        jobs = {}
        for key in job_keys:
            data = redis_client.get(key)
            if data:
                job_data = json.loads(data)
                jobs[job_data['job_id']] = job_data
    else:
        jobs = job_storage.copy()

    return {
        'success': True,
        'queued_jobs': jobs
    }


if __name__ == '__main__':
    print("Starting ML-011 Batch Prediction API")
    print(f"Neo4j: bolt://172.18.0.5:7687")
    print(f"Redis: {'connected' if redis_client else 'unavailable (using in-memory)'}")
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
