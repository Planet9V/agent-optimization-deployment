# Clerk Authentication Integration

**File:** Clerk_Authentication_Integration.md
**Created:** 2025-11-04
**Version:** 1.0.0
**Category:** Security / Authentication
**Status:** ACTIVE

---

## Table of Contents

1. [Overview](#overview)
2. [Quick Start Guide](#quick-start-guide)
3. [Components Reference](#components-reference)
4. [Hooks Reference](#hooks-reference)
5. [Server-Side Helpers](#server-side-helpers)
6. [Middleware Configuration](#middleware-configuration)
7. [Custom Onboarding Flow](#custom-onboarding-flow)
8. [Organizations & Multi-Tenancy](#organizations--multi-tenancy)
9. [Production Deployment](#production-deployment)
10. [Appearance Customization](#appearance-customization)
11. [Best Practices](#best-practices)
12. [Troubleshooting](#troubleshooting)

---

## Overview

### What is Clerk?

Clerk is a complete user authentication and management solution for Next.js applications. It provides:

- **Pre-built UI components** for sign-in, sign-up, and user management
- **Multiple authentication strategies** (email/password, OAuth, magic links, SMS)
- **Organization management** for multi-tenant B2B applications
- **Role-based access control** (RBAC) and permissions
- **Session management** with multi-session support
- **Production-ready security** with JWT tokens and middleware protection

### Key Features

- 🔐 **Complete Authentication Flow** - Sign-in, sign-up, password reset, email verification
- 👤 **User Management** - Profile management, account settings, avatar uploads
- 🏢 **Organizations** - Multi-tenant B2B applications with team management
- 🔑 **OAuth Providers** - Google, GitHub, Microsoft, Facebook, and more
- 📱 **Multi-factor Authentication** - TOTP, SMS, backup codes
- 🎨 **Customizable UI** - Fully customizable components with theming support
- ⚡ **Next.js Optimized** - Built specifically for App Router and Pages Router

### Framework Support

- **Next.js App Router** (Recommended) - Modern Next.js with Server Components
- **Next.js Pages Router** - Legacy Next.js routing system
- **SDK Package:** `@clerk/nextjs`
- **Documentation:** https://clerk.com/docs/nextjs

---

## Quick Start Guide

### Stage 1: Create Next.js Application

Create a new Next.js project using your preferred package manager:

```bash
# Using npm
npm create next-app@latest my-clerk-app -- --yes

# Using yarn
yarn create next-app my-clerk-app --yes

# Using pnpm
pnpm create next-app my-clerk-app --yes

# Using bun
bun create next-app my-clerk-app --yes
```

**Notes:**
- Choose package manager based on your preference
- All commands scaffold identical Next.js projects

### Stage 2: Install Clerk SDK

Add the Clerk Next.js SDK to your project:

```bash
# Using npm
npm install @clerk/nextjs

# Using yarn
yarn add @clerk/nextjs

# Using pnpm
pnpm add @clerk/nextjs

# Using bun
bun add @clerk/nextjs
```

**Package:** `@clerk/nextjs`
**Purpose:** Next.js-specific Clerk SDK with App Router and Pages Router support

### Stage 3: Configure Environment Variables

Create a `.env.local` file in your project root with your Clerk API keys:

```env
# Required Environment Variables
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
CLERK_SECRET_KEY=sk_test_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Optional: Custom URLs
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up
NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL=/dashboard
NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL=/dashboard
```

#### Required Variables

| Variable | Description | Format | Source |
|----------|-------------|--------|--------|
| `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` | Client-side publishable key | `pk_test_*` (dev) or `pk_live_*` (prod) | Clerk Dashboard > API Keys |
| `CLERK_SECRET_KEY` | Server-side secret key | `sk_test_*` (dev) or `sk_live_*` (prod) | Clerk Dashboard > API Keys |

#### Optional Variables

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `NEXT_PUBLIC_CLERK_SIGN_IN_URL` | Custom sign-in page path | `/sign-in` | `/auth/login` |
| `NEXT_PUBLIC_CLERK_SIGN_UP_URL` | Custom sign-up page path | `/sign-up` | `/auth/register` |
| `NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL` | Redirect after sign-in | `/` | `/dashboard` |
| `NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL` | Redirect after sign-up | `/` | `/onboarding` |
| `CLERK_ENCRYPTION_KEY` | Required for dynamic keys | - | Used with middleware options |

### Stage 4: Add Middleware

Create `middleware.ts` in your project root or `/src` directory:

```typescript
import { clerkMiddleware } from '@clerk/nextjs/server'

export default clerkMiddleware()

export const config = {
  matcher: [
    '/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)',
    '/(api|trpc)(.*)',
  ],
}
```

**Important:** By default, ALL routes are PUBLIC. You must explicitly protect routes that require authentication.

#### Route Protection Patterns

**Protect Specific Routes:**

```typescript
import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server'

const isProtectedRoute = createRouteMatcher(['/dashboard(.*)', '/forum(.*)'])

export default clerkMiddleware(async (auth, req) => {
  if (isProtectedRoute(req)) await auth.protect()
})
```

**Protect All Except Public Routes:**

```typescript
const isPublicRoute = createRouteMatcher(['/sign-in(.*)', '/sign-up(.*)', '/'])

export default clerkMiddleware(async (auth, req) => {
  if (!isPublicRoute(req)) await auth.protect()
})
```

**Permission-Based Protection:**

```typescript
await auth.protect((has) => {
  return has({ permission: 'org:admin:example' })
})
```

### Stage 5: Add ClerkProvider to Layout

Wrap your application with `ClerkProvider` in `app/layout.tsx`:

```typescript
import {
  ClerkProvider,
  SignInButton,
  SignUpButton,
  SignedIn,
  SignedOut,
  UserButton,
} from '@clerk/nextjs'
import './globals.css'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body>
          <header className="flex justify-end items-center p-4 gap-4 h-16">
            <SignedOut>
              <SignInButton />
              <SignUpButton>
                <button className="bg-[#6c47ff] text-white rounded-full px-4 py-2">
                  Sign Up
                </button>
              </SignUpButton>
            </SignedOut>
            <SignedIn>
              <UserButton />
            </SignedIn>
          </header>
          {children}
        </body>
      </html>
    </ClerkProvider>
  )
}
```

**Key Components Used:**

- `ClerkProvider` - Provides authentication context application-wide
- `SignedIn` - Conditional rendering for authenticated users
- `SignedOut` - Conditional rendering for unauthenticated users
- `SignInButton` - Pre-built sign-in button
- `SignUpButton` - Pre-built sign-up button
- `UserButton` - User profile menu with account management

### Stage 6: Run Development Server

Start your Next.js development server:

```bash
# Using npm
npm run dev

# Using yarn
yarn dev

# Using pnpm
pnpm dev

# Using bun
bun dev
```

**Testing Steps:**

1. Visit http://localhost:3000
2. Click 'Sign Up' button
3. Complete sign-up flow
4. Verify user appears in Clerk Dashboard
5. Test sign-out and sign-in flows

**Expected Behavior:**

- **Signed Out:** Shows SignInButton and SignUpButton
- **Signed In:** Shows UserButton with user avatar
- **UserButton Click:** Opens dropdown with "Manage account" and "Sign out"

---

## Components Reference

### Authentication Components

#### SignIn

Complete sign-in UI with authentication strategies.

```typescript
import { SignIn } from '@clerk/nextjs'

export default function SignInPage() {
  return <SignIn />
}
```

**Props:**

| Prop | Type | Description | Default |
|------|------|-------------|---------|
| `appearance` | `Appearance` | Customize component styling | - |
| `fallbackRedirectUrl` | `string` | Redirect after sign-in | `/` |
| `forceRedirectUrl` | `string` | Always redirect to this URL | - |
| `initialValues` | `SignInInitialValues` | Pre-fill form fields | - |
| `oauthFlow` | `'redirect' \| 'popup' \| 'auto'` | OAuth authentication method | `auto` |
| `routing` | `'hash' \| 'path'` | Routing strategy | `path` |

**Important Notes:**
- Cannot render when user is signed in (unless multi-session enabled)
- Automatically redirects signed-in users
- Configure strategies in Clerk Dashboard

#### SignUp

Complete sign-up UI with registration strategies.

```typescript
import { SignUp } from '@clerk/nextjs'

export default function SignUpPage() {
  return <SignUp />
}
```

**Props:**

| Prop | Type | Description | Default |
|------|------|-------------|---------|
| `appearance` | `Appearance` | Customize component styling | - |
| `fallbackRedirectUrl` | `string` | Redirect after sign-up | `/` |
| `forceRedirectUrl` | `string` | Always redirect to this URL | - |
| `initialValues` | `SignUpInitialValues` | Pre-fill form fields | - |
| `unsafeMetadata` | `object` | Custom metadata for user profile | - |

#### SignInButton / SignUpButton

Buttons that trigger authentication flows.

```typescript
import { SignInButton, SignUpButton } from '@clerk/nextjs'

// Default buttons
<SignInButton />
<SignUpButton />

// Custom buttons
<SignInButton mode="modal">
  <button>Custom Sign In</button>
</SignInButton>

<SignUpButton mode="modal">
  <button className="btn-primary">Get Started</button>
</SignUpButton>
```

### Control Components

#### SignedIn / SignedOut

Conditional rendering based on authentication state.

```typescript
import { SignedIn, SignedOut } from '@clerk/nextjs'

export default function Navigation() {
  return (
    <nav>
      <SignedOut>
        <SignInButton />
      </SignedOut>
      <SignedIn>
        <UserProfile />
      </SignedIn>
    </nav>
  )
}
```

### User Components

#### UserButton

User profile button with dropdown menu.

```typescript
import { UserButton } from '@clerk/nextjs'

export default function Header() {
  return (
    <header>
      <UserButton />
    </header>
  )
}
```

**Props:**

| Prop | Type | Description | Default |
|------|------|-------------|---------|
| `afterSwitchSessionUrl` | `string` | Navigation after account switching | - |
| `appearance` | `Appearance` | Customize styling | - |
| `showName` | `boolean` | Display user name beside avatar | `false` |
| `userProfileMode` | `'modal' \| 'navigation'` | Profile opens as modal or page | `modal` |

**Default Menu Items:**
- Manage account (opens UserProfile)
- Sign out

**Customization:**

```typescript
<UserButton>
  <UserButton.MenuItems>
    <UserButton.Link
      label="Settings"
      labelIcon={<SettingsIcon />}
      href="/settings"
    />
    <UserButton.Action
      label="Help"
      labelIcon={<HelpIcon />}
      onClick={() => openHelpModal()}
    />
  </UserButton.MenuItems>
</UserButton>
```

#### UserProfile

Complete user profile management interface.

```typescript
import { UserProfile } from '@clerk/nextjs'

export default function ProfilePage() {
  return <UserProfile />
}
```

**Features:**
- Update profile information
- Change password
- Manage connected accounts
- Security settings
- Delete account

### Organization Components

#### OrganizationSwitcher

Dropdown to create and switch between organizations.

```typescript
import { OrganizationSwitcher } from '@clerk/nextjs'

export default function Header() {
  return (
    <header>
      <OrganizationSwitcher />
    </header>
  )
}
```

**Features:**
- Create new organizations
- Switch between organizations
- Invite members
- Manage organization settings

#### OrganizationProfile

Organization management interface for settings, members, and permissions.

#### OrganizationList

Display all user's organizations for navigation and management.

---

## Hooks Reference

### Client-Side Hooks

#### useUser

Access current user's User object and authentication state.

```typescript
import { useUser } from '@clerk/nextjs'

export default function Profile() {
  const { isLoaded, isSignedIn, user } = useUser()

  if (!isLoaded) return <div>Loading...</div>
  if (!isSignedIn) return <div>Not signed in</div>

  return <div>Hello, {user.firstName}!</div>
}
```

**Return Values:**

| Property | Type | Description |
|----------|------|-------------|
| `isLoaded` | `boolean` | Clerk initialization complete |
| `isSignedIn` | `boolean` | User authentication status |
| `user` | `User \| null \| undefined` | Complete user object |

**User Object Properties:**

- `id` - Unique user identifier
- `firstName` / `lastName` / `fullName` - Name fields
- `emailAddress` / `primaryEmailAddress` - Email fields
- `phoneNumbers` - Array of phone numbers
- `imageUrl` - Avatar URL
- `publicMetadata` / `privateMetadata` / `unsafeMetadata` - Custom metadata
- `createdAt` / `updatedAt` - Timestamps

**User Methods:**

- `update()` - Update user information
- `reload()` - Refresh user data from server
- `delete()` - Delete user account

#### useAuth

Access authentication state and session management methods.

```typescript
import { useAuth } from '@clerk/nextjs'

export default function DataFetcher() {
  const { isSignedIn, userId, getToken, signOut } = useAuth()

  const fetchData = async () => {
    const token = await getToken()
    const response = await fetch('/api/data', {
      headers: { Authorization: `Bearer ${token}` }
    })
    return response.json()
  }

  return <div>...</div>
}
```

**Return Values:**

| Property | Type | Description |
|----------|------|-------------|
| `isLoaded` | `boolean` | Clerk loaded |
| `isSignedIn` | `boolean` | Authentication status |
| `userId` | `string \| null` | Current user ID |
| `sessionId` | `string \| null` | Current session ID |
| `orgId` | `string \| null` | Active organization ID |
| `orgRole` | `string \| null` | User's role in organization |
| `getToken()` | `Promise<string \| null>` | Retrieve session token |
| `signOut()` | `Promise<void>` | Sign out current user |

**getToken Usage:**

```typescript
// Basic usage
const token = await getToken()

// With custom JWT template
const token = await getToken({ template: 'custom_jwt' })

// For integrations (must prefix with 'integration_')
const token = await getToken({ template: 'integration_firebase' })
```

#### useClerk

Access Clerk instance and global methods.

```typescript
import { useClerk } from '@clerk/nextjs'

export default function CustomAuth() {
  const clerk = useClerk()

  const handleSignIn = () => {
    clerk.openSignIn()
  }

  return <button onClick={handleSignIn}>Sign In</button>
}
```

**Methods:**

- `openSignIn()` - Open sign-in modal
- `openSignUp()` - Open sign-up modal
- `openUserProfile()` - Open user profile modal
- `redirectToSignIn()` - Navigate to sign-in page
- `redirectToSignUp()` - Navigate to sign-up page
- `setActive()` - Set active session/organization

#### useOrganization

Access current organization information.

```typescript
import { useOrganization } from '@clerk/nextjs'

export default function OrgDashboard() {
  const { organization, membership, isLoaded } = useOrganization()

  if (!isLoaded) return <div>Loading...</div>
  if (!organization) return <div>No organization</div>

  if (membership?.role === 'admin') {
    return <AdminPanel />
  }

  return <div>{organization.name}</div>
}
```

**Return Values:**

- `organization` - Organization object
- `membership` - User's membership in organization
- `isLoaded` - Loading state

#### Additional Hooks

- `useSignIn()` - Programmatic sign-in flow control
- `useSignUp()` - Programmatic sign-up flow control
- `useSession()` - Access current session information
- `useSessionList()` - Manage multiple active sessions
- `useOrganizationList()` - Access list of user's organizations

---

## Server-Side Helpers

### App Router (Recommended)

#### auth()

Returns authentication data for server components and route handlers.

```typescript
import { auth } from '@clerk/nextjs/server'

export default async function DashboardPage() {
  const { userId, sessionId, orgId } = await auth()

  if (!userId) {
    return <div>Not authenticated</div>
  }

  return <div>User ID: {userId}</div>
}
```

**Return Type:** `Promise<Auth>`

**Auth Object Properties:**

- `userId` - Current user ID
- `sessionId` - Current session ID
- `orgId` - Active organization ID
- `orgRole` - User role in organization
- `orgSlug` - Organization slug
- `sessionClaims` - Full JWT claims
- `isAuthenticated` - Authentication status

**Methods:**

```typescript
// Throw error if not authenticated
await auth.protect()

// Protect with permission check
await auth.protect((has) => has({ permission: 'org:admin' }))

// Redirect to sign-in
return auth.redirectToSignIn()
```

**Usage Contexts:**

- Server Components
- Route Handlers (app/api/**/route.ts)
- Server Actions
- Middleware

#### currentUser()

Retrieve current user's complete Backend User object.

```typescript
import { currentUser } from '@clerk/nextjs/server'

export default async function ProfilePage() {
  const user = await currentUser()

  if (!user) return <div>Not signed in</div>

  return (
    <div>
      <h1>{user.fullName}</h1>
      <p>{user.primaryEmailAddress?.emailAddress}</p>
    </div>
  )
}
```

**Return Type:** `Promise<User | null>`

**⚠️ Rate Limit Warning:** Counts towards Backend API request rate limit.
**Recommendation:** Use client-side `useUser()` when possible to avoid rate limits.

#### clerkClient

Access Backend API for user/organization management.

```typescript
import { auth, clerkClient } from '@clerk/nextjs/server'

export async function POST(req: Request) {
  const { userId } = await auth()
  const client = await clerkClient()

  await client.users.updateUser(userId, {
    publicMetadata: { role: 'admin' }
  })

  return Response.json({ success: true })
}
```

**Methods:**

**Users:**
- `getUser(id)` - Fetch user by ID
- `getUserList()` - List all users
- `updateUser(id, data)` - Update user
- `deleteUser(id)` - Delete user
- `createUser(data)` - Create new user

**Organizations:**
- `getOrganization(id)` - Fetch organization
- `getOrganizationList()` - List organizations
- `createOrganization(data)` - Create organization
- `updateOrganization(id, data)` - Update organization
- `deleteOrganization(id)` - Delete organization

**Sessions:**
- `getSession(id)` - Fetch session
- `getSessionList(userId)` - List user sessions
- `revokeSession(id)` - Revoke session

### Pages Router (Legacy)

#### getAuth()

Extract authentication data from requests.

```typescript
import { getAuth } from '@clerk/nextjs/server'

export async function getServerSideProps(context) {
  const { userId } = getAuth(context.req)

  if (!userId) {
    return { redirect: { destination: '/sign-in', permanent: false } }
  }

  return { props: { userId } }
}
```

**Contexts:**
- `getServerSideProps`
- API Routes
- `getStaticProps` (with SSG helper)

#### buildClerkProps()

Prepare Clerk properties for client-side hydration.

```typescript
import { buildClerkProps, getAuth } from '@clerk/nextjs/server'

export async function getServerSideProps(context) {
  const { userId } = getAuth(context.req)

  return {
    props: {
      ...buildClerkProps(context.req),
      userId
    }
  }
}
```

**Purpose:** Pass authentication state from server to client.

---

## Middleware Configuration

### Basic Setup

```typescript
import { clerkMiddleware } from '@clerk/nextjs/server'

// Minimal configuration (all routes public)
export default clerkMiddleware()

// With route matcher
export const config = {
  matcher: [
    '/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)',
    '/(api|trpc)(.*)',
  ],
}
```

### Route Protection Strategies

#### Explicit Protection

Protect specific routes only:

```typescript
import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server'

const isProtectedRoute = createRouteMatcher([
  '/dashboard(.*)',
  '/settings(.*)',
  '/api/protected(.*)'
])

export default clerkMiddleware(async (auth, req) => {
  if (isProtectedRoute(req)) await auth.protect()
})
```

#### Protect All Except Public

Default to protected, whitelist public routes:

```typescript
const isPublicRoute = createRouteMatcher([
  '/',
  '/sign-in(.*)',
  '/sign-up(.*)',
  '/api/public(.*)'
])

export default clerkMiddleware(async (auth, req) => {
  if (!isPublicRoute(req)) await auth.protect()
})
```

#### Permission-Based Protection

Protect based on permissions:

```typescript
const isAdminRoute = createRouteMatcher(['/admin(.*)'])

export default clerkMiddleware(async (auth, req) => {
  if (isAdminRoute(req)) {
    await auth.protect((has) => {
      return has({ permission: 'org:admin:access' })
    })
  }
})
```

#### Multi-Level Protection

Different protection levels for different routes:

```typescript
const isPublicRoute = createRouteMatcher(['/'])
const isAuthRoute = createRouteMatcher(['/dashboard(.*)'])
const isAdminRoute = createRouteMatcher(['/admin(.*)'])

export default clerkMiddleware(async (auth, req) => {
  if (isPublicRoute(req)) return

  if (isAdminRoute(req)) {
    return await auth.protect((has) =>
      has({ permission: 'org:admin:access' })
    )
  }

  if (isAuthRoute(req)) {
    return await auth.protect()
  }
})
```

### Configuration Options

| Option | Type | Description |
|--------|------|-------------|
| `audience` | `string \| string[]` | JWT audience claim verification |
| `authorizedParties` | `string[]` | Allowed origins (CSRF protection) |
| `clockSkewInMs` | `number` | Token validation time tolerance (default: 5000ms) |
| `domain` | `string` | Satellite deployment domain |
| `signInUrl` | `string` | Custom sign-in page URL |
| `signUpUrl` | `string` | Custom sign-up page URL |
| `debug` | `boolean` | Enable debug logging |

**Example:**

```typescript
clerkMiddleware({
  authorizedParties: [
    'https://example.com',
    'https://dashboard.example.com'
  ],
  clockSkewInMs: 10000,
  debug: process.env.NODE_ENV === 'development'
})
```

---

## Custom Onboarding Flow

### Overview

Implement mandatory onboarding flow using session tokens and metadata to collect additional user information after sign-up.

### Setup Steps

#### Step 1: Configure Session Token Claims

**Location:** Clerk Dashboard > Sessions

Add custom claims to session token:

```json
{
  "metadata": "{{user.public_metadata}}"
}
```

**TypeScript Types:**

```typescript
declare global {
  interface CustomJwtSessionClaims {
    metadata: {
      onboardingComplete?: boolean
    }
  }
}
```

#### Step 2: Implement Middleware Logic

**File:** `src/middleware.ts` or `src/proxy.ts`

```typescript
import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server'
import { NextResponse } from 'next/server'

const isOnboardingRoute = createRouteMatcher(['/onboarding'])
const isPublicRoute = createRouteMatcher(['/sign-in(.*)', '/sign-up(.*)'])

export default clerkMiddleware(async (auth, req) => {
  const { isAuthenticated, sessionClaims, redirectToSignIn } = await auth()

  // Public routes accessible to all
  if (isPublicRoute(req)) {
    return NextResponse.next()
  }

  // Redirect unauthenticated to sign-in
  if (!isAuthenticated) {
    return redirectToSignIn()
  }

  // Allow access to onboarding page
  if (isOnboardingRoute(req)) {
    return NextResponse.next()
  }

  // Redirect incomplete onboarding
  if (!sessionClaims?.metadata?.onboardingComplete) {
    const onboardingUrl = new URL('/onboarding', req.url)
    return NextResponse.redirect(onboardingUrl)
  }

  return NextResponse.next()
})
```

#### Step 3: Create Onboarding Layout

**File:** `src/app/onboarding/layout.tsx`

```typescript
import { auth } from '@clerk/nextjs/server'
import { redirect } from 'next/navigation'

export default async function OnboardingLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const { sessionClaims } = await auth()

  // Redirect already-onboarded users
  if (sessionClaims?.metadata?.onboardingComplete === true) {
    redirect('/')
  }

  return <>{children}</>
}
```

#### Step 4: Create Onboarding Form

**File:** `src/app/onboarding/page.tsx`

```typescript
'use client'

import { useState } from 'react'
import { completeOnboarding } from './_actions'

export default function OnboardingPage() {
  const [applicationName, setApplicationName] = useState('')
  const [applicationType, setApplicationType] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    const formData = new FormData()
    formData.append('applicationName', applicationName)
    formData.append('applicationType', applicationType)

    await completeOnboarding(formData)
    window.location.href = '/'
  }

  return (
    <div className="min-h-screen flex items-center justify-center">
      <form onSubmit={handleSubmit} className="space-y-4">
        <h1 className="text-2xl font-bold">Complete Your Profile</h1>

        <div>
          <label>Application Name</label>
          <input
            type="text"
            value={applicationName}
            onChange={(e) => setApplicationName(e.target.value)}
            required
          />
        </div>

        <div>
          <label>Application Type</label>
          <select
            value={applicationType}
            onChange={(e) => setApplicationType(e.target.value)}
            required
          >
            <option value="">Select type...</option>
            <option value="web">Web Application</option>
            <option value="mobile">Mobile Application</option>
            <option value="desktop">Desktop Application</option>
          </select>
        </div>

        <button type="submit">Complete Onboarding</button>
      </form>
    </div>
  )
}
```

#### Step 5: Update User Metadata

**File:** `src/app/onboarding/_actions.ts`

```typescript
'use server'

import { auth, clerkClient } from '@clerk/nextjs/server'

export const completeOnboarding = async (formData: FormData) => {
  const { userId } = await auth()

  if (!userId) {
    throw new Error('Not authenticated')
  }

  const client = await clerkClient()

  await client.users.updateUser(userId, {
    publicMetadata: {
      onboardingComplete: true,
      applicationName: formData.get('applicationName'),
      applicationType: formData.get('applicationType'),
    },
  })

  return { success: true }
}
```

### Environment Configuration

```env
NEXT_PUBLIC_CLERK_SIGN_IN_FALLBACK_REDIRECT_URL=/dashboard
NEXT_PUBLIC_CLERK_SIGN_UP_FORCE_REDIRECT_URL=/onboarding
```

### Metadata Types

#### publicMetadata

- **Visibility:** Readable by client and server
- **Writeable:** Server-side only
- **Use Cases:** Onboarding status, user preferences, public profile data

#### privateMetadata

- **Visibility:** Server-side only
- **Writeable:** Server-side only
- **Use Cases:** Sensitive user data, internal flags, admin notes

#### unsafeMetadata

- **Visibility:** Readable by client and server
- **Writeable:** Client and server
- **Use Cases:** User-controlled preferences, temporary data
- **⚠️ Warning:** Can be modified by client - validate server-side

---

## Organizations & Multi-Tenancy

### Overview

Build multi-tenant B2B applications with Clerk Organizations for:

- **B2B SaaS applications**
- **Team collaboration tools**
- **Enterprise applications**
- **Multi-tenant platforms**

### Features

- Create and manage organizations
- Invite and manage members
- Role-based access control
- Organization switching
- Isolated data per organization

### Setup Steps

#### Step 1: Enable Organizations

**Location:** Clerk Dashboard > Configure > Settings

Toggle "Enable organizations" to activate the feature.

#### Step 2: Add Organization Components

```typescript
import { OrganizationSwitcher } from '@clerk/nextjs'

export default function Header() {
  return (
    <header>
      <OrganizationSwitcher />
    </header>
  )
}
```

**Available Components:**

- `<OrganizationSwitcher />` - Create, switch, and manage organizations
- `<OrganizationProfile />` - Organization settings and member management
- `<OrganizationList />` - Display all user's organizations

#### Step 3: Configure Roles and Permissions

**Location:** Clerk Dashboard > Roles and Permissions

**Default Roles:**

- `admin` - Full organization control
- `member` - Basic organization access

**Actions:**

- Create custom permissions
- Define roles with permission sets
- Assign roles to organization members

### Accessing Organization Data

#### Server-Side

```typescript
import { auth } from '@clerk/nextjs/server'

export async function GET() {
  const { userId, orgId, orgRole } = await auth()

  if (!orgId) {
    return Response.json({ error: 'No organization selected' }, { status: 400 })
  }

  // Fetch organization-specific data
  const data = await db.query(
    'SELECT * FROM projects WHERE org_id = ?',
    [orgId]
  )

  return Response.json({ data })
}
```

#### Client-Side

```typescript
import { useOrganization } from '@clerk/nextjs'

export default function OrgDashboard() {
  const { organization, membership } = useOrganization()

  if (membership?.role === 'admin') {
    return <AdminPanel />
  }

  return <div>{organization?.name}</div>
}
```

### Permission Checking

#### Middleware Protection

```typescript
import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server'

const isAdminRoute = createRouteMatcher(['/admin(.*)'])

export default clerkMiddleware(async (auth, req) => {
  if (isAdminRoute(req)) {
    await auth.protect((has) => {
      return has({ permission: 'org:admin:access' })
    })
  }
})
```

#### Component-Level

```typescript
import { useOrganization } from '@clerk/nextjs'

function AdminSection() {
  const { membership } = useOrganization()

  if (membership?.role !== 'admin') {
    return null
  }

  return <div>Admin controls</div>
}
```

### Data Isolation Patterns

#### Database Approach

Add `org_id` column to all tables:

```sql
CREATE TABLE projects (
  id UUID PRIMARY KEY,
  org_id VARCHAR NOT NULL,
  name VARCHAR,
  FOREIGN KEY (org_id) REFERENCES organizations(id)
)
```

**Query Pattern:**

```sql
SELECT * FROM projects WHERE org_id = ?
```

#### API Approach

Include orgId in all API calls:

```typescript
export async function GET(req: Request) {
  const { orgId } = await auth()

  // Automatically filter by orgId
  const projects = await db.projects.findMany({
    where: { orgId }
  })

  return Response.json({ projects })
}
```

---

## Production Deployment

### Prerequisites

- Domain you own with DNS record access
- OAuth credentials for each social provider (production-specific)
- Hosting platform with environment variable support

### Deployment Steps

#### Step 1: Create Production Instance

**Location:** Clerk Dashboard

1. Click "Development" button at top
2. Select "Create production instance"
3. Choose to clone development settings or use defaults

**⚠️ Important Notes:**

- SSO connections do NOT copy over - must reconfigure
- Integrations do NOT copy over - must reconfigure
- Path settings do NOT copy over - must reconfigure

#### Step 2: Update Environment Variables

**Critical Changes:**

| Variable | Development | Production |
|----------|-------------|------------|
| `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` | `pk_test_*` | `pk_live_*` |
| `CLERK_SECRET_KEY` | `sk_test_*` | `sk_live_*` |

**Deployment Locations:**

- **Vercel:** Environment Variables in project settings
- **Netlify:** Environment variables in site settings
- **AWS:** Parameter Store or Secrets Manager
- **Docker:** Docker secrets or environment files
- **Kubernetes:** ConfigMaps and Secrets

**After Update:** Redeploy application for changes to take effect.

#### Step 3: Configure Domain

**Location:** Clerk Dashboard > Domains

1. Obtain DNS records from Domains page
2. Add DNS records to your domain provider
3. Wait for DNS propagation (up to 48 hours)

**Subdomain Behavior:**

- Root domain set → Authentication works across all subdomains
- Session sharing enabled across subdomains
- Example: `example-site.com` and `dashboard.example-site.com` share authentication

#### Step 4: Configure Authorized Parties

Prevent subdomain cookie leaking (CSRF protection):

```typescript
clerkMiddleware({
  authorizedParties: [
    'https://example.com',
    'https://dashboard.example.com'
  ],
})
```

**Security Benefit:** Restricts which origins can make authenticated requests.

#### Step 5: Configure OAuth Providers

Set up production-specific OAuth credentials:

**Providers to Configure:**

- Google OAuth
- GitHub OAuth
- Facebook OAuth
- Microsoft OAuth
- Other enabled providers

**Reason:** Development credentials are not secure for production.

#### Step 6: Update Webhook Endpoints

**Changes Required:**

- Update webhook URLs to production endpoints
- Update webhook signing secrets
- Test webhook delivery in production

#### Step 7: Deploy Certificates

**Location:** Clerk Dashboard

Click "Deploy certificates" button after completing all above steps.

### Security Considerations

#### Authorized Parties

- **Purpose:** CSRF protection for multi-subdomain applications
- **Configuration:** Array of allowed origins
- **Example:** `['https://example.com', 'https://api.example.com']`

#### Content Security Policy

If implementing CSP headers, configure appropriately. Consult Clerk CSP guide.

#### Rate Limiting

- Monitor Backend API rate limits
- Use client-side hooks when possible for optimization

### Troubleshooting

#### DNS Issues with Cloudflare

**Problem:** DNS not resolving with Cloudflare
**Solution:** Set subdomain to "DNS only" mode (disable proxy)

#### Certificate Delays

**Problem:** Certificate issuance taking too long
**Check:** CAA DNS records on primary domain

```bash
dig example.com +short CAA
```

**Expected:** Empty response (no restrictive CAA records)

#### Wrong Domain

**Problem:** Need to change domain after deployment
**Solution:** Use Clerk Dashboard or Backend API to update domain

### Deployment Checklist

- ✓ Created production Clerk instance
- ✓ Updated environment variables (`pk_live_*`, `sk_live_*`)
- ✓ Configured DNS records for domain
- ✓ Added authorizedParties for subdomain security
- ✓ Configured production OAuth credentials
- ✓ Updated webhook endpoints and secrets
- ✓ Tested authentication flows in production
- ✓ Verified subdomain authentication working
- ✓ Deployed certificates via Clerk Dashboard
- ✓ Monitored for DNS propagation completion

---

## Appearance Customization

### Overview

Customize Clerk component appearance using the `appearance` prop at global or component level.

### Customization Methods

1. **baseTheme** - Use prebuilt themes
2. **variables** - Customize colors, fonts, spacing
3. **elements** - Target specific CSS classes
4. **layout** - Adjust component structure

### Global Styling

Apply styles to all Clerk components via `ClerkProvider`:

```typescript
import { ClerkProvider } from '@clerk/nextjs'
import { dark } from '@clerk/themes'

export default function RootLayout({ children }) {
  return (
    <ClerkProvider
      appearance={{
        baseTheme: dark,
        variables: {
          colorPrimary: '#6c47ff',
          fontFamily: 'Inter'
        }
      }}
    >
      <html lang="en">
        <body>{children}</body>
      </html>
    </ClerkProvider>
  )
}
```

### Component-Specific Styling

Override global styles for individual components:

```typescript
<SignIn
  appearance={{
    elements: {
      card: 'shadow-xl',
      headerTitle: 'text-blue-600'
    }
  }}
/>
```

**Precedence:** Component appearance overrides ClerkProvider appearance.

### Appearance Prop Structure

#### baseTheme

```typescript
appearance={{
  baseTheme: dark  // or 'light'
}}
```

#### variables

```typescript
appearance={{
  variables: {
    colorPrimary: '#6c47ff',
    colorBackground: '#ffffff',
    colorText: '#000000',
    fontFamily: 'Inter, sans-serif',
    fontSize: '16px',
    borderRadius: '8px'
  }
}}
```

#### elements

```typescript
appearance={{
  elements: {
    card: 'shadow-lg',
    headerTitle: 'text-2xl font-bold',
    formButtonPrimary: 'bg-blue-600 hover:bg-blue-700'
  }
}}
```

**Common Elements:**

- `card` - Main card container
- `headerTitle` - Component header title
- `headerSubtitle` - Component header subtitle
- `socialButtons` - Social provider buttons container
- `formFieldInput` - Form input fields
- `formButtonPrimary` - Primary form button
- `footerActionLink` - Footer action links

#### layout

```typescript
appearance={{
  layout: {
    socialButtonsPlacement: 'bottom',
    socialButtonsVariant: 'iconButton',
    showOptionalFields: false
  }
}}
```

### UserButton Customization

#### Add Custom Menu Items

```typescript
<UserButton>
  <UserButton.MenuItems>
    <UserButton.Link
      label="Settings"
      labelIcon={<SettingsIcon />}
      href="/settings"
    />
    <UserButton.Action
      label="Help"
      labelIcon={<HelpIcon />}
      onClick={() => openHelpModal()}
    />
  </UserButton.MenuItems>
</UserButton>
```

#### Avatar Customization

```typescript
<UserButton
  showName={true}
  appearance={{
    elements: {
      avatarBox: 'rounded-full border-2'
    }
  }}
/>
```

---

## Best Practices

### Security

- ✅ Always use environment variables for API keys
- ✅ Never commit .env files to version control
- ✅ Use `authorizedParties` for multi-subdomain applications
- ✅ Implement proper permission checks in middleware
- ✅ Validate user permissions on both client and server
- ✅ Use `privateMetadata` for sensitive data, not `publicMetadata`

### Performance

- ✅ Prefer client-side `useUser()` over server-side `currentUser()`
- ✅ Cache user data to reduce Backend API calls
- ✅ Use `auth()` instead of `currentUser()` when only needing userId
- ✅ Implement proper loading states while Clerk initializes
- ✅ Use conditional rendering (`SignedIn`/`SignedOut`) to avoid flashes

### User Experience

- ✅ Provide fallback content during component mounting
- ✅ Implement smooth loading transitions
- ✅ Show meaningful error messages for authentication failures
- ✅ Use redirects appropriately for unauthenticated users
- ✅ Consider multi-session support for better UX

### Development Workflow

- ✅ Start with development instance, deploy to production when ready
- ✅ Test authentication flows thoroughly before production
- ✅ Use Clerk Dashboard to manage users and organizations
- ✅ Monitor Backend API rate limits
- ✅ Implement proper error handling and logging

### Organization Management

- ✅ Enable organizations for B2B applications
- ✅ Implement proper data isolation by `orgId`
- ✅ Use role-based access control for permissions
- ✅ Provide clear organization switching UI
- ✅ Document permission requirements for features

---

## Troubleshooting

### Common Issues

#### Environment Variables Not Loading

**Causes:**

- Missing `.env.local` file
- Variables don't start with `NEXT_PUBLIC_` for client-side access
- Server not restarted after adding variables

**Solutions:**

- Create `.env.local` in project root
- Ensure `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` is public
- Restart development server after changes

#### clerkMiddleware Not Protecting Routes

**Cause:** Default behavior is public - must opt-in to protection

**Solution:** Use `auth.protect()` in middleware callback:

```typescript
export default clerkMiddleware(async (auth, req) => {
  if (isProtectedRoute(req)) await auth.protect()
})
```

#### User Data Not Available Immediately

**Cause:** Clerk still initializing (`isLoaded = false`)

**Solution:** Check `isLoaded` before accessing user data:

```typescript
const { isLoaded, user } = useUser()

if (!isLoaded) return <div>Loading...</div>
```

#### Rate Limit Errors with currentUser()

**Cause:** Too many Backend API calls

**Solution:** Use client-side `useUser()` or cache user data:

```typescript
// Client-side (recommended)
const { user } = useUser()

// Server-side (use sparingly)
const user = await currentUser()
```

#### DNS Not Resolving for Custom Domain

**Causes:**

- DNS records not configured correctly
- Cloudflare proxy interfering
- DNS propagation not complete

**Solutions:**

- Verify DNS records in Clerk Dashboard
- Set Cloudflare to DNS-only mode
- Wait up to 48 hours for propagation

### Error Messages

#### "Clerk: Publishable key not found"

Missing or incorrect `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` in `.env.local`.

#### "Clerk: Session token expired"

User session expired. Prompt user to sign in again.

#### "Permission denied"

User doesn't have required permissions. Check middleware protection rules.

---

## AEON Integration Notes

### AEON-Specific Configuration

When integrating Clerk with AEON Cybersecurity systems:

1. **Environment Variables:** Store in secure credential management system
2. **Multi-Tenancy:** Enable organizations for AEON clients
3. **Role-Based Access:** Configure custom roles for AEON security levels
4. **Audit Logging:** Integrate Clerk webhooks with AEON audit systems
5. **API Protection:** Use middleware for all AEON API endpoints

### AEON Security Requirements

- Use `privateMetadata` for AEON internal security classifications
- Implement custom permissions for AEON access levels
- Configure `authorizedParties` for AEON subdomain architecture
- Enable multi-factor authentication for all AEON users
- Integrate with AEON credential management system

### AEON Development Workflow

1. Development instance for AEON development environment
2. Staging instance for AEON testing environment
3. Production instance for AEON production environment
4. Separate OAuth credentials for each environment
5. Environment-specific webhook endpoints

---

## Additional Resources

### Official Documentation

- **Clerk Documentation:** https://clerk.com/docs
- **Next.js SDK Reference:** https://clerk.com/docs/reference/nextjs/overview
- **Component Reference:** https://clerk.com/docs/components/overview

### Example Repositories

- **Clerk + Next.js App Router Demo:** https://github.com/clerk/clerk-nextjs-app-quickstart
- **Clerk + Next.js Pages Router Demo:** https://github.com/clerk/clerk-nextjs-pages-quickstart

### Tutorials

- **Building Multi-Tenant Apps with Clerk:** https://clerk.com/blog/how-to-build-multitenant-authentication-with-clerk
- **Team-Based Task Manager Tutorial:** https://clerk.com/blog/build-a-team-based-task-manager-with-organizations

---

## Version History

- **v1.0.0 (2025-11-04):** Initial comprehensive documentation for AEON Wiki

---

**End of Document**
