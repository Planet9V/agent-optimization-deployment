import { useState } from 'react';
import { Card, Text, Badge, TextInput, Button, Flex } from '@tremor/react';
import { Tag, X, Plus, Search } from 'lucide-react';

interface TagItem {
  id: string;
  name: string;
  color: string;
}

interface TagSelectorProps {
  availableTags: TagItem[];
  selectedTags: string[];
  onTagsChange: (tagIds: string[]) => void;
  allowCreate?: boolean;
  onCreateTag?: (name: string) => Promise<TagItem>;
  maxTags?: number;
  placeholder?: string;
  label?: string;
}

export default function TagSelector({
  availableTags,
  selectedTags,
  onTagsChange,
  allowCreate = false,
  onCreateTag,
  maxTags,
  placeholder = 'Search or add tags...',
  label = 'Tags'
}: TagSelectorProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [isCreating, setIsCreating] = useState(false);
  const [showDropdown, setShowDropdown] = useState(false);

  const selectedTagObjects = availableTags.filter(tag =>
    selectedTags.includes(tag.id)
  );

  const filteredTags = availableTags.filter(tag =>
    !selectedTags.includes(tag.id) &&
    tag.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleAddTag = (tagId: string) => {
    if (maxTags && selectedTags.length >= maxTags) {
      return;
    }
    onTagsChange([...selectedTags, tagId]);
    setSearchQuery('');
    setShowDropdown(false);
  };

  const handleRemoveTag = (tagId: string) => {
    onTagsChange(selectedTags.filter(id => id !== tagId));
  };

  const handleCreateTag = async () => {
    if (!searchQuery.trim() || !onCreateTag) return;

    setIsCreating(true);
    try {
      const newTag = await onCreateTag(searchQuery.trim());
      handleAddTag(newTag.id);
      setSearchQuery('');
      setShowDropdown(false);
    } catch (error) {
      console.error('Failed to create tag:', error);
    } finally {
      setIsCreating(false);
    }
  };

  const canAddMore = !maxTags || selectedTags.length < maxTags;

  return (
    <div className="space-y-3">
      <label className="block text-sm font-medium text-gray-700">
        {label}
        {maxTags && (
          <span className="text-gray-500 ml-2">
            ({selectedTags.length}/{maxTags})
          </span>
        )}
      </label>

      <div className="relative">
        <TextInput
          icon={Search}
          placeholder={placeholder}
          value={searchQuery}
          onChange={(e) => {
            setSearchQuery(e.target.value);
            setShowDropdown(true);
          }}
          onFocus={() => setShowDropdown(true)}
          disabled={!canAddMore}
        />

        {showDropdown && canAddMore && (searchQuery || filteredTags.length > 0) && (
          <Card className="absolute z-10 w-full mt-1 max-h-60 overflow-y-auto shadow-lg">
            {filteredTags.length > 0 ? (
              <div className="space-y-1">
                {filteredTags.map((tag) => (
                  <button
                    key={tag.id}
                    onClick={() => handleAddTag(tag.id)}
                    className="w-full text-left px-3 py-2 hover:bg-gray-100 rounded transition-colors flex items-center justify-between"
                  >
                    <Badge color={tag.color as any}>{tag.name}</Badge>
                    <Plus className="h-4 w-4 text-gray-400" />
                  </button>
                ))}
              </div>
            ) : searchQuery && (
              <div className="text-center py-4">
                <Text className="text-gray-500 mb-2">No tags found</Text>
                {allowCreate && onCreateTag && (
                  <Button
                    size="xs"
                    icon={Plus}
                    onClick={handleCreateTag}
                    loading={isCreating}
                  >
                    Create &quot;{searchQuery}&quot;
                  </Button>
                )}
              </div>
            )}
          </Card>
        )}
      </div>

      {selectedTagObjects.length > 0 && (
        <div className="flex flex-wrap gap-2 p-3 bg-gray-50 rounded-lg">
          {selectedTagObjects.map((tag) => (
            <Badge
              key={tag.id}
              color={tag.color as any}
              className="flex items-center space-x-1"
            >
              <span>{tag.name}</span>
              <button
                onClick={() => handleRemoveTag(tag.id)}
                className="ml-1 hover:bg-white/20 rounded-full p-0.5 transition-colors"
                aria-label={`Remove ${tag.name}`}
              >
                <X className="h-3 w-3" />
              </button>
            </Badge>
          ))}
        </div>
      )}

      {selectedTagObjects.length === 0 && (
        <div className="text-center py-4 border border-dashed border-gray-300 rounded-lg">
          <Tag className="h-8 w-8 text-gray-300 mx-auto mb-2" />
          <Text className="text-sm text-gray-500">No tags selected</Text>
        </div>
      )}
    </div>
  );
}
