# Clerk Authentication Configuration Guide

**Date:** 2025-11-04
**Status:** Environment Configured - Implementation Pending
**Reference:** `/home/jim/2_OXOT_Projects_Dev/Agents_Special/docs/Clerk_Quick_Start.md`

## Overview

This document provides the complete configuration and implementation guide for Clerk authentication in the AEON Digital Twin SaaS application using Next.js App Router.

## Current Configuration Status

### ✅ Completed

1. **Environment Variables Configured** (`.env.development`)
   - `CLERK_PUBLISHABLE_KEY_DEV` - Placeholder ready for actual key
   - `CLERK_SECRET_KEY_DEV` - Placeholder ready for actual key
   - `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` - References DEV key
   - `CLERK_SECRET_KEY` - References DEV key
   - Clerk URLs configured:
     - Sign In: `/sign-in`
     - Sign Up: `/sign-up`
     - After Sign In: `/dashboard`
     - After Sign Up: `/dashboard`

2. **OpenAI API Key Configured**
   - `OPENAI_API_KEY` - ✅ Configured with project key

3. **Clerk Quick Start Guide Stored**
   - Stored in Qdrant memory (namespace: `aeon-ui-redesign`)
   - Key: `clerk-authentication-guide`
   - Accessible for future reference

### 🔜 Pending Implementation

1. **Get Clerk API Keys**
   - Visit: https://dashboard.clerk.com/last-active?path=api-keys
   - Copy Publishable Key → Update `CLERK_PUBLISHABLE_KEY_DEV`
   - Copy Secret Key → Update `CLERK_SECRET_KEY_DEV`

2. **Create `middleware.ts`**
   - Location: Project root or `src/` directory
   - Implementation required (see below)

3. **Update `app/layout.tsx`**
   - Wrap with `<ClerkProvider>`
   - Add authentication UI components

## Implementation Guide

### Step 1: Get Clerk API Keys

1. Sign up or log in to Clerk Dashboard: https://dashboard.clerk.com
2. Create a new application or select existing one
3. Navigate to **API Keys** page
4. Copy your keys:
   - **Publishable Key** (starts with `pk_test_` or `pk_live_`)
   - **Secret Key** (starts with `sk_test_` or `sk_live_`)

5. Update `.env.development`:
   ```bash
   CLERK_PUBLISHABLE_KEY_DEV=pk_test_your_actual_key_here
   CLERK_SECRET_KEY_DEV=sk_test_your_actual_key_here
   ```

### Step 2: Install Clerk Package

```bash
npm install @clerk/nextjs
```

**Current Status:** Check if already installed in `package.json`

### Step 3: Create `middleware.ts`

**Location:** `/home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/web_interface/middleware.ts`

```typescript
// middleware.ts
import { clerkMiddleware } from "@clerk/nextjs/server";

export default clerkMiddleware();

export const config = {
  matcher: [
    // Skip Next.js internals and all static files, unless found in search params
    "/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)",
    // Always run for API routes
    "/(api|trpc)(.*)",
  ],
};
```

### Step 4: Update `app/layout.tsx`

**Current File:** `/home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/web_interface/app/layout.tsx`

**Required Changes:**

1. Add Clerk imports:
```typescript
import {
  ClerkProvider,
  SignInButton,
  SignUpButton,
  SignedIn,
  SignedOut,
  UserButton,
} from "@clerk/nextjs";
```

2. Wrap the application with `<ClerkProvider>`:
```typescript
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body>
          <header>
            <SignedOut>
              <SignInButton />
              <SignUpButton />
            </SignedOut>
            <SignedIn>
              <UserButton />
            </SignedIn>
          </header>
          {children}
        </body>
      </html>
    </ClerkProvider>
  );
}
```

### Step 5: Add Authentication Components

**Available Clerk Components:**

- `<SignInButton />` - Renders sign-in button
- `<SignUpButton />` - Renders sign-up button
- `<UserButton />` - Renders user profile button with dropdown
- `<SignedIn>` - Renders children only when user is signed in
- `<SignedOut>` - Renders children only when user is signed out

**Example Usage in Pages:**

```typescript
import { SignedIn, SignedOut, UserButton } from "@clerk/nextjs";

export default function DashboardPage() {
  return (
    <div>
      <SignedIn>
        <UserButton />
        <h1>Welcome to your dashboard!</h1>
        {/* Protected content */}
      </SignedIn>

      <SignedOut>
        <p>Please sign in to access the dashboard.</p>
      </SignedOut>
    </div>
  );
}
```

## Critical Rules (MUST FOLLOW)

### ✅ ALWAYS DO

1. **Use `clerkMiddleware()`** from `@clerk/nextjs/server` in `middleware.ts`
2. **Wrap app with `<ClerkProvider>`** in `app/layout.tsx`
3. **Import from correct packages:**
   - UI components: `@clerk/nextjs`
   - Server utilities: `@clerk/nextjs/server`
4. **Use App Router approach** (not pages-based)
5. **Store real keys only in `.env.local`** or `.env.development`
6. **Verify `.gitignore` excludes `.env*`**
7. **Use placeholders in code examples**

### ❌ NEVER DO

1. **Do not reference `_app.tsx`** or pages-based structure
2. **Do not use `authMiddleware()`** (deprecated, use `clerkMiddleware()`)
3. **Do not use older environment variable patterns**
4. **Do not import from deprecated APIs**
5. **Do not print actual keys** in code, logs, or documentation
6. **Do not create tracked files with real key values**

## Verification Checklist

Before deploying authentication:

- [ ] Clerk package installed (`@clerk/nextjs`)
- [ ] Actual API keys obtained from Clerk Dashboard
- [ ] `.env.development` updated with real keys
- [ ] `middleware.ts` created with `clerkMiddleware()`
- [ ] `app/layout.tsx` wrapped with `<ClerkProvider>`
- [ ] Clerk components added to UI
- [ ] `.gitignore` excludes `.env*` files
- [ ] Test sign-in/sign-up flow works
- [ ] User creation confirmed in Clerk Dashboard

## Environment Variables Reference

### Current Configuration (`.env.development`)

```bash
# Clerk Authentication (Development)
CLERK_PUBLISHABLE_KEY_DEV=pk_test_your_development_key_here  # ⚠️ UPDATE
CLERK_SECRET_KEY_DEV=sk_test_your_development_key_here       # ⚠️ UPDATE

# Clerk URLs (Already Configured ✅)
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=${CLERK_PUBLISHABLE_KEY_DEV}
CLERK_SECRET_KEY=${CLERK_SECRET_KEY_DEV}
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up
NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL=/dashboard
NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL=/dashboard
```

### Variable Explanations

| Variable | Purpose | Visibility | Required |
|----------|---------|------------|----------|
| `CLERK_PUBLISHABLE_KEY_DEV` | Client-side authentication | Public | Yes |
| `CLERK_SECRET_KEY_DEV` | Server-side API calls | Private | Yes |
| `NEXT_PUBLIC_CLERK_SIGN_IN_URL` | Custom sign-in page URL | Public | No |
| `NEXT_PUBLIC_CLERK_SIGN_UP_URL` | Custom sign-up page URL | Public | No |
| `NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL` | Redirect after sign-in | Public | No |
| `NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL` | Redirect after sign-up | Public | No |

## Integration with AEON Architecture

### Multi-Database Strategy

Clerk manages **user authentication**, while the AEON system uses **PostgreSQL** for user profiles, teams, and RBAC:

```
Clerk (Authentication)
  ↓ User ID
PostgreSQL (User Profiles)
  ├─ users table (synced with Clerk user IDs)
  ├─ teams table
  ├─ team_members table
  └─ user_roles table (RBAC)
```

### Synchronization Pattern

1. User signs in via Clerk → Clerk User ID generated
2. Webhook or API call creates user record in PostgreSQL
3. User ID stored in PostgreSQL `users.clerk_id` column
4. Team membership and roles managed in PostgreSQL
5. Authentication state managed by Clerk
6. Authorization (permissions) managed by AEON

### Database Schema Integration

**PostgreSQL `users` table** (from `scripts/init-db.sql`):

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    clerk_id VARCHAR(255) UNIQUE NOT NULL,  -- Clerk User ID
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(255),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    avatar_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_sign_in_at TIMESTAMP WITH TIME ZONE,
    metadata JSONB DEFAULT '{}'::jsonb
);
```

## Server-Side Authentication

### Using `auth()` in API Routes

```typescript
// app/api/protected/route.ts
import { auth } from "@clerk/nextjs/server";

export async function GET() {
  const { userId } = await auth();

  if (!userId) {
    return new Response("Unauthorized", { status: 401 });
  }

  // User is authenticated
  return Response.json({ message: "Protected data", userId });
}
```

### Using `currentUser()` for User Details

```typescript
// app/api/user/route.ts
import { currentUser } from "@clerk/nextjs/server";

export async function GET() {
  const user = await currentUser();

  if (!user) {
    return new Response("Unauthorized", { status: 401 });
  }

  // Access user details
  return Response.json({
    id: user.id,
    email: user.emailAddresses[0].emailAddress,
    firstName: user.firstName,
    lastName: user.lastName,
  });
}
```

## Testing Authentication

### Manual Testing Steps

1. **Start development server:**
   ```bash
   docker-compose -f docker-compose.dev.yml up
   # or
   npm run dev
   ```

2. **Navigate to:** http://localhost:3000

3. **Test sign-up flow:**
   - Click "Sign Up" button
   - Complete registration
   - Verify redirect to `/dashboard`
   - Check user appears in Clerk Dashboard

4. **Test sign-in flow:**
   - Sign out
   - Click "Sign In" button
   - Enter credentials
   - Verify redirect to `/dashboard`

5. **Test protected routes:**
   - Try accessing `/dashboard` without signing in
   - Should redirect to sign-in page

6. **Test user button:**
   - Click user avatar/button
   - Verify dropdown with profile options
   - Test sign-out functionality

## Troubleshooting

### Issue: "Invalid publishable key"

**Solution:**
- Verify key starts with `pk_test_` or `pk_live_`
- Check key is correctly set in `.env.development`
- Restart development server after updating

### Issue: "Clerk is not defined"

**Solution:**
- Verify `<ClerkProvider>` wraps your app in `app/layout.tsx`
- Check imports are from `@clerk/nextjs`
- Clear `.next` cache: `rm -rf .next`

### Issue: Infinite redirect loop

**Solution:**
- Check middleware matcher pattern
- Verify sign-in URL is not in protected routes
- Review `NEXT_PUBLIC_CLERK_SIGN_IN_URL` configuration

### Issue: User not syncing to PostgreSQL

**Solution:**
- Implement webhook handler for Clerk events
- Create API route to sync user data
- Update `users` table with `clerk_id`

## Next Steps

### Immediate (Week 1-2)

1. ✅ Environment variables configured
2. ✅ OpenAI API key set
3. ✅ Clerk guide stored in memory
4. 🔜 Get Clerk API keys from dashboard
5. 🔜 Create `middleware.ts`
6. 🔜 Update `app/layout.tsx` with `<ClerkProvider>`
7. 🔜 Add authentication UI components

### Short-term (Week 3-4)

1. Implement Clerk webhook handler
2. Sync Clerk users to PostgreSQL
3. Create user profile API routes
4. Implement RBAC with team roles
5. Add protected route guards
6. Test authentication flow end-to-end

### Long-term (Week 5-16)

1. Integrate with AEON dashboard pages
2. Add team management UI
3. Implement invitation system
4. Add API key management
5. Create audit logging
6. Add SSO configuration (if needed)

## Reference Documentation

- **Clerk Official Docs:** https://clerk.com/docs/quickstarts/nextjs
- **Clerk Dashboard:** https://dashboard.clerk.com
- **Clerk API Reference:** https://clerk.com/docs/reference/backend-api
- **Next.js App Router:** https://nextjs.org/docs/app
- **AEON Integration Plan:** See `/home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Front End UI Builder/SAAS_BOILERPLATE_AEON_INTEGRATION_PLAN.md`

## Memory Reference

**Qdrant Namespace:** `aeon-ui-redesign`
**Memory Key:** `clerk-authentication-guide`
**Retrieval Command:**
```typescript
await memoryUsage({
  action: "retrieve",
  namespace: "aeon-ui-redesign",
  key: "clerk-authentication-guide"
});
```

---

**Configuration Status:** ✅ Environment Configured
**Implementation Status:** 🔜 Pending Clerk API Keys and Code Implementation
**Last Updated:** 2025-11-04
**Next Action:** Obtain Clerk API keys from dashboard and implement `middleware.ts`
