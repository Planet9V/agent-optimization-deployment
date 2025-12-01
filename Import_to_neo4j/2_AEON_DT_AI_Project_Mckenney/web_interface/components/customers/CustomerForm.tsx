import { useState } from 'react';
import { Card, Text, Button, TextInput, Select, SelectItem } from '@tremor/react';
import { Building2, Mail, Phone, MapPin, Save, X } from 'lucide-react';

interface CustomerFormData {
  name: string;
  email: string;
  phone: string;
  address: string;
  status: 'active' | 'inactive' | 'pending';
}

interface CustomerFormProps {
  initialData?: Partial<CustomerFormData>;
  onSubmit: (data: CustomerFormData) => Promise<void>;
  onCancel?: () => void;
  loading?: boolean;
  mode?: 'create' | 'edit';
}

export default function CustomerForm({
  initialData,
  onSubmit,
  onCancel,
  loading = false,
  mode = 'create'
}: CustomerFormProps) {
  const [formData, setFormData] = useState<CustomerFormData>({
    name: initialData?.name || '',
    email: initialData?.email || '',
    phone: initialData?.phone || '',
    address: initialData?.address || '',
    status: initialData?.status || 'active'
  });

  const [errors, setErrors] = useState<Partial<Record<keyof CustomerFormData, string>>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const validateForm = (): boolean => {
    const newErrors: Partial<Record<keyof CustomerFormData, string>> = {};

    if (!formData.name.trim()) {
      newErrors.name = 'Name is required';
    }

    if (!formData.email.trim()) {
      newErrors.email = 'Email is required';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = 'Invalid email format';
    }

    if (formData.phone && !/^[\d\s\-\+\(\)]+$/.test(formData.phone)) {
      newErrors.phone = 'Invalid phone format';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setIsSubmitting(true);
    try {
      await onSubmit(formData);
    } catch (error) {
      console.error('Form submission error:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleChange = (field: keyof CustomerFormData, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: undefined }));
    }
  };

  return (
    <Card>
      <div className="flex items-center space-x-3 mb-6">
        <div className="p-2 bg-blue-100 rounded-lg">
          <Building2 className="h-6 w-6 text-blue-600" />
        </div>
        <Text className="text-xl font-semibold">
          {mode === 'create' ? 'Create New Customer' : 'Edit Customer'}
        </Text>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-2">
            Customer Name *
          </label>
          <TextInput
            id="name"
            placeholder="Enter customer name"
            value={formData.name}
            onChange={(e) => handleChange('name', e.target.value)}
            error={!!errors.name}
            errorMessage={errors.name}
            disabled={isSubmitting || loading}
            icon={Building2}
          />
        </div>

        <div>
          <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
            Email Address *
          </label>
          <TextInput
            id="email"
            type="email"
            placeholder="customer@example.com"
            value={formData.email}
            onChange={(e) => handleChange('email', e.target.value)}
            error={!!errors.email}
            errorMessage={errors.email}
            disabled={isSubmitting || loading}
            icon={Mail}
          />
        </div>

        <div>
          <label htmlFor="phone" className="block text-sm font-medium text-gray-700 mb-2">
            Phone Number
          </label>
          <TextInput
            id="phone"
            type="tel"
            placeholder="+1 (555) 123-4567"
            value={formData.phone}
            onChange={(e) => handleChange('phone', e.target.value)}
            error={!!errors.phone}
            errorMessage={errors.phone}
            disabled={isSubmitting || loading}
            icon={Phone}
          />
        </div>

        <div>
          <label htmlFor="address" className="block text-sm font-medium text-gray-700 mb-2">
            Address
          </label>
          <TextInput
            id="address"
            placeholder="123 Main St, City, State ZIP"
            value={formData.address}
            onChange={(e) => handleChange('address', e.target.value)}
            disabled={isSubmitting || loading}
            icon={MapPin}
          />
        </div>

        <div>
          <label htmlFor="status" className="block text-sm font-medium text-gray-700 mb-2">
            Status
          </label>
          <Select
            id="status"
            value={formData.status}
            onValueChange={(value) => handleChange('status', value as CustomerFormData['status'])}
            disabled={isSubmitting || loading}
          >
            <SelectItem value="active">Active</SelectItem>
            <SelectItem value="inactive">Inactive</SelectItem>
            <SelectItem value="pending">Pending</SelectItem>
          </Select>
        </div>

        <div className="flex justify-end space-x-3 pt-4 border-t border-gray-200">
          {onCancel && (
            <Button
              type="button"
              variant="secondary"
              icon={X}
              onClick={onCancel}
              disabled={isSubmitting || loading}
            >
              Cancel
            </Button>
          )}
          <Button
            type="submit"
            icon={Save}
            disabled={isSubmitting || loading}
            loading={isSubmitting || loading}
          >
            {mode === 'create' ? 'Create Customer' : 'Save Changes'}
          </Button>
        </div>
      </form>
    </Card>
  );
}
