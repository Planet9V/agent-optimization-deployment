import { Card, Text, Badge, Flex, Button } from '@tremor/react';
import { Building2, Mail, Phone, MapPin, Calendar, Edit, Trash2, Eye } from 'lucide-react';
import { format, isValid, parseISO } from 'date-fns';

interface Customer {
  id: string;
  name: string;
  email?: string;
  phone?: string;
  address?: string;
  status?: 'active' | 'inactive' | 'pending';
  documentCount?: number;
  createdAt?: Date;
  lastActivity?: Date;
}

interface CustomerCardProps {
  customer: Customer;
  onEdit?: (customer: Customer) => void;
  onDelete?: (customer: Customer) => void;
  onView?: (customer: Customer) => void;
  compact?: boolean;
}

const statusConfig = {
  active: { color: 'emerald', label: 'Active' },
  inactive: { color: 'gray', label: 'Inactive' },
  pending: { color: 'amber', label: 'Pending' }
};

// Safe date formatter - handles both Date objects and ISO strings from JSON
function safeFormatDate(date: Date | string | undefined, formatString: string): string {
  if (!date) return 'N/A';

  try {
    // Convert string to Date if needed
    const dateObj = typeof date === 'string' ? parseISO(date) : date;

    // Validate before formatting
    if (!isValid(dateObj)) return 'N/A';

    return format(dateObj, formatString);
  } catch {
    return 'N/A';
  }
}

export default function CustomerCard({
  customer,
  onEdit,
  onDelete,
  onView,
  compact = false
}: CustomerCardProps) {
  return (
    <Card className="hover:shadow-lg transition-shadow duration-200">
      <Flex justifyContent="between" alignItems="start" className="mb-3">
        <div className="flex items-start space-x-3">
          <div className="p-2 bg-blue-100 rounded-lg">
            <Building2 className="h-6 w-6 text-blue-600" />
          </div>
          <div>
            <Text className="text-lg font-semibold text-gray-900">{customer.name}</Text>
            <Badge color={statusConfig[customer.status || 'active'].color} size="sm" className="mt-1">
              {statusConfig[customer.status || 'active'].label}
            </Badge>
          </div>
        </div>

        <Flex justifyContent="end" className="space-x-1">
          {onView && (
            <Button
              size="xs"
              variant="light"
              icon={Eye}
              onClick={() => onView(customer)}
            >
              View
            </Button>
          )}
          {onEdit && (
            <Button
              size="xs"
              variant="light"
              icon={Edit}
              onClick={() => onEdit(customer)}
            >
              Edit
            </Button>
          )}
          {onDelete && (
            <Button
              size="xs"
              variant="light"
              color="red"
              icon={Trash2}
              onClick={() => onDelete(customer)}
            >
              Delete
            </Button>
          )}
        </Flex>
      </Flex>

      {!compact && (
        <div className="space-y-2 mt-4">
          {customer.email && (
            <Flex justifyContent="start" className="space-x-2">
              <Mail className="h-4 w-4 text-gray-400" />
              <Text className="text-sm text-gray-600">{customer.email}</Text>
            </Flex>
          )}

          {customer.phone && (
            <Flex justifyContent="start" className="space-x-2">
              <Phone className="h-4 w-4 text-gray-400" />
              <Text className="text-sm text-gray-600">{customer.phone}</Text>
            </Flex>
          )}

          {customer.address && (
            <Flex justifyContent="start" className="space-x-2">
              <MapPin className="h-4 w-4 text-gray-400" />
              <Text className="text-sm text-gray-600">{customer.address}</Text>
            </Flex>
          )}
        </div>
      )}

      <div className="mt-4 pt-4 border-t border-gray-200">
        <Flex justifyContent="between" alignItems="center">
          <div>
            <Text className="text-sm text-gray-500">Documents</Text>
            <Text className="text-lg font-semibold">
              {typeof customer.documentCount === 'object' && customer.documentCount !== null && 'low' in customer.documentCount
                ? (customer.documentCount as any).toNumber?.() ?? (customer.documentCount as any).low ?? 0
                : customer.documentCount ?? 0}
            </Text>
          </div>

          <div className="text-right">
            <Flex justifyContent="end" className="space-x-1 items-center">
              <Calendar className="h-3 w-3 text-gray-400" />
              <Text className="text-xs text-gray-500">
                {safeFormatDate(customer.createdAt, 'MMM dd, yyyy')}
              </Text>
            </Flex>
            {customer.lastActivity && (
              <Text className="text-xs text-gray-400 mt-1">
                Last activity: {safeFormatDate(customer.lastActivity, 'MMM dd')}
              </Text>
            )}
          </div>
        </Flex>
      </div>
    </Card>
  );
}
