---
title: Creating Workflow Templates (Part 1 of 2)
category: 07_Development
last_updated: 2025-10-25
line_count: 461
status: published
tags: [neocoder, mcp, documentation]
---


# Creating Workflow Templates

[← Back to Creating Tools](01_Creating_Tools.md) | [Next: Contributing →](03_Contributing.md)

## Overview

Workflow templates (ActionTemplates) define reusable automation patterns in NeoCoder. This guide covers template design, implementation, testing, and versioning strategies.

## Template Architecture

### Template Structure

```cypher
CREATE (template:ActionTemplate {
  keyword: 'FEATURE',
  description: 'Add new feature with tests and documentation',
  isCurrent: true,
  version: '1.0.0',
  cypher: '...',  // Template implementation
  guidance: '...',  // User guidance text
  parameters: {
    feature_name: 'string',
    feature_type: 'string',
    test_coverage_required: 'boolean'
  },
  category: 'development',
  tags: ['development', 'feature', 'testing'],
  created: datetime(),
  updated: datetime()
})
```

### Template Components

**Keyword**: Unique identifier for template activation
- **Format**: UPPERCASE_SNAKE_CASE
- **Examples**: `CODE_ANALYZE`, `FEATURE`, `KNOWLEDGE_QUERY`
- **Uniqueness**: Must be unique across all templates

**Description**: Human-readable template purpose
- **Length**: 50-200 characters
- **Content**: Clear, action-oriented description
- **Example**: "Analyze code structure and generate AST/ASG representation"

**Cypher**: Template execution logic
- **Type**: Multi-line Cypher query
- **Parameters**: Use $param_name for dynamic values
- **Returns**: Standardized result format

**Guidance**: AI assistant instructions
- **Purpose**: Guide LLM in template usage
- **Format**: Structured text with examples
- **Content**: Context, parameters, expected outcomes

## Creating Templates

### Step 1: Define Template Purpose

```yaml
template_definition:
  keyword: "DEPLOY"
  purpose: "Deploy project to production environment"
  scope: "Single project deployment with validation"
  prerequisites:
    - Project with tested code
    - Deployment configuration present
    - Access to deployment environment
  outcomes:
    - Code deployed to production
    - Deployment verified
    - Rollback plan documented
```

### Step 2: Design Parameters

```json
{
  "parameters": {
    "project_id": {
      "type": "string",
      "description": "Project UUID to deploy",
      "required": true,
      "validation": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
    },
    "environment": {
      "type": "string",
      "description": "Target environment",
      "required": true,
      "enum": ["staging", "production"],
      "default": "staging"
    },
    "rollback_enabled": {
      "type": "boolean",
      "description": "Enable automatic rollback on failure",
      "required": false,
      "default": true
    },
    "validation_steps": {
      "type": "array",
      "description": "Post-deployment validation checks",
      "required": false,
      "items": {
        "type": "string",
        "enum": ["health_check", "smoke_test", "integration_test"]
      }
    }
  }
}
```

### Step 3: Implement Cypher Logic

```cypher
// DEPLOY template implementation
MATCH (p:Project {id: $project_id})

// Create deployment execution record
CREATE (exec:WorkflowExecution {
  id: randomUUID(),
  workflow_keyword: 'DEPLOY',
  project_id: $project_id,
  status: 'in_progress',
  started: datetime(),
  parameters: $parameters
})

// Get project files for deployment
MATCH (p)-[:HAS_FILE]->(file:File)
WHERE file.status = 'ready'

// Create deployment nodes
CREATE (deployment:Deployment {
  id: randomUUID(),
  project_id: $project_id,
  environment: $environment,
  version: p.version,
  files_count: count(file),
  rollback_enabled: $rollback_enabled,
  status: 'deploying',
  deployed_at: datetime()
})

// Link deployment to execution
CREATE (exec)-[:RESULTED_IN]->(deployment)

// Track deployment files
WITH deployment, collect(file) as files
UNWIND files as f
CREATE (deployment)-[:INCLUDES_FILE]->(f)

// Set execution status
WITH exec, deployment
SET exec.status = 'completed',
    exec.completed = datetime(),
    exec.result = {
      deployment_id: deployment.id,
      environment: $environment,
      files_deployed: size(files),
      rollback_available: $rollback_enabled
    }

RETURN exec, deployment
```

### Step 4: Write Guidance

```markdown
# DEPLOY Template Guidance

## Purpose
Deploy a project to a target environment with automated validation and rollback capabilities.

## Usage
```
User: "Deploy project X to staging"
Assistant: I'll use the DEPLOY template with:
- project_id: [lookup project X]
- environment: staging
- rollback_enabled: true
- validation_steps: [health_check, smoke_test]
```

## Parameters

**project_id** (required)
- Project UUID to deploy
- Verify project exists and has ready files
- Check for deployment configuration

**environment** (required)
- Target: 'staging' or 'production'
- Staging: Use for testing before production
- Production: Requires additional validation

**rollback_enabled** (optional, default: true)
- Enable automatic rollback on deployment failure
- Recommended: Always true for production
- Can disable for staging/testing environments

**validation_steps** (optional)
- Post-deployment checks to run
- Available: health_check, smoke_test, integration_test
- Recommended: At least health_check

## Pre-deployment Checks
1. Verify all tests passing
2. Check deployment configuration exists
3. Ensure target environment accessible
4. Confirm rollback capability if enabled

## Post-deployment Steps
1. Execute validation_steps
2. Monitor deployment health
3. Document deployment in changelog
4. Prepare rollback instructions

## Error Handling
- If deployment fails: Trigger rollback if enabled
- If validation fails: Report issues, do not rollback automatically
- Document all failures for troubleshooting
```

## Template Categories

### Development Templates

```yaml
FIX:
  category: development
  purpose: Bug fixing with root cause analysis
  requires: [bug_description, affected_files]

REFACTOR:
  category: development
  purpose: Code improvement without behavior change
  requires: [target_code, refactor_goals]

FEATURE:
  category: development
  purpose: New feature implementation
  requires: [feature_spec, acceptance_criteria]
```

### Analysis Templates

```yaml
CODE_ANALYZE:
  category: analysis
  purpose: Code structure and complexity analysis
  requires: [file_path, analysis_depth]

KNOWLEDGE_QUERY:
  category: analysis
  purpose: Query knowledge graph
  requires: [query_text, result_limit]

RESEARCH_ANALYZE:
  category: analysis
  purpose: Research paper analysis
  requires: [paper_id, analysis_focus]
```

### Knowledge Templates

```yaml
KNOWLEDGE_EXTRACT:
  category: knowledge
  purpose: Extract entities from documents
  requires: [document_path, entity_types]

KNOWLEDGE_LINK:
  category: knowledge
  purpose: Create knowledge relationships
  requires: [source_id, target_id, relationship_type]

SYNTHESIZE:
  category: knowledge
  purpose: F-Contraction knowledge synthesis
  requires: [source_ids, synthesis_method]
```

## Versioning Strategy

### Semantic Versioning

```yaml
version_format: "MAJOR.MINOR.PATCH"

MAJOR: Breaking changes
  - Parameter changes (removal, type change)
  - Cypher logic fundamental changes
  - Output format changes

MINOR: New features
  - New optional parameters
  - Enhanced functionality
  - Additional output fields

PATCH: Bug fixes
  - Error handling improvements
  - Performance optimizations
  - Documentation updates
```

### Version Management

```cypher
// Create new template version
MATCH (old:ActionTemplate {keyword: 'FEATURE', isCurrent: true})

// Mark old version as superseded
SET old.isCurrent = false,
    old.superseded_at = datetime()

// Create new version
CREATE (new:ActionTemplate {
  keyword: 'FEATURE',
  version: '2.0.0',
  isCurrent: true,
  description: 'Enhanced feature template with auto-testing',
  cypher: '...',  // Updated implementation
  guidance: '...',  // Updated guidance
  created: datetime()
})

// Link versions
CREATE (new)-[:SUPERSEDES]->(old)

RETURN new, old
```

### Migration Scripts

```python
async def migrate_template_executions(
    old_version: str,
    new_version: str,
    keyword: str
) -> Dict:
    """Migrate template executions to new version."""

    async with neo4j_session() as session:
        # Find executions using old version
        result = await session.run("""
            MATCH (exec:WorkflowExecution {workflow_keyword: $keyword})
            WHERE exec.template_version = $old_version
            RETURN count(exec) as execution_count
        """, {
            "keyword": keyword,
            "old_version": old_version
        })

        count = (await result.single())["execution_count"]

        # Update to new version if compatible
        await session.run("""
            MATCH (exec:WorkflowExecution {workflow_keyword: $keyword})
            WHERE exec.template_version = $old_version
            SET exec.template_version = $new_version,
                exec.migrated_at = datetime()
        """, {
            "keyword": keyword,
            "old_version": old_version,
            "new_version": new_version
        })

        return {
            "success": True,
            "migrated_count": count,
            "message": f"Migrated {count} executions to v{new_version}"
        }
```

## Testing Templates

### Unit Testing

```python
@pytest.mark.asyncio
async def test_deploy_template_execution():
    """Test DEPLOY template execution."""

    # Setup test project
    async with neo4j_session() as session:
        await session.run("""
            CREATE (p:Project {
              id: 'test-project-uuid',
              name: 'Test Project',
              version: '1.0.0'
            })
            CREATE (f:File {
              id: 'test-file-uuid',
              path: 'src/main.py',
              status: 'ready'
            })
            CREATE (p)-[:HAS_FILE]->(f)
        """)

    # Execute template
    result = await execute_workflow(
        keyword='DEPLOY',
        parameters={
            'project_id': 'test-project-uuid',
            'environment': 'staging',
            'rollback_enabled': True
        }
    )

    assert result["success"] is True
    assert "deployment_id" in result

    # Verify deployment created
    async with neo4j_session() as session:
        verify = await session.run("""
            MATCH (d:Deployment {project_id: 'test-project-uuid'})
            RETURN d.environment as env, d.files_count as count
        """)

        record = await verify.single()
        assert record["env"] == "staging"
        assert record["count"] == 1
```

### Integration Testing

```python
@pytest.mark.integration
async def test_template_with_real_project():
    """Test template with actual project deployment."""

    # Create real project structure
    project_id = await create_test_project(
        name="Integration Test Project",
        files=[
            "src/app.py",
            "tests/test_app.py",
            "requirements.txt"
        ]
    )

    # Execute deployment template
    result = await execute_workflow(
        keyword='DEPLOY',
        parameters={
            'project_id': project_id,
            'environment': 'staging',
            'validation_steps': ['health_check', 'smoke_test']
        }
    )

    assert result["success"] is True

    # Verify deployment artifact
    deployment_id = result["deployment_id"]
    deployment = await get_deployment(deployment_id)

    assert deployment["status"] == "deployed"
    assert deployment["validated"] is True
```
