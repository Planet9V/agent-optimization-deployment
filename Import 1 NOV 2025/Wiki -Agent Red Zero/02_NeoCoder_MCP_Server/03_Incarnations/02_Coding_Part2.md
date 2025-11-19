---
title: 1. Create project (Part 2 of 2)
category: 03_Incarnations
last_updated: 2025-10-25
line_count: 110
status: published
tags: [neocoder, mcp, documentation]
---

## Common Workflows

### Project Setup Workflow

```python
# 1. Create project
project_result = await create_project(
    name="AuthService",
    root_path="/src/auth-service",
    description="User authentication microservice"
)
project_id = project_result["project_id"]

# 2. Add directory structure
await add_directory_to_project(
    project_id=project_id,
    directory_path="src",
    recursive=True
)

# 3. Add individual files
files = ["src/main.py", "src/auth.py", "tests/test_auth.py"]
for file_path in files:
    await add_file_to_project(
        project_id=project_id,
        file_path=file_path,
        language="Python"
    )

# 4. Update project metadata
await update_project_metadata(
    project_id=project_id,
    metadata={
        "language": "Python",
        "framework": "FastAPI",
        "version": "1.0.0"
    },
    tags=["microservice", "auth"]
)
```

### Build and Deploy Workflow

```python
# 1. Create build template (if not exists)
await create_action_template(
    keyword="BUILD_AND_DEPLOY",
    description="Build project and deploy to staging",
    cypher_query=build_deploy_cypher,
    guidance="Use for deployment workflows",
    parameters={
        "project_id": "string",
        "environment": "string"
    }
)

# 2. Execute workflow
result = await execute_workflow(
    template_keyword="BUILD_AND_DEPLOY",
    parameters={
        "project_id": project_id,
        "environment": "staging"
    }
)

# 3. Check execution status
if result["status"] == "completed":
    print("Deployment successful")
else:
    print(f"Deployment failed: {result.get('error')}")

# 4. Review execution history
history = await get_workflow_history(
    project_id=project_id,
    template_keyword="BUILD_AND_DEPLOY",
    limit=10
)
```

### Code Modification Tracking

```python
# 1. Record pre-modification state
pre_hash = calculate_file_hash("src/auth.py")

# 2. Perform modification (external operation)
# ... edit file ...

# 3. Record post-modification state
post_hash = calculate_file_hash("src/auth.py")

# 4. Update file in graph
await update_file_metadata(
    file_path="src/auth.py",
    content_hash=post_hash,
    modification_type="refactor"
)

# 5. Create workflow execution record
await execute_workflow(
    template_keyword="CODE_MODIFY",
    parameters={
        "file_path": "src/auth.py",
        "change_type": "refactor",
        "pre_hash": pre_hash,
        "post_hash": post_hash
    }
)
```
