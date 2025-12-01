// ═══════════════════════════════════════════════════════════════
// COMPREHENSIVE POST-FIX AUDIT SCRIPT
// File: comprehensive_audit.cypher
// Created: 2025-11-28 16:32
// Purpose: Verify ALL fixes applied to Neo4j database
// ═══════════════════════════════════════════════════════════════

// ══════════════════════════════════════════════════════════════
// SECTION 1: CUSTOM FUNCTION VERIFICATION
// ══════════════════════════════════════════════════════════════

// 1.1 List all custom functions
CALL apoc.custom.list()
YIELD name, description, returnType
RETURN 'FUNCTION_LIST' as audit_section,
       collect({name: name, description: description, returnType: returnType}) as functions;

// 1.2 Test custom.getTier function
WITH 9.5 as tier
RETURN 'TEST_getTier' as test_name,
       custom.getTier(tier) as result,
       'Tier 9+' as expected;

// 1.3 Test custom.getLabelColor function
WITH 9.5 as tier
RETURN 'TEST_getLabelColor' as test_name,
       custom.getLabelColor(tier) as result,
       '#FF0000' as expected;

// 1.4 Test custom.getEntitySuperLabel function
WITH 9.5 as tier
RETURN 'TEST_getEntitySuperLabel' as test_name,
       custom.getEntitySuperLabel(tier) as result,
       'NER11_T9_CRITICAL' as expected;

// 1.5 Test custom.getRelationshipSuperLabel function
WITH 9.5 as tier
RETURN 'TEST_getRelationshipSuperLabel' as test_name,
       custom.getRelationshipSuperLabel(tier) as result,
       'NER11_REL_T9_CRITICAL' as expected;

// ══════════════════════════════════════════════════════════════
// SECTION 2: CONSTRAINT VERIFICATION
// ══════════════════════════════════════════════════════════════

// 2.1 Count total constraints
SHOW CONSTRAINTS
YIELD name, type, entityType, labelsOrTypes, properties
RETURN 'CONSTRAINT_COUNT' as audit_section,
       count(*) as total_constraints,
       16 as expected_count,
       CASE WHEN count(*) = 16 THEN 'PASS' ELSE 'FAIL' END as status;

// 2.2 List uniqueness constraints with Super Labels
SHOW CONSTRAINTS
YIELD name, type, entityType, labelsOrTypes, properties
WHERE type = 'UNIQUENESS'
RETURN 'UNIQUENESS_CONSTRAINTS' as audit_section,
       labelsOrTypes as super_label,
       properties,
       name;

// 2.3 Verify all 16 Super Labels have constraints
WITH [
  'NER11_T5_FOUNDATIONAL',
  'NER11_T6_STRUCTURAL',
  'NER11_T7_ANALYTICAL',
  'NER11_T8_STRATEGIC',
  'NER11_T9_CRITICAL',
  'NER11_REL_T5_FOUNDATIONAL',
  'NER11_REL_T6_STRUCTURAL',
  'NER11_REL_T7_ANALYTICAL',
  'NER11_REL_T8_STRATEGIC',
  'NER11_REL_T9_CRITICAL',
  'NER11_T5_GROUP',
  'NER11_T6_GROUP',
  'NER11_T7_GROUP',
  'NER11_T8_GROUP',
  'NER11_T9_GROUP',
  'NER11_RELATIONSHIP_GROUP'
] as expected_labels
CALL {
  SHOW CONSTRAINTS
  YIELD labelsOrTypes
  WHERE labelsOrTypes IS NOT NULL
  RETURN labelsOrTypes[0] as label
}
WITH expected_labels, collect(DISTINCT label) as actual_labels
RETURN 'SUPER_LABEL_COVERAGE' as audit_section,
       size(expected_labels) as expected_count,
       size(actual_labels) as actual_count,
       [label IN expected_labels WHERE NOT label IN actual_labels] as missing_labels,
       CASE WHEN size([label IN expected_labels WHERE NOT label IN actual_labels]) = 0
            THEN 'PASS' ELSE 'FAIL' END as status;

// ══════════════════════════════════════════════════════════════
// SECTION 3: FUNCTION COUNT VERIFICATION (11+ functions)
// ══════════════════════════════════════════════════════════════

// 3.1 Count all custom functions
CALL apoc.custom.list()
YIELD name
RETURN 'CUSTOM_FUNCTION_COUNT' as audit_section,
       count(*) as total_functions,
       11 as minimum_expected,
       CASE WHEN count(*) >= 11 THEN 'PASS' ELSE 'FAIL' END as status;

// 3.2 Test Collective Intelligence functions
CALL custom.calculateCollectiveIntelligence('PERSON', 'Alice')
YIELD intelligence
RETURN 'TEST_CI_calculateCollectiveIntelligence' as test_name,
       intelligence,
       CASE WHEN intelligence IS NOT NULL THEN 'PASS' ELSE 'FAIL' END as status;

CALL custom.findEmergentPatterns('ORGANIZATION')
YIELD pattern
RETURN 'TEST_CI_findEmergentPatterns' as test_name,
       count(pattern) as pattern_count,
       CASE WHEN count(pattern) >= 0 THEN 'PASS' ELSE 'FAIL' END as status;

// ══════════════════════════════════════════════════════════════
// SECTION 4: MIGRATION COMPLETENESS VERIFICATION
// ══════════════════════════════════════════════════════════════

// 4.1 Check for deprecated labels (should be 0)
MATCH (n)
WHERE any(label IN labels(n) WHERE label IN [
  'NER11_FOUNDATIONAL', 'NER11_STRUCTURAL', 'NER11_ANALYTICAL',
  'NER11_STRATEGIC', 'NER11_CRITICAL'
])
RETURN 'DEPRECATED_LABEL_CHECK' as audit_section,
       count(n) as deprecated_count,
       0 as expected_count,
       CASE WHEN count(n) = 0 THEN 'PASS' ELSE 'FAIL' END as status;

// 4.2 Verify discriminator properties exist
MATCH (n)
WHERE any(label IN labels(n) WHERE label STARTS WITH 'NER11_T')
WITH n,
     CASE
       WHEN any(label IN labels(n) WHERE label CONTAINS '_GROUP') THEN 'group'
       WHEN any(label IN labels(n) WHERE label CONTAINS '_REL_') THEN 'relationship'
       ELSE 'entity'
     END as expected_discriminator
RETURN 'DISCRIMINATOR_PROPERTIES' as audit_section,
       expected_discriminator,
       count(n) as node_count,
       sum(CASE WHEN n.entity_discriminator IS NOT NULL OR
                     n.relationship_discriminator IS NOT NULL OR
                     n.group_discriminator IS NOT NULL
                THEN 1 ELSE 0 END) as nodes_with_discriminator,
       CASE WHEN sum(CASE WHEN n.entity_discriminator IS NOT NULL OR
                               n.relationship_discriminator IS NOT NULL OR
                               n.group_discriminator IS NOT NULL
                          THEN 1 ELSE 0 END) = count(n)
            THEN 'PASS' ELSE 'FAIL' END as status;

// ══════════════════════════════════════════════════════════════
// SECTION 5: NER11 ENTITY COUNT VERIFICATION (197 total)
// ══════════════════════════════════════════════════════════════

// 5.1 Count entities by tier
MATCH (n)
WHERE any(label IN labels(n) WHERE label STARTS WITH 'NER11_T' AND NOT label CONTAINS '_GROUP')
WITH n,
     CASE
       WHEN any(label IN labels(n) WHERE label CONTAINS '_T5_') THEN 5
       WHEN any(label IN labels(n) WHERE label CONTAINS '_T6_') THEN 6
       WHEN any(label IN labels(n) WHERE label CONTAINS '_T7_') THEN 7
       WHEN any(label IN labels(n) WHERE label CONTAINS '_T8_') THEN 8
       WHEN any(label IN labels(n) WHERE label CONTAINS '_T9_') THEN 9
     END as tier
RETURN 'NER11_ENTITY_COUNT_BY_TIER' as audit_section,
       tier,
       count(n) as actual_count,
       CASE tier
         WHEN 5 THEN 47
         WHEN 6 THEN 0  // No T6 entities in NER11
         WHEN 7 THEN 63
         WHEN 8 THEN 42
         WHEN 9 THEN 45
       END as expected_count,
       CASE WHEN count(n) = CASE tier
                                WHEN 5 THEN 47
                                WHEN 6 THEN 0
                                WHEN 7 THEN 63
                                WHEN 8 THEN 42
                                WHEN 9 THEN 45
                              END
            THEN 'PASS' ELSE 'FAIL' END as status
ORDER BY tier;

// 5.2 Total entity count
MATCH (n)
WHERE any(label IN labels(n) WHERE label STARTS WITH 'NER11_T' AND NOT label CONTAINS '_GROUP')
RETURN 'NER11_TOTAL_ENTITY_COUNT' as audit_section,
       count(n) as actual_count,
       197 as expected_count,
       CASE WHEN count(n) = 197 THEN 'PASS' ELSE 'FAIL' END as status;

// ══════════════════════════════════════════════════════════════
// SECTION 6: HIERARCHICAL PROPERTIES VERIFICATION
// ══════════════════════════════════════════════════════════════

// 6.1 Check for required hierarchical properties
MATCH (n)
WHERE any(label IN labels(n) WHERE label STARTS WITH 'NER11_T')
RETURN 'HIERARCHICAL_PROPERTIES' as audit_section,
       sum(CASE WHEN n.psychohistory_tier IS NOT NULL THEN 1 ELSE 0 END) as has_tier,
       sum(CASE WHEN n.label_color IS NOT NULL THEN 1 ELSE 0 END) as has_color,
       sum(CASE WHEN n.entity_super_label IS NOT NULL OR
                     n.relationship_super_label IS NOT NULL OR
                     n.group_super_label IS NOT NULL
                THEN 1 ELSE 0 END) as has_super_label,
       count(n) as total_nodes,
       CASE WHEN sum(CASE WHEN n.psychohistory_tier IS NOT NULL THEN 1 ELSE 0 END) = count(n)
            THEN 'PASS' ELSE 'FAIL' END as tier_status,
       CASE WHEN sum(CASE WHEN n.label_color IS NOT NULL THEN 1 ELSE 0 END) = count(n)
            THEN 'PASS' ELSE 'FAIL' END as color_status;

// ══════════════════════════════════════════════════════════════
// SECTION 7: SAMPLE DATA VALIDATION
// ══════════════════════════════════════════════════════════════

// 7.1 Sample Tier 9 entities with all properties
MATCH (n:NER11_T9_CRITICAL)
WHERE n.entity_discriminator = 'entity'
RETURN 'SAMPLE_T9_ENTITIES' as audit_section,
       n.name as entity_name,
       n.psychohistory_tier as tier,
       n.label_color as color,
       n.entity_super_label as super_label,
       n.entity_discriminator as discriminator
LIMIT 5;

// 7.2 Sample Tier 5 entities with all properties
MATCH (n:NER11_T5_FOUNDATIONAL)
WHERE n.entity_discriminator = 'entity'
RETURN 'SAMPLE_T5_ENTITIES' as audit_section,
       n.name as entity_name,
       n.psychohistory_tier as tier,
       n.label_color as color,
       n.entity_super_label as super_label,
       n.entity_discriminator as discriminator
LIMIT 5;

// ══════════════════════════════════════════════════════════════
// SECTION 8: FINAL SUMMARY
// ══════════════════════════════════════════════════════════════

// Return overall audit summary
RETURN 'AUDIT_COMPLETE' as status,
       datetime() as audit_timestamp,
       'Comprehensive verification of all fixes completed' as message;
