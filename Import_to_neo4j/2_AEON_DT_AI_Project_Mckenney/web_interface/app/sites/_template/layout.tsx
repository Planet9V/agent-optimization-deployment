import React from 'react';
import type { Metadata } from 'next';

export const metadata: Metadata = {
    title: 'Template Site | AEON SaaS',
    description: 'A hosted informational site.',
};

export default function TemplateLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <div className="template-site-layout">
            {children}
        </div>
    );
}
