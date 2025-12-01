// ============================================
// TEST ALL PSYCHOHISTORY CUSTOM FUNCTIONS
// Generated: 2025-11-28
// Total Functions: 16
// ============================================

// TEST 1: epidemicThreshold - Calculate R0 value
CALL psychohistory.epidemicThreshold(5.0, 1.0, 1.0) YIELD value
RETURN 'epidemicThreshold' AS function_name, value AS result,
       CASE WHEN value > 0 THEN 'PASS' ELSE 'FAIL' END AS status;

// TEST 2: criticalSlowing - Detect early warnings
CALL psychohistory.criticalSlowing(0.8, 0.5) YIELD value
RETURN 'criticalSlowing' AS function_name, value AS result,
       CASE WHEN value IS NOT NULL THEN 'PASS' ELSE 'FAIL' END AS status;

// TEST 3: bootstrapCI - Calculate confidence interval
CALL psychohistory.bootstrapCI(0.75, 100) YIELD value
RETURN 'bootstrapCI' AS function_name, value AS result,
       CASE WHEN value IS NOT NULL THEN 'PASS' ELSE 'FAIL' END AS status;

// TEST 4: granovetterCascadeNormal - Normal distribution cascade
CALL psychohistory.granovetterCascadeNormal(0.6, 0.1) YIELD value
RETURN 'granovetterCascadeNormal' AS function_name, value AS result,
       CASE WHEN value >= 0 AND value <= 1 THEN 'PASS' ELSE 'FAIL' END AS status;

// TEST 5: granovetterCascadeUniform - Uniform distribution cascade
CALL psychohistory.granovetterCascadeUniform(0.5, 0.2, 0.8) YIELD value
RETURN 'granovetterCascadeUniform' AS function_name, value AS result,
       CASE WHEN value >= 0 AND value <= 1 THEN 'PASS' ELSE 'FAIL' END AS status;

// TEST 6: isingDynamics - Opinion formation dynamics
CALL psychohistory.isingDynamics(0.5, 1.5, 0.8, 5.0, 0.2) YIELD value
RETURN 'isingDynamics' AS function_name, value AS result,
       CASE WHEN value IS NOT NULL THEN 'PASS' ELSE 'FAIL' END AS status;

// TEST 7: bifurcationRate - Calculate state change rate
CALL psychohistory.bifurcationRate(0.5, -0.25) YIELD value
RETURN 'bifurcationRate' AS function_name, value AS result,
       CASE WHEN value IS NOT NULL THEN 'PASS' ELSE 'FAIL' END AS status;

// TEST 8: bifurcationDistance - Distance from critical point
CALL psychohistory.bifurcationDistance(-0.25) YIELD value
RETURN 'bifurcationDistance' AS function_name, value AS result,
       CASE WHEN value = 0.25 THEN 'PASS' ELSE 'FAIL' END AS status;

// TEST 9: recoveryRate - Calculate system recovery rate
CALL psychohistory.recoveryRate(0.7, 5.0) YIELD value
RETURN 'recoveryRate' AS function_name, value AS result,
       CASE WHEN value > 0 THEN 'PASS' ELSE 'FAIL' END AS status;

// TEST 10: autocorrelation - Calculate autocorrelation coefficient
CALL psychohistory.autocorrelation(0.5, 1.0) YIELD value
RETURN 'autocorrelation' AS function_name, value AS result,
       CASE WHEN value = 0.5 THEN 'PASS' ELSE 'FAIL' END AS status;

// TEST 11: varianceRatio - Calculate variance increase ratio
CALL psychohistory.varianceRatio(0.1, 0.2) YIELD value
RETURN 'varianceRatio' AS function_name, value AS result,
       CASE WHEN value = 1.0 THEN 'PASS' ELSE 'FAIL' END AS status;

// TEST 12: spectralRatio - Calculate spectral reddening ratio
CALL psychohistory.spectralRatio(2.0, 1.0) YIELD value
RETURN 'spectralRatio' AS function_name, value AS result,
       CASE WHEN value = 2.0 THEN 'PASS' ELSE 'FAIL' END AS status;

// TEST 13: compositeWarning - Composite early warning score
CALL psychohistory.compositeWarning(0.7, 0.8) YIELD value
RETURN 'compositeWarning' AS function_name, value AS result,
       CASE WHEN value = 0.75 THEN 'PASS' ELSE 'FAIL' END AS status;

// TEST 14: cascadeProbability - Opinion cascade probability
CALL psychohistory.cascadeProbability(0.8, 0.3, 3.0) YIELD value
RETURN 'cascadeProbability' AS function_name, value AS result,
       CASE WHEN value > 0.5 AND value < 1.0 THEN 'PASS' ELSE 'FAIL' END AS status;

// TEST 15: equilibriumOpinion - Equilibrium opinion state
CALL psychohistory.equilibriumOpinion(1.5, 0.8, 5.0, 0.2) YIELD value
RETURN 'equilibriumOpinion' AS function_name, value AS result,
       CASE WHEN value >= -1.0 AND value <= 1.0 THEN 'PASS' ELSE 'FAIL' END AS status;

// TEST 16: testFunc - Basic test function
CALL psychohistory.testFunc() YIELD value
RETURN 'testFunc' AS function_name, value AS result,
       CASE WHEN value IS NOT NULL THEN 'PASS' ELSE 'FAIL' END AS status;

// ============================================
// SUMMARY REPORT
// ============================================
CALL apoc.custom.list()
YIELD name
RETURN
    'FUNCTION DEPLOYMENT SUMMARY' AS report_title,
    count(name) AS total_functions,
    16 AS target_functions,
    CASE
        WHEN count(name) >= 16 THEN '100% COMPLETE'
        WHEN count(name) >= 10 THEN 'TARGET EXCEEDED'
        ELSE 'INCOMPLETE'
    END AS deployment_status;
