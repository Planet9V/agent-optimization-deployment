import type { Metadata } from 'next';
import './globals.css';
import ModernNav from '@/components/ModernNav';
import WaveBackground from '@/components/WaveBackground';
import { ClerkProvider } from '@clerk/nextjs';

export const metadata: Metadata = {
  title: 'AEON Digital Twin | Cybersecurity Intelligence Platform',
  description: 'Advanced cybersecurity digital twin powered by Neo4j knowledge graphs and real-time threat intelligence',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <ClerkProvider>
      <html lang="en" className="dark">
        <body>
          <WaveBackground />
          <ModernNav />
          <main className="min-h-screen pt-20 px-6">
            {children}
          </main>
        </body>
      </html>
    </ClerkProvider>
  );
}
