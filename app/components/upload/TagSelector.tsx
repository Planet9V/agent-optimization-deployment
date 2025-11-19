'use client';

import { Badge, Text } from '@tremor/react';

const TAGS = [
  { id: 'critical', name: 'Critical', color: 'red' },
  { id: 'confidential', name: 'Confidential', color: 'orange' },
  { id: 'internal', name: 'Internal', color: 'yellow' },
  { id: 'public', name: 'Public', color: 'green' },
  { id: 'technical', name: 'Technical', color: 'blue' },
  { id: 'compliance', name: 'Compliance', color: 'purple' }
];

interface TagSelectorProps {
  selected: string[];
  onChange: (tags: string[]) => void;
}

export default function TagSelector({ selected, onChange }: TagSelectorProps) {
  const toggleTag = (tagId: string) => {
    if (selected.includes(tagId)) {
      onChange(selected.filter(t => t !== tagId));
    } else if (selected.length < 5) {
      onChange([...selected, tagId]);
    }
  };

  return (
    <div className="space-y-4">
      <Text>Select Tags (Optional, max 5)</Text>
      <div className="flex flex-wrap gap-2">
        {TAGS.map(tag => (
          <Badge
            key={tag.id}
            color={selected.includes(tag.id) ? tag.color as any : 'gray'}
            className="cursor-pointer"
            onClick={() => toggleTag(tag.id)}
          >
            {tag.name} {selected.includes(tag.id) && '✓'}
          </Badge>
        ))}
      </div>
      <Text className="text-sm text-gray-500">Selected: {selected.length}/5</Text>
    </div>
  );
}
