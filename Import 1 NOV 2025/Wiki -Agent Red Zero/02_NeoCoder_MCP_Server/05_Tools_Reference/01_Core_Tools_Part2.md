---
title: 01_Core_Tools_Part1 (Part 2 of 2)
category: 05_Tools_Reference
last_updated: 2025-10-25
line_count: 98
status: published
tags: [neocoder, mcp, documentation]
---

## Utility Tools

### get_incarnation_info

Gets information about an incarnation.

**Signature**:
```python
async def get_incarnation_info(
    incarnation_type: str | None = None
) -> dict
```

**Returns**: Incarnation details including description, version, tools, schema

---

### validate_parameters

Validates parameters against template schema.

**Signature**:
```python
def validate_parameters(
    template_keyword: str,
    parameters: dict
) -> dict
```

**Returns**:
```json
{
  "valid": true,
  "errors": [],
  "warnings": []
}
```

---

## Best Practices

### Tool Selection

**Match tools to incarnation**:
```python
# Good: Use incarnation-specific tools
await switch_incarnation("code_analysis")
await analyze_code_structure("src/main.py")

# Avoid: Wrong incarnation for task
await switch_incarnation("knowledge_graph")
await analyze_code_structure("src/main.py")  # Wrong incarnation
```

### Parameter Validation

**Always validate before execution**:
```python
# Validate parameters
validation = await validate_parameters("CODE_ANALYZE", {
    "file_path": "src/auth.py",
    "analysis_depth": 3
})

if validation["valid"]:
    result = await execute_workflow("CODE_ANALYZE", parameters)
else:
    print(f"Validation errors: {validation['errors']}")
```

### Error Handling

**Check success and handle errors**:
```python
result = await create_project(name="MyProject", root_path="/src")

if result["success"]:
    project_id = result["project_id"]
    # Continue with project operations
else:
    error = result.get("error", "Unknown error")
    # Handle error appropriately
```

### Batch Operations

**Use batch tools when available**:
```python
# Good: Batch file addition
files = ["file1.py", "file2.py", "file3.py"]
await add_files_batch(project_id, files)

# Avoid: Loop over individual additions
for file in files:
    await add_file_to_project(project_id, file)
```
