import { redirect } from 'next/navigation';

/**
 * Legacy redirect page
 *
 * This page handles redirects from the old /analytics/threats route
 * to the new /threat-intel route.
 *
 * Context: The menu restructure (Nov 2025) promoted Threat Intelligence
 * from a dropdown item to a top-level page at /threat-intel.
 */
export default function AnalyticsThreatsRedirect() {
  redirect('/threat-intel');
}
