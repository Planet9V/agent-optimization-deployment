// ═══════════════════════════════════════════════════════════════
// COMPLETE POST-FIX AUDIT - Testing Actual Database State
// ═══════════════════════════════════════════════════════════════

// 1. FUNCTION COUNT
CALL apoc.custom.list()
YIELD name
RETURN 'SECTION_1_FUNCTIONS' as section,
       count(*) as total_functions,
       11 as expected_minimum,
       CASE WHEN count(*) >= 11 THEN 'PASS' ELSE 'FAIL' END as status;

// 2. LIST ALL FUNCTIONS
CALL apoc.custom.list()
YIELD name, description
RETURN 'FUNCTION_DETAIL' as section,
       name, description
ORDER BY name;

// 3. CONSTRAINT COUNT
SHOW CONSTRAINTS
YIELD name, type
RETURN 'SECTION_2_CONSTRAINTS' as section,
       count(*) as total_constraints,
       16 as expected_count,
       CASE WHEN count(*) = 16 THEN 'PASS' ELSE 'FAIL' END as status;

// 4. LIST UNIQUENESS CONSTRAINTS
SHOW CONSTRAINTS
YIELD name, type, labelsOrTypes, properties
WHERE type = 'UNIQUENESS'
RETURN 'CONSTRAINT_DETAIL' as section,
       labelsOrTypes[0] as super_label,
       properties,
       name
ORDER BY super_label;

// 5. CHECK DEPRECATED LABELS
MATCH (n)
WHERE any(label IN labels(n) WHERE label IN [
  'NER11_FOUNDATIONAL', 'NER11_STRUCTURAL', 'NER11_ANALYTICAL',
  'NER11_STRATEGIC', 'NER11_CRITICAL'
])
RETURN 'SECTION_3_MIGRATION' as section,
       'deprecated_labels' as check_type,
       count(n) as deprecated_count,
       0 as expected_count,
       CASE WHEN count(n) = 0 THEN 'PASS' ELSE 'FAIL' END as status;

// 6. COUNT ENTITIES BY TIER
MATCH (n)
WHERE any(label IN labels(n) WHERE label STARTS WITH 'NER11_T'
      AND NOT label CONTAINS '_GROUP'
      AND NOT label CONTAINS '_REL_')
WITH n,
     CASE
       WHEN any(label IN labels(n) WHERE label CONTAINS '_T5_') THEN 5
       WHEN any(label IN labels(n) WHERE label CONTAINS '_T7_') THEN 7
       WHEN any(label IN labels(n) WHERE label CONTAINS '_T8_') THEN 8
       WHEN any(label IN labels(n) WHERE label CONTAINS '_T9_') THEN 9
     END as tier
RETURN 'SECTION_4_ENTITIES' as section,
       tier,
       count(n) as actual_count,
       CASE tier
         WHEN 5 THEN 47
         WHEN 7 THEN 63
         WHEN 8 THEN 42
         WHEN 9 THEN 45
       END as expected_count,
       CASE WHEN count(n) = CASE tier
                                WHEN 5 THEN 47
                                WHEN 7 THEN 63
                                WHEN 8 THEN 42
                                WHEN 9 THEN 45
                              END
            THEN 'PASS' ELSE 'FAIL' END as status
ORDER BY tier;

// 7. TOTAL ENTITY COUNT
MATCH (n)
WHERE any(label IN labels(n) WHERE label STARTS WITH 'NER11_T'
      AND NOT label CONTAINS '_GROUP'
      AND NOT label CONTAINS '_REL_')
RETURN 'TOTAL_ENTITIES' as section,
       count(n) as actual_count,
       197 as expected_count,
       CASE WHEN count(n) = 197 THEN 'PASS' ELSE 'FAIL' END as status;

// 8. DISCRIMINATOR PROPERTIES
MATCH (n)
WHERE any(label IN labels(n) WHERE label STARTS WITH 'NER11_T')
RETURN 'SECTION_5_PROPERTIES' as section,
       'discriminator_check' as check_type,
       count(n) as total_nodes,
       sum(CASE WHEN n.entity_discriminator IS NOT NULL OR
                     n.relationship_discriminator IS NOT NULL OR
                     n.group_discriminator IS NOT NULL
                THEN 1 ELSE 0 END) as nodes_with_discriminator,
       CASE WHEN sum(CASE WHEN n.entity_discriminator IS NOT NULL OR
                               n.relationship_discriminator IS NOT NULL OR
                               n.group_discriminator IS NOT NULL
                          THEN 1 ELSE 0 END) = count(n)
            THEN 'PASS' ELSE 'FAIL' END as status;

// 9. HIERARCHICAL PROPERTIES
MATCH (n)
WHERE any(label IN labels(n) WHERE label STARTS WITH 'NER11_T')
RETURN 'HIERARCHICAL_PROPS' as section,
       count(n) as total_nodes,
       sum(CASE WHEN n.psychohistory_tier IS NOT NULL THEN 1 ELSE 0 END) as has_tier,
       sum(CASE WHEN n.label_color IS NOT NULL THEN 1 ELSE 0 END) as has_color,
       CASE WHEN sum(CASE WHEN n.psychohistory_tier IS NOT NULL THEN 1 ELSE 0 END) = count(n)
            THEN 'PASS' ELSE 'FAIL' END as tier_status,
       CASE WHEN sum(CASE WHEN n.label_color IS NOT NULL THEN 1 ELSE 0 END) = count(n)
            THEN 'PASS' ELSE 'FAIL' END as color_status;

// 10. SAMPLE T9 ENTITIES
MATCH (n:NER11_T9_CRITICAL)
WHERE n.entity_discriminator = 'entity'
RETURN 'SAMPLE_DATA_T9' as section,
       n.name as entity_name,
       n.psychohistory_tier as tier,
       n.label_color as color,
       n.entity_discriminator as discriminator
LIMIT 5;

// 11. SAMPLE T5 ENTITIES
MATCH (n:NER11_T5_FOUNDATIONAL)
WHERE n.entity_discriminator = 'entity'
RETURN 'SAMPLE_DATA_T5' as section,
       n.name as entity_name,
       n.psychohistory_tier as tier,
       n.label_color as color,
       n.entity_discriminator as discriminator
LIMIT 5;
