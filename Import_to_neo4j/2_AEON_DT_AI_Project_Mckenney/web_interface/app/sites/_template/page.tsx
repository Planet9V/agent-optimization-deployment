import React from 'react';

export default function TemplatePage() {
    return (
        <div className="flex min-h-screen flex-col items-center justify-center bg-white text-black">
            <h1 className="text-4xl font-bold">Template Site</h1>
            <p className="mt-4 text-lg text-gray-600">
                This is a template for an independent informational site hosted on AEON SaaS.
            </p>
            <div className="mt-8 p-4 border rounded bg-gray-50">
                <p className="font-mono text-sm">Served via Domain-Based Routing</p>
            </div>
        </div>
    );
}
