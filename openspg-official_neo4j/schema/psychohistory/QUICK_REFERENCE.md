# Psychohistory Functions - Quick Reference

**Last Updated**: 2025-11-28
**Total Functions**: 16
**Status**: ✅ Production Ready

## Summary

All 16 psychohistory custom functions successfully deployed to Neo4j:
- 6 core functions (epidemic, critical slowing, cascade, bootstrap, test)
- 10 new functions (Ising dynamics, bifurcation, autocorrelation, variance, spectral, composite, cascade probability, equilibrium)

## Quick Test

```bash
# Verify all functions are registered
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "CALL apoc.custom.list() YIELD name RETURN count(name) AS total"
# Expected: 16
```

## Documentation

- **Full Reference**: See `/schema/psychohistory/DEPLOYMENT_SUMMARY.md`
- **Test Suite**: `/schema/psychohistory/test_all_functions.cypher`
- **Deployment Script**: `/schema/psychohistory/deploy_remaining_functions.cypher`

## Function List

1. epidemicThreshold - R₀ calculation
2. criticalSlowing - Early warning composite
3. bootstrapCI - Confidence intervals
4. granovetterCascadeNormal - Normal cascade
5. granovetterCascadeUniform - Uniform cascade
6. testFunc - Basic test
7. isingDynamics - Opinion dynamics
8. bifurcationRate - State change
9. bifurcationDistance - Crisis proximity
10. recoveryRate - Resilience measure
11. autocorrelation - Time correlation
12. varianceRatio - Variance increase
13. spectralRatio - Frequency analysis
14. compositeWarning - Multi-signal alert
15. cascadeProbability - Cascade likelihood
16. equilibriumOpinion - Final state prediction

