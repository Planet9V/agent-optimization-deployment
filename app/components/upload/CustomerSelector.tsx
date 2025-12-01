'use client';

import { Select, SelectItem, Text } from '@tremor/react';

const CUSTOMERS = [
  { id: 'mckenney', name: "McKenney's Inc.", type: 'Primary' },
  { id: 'demo-corp', name: 'Demo Corporation', type: 'Demo' },
  { id: 'test-client', name: 'Test Client', type: 'Test' }
];

interface CustomerSelectorProps {
  selected: string;
  onSelect: (customer: string) => void;
}

export default function CustomerSelector({ selected, onSelect }: CustomerSelectorProps) {
  return (
    <div className="space-y-4">
      <Text>Select Customer Organization *</Text>
      <Select value={selected} onValueChange={onSelect}>
        {CUSTOMERS.map(customer => (
          <SelectItem key={customer.id} value={customer.id}>
            {customer.name} ({customer.type})
          </SelectItem>
        ))}
      </Select>
    </div>
  );
}
