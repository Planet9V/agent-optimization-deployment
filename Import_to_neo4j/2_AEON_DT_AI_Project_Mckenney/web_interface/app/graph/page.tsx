'use client';

// Force dynamic rendering - skip static generation for browser-only libraries
export const dynamic = 'force-dynamic';
export const dynamicParams = true;

import React, { useState, useEffect } from 'react';
import GraphVisualization from '@/components/graph/GraphVisualization';
import GraphFilters from '@/components/graph/GraphFilters';
import NodeDetails from '@/components/graph/NodeDetails';
import { ErrorBoundary, DatabaseConnectionError } from '@/components/error-boundary';
import { Loader2 } from 'lucide-react';

function GraphExplorerPageContent() {
  const [dbConnected, setDbConnected] = useState<boolean | null>(null);
  const [filters, setFilters] = useState({
    nodeTypes: [],
    relationshipTypes: [],
    customers: [],
    tags: [],
    confidenceMin: 0,
    dateRange: null,
  });
  const [layout, setLayout] = useState<'force' | 'hierarchical'>('force');
  const [selectedNode, setSelectedNode] = useState<any>(null);
  const [showQueryBuilder, setShowQueryBuilder] = useState(false);
  const [customQuery, setCustomQuery] = useState('');
  const [savedQueries, setSavedQueries] = useState<Array<{ name: string; query: string }>>([]);

  // Pre-built cybersecurity queries - READ-ONLY, schema-compliant
  const cyberQueries = [
    {
      name: "Critical CVEs",
      query: "MATCH (c:CVE) WHERE c.severity = 'CRITICAL' RETURN c LIMIT 25",
      description: "Show 25 most recent critical vulnerabilities"
    },
    {
      name: "Threat Actor Network",
      query: "MATCH (t:ThreatActor)-[r]-(m:Malware) RETURN t, r, m LIMIT 50",
      description: "Threat actors and their associated malware"
    },
    {
      name: "Attack Techniques",
      query: "MATCH (a:AttackTechnique)-[:PART_OF]->(t:Tactic) RETURN a, t LIMIT 30",
      description: "MITRE ATT&CK techniques by tactic"
    },
    {
      name: "Vulnerable ICS Assets",
      query: "MATCH (i:ICSAsset)-[:HAS_VULNERABILITY]->(v:CVE) WHERE v.cvss_score > 7.0 RETURN i, v LIMIT 25",
      description: "ICS assets with high-severity vulnerabilities"
    },
    {
      name: "CWE Relationships",
      query: "MATCH (cve:CVE)-[:HAS_WEAKNESS]->(cwe:CWE) RETURN cve, cwe LIMIT 50",
      description: "CVEs and their associated CWE weaknesses"
    },
    {
      name: "High-Severity CVEs",
      query: "MATCH (cve:CVE) WHERE cve.cvss_score > 7.0 RETURN cve LIMIT 100",
      description: "All CVEs with CVSS score above 7.0"
    },
    {
      name: "Threat Actor Campaigns",
      query: "MATCH (actor:ThreatActor)-[:CONDUCTS]->(campaign:Campaign) RETURN actor, campaign LIMIT 50",
      description: "Active threat actor campaigns"
    },
    {
      name: "Attack Paths",
      query: "MATCH path=(actor:ThreatActor)-[:USES_TTP]->(technique:AttackTechnique)-[:TARGETS]->(asset) RETURN path LIMIT 50",
      description: "Complete attack paths from threat actors to targets"
    },
    {
      name: "Malware Families",
      query: "MATCH (malware:Malware) RETURN malware.name, labels(malware) LIMIT 50",
      description: "Known malware families and their classifications"
    },
    {
      name: "MITRE ATT&CK Techniques",
      query: "MATCH (technique:AttackTechnique) RETURN technique LIMIT 100",
      description: "All MITRE ATT&CK techniques in the database"
    }
  ];

  // Check database connection on mount
  useEffect(() => {
    checkConnection();
  }, []);

  const checkConnection = async () => {
    try {
      const response = await fetch('/api/health');
      const data = await response.json();

      if (data.neo4j?.connected) {
        setDbConnected(true);
      } else {
        setDbConnected(false);
      }
    } catch (error) {
      console.error('Connection check failed:', error);
      setDbConnected(false);
    }
  };

  const handleFilterChange = (newFilters: any) => {
    setFilters(newFilters);
  };

  const handleLayoutChange = (newLayout: 'force' | 'hierarchical') => {
    setLayout(newLayout);
  };

  const handleNodeClick = (node: any) => {
    setSelectedNode(node);
  };

  const handleCloseDetails = () => {
    setSelectedNode(null);
  };

  const handleExecuteQuery = async () => {
    try {
      const response = await fetch('/api/graph/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: customQuery }),
      });

      const data = await response.json();
      if (data.error) {
        alert(`Query error: ${data.error}`);
      } else {
        alert('Query executed successfully');
        // Refresh the graph
        window.location.reload();
      }
    } catch (error) {
      console.error('Error executing query:', error);
      alert('Failed to execute query');
    }
  };

  const handleSaveQuery = () => {
    const name = prompt('Enter a name for this query:');
    if (!name) return;

    setSavedQueries(prev => [...prev, { name, query: customQuery }]);
    alert('Query saved');
  };

  const handleLoadQuery = (query: string) => {
    setCustomQuery(query);
  };

  // Show connection error if database is not available
  if (dbConnected === false) {
    return <DatabaseConnectionError serviceName="Neo4j" onRetry={checkConnection} />;
  }

  // Show loading state while checking connection
  if (dbConnected === null) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
      </div>
    );
  }

  return (
    <div className="flex h-screen" style={{ backgroundColor: 'var(--background)' }}>
      {/* Filters Panel */}
      <GraphFilters
        onFilterChange={handleFilterChange}
        onLayoutChange={handleLayoutChange}
      />

      {/* Main Graph Area */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="card-modern border-b px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold" style={{ color: 'var(--text-primary)' }}>Graph Explorer</h1>
              <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>
                Visualize and explore knowledge graph relationships
              </p>
            </div>
            <button
              onClick={() => setShowQueryBuilder(!showQueryBuilder)}
              className="btn-primary px-4 py-2 rounded"
            >
              {showQueryBuilder ? 'Hide' : 'Show'} Query Builder
            </button>
          </div>

          {/* Query Builder */}
          {showQueryBuilder && (
            <div className="mt-4 p-4 rounded-lg" style={{ backgroundColor: 'var(--slate-50)' }}>
              <div className="mb-4">
                <label className="block text-sm font-medium mb-2" style={{ color: 'var(--text-secondary)' }}>
                  Pre-built Cybersecurity Queries
                </label>
                <select
                  onChange={(e) => {
                    const selectedQuery = cyberQueries.find(q => q.query === e.target.value);
                    setCustomQuery(e.target.value);
                  }}
                  className="w-full px-3 py-2 text-sm rounded"
                  style={{
                    border: '1px solid var(--border-default)',
                    backgroundColor: 'var(--surface)',
                    color: 'var(--text-primary)'
                  }}
                >
                  <option value="">Select a cybersecurity query template...</option>
                  {cyberQueries.map((cq, idx) => (
                    <option key={idx} value={cq.query} title={cq.description}>
                      {cq.name} - {cq.description}
                    </option>
                  ))}
                </select>
                <p className="mt-1 text-xs" style={{ color: 'var(--text-tertiary)' }}>
                  Quick access to common threat intelligence queries - All queries are READ-ONLY and schema-compliant
                </p>
              </div>
              <div className="mb-2">
                <label className="block text-sm font-medium mb-1" style={{ color: 'var(--text-secondary)' }}>
                  Custom Cypher Query
                </label>
                <textarea
                  value={customQuery}
                  onChange={(e) => setCustomQuery(e.target.value)}
                  className="w-full h-32 px-3 py-2 text-sm rounded font-mono"
                  style={{
                    border: '1px solid var(--border-default)',
                    backgroundColor: 'var(--surface)',
                    color: 'var(--text-primary)'
                  }}
                  placeholder="MATCH (n:Document)-[r:MENTIONS]->(e:Entity) RETURN n, r, e LIMIT 100"
                />
              </div>
              <div className="flex items-center justify-between">
                <div className="flex gap-2">
                  <button
                    onClick={handleExecuteQuery}
                    className="px-4 py-2 rounded text-sm text-white"
                    style={{ backgroundColor: 'var(--success-500)' }}
                  >
                    Execute Query
                  </button>
                  <button
                    onClick={handleSaveQuery}
                    className="px-4 py-2 rounded text-sm"
                    style={{
                      backgroundColor: 'var(--slate-600)',
                      color: 'white'
                    }}
                  >
                    Save Query
                  </button>
                </div>
                {savedQueries.length > 0 && (
                  <select
                    onChange={(e) => handleLoadQuery(e.target.value)}
                    className="px-3 py-2 text-sm rounded"
                    style={{
                      border: '1px solid var(--border-default)',
                      backgroundColor: 'var(--surface)',
                      color: 'var(--text-primary)'
                    }}
                  >
                    <option value="">Load saved query...</option>
                    {savedQueries.map((sq, idx) => (
                      <option key={idx} value={sq.query}>
                        {sq.name}
                      </option>
                    ))}
                  </select>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Graph Visualization */}
        <GraphVisualization
          filters={filters}
          layout={layout}
          onNodeClick={handleNodeClick}
        />
      </div>

      {/* Node Details Panel */}
      <NodeDetails node={selectedNode} onClose={handleCloseDetails} />
    </div>
  );
}

export default function GraphExplorerPage() {
  return (
    <ErrorBoundary fallbackMessage="Graph explorer encountered an error. The database may be unavailable.">
      <GraphExplorerPageContent />
    </ErrorBoundary>
  );
}
