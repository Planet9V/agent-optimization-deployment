# Clerk Quick Setup Guide - Get AEON Running in 30 Minutes

**Current Status:** App returning 500 errors due to invalid/expired Clerk API keys
**Solution:** Get fresh keys from Clerk dashboard
**Time Required:** 30 minutes
**Result:** Fully operational authentication + UI

---

## Step 1: Get Clerk API Keys (10 minutes)

### A. Access Clerk Dashboard
1. Visit: https://dashboard.clerk.com
2. Sign in (or create account if first time)

### B. Create/Select Application
- **Option 1 - New App:** Click "Add application" button
  - Name: `AEON Digital Twin - Development`
  - Select: `Next.js`
  - Framework: `App Router`

- **Option 2 - Existing:** Select your AEON application from list

### C. Copy API Keys
1. Navigate to: **API Keys** (left sidebar or https://dashboard.clerk.com/last-active?path=api-keys)
2. Find section: **Quick Copy**
3. Copy two keys:
   - **Publishable Key** (starts with `pk_test_`)
   - **Secret Key** (starts with `sk_test_`)

**⚠️ IMPORTANT:** Keep secret key private - never commit to git!

---

## Step 2: Update Environment Variables (5 minutes)

### Location
`/home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/web_interface/.env.development`

### Update These Lines
```bash
# OLD (invalid/expired keys)
CLERK_PUBLISHABLE_KEY_DEV=pk_test_dmFsaWQtc2FpbGZpc2gtOTUuY2xlcmsuYWNjb3VudHMuZGV2JA
CLERK_SECRET_KEY_DEV=sk_test_5jjk7jSqlDy3FXX8OVWAH4JFfhcQ5ohI3m3cBDL6bm

# NEW (paste your actual keys from Clerk dashboard)
CLERK_PUBLISHABLE_KEY_DEV=pk_test_[PASTE_YOUR_KEY_HERE]
CLERK_SECRET_KEY_DEV=sk_test_[PASTE_YOUR_KEY_HERE]
```

### Verify Other Settings (should already be correct)
```bash
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=${CLERK_PUBLISHABLE_KEY_DEV}
CLERK_SECRET_KEY=${CLERK_SECRET_KEY_DEV}
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up
NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL=/dashboard
NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL=/dashboard
```

---

## Step 3: Rebuild Container (10 minutes)

### Commands
```bash
# Navigate to project directory
cd /home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/web_interface

# Stop current container
docker-compose -f docker-compose.dev.yml down

# Rebuild with new environment variables
docker-compose -f docker-compose.dev.yml up --build -d

# Monitor startup
docker logs -f aeon-saas-dev
```

### Expected Output
```
✓ Ready in [time]
○ Compiling /...
✓ Compiled successfully
```

### Stop Monitoring
Press `Ctrl+C` to exit logs

---

## Step 4: Verify Application (5 minutes)

### A. Check Container Health
```bash
docker ps --filter "name=aeon-saas-dev"
```
**Expected:** Status shows `healthy` (may take 30-60 seconds)

### B. Test Homepage
Open browser: http://localhost:3000

**Expected:**
- Page loads without errors
- See AEON dashboard interface
- **NO** 500 Internal Server Error

### C. Test Health Endpoint
```bash
curl http://localhost:3000/api/health
```
**Expected:** JSON response with services status (not "Internal Server Error")

### D. Test Authentication Flow
1. Open: http://localhost:3000
2. Click "Sign In" button (top right)
3. You should see Clerk sign-in modal
4. Try signing up with test account:
   - Email: test@aeon.local
   - Password: TestPassword123!
5. After signup, should redirect to `/dashboard`

---

## Troubleshooting

### Issue: Container Still Unhealthy After Rebuild

**Check logs for errors:**
```bash
docker logs aeon-saas-dev --tail 50
```

**Common causes:**
- **Invalid Clerk keys:** Double-check you copied complete keys from dashboard
- **Whitespace in keys:** Ensure no extra spaces before/after keys in .env file
- **Environment not loaded:** Verify `.env.development` exists and is readable

**Solution:**
```bash
# Verify environment file
cat .env.development | grep CLERK

# Force rebuild
docker-compose -f docker-compose.dev.yml down
docker system prune -f
docker-compose -f docker-compose.dev.yml up --build -d
```

### Issue: "Invalid Publishable Key" Error

**Symptom:** Console shows Clerk error about invalid key

**Causes:**
- Copied wrong key type (secret instead of publishable or vice versa)
- Key from different Clerk application
- Key is for wrong environment (production vs development)

**Solution:**
1. Return to Clerk dashboard
2. Verify you're in correct application
3. Copy keys again carefully:
   - Publishable key → `CLERK_PUBLISHABLE_KEY_DEV`
   - Secret key → `CLERK_SECRET_KEY_DEV`

### Issue: Clerk Modal Not Appearing

**Symptom:** Sign-in button does nothing

**Solution:**
```bash
# Check browser console for errors (F12 → Console tab)
# Common issue: ClerkProvider not initialized

# Verify layout.tsx has ClerkProvider
docker exec aeon-saas-dev cat app/layout.tsx | grep ClerkProvider
```

### Issue: Redirect Loop After Sign-In

**Symptom:** Signs in but keeps redirecting

**Causes:**
- Middleware protecting sign-in routes incorrectly
- Redirect URLs misconfigured

**Check middleware:**
```bash
docker exec aeon-saas-dev cat middleware.ts
```

**Verify these routes are public:**
- `/sign-in`
- `/sign-up`
- `/`
- `/api/health`

---

## Next Steps After Clerk is Working

### 1. Create Test Users
- Sign up 2-3 test accounts
- Verify user appears in Clerk dashboard
- Test sign-out/sign-in flow

### 2. Test Protected Routes
- Visit http://localhost:3000/dashboard (should work when signed in)
- Sign out
- Try accessing /dashboard again (should redirect to sign-in)

### 3. Begin UI Development
With authentication working, proceed with:
- Backend data integration (Neo4j, Qdrant queries)
- Dashboard visualizations
- Search functionality
- Graph explorer

---

## Quick Reference: Complete Workflow

```bash
# 1. Get keys from https://dashboard.clerk.com
# 2. Update .env.development with real keys
# 3. Rebuild:
docker-compose -f docker-compose.dev.yml down
docker-compose -f docker-compose.dev.yml up --build -d

# 4. Verify:
docker logs -f aeon-saas-dev  # Watch for "Ready"
curl http://localhost:3000    # Should return HTML, not "Internal Server Error"

# 5. Test in browser:
open http://localhost:3000    # Homepage loads
# Click Sign In → Clerk modal appears
# Sign up test user → Redirects to /dashboard
```

---

## Why This Approach is Recommended

✅ **Fast:** 30 minutes total
✅ **Production-Ready:** Proper authentication from start
✅ **No Technical Debt:** Nothing to remove/refactor later
✅ **Secure:** Routes properly protected
✅ **Complete:** User management fully functional
✅ **Backend Ready:** All 5 services already operational

**Alternative (Not Recommended):** Bypassing Clerk temporarily means:
- Additional work later to re-enable
- Security gaps during development
- Risk of forgetting to add auth before production
- Testing without realistic authentication flows

---

**Status After Completion:**
- ✅ Container: Healthy
- ✅ Authentication: Working
- ✅ Backend: 5/5 services operational
- ✅ Ready For: Full UI development

**Time Investment:** 30 minutes now saves hours of debugging and refactoring later.
