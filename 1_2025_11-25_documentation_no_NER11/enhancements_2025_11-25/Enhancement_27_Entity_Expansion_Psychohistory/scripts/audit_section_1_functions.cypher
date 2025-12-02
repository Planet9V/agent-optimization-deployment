// SECTION 1: CUSTOM FUNCTION VERIFICATION

// 1.1 List all custom functions
CALL apoc.custom.list()
YIELD name, description
RETURN 'FUNCTION_LIST' as audit_section,
       name, description;
