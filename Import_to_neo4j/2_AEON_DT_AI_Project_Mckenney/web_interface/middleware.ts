import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server'
import { NextResponse } from 'next/server'

// Define public routes that don't require authentication
const isPublicRoute = createRouteMatcher([
  '/sign-in(.*)',
  '/sign-up(.*)',
  '/',
  '/api/health',
  '/sites(.*)' // Allow public access to hosted sites
])

// Define protected routes that require authentication
const isProtectedRoute = createRouteMatcher([
  '/dashboard(.*)',
  '/graph(.*)',
  '/search(.*)',
  '/chat(.*)',
  '/customers(.*)',
  '/upload(.*)',
  '/tags(.*)',
  '/analytics(.*)'
])

export default clerkMiddleware(async (auth, req) => {
  const url = req.nextUrl
  const hostname = req.headers.get('host')

  // Domain-Based Routing Logic
  // Map specific domains to their respective folders in app/sites/
  // For testing/template purposes, we map 'oxot.nl' to the template site
  if (hostname === 'oxot.nl' || hostname === 'www.oxot.nl') {
    // Rewrite the URL to serve from the /sites/_template folder
    // We preserve the pathname so sub-pages work (e.g. oxot.nl/about -> /sites/_template/about)
    return NextResponse.rewrite(new URL(`/sites/_template${url.pathname}`, req.url))
  }

  // Protect routes that require authentication (Main App)
  if (isProtectedRoute(req)) {
    await auth.protect()
  }
}, {
  // Enable debug mode in development for troubleshooting
  debug: process.env.NODE_ENV === 'development'
})

export const config = {
  matcher: [
    // Skip Next.js internals and static files
    '/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)',
    // Always run for API routes
    '/(api|trpc)(.*)',
  ],
}
