"use client";

import { Card, Select, SelectItem, Text } from "@tremor/react";

interface Customer {
  id: string;
  name: string;
  type: string;
}

interface CustomerSelectorProps {
  selected: string;
  onSelect: (customerId: string) => void;
}

const CUSTOMERS: Customer[] = [
  { id: "mckenney", name: "McKenney's Inc.", type: "Primary" },
  { id: "demo-corp", name: "Demo Corporation", type: "Demo" },
  { id: "test-client", name: "Test Client", type: "Test" },
];

export default function CustomerSelector({ selected, onSelect }: CustomerSelectorProps) {
  return (
    <Card className="mt-4">
      <Text className="font-semibold mb-2">Select Customer</Text>
      <Select
        value={selected}
        onValueChange={onSelect}
        placeholder="Choose a customer..."
        required
      >
        {CUSTOMERS.map((customer) => (
          <SelectItem key={customer.id} value={customer.id}>
            {customer.name} ({customer.type})
          </SelectItem>
        ))}
      </Select>
    </Card>
  );
}
