'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import CustomerForm from '@/components/customers/CustomerForm';
import { Button } from '@/components/ui/button';
import { ArrowLeft } from 'lucide-react';
import Link from 'next/link';

interface CustomerFormData {
  name: string;
  email?: string;
  phone?: string;
  company?: string;
  address?: string;
  notes?: string;
}

export default function NewCustomerPage() {
  const router = useRouter();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (data: CustomerFormData) => {
    setIsSubmitting(true);
    setError(null);

    try {
      const response = await fetch('/api/customers', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to create customer');
      }

      const result = await response.json();

      // Show success message
      alert('Customer created successfully!');

      // Redirect to customer detail page
      router.push(`/customers/${result.customer.id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create customer');
      setIsSubmitting(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8 max-w-2xl">
      <div className="mb-8">
        <Link href="/customers">
          <Button variant="ghost" className="mb-4">
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Customers
          </Button>
        </Link>
        <h1 className="text-3xl font-bold text-gray-900">Create New Customer</h1>
        <p className="text-gray-600 mt-2">
          Add a new customer to your database
        </p>
      </div>

      {error && (
        <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-800 font-semibold">Error</p>
          <p className="text-red-600 mt-1">{error}</p>
        </div>
      )}

      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <CustomerForm
          onSubmit={handleSubmit}
          loading={isSubmitting}
          mode="create"
        />
      </div>
    </div>
  );
}
