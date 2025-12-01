# PHASE 2: Clerk Implementation Execution Guide

**Date:** 2025-11-04 13:08:00
**Status:** Ready for execution
**Estimated Time:** 30-35 minutes
**Complexity:** Low (0.25/1.0)

---

## 📊 CURRENT STATE SUMMARY

### ✅ Completed Work (Phase 0 - Backend)

**Backend Infrastructure: 100% OPERATIONAL**

| Service | Status | Connection | Verification |
|---------|--------|------------|--------------|
| openspg-neo4j | ✅ OPERATIONAL | bolt://openspg-neo4j:7687 | HTTP 200 |
| openspg-qdrant | ✅ OPERATIONAL | http://openspg-qdrant:6333 | HTTP 401 (auth working) |
| openspg-mysql | ✅ OPERATIONAL | openspg-mysql:3306 | Queries successful |
| openspg-minio | ✅ OPERATIONAL | http://openspg-minio:9000 | HTTP 200 |
| openspg-server | ✅ OPERATIONAL | http://openspg-server:8887 | HTTP 200 |

**Critical Actions Completed:**
1. ✅ openspg-server relocated to main docker-compose.yml
2. ✅ openspg-qdrant configured with docker-compose.qdrant.yml
3. ✅ All 11 data volumes preserved (zero data loss)
4. ✅ Network connectivity: 100% verified
5. ✅ Application connectivity: 5/5 services tested and working
6. ✅ Documentation created:
   - `tests/backend-connectivity.test.js`
   - `docs/BACKEND_CONNECTION_PATTERNS.md`
   - `docs/CLERK_QUICK_SETUP.md`

**Docker Volumes Status:**
```
openspg-mysql-data ✅
openspg-neo4j-data ✅
openspg-minio-data ✅
openspg-qdrant-data ✅
+ 7 more configuration/log volumes ✅
Total: 11 volumes intact
```

### ⚠️ Current Blocker

**aeon-saas-dev Container:**
- Status: UP but UNHEALTHY
- Next.js: Running (PID 18)
- Issue: HTTP 500 Internal Server Error
- Root Cause: Invalid/expired Clerk API keys

**Clerk Integration Status:**
```typescript
// middleware.ts ✅ EXISTS - Route protection configured
export default clerkMiddleware(async (auth, req) => {
  if (isProtectedRoute(req)) {
    await auth.protect()
  }
})

// layout.tsx ✅ EXISTS - ClerkProvider wrapping
<ClerkProvider>
  <html>...</html>
</ClerkProvider>

// Environment: ⚠️ NEEDS REAL KEYS
CLERK_PUBLISHABLE_KEY_DEV=pk_test_[EXPIRED/INVALID]
CLERK_SECRET_KEY_DEV=sk_test_[EXPIRED/INVALID]
```

**Why Container is Unhealthy:**
- ClerkProvider tries to initialize on app startup
- Invalid keys cause initialization failure
- Failure crashes the app → 500 errors
- Health check (`/api/health`) also fails due to app crash

**The Fix:** Get fresh API keys from Clerk dashboard (5 minutes)

---

## 🚀 EXECUTION STEPS

### Step 1: Obtain Clerk API Keys (10 minutes)

#### A. Access Clerk Dashboard
**URL:** https://dashboard.clerk.com/last-active?path=api-keys

**First Time Setup:**
1. Visit https://dashboard.clerk.com
2. Sign up/Sign in with email
3. Click "Add application"
4. Name: `AEON Digital Twin - Development`
5. Select: `Next.js` framework
6. Select: `App Router` (not Pages Router)

**Existing Account:**
1. Visit https://dashboard.clerk.com
2. Select your AEON application (or create new)
3. Navigate to "API Keys" in left sidebar

#### B. Copy API Keys

**Location:** API Keys page → "Quick Copy" section

**Keys to Copy:**
1. **Publishable Key** (starts with `pk_test_` or `pk_live_`)
   - This key is PUBLIC (safe for frontend)
   - Used by ClerkProvider for initialization

2. **Secret Key** (starts with `sk_test_` or `sk_live_`)
   - This key is PRIVATE (never expose!)
   - Used for backend API calls
   - Never commit to git or share publicly

**Example Format:**
```bash
# Publishable Key (PUBLIC)
pk_test_YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXoxMjM0NTY=

# Secret Key (PRIVATE - KEEP SECURE!)
sk_test_MTIzNDU2Nzg5MGFiY2RlZmdoaWprbG1ub3BxcnN0dXZ3eHl6QUJDREU=
```

**⚠️ SECURITY WARNING:**
- Secret key must NEVER be committed to git
- `.env.development` is in `.gitignore` (safe to store here)
- Never share secret key in chat, screenshots, or public repos

---

### Step 2: Update Environment Configuration (2 minutes)

#### File Location
```
/home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/web_interface/.env.development
```

#### Lines to Update

**Find these lines (around line 31-32):**
```bash
# OLD (invalid/expired)
CLERK_PUBLISHABLE_KEY_DEV=pk_test_dmFsaWQtc2FpbGZpc2gtOTUuY2xlcmsuYWNjb3VudHMuZGV2JA
CLERK_SECRET_KEY_DEV=sk_test_5jjk7jSqlDy3FXX8OVWAH4JFfhcQ5ohI3m3cBDL6bm
```

**Replace with your REAL keys:**
```bash
# NEW (paste your actual keys from Clerk dashboard)
CLERK_PUBLISHABLE_KEY_DEV=pk_test_[PASTE_YOUR_PUBLISHABLE_KEY_HERE]
CLERK_SECRET_KEY_DEV=sk_test_[PASTE_YOUR_SECRET_KEY_HERE]
```

**⚠️ IMPORTANT:**
- Remove any extra spaces before/after the keys
- Ensure no line breaks in the middle of keys
- Keys are typically 50-100 characters long
- Don't add quotes around the keys

#### Verification
After pasting, verify the file:
```bash
cat .env.development | grep CLERK_
```

**Expected Output:**
```bash
CLERK_PUBLISHABLE_KEY_DEV=pk_test_[YOUR_KEY]
CLERK_SECRET_KEY_DEV=sk_test_[YOUR_KEY]
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=${CLERK_PUBLISHABLE_KEY_DEV}
CLERK_SECRET_KEY=${CLERK_SECRET_KEY_DEV}
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up
NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL=/dashboard
NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL=/dashboard
```

---

### Step 3: Rebuild Container (10 minutes)

#### Commands

**Navigate to project:**
```bash
cd /home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/web_interface
```

**Stop current container:**
```bash
docker-compose -f docker-compose.dev.yml down
```

**Rebuild with new environment:**
```bash
docker-compose -f docker-compose.dev.yml up --build -d
```

**Monitor startup:**
```bash
docker logs -f aeon-saas-dev
```

#### Expected Build Output

```
✓ Creating optimized production build
✓ Compiled successfully
✓ Linting and checking validity of types
✓ Collecting page data
✓ Generating static pages
✓ Finalizing page optimization

Route (app)                              Size
┌ ○ /                                    [size]
├ ○ /dashboard                           [size]
└ ○ /api/health                          [size]

○ (Static)  prerendered as static content

✓ Ready in [time]ms
```

**Key Indicators of Success:**
- ✅ "Compiled successfully"
- ✅ "Ready in [time]"
- ✅ No Clerk error messages
- ❌ If you see "Invalid publishable key" → Keys are wrong, check again

**Stop Monitoring:**
Press `Ctrl+C` to exit logs (container keeps running)

---

### Step 4: Health Validation (3 minutes)

#### A. Check Container Status
```bash
docker ps --filter "name=aeon-saas-dev" --format "table {{.Names}}\t{{.Status}}"
```

**Expected:** `Up X minutes (healthy)` - not unhealthy

**If still unhealthy after 30-60 seconds:**
```bash
# Check detailed logs for errors
docker logs aeon-saas-dev --tail 50
```

#### B. Test Homepage
```bash
curl -s http://localhost:3000 | head -50
```

**Expected:** HTML content (not "Internal Server Error")

**Should see:**
```html
<!DOCTYPE html>
<html>
  <head>...</head>
  <body>
    <div id="__next">...</div>
  </body>
</html>
```

#### C. Test Health Endpoint
```bash
curl http://localhost:3000/api/health
```

**Expected:** JSON with backend status (not 500 error)

```json
{
  "services": {
    "neo4j": "healthy",
    "qdrant": "healthy",
    "mysql": "healthy",
    "minio": "healthy"
  },
  "overall": "healthy"
}
```

#### D. Verify Backend Connectivity Maintained

```bash
docker exec aeon-saas-dev node -e "
Promise.all([
  fetch('http://openspg-neo4j:7474').then(r => ({service: 'Neo4j', status: r.status})),
  fetch('http://openspg-qdrant:6333/health').then(r => ({service: 'Qdrant', status: r.status})),
  fetch('http://openspg-minio:9000/minio/health/live').then(r => ({service: 'MinIO', status: r.status})),
  fetch('http://openspg-server:8887').then(r => ({service: 'OpenSPG', status: r.status}))
]).then(results => console.log(JSON.stringify(results, null, 2)))
"
```

**Expected:** All 200 OK (or 401 for Qdrant auth)

---

### Step 5: Authentication Testing (5 minutes)

#### A. Access Homepage in Browser
**URL:** http://localhost:3000

**Expected Behavior:**
- ✅ Page loads without 500 error
- ✅ Navigation bar visible
- ✅ "Sign In" and "Sign Up" buttons present
- ✅ No console errors about Clerk

#### B. Test Sign-In Page
**Click:** "Sign In" button (top right)

**Expected:**
- ✅ Clerk sign-in modal appears (overlay on page)
- ✅ Email and password fields visible
- ✅ "Don't have an account? Sign up" link present

**If modal doesn't appear:**
- Check browser console (F12 → Console)
- Look for Clerk errors
- Common issue: Keys still invalid

#### C. Create Test User
**In Clerk Modal:**
1. Click "Sign up" tab
2. Enter test email: `test@aeon.local`
3. Enter password: `TestPassword123!`
4. Click "Continue"

**Expected Flow:**
1. ✅ Email verification modal (or automatic sign-in for test mode)
2. ✅ Redirects to `/dashboard`
3. ✅ User button appears in navigation (your avatar/initials)
4. ✅ Dashboard page loads successfully

#### D. Verify in Clerk Dashboard
1. Go back to https://dashboard.clerk.com
2. Navigate to "Users" tab
3. **Expected:** See your test user listed with email `test@aeon.local`

#### E. Test Protected Routes

**While Signed In:**
```bash
# Should work (200 OK)
curl http://localhost:3000/dashboard
```

**Sign Out:**
- Click user button → "Sign out"

**Try Accessing Protected Route:**
```bash
# Should redirect to sign-in (not 200 OK with dashboard content)
curl -I http://localhost:3000/dashboard
```

**Expected:** Redirect to `/sign-in` (302 or 307 status)

---

### Step 6: Documentation Update (5 minutes)

Will be handled in Phase 3 (automated).

---

## 🐛 TROUBLESHOOTING

### Issue: Container Still Unhealthy

**Symptoms:**
- `docker ps` shows "(unhealthy)" after 2+ minutes
- HTTP 500 errors persist

**Diagnosis:**
```bash
docker logs aeon-saas-dev --tail 100 | grep -i "error\|clerk"
```

**Common Causes:**

1. **Invalid Clerk Keys**
   - Error message: "Invalid publishable key"
   - Solution: Double-check you copied COMPLETE keys
   - Verify: No spaces, no line breaks, correct format

2. **Whitespace in Keys**
   - Check: `cat .env.development | grep CLERK | od -c`
   - Should show no spaces after equals sign
   - Solution: Re-paste keys carefully

3. **Environment Not Loading**
   - Check: `.env.development` location is correct
   - Should be in: `web_interface/.env.development`
   - Not in subdirectories

4. **Old Container Cached**
   - Solution: Force clean rebuild
   ```bash
   docker-compose -f docker-compose.dev.yml down
   docker system prune -f
   docker-compose -f docker-compose.dev.yml up --build -d
   ```

### Issue: Clerk Modal Not Appearing

**Symptoms:**
- Sign-in button does nothing
- No Clerk overlay

**Diagnosis:**
Open browser console (F12), look for errors

**Common Causes:**

1. **ClerkProvider Not Initialized**
   - Check browser console for: "Clerk: publishable key not found"
   - Solution: Keys still invalid, check .env.development

2. **JavaScript Errors**
   - Red errors in console
   - Solution: Check Next.js compilation logs

3. **Wrong Key Type**
   - Using secret key in publishable field (or vice versa)
   - Solution: Verify pk_test_ is in PUBLISHABLE, sk_test_ in SECRET

### Issue: Redirect Loop

**Symptoms:**
- Signs in but keeps redirecting
- Never reaches dashboard

**Common Cause:**
- Middleware protecting sign-in routes

**Check:**
```bash
docker exec aeon-saas-dev cat middleware.ts | grep "isPublicRoute"
```

**Should Include:**
- `/sign-in`
- `/sign-up`
- `/`

---

## ✅ SUCCESS CHECKLIST

**Before Moving to Phase 3:**

### Container Health
- [ ] `docker ps` shows `(healthy)` not `(unhealthy)`
- [ ] HTTP 200 responses from http://localhost:3000
- [ ] `/api/health` returns JSON (not 500)
- [ ] No Clerk errors in logs

### Backend Connectivity
- [ ] Neo4j: Reachable and responding
- [ ] Qdrant: Reachable and responding
- [ ] MySQL: Reachable and responding
- [ ] MinIO: Reachable and responding
- [ ] OpenSPG: Reachable and responding

### Authentication Flow
- [ ] Sign-in page accessible
- [ ] Clerk modal appears on button click
- [ ] Can create test user
- [ ] Redirects to dashboard after sign-in
- [ ] User appears in Clerk dashboard
- [ ] Protected routes enforce authentication
- [ ] Middleware functioning correctly

### Code Integrity
- [ ] No code changes required (only env vars updated)
- [ ] middleware.ts unchanged
- [ ] layout.tsx unchanged
- [ ] All other files unchanged

**When all checkboxes are complete → Proceed to Phase 3**

---

## 📊 PHASE 2 METRICS

**Track for Post-Execution Analysis:**

```yaml
execution_time:
  get_keys: [actual minutes]
  update_env: [actual minutes]
  rebuild: [actual minutes]
  testing: [actual minutes]
  total: [actual minutes]

issues_encountered:
  - [list any issues]
  - [and how resolved]

success_rate:
  first_attempt: [yes/no]
  attempts_needed: [number]

backend_health_maintained: [yes/no]
data_integrity: [all volumes intact: yes/no]
```

---

**Next Step:** Complete this phase, then proceed to Phase 3 for documentation and learning capture.
