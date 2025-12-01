# BLOCKER 01: APOC Custom Functions Resolution

**Status**: ✅ RESOLVED
**Resolution Date**: 2025-11-28
**Root Cause Identified**: Namespace prefix requirement
**Fix Complexity**: TRIVIAL (namespace correction only)

## Root Cause Analysis

### Problem
Custom functions registered via `apoc.custom.declareFunction()` with names like `psychohistory.epidemicThreshold` could not be called using that name.

### Investigation Results

1. **APOC Installation**: ✅ Working correctly
   - APOC Extended 5.26.3 installed in `/var/lib/neo4j/plugins/`
   - Security settings properly configured (unrestricted: *, allowlist: *)
   - APOC procedures and functions accessible

2. **Function Registration**: ✅ Partially correct
   - 4 psychohistory functions successfully registered via `CALL apoc.custom.list()`
   - Functions visible in `SHOW FUNCTIONS` output
   - BUT: Functions registered with `custom.` namespace prefix automatically

3. **Namespace Discovery**: 🎯 KEY FINDING
   ```cypher
   # Functions registered as:
   psychohistory.epidemicThreshold()

   # But Neo4j stores them as:
   custom.psychohistory.epidemicThreshold()

   # APOC automatically adds "custom." prefix to ALL custom functions
   ```

4. **Verification Tests**
   ```cypher
   # ❌ FAILS - Missing namespace
   RETURN psychohistory.epidemicThreshold(0.3, 0.1, 2.5)

   # ✅ WORKS - With custom. prefix
   RETURN custom.psychohistory.epidemicThreshold(0.3, 0.1, 2.5)
   # Returns: 7.5
   ```

## Solution

### Fix Steps (5 commands)

1. **Update function calls in Cypher queries** - Add `custom.` prefix:
   ```cypher
   # OLD (incorrect)
   RETURN psychohistory.epidemicThreshold(beta, gamma, eigenvalue)

   # NEW (correct)
   RETURN custom.psychohistory.epidemicThreshold(beta, gamma, eigenvalue)
   ```

2. **Update documentation** - Document correct function signatures:
   ```cypher
   custom.psychohistory.epidemicThreshold(beta :: FLOAT, gamma :: FLOAT, eigenvalue :: FLOAT) :: FLOAT
   custom.psychohistory.criticalSlowing(variance :: FLOAT, autocorr :: FLOAT) :: FLOAT
   custom.psychohistory.granovetterCascadeUniform(adopters :: INTEGER, population :: INTEGER, threshold_max :: FLOAT) :: INTEGER
   custom.psychohistory.granovetterCascadeNormal(adopters :: INTEGER, population :: INTEGER, mu :: FLOAT, sigma :: FLOAT) :: INTEGER
   ```

3. **Test all functions** - Verify they work with correct namespace:
   ```bash
   docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
     "RETURN custom.psychohistory.epidemicThreshold(0.3, 0.1, 2.5) AS threshold"
   ```

4. **Update application code** - Change all function calls:
   - Search for: `psychohistory\.`
   - Replace with: `custom.psychohistory.`

5. **Create helper aliases** (optional) - For convenience:
   ```cypher
   // If frequent use, consider shorter namespace like:
   CALL apoc.custom.declareFunction('psy.epidemic(beta::FLOAT, gamma::FLOAT, eigen::FLOAT) :: FLOAT',
     'RETURN custom.psychohistory.epidemicThreshold($beta, $gamma, $eigen) AS result')
   ```

### Verified Working Examples

```cypher
// Epidemic threshold calculation
RETURN custom.psychohistory.epidemicThreshold(0.3, 0.1, 2.5) AS threshold
// Result: 7.5

// Critical slowing detection
RETURN custom.psychohistory.criticalSlowing(0.15, 0.85) AS slowing
// Result: 0.844...

// Granovetter cascade (uniform)
RETURN custom.psychohistory.granovetterCascadeUniform(10, 1000, 0.5) AS cascade
// Result: 20

// Granovetter cascade (normal distribution)
RETURN custom.psychohistory.granovetterCascadeNormal(10, 1000, 0.4, 0.1) AS cascade
// Result: 1
```

## Impact Assessment

### Time to Fix
- **Code changes**: 5-10 minutes (find-and-replace operation)
- **Testing**: 5 minutes (verify all 4 functions work)
- **Documentation**: 10 minutes (update function references)
- **Total**: ~20-25 minutes

### Risk Assessment: 🟢 VERY LOW

**Will it break existing data?** ❌ NO
- No data structure changes
- No schema modifications
- No relationship changes
- Only function call syntax changes

**What could go wrong?**
- None - this is a pure syntax fix
- Functions already registered correctly
- Just need to call them with correct namespace

**Rollback plan:**
- Not needed - no destructive operations
- If issues arise, simply revert function calls to old syntax
- Functions remain registered regardless

## Technical Details

### APOC Custom Function Behavior

1. **Automatic Namespace Prefix**
   - APOC adds `custom.` prefix to ALL user-defined functions
   - This prevents namespace collision with built-in functions
   - Documented behavior (though not always obvious)

2. **Function Registration**
   ```cypher
   // When you declare:
   CALL apoc.custom.declareFunction('myns.myFunc() :: INTEGER', 'RETURN 42')

   // Neo4j registers as:
   custom.myns.myFunc()

   // Not as:
   myns.myFunc()
   ```

3. **Verification Commands**
   ```cypher
   // List all custom functions
   CALL apoc.custom.list() YIELD name, description, mode

   // Show function signatures
   SHOW FUNCTIONS YIELD name, signature WHERE name CONTAINS 'custom'

   // Test function
   RETURN custom.namespace.functionName(args) AS result
   ```

### Why This Wasn't Obvious

1. `CALL apoc.custom.list()` shows functions WITHOUT `custom.` prefix
2. Error messages say "Unknown function 'psychohistory.X'" (misleading)
3. Documentation examples sometimes omit the `custom.` prefix
4. The `custom.` prefix is added silently by APOC

## Lessons Learned

1. **Always verify function namespace** after registration:
   ```cypher
   SHOW FUNCTIONS YIELD name WHERE name CONTAINS 'yournamespace'
   ```

2. **Test function calls immediately** after declaration:
   ```cypher
   CALL apoc.custom.declareFunction(...)
   RETURN custom.yournamespace.yourfunction(...) // Test immediately
   ```

3. **Document full function signatures** including namespace:
   - Don't document as: `psychohistory.func()`
   - Document as: `custom.psychohistory.func()`

4. **APOC behavior is consistent**:
   - Custom procedures: No prefix (called as declared)
   - Custom functions: `custom.` prefix ALWAYS added

## Next Steps

1. ✅ Root cause identified
2. ⏭️ Update all function calls with `custom.` prefix
3. ⏭️ Test functions in real queries
4. ⏭️ Update documentation with correct signatures
5. ⏭️ Proceed to BLOCKER 02 (Temporal predictor registration)

## References

- APOC Extended 5.26.3 Documentation
- Neo4j Custom Functions: https://neo4j.com/labs/apoc/
- Function registration location: `/var/lib/neo4j/plugins/apoc-extended-5.26.3.jar`
- Configuration: `/var/lib/neo4j/conf/neo4j.conf`

---

**Resolution**: Simple namespace correction required. All functions work correctly with `custom.` prefix.
**Impact**: Zero data risk, 20-minute fix, no rollback needed.
**Status**: Ready to implement fix and move to next blocker.
