import { useState } from 'react';
import { Card, Text, Button, TextInput, Badge, Flex, Grid } from '@tremor/react';
import { Tag, Plus, X, Edit2, Save, Search } from 'lucide-react';

interface TagItem {
  id: string;
  name: string;
  color: string;
  documentCount: number;
  createdAt: Date;
}

interface TagManagerProps {
  tags?: TagItem[];
  onCreateTag?: (name: string, color: string) => Promise<void>;
  onUpdateTag?: (id: string, name: string, color: string) => Promise<void>;
  onDeleteTag?: (id: string) => Promise<void>;
  loading?: boolean;
}

const tagColors = [
  { value: 'blue', label: 'Blue' },
  { value: 'green', label: 'Green' },
  { value: 'red', label: 'Red' },
  { value: 'yellow', label: 'Yellow' },
  { value: 'purple', label: 'Purple' },
  { value: 'pink', label: 'Pink' },
  { value: 'indigo', label: 'Indigo' },
  { value: 'gray', label: 'Gray' }
];

export default function TagManager({
  tags = [],
  onCreateTag,
  onUpdateTag,
  onDeleteTag,
  loading = false
}: TagManagerProps) {
  const [isCreating, setIsCreating] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [newTagName, setNewTagName] = useState('');
  const [newTagColor, setNewTagColor] = useState('blue');
  const [searchQuery, setSearchQuery] = useState('');
  const [editName, setEditName] = useState('');
  const [editColor, setEditColor] = useState('blue');

  const filteredTags = tags.filter(tag =>
    tag.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleCreate = async () => {
    if (!newTagName.trim() || !onCreateTag) return;

    await onCreateTag(newTagName.trim(), newTagColor);
    setNewTagName('');
    setNewTagColor('blue');
    setIsCreating(false);
  };

  const handleStartEdit = (tag: TagItem) => {
    setEditingId(tag.id);
    setEditName(tag.name);
    setEditColor(tag.color);
  };

  const handleSaveEdit = async (id: string) => {
    if (!editName.trim() || !onUpdateTag) return;

    await onUpdateTag(id, editName.trim(), editColor);
    setEditingId(null);
  };

  const handleDelete = async (id: string) => {
    if (!onDeleteTag) return;
    if (window.confirm('Are you sure you want to delete this tag?')) {
      await onDeleteTag(id);
    }
  };

  return (
    <Card>
      <Flex justifyContent="between" alignItems="center" className="mb-6">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-blue-100 rounded-lg">
            <Tag className="h-6 w-6 text-blue-600" />
          </div>
          <Text className="text-xl font-semibold">Tag Manager</Text>
        </div>
        <Button
          icon={Plus}
          onClick={() => setIsCreating(true)}
          disabled={isCreating || loading}
        >
          New Tag
        </Button>
      </Flex>

      <div className="mb-4">
        <TextInput
          icon={Search}
          placeholder="Search tags..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
      </div>

      {isCreating && (
        <Card className="mb-4 bg-blue-50">
          <Text className="font-semibold mb-3">Create New Tag</Text>
          <div className="space-y-3">
            <TextInput
              placeholder="Tag name"
              value={newTagName}
              onChange={(e) => setNewTagName(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleCreate()}
            />
            <div className="flex flex-wrap gap-2">
              {tagColors.map((color) => (
                <button
                  key={color.value}
                  onClick={() => setNewTagColor(color.value)}
                  className={`px-3 py-1 rounded-full text-sm font-medium transition-all ${
                    newTagColor === color.value
                      ? `bg-${color.value}-500 text-white ring-2 ring-${color.value}-300`
                      : `bg-${color.value}-100 text-${color.value}-700 hover:bg-${color.value}-200`
                  }`}
                >
                  {color.label}
                </button>
              ))}
            </div>
            <Flex justifyContent="end" className="space-x-2">
              <Button
                variant="secondary"
                icon={X}
                onClick={() => {
                  setIsCreating(false);
                  setNewTagName('');
                  setNewTagColor('blue');
                }}
              >
                Cancel
              </Button>
              <Button
                icon={Save}
                onClick={handleCreate}
                disabled={!newTagName.trim()}
              >
                Create
              </Button>
            </Flex>
          </div>
        </Card>
      )}

      <div className="space-y-2">
        {filteredTags.length === 0 ? (
          <div className="text-center py-8">
            <Tag className="h-12 w-12 text-gray-300 mx-auto mb-2" />
            <Text className="text-gray-500">
              {searchQuery ? 'No tags found' : 'No tags created yet'}
            </Text>
          </div>
        ) : (
          filteredTags.map((tag) => (
            <Card key={tag.id} className="bg-gray-50">
              {editingId === tag.id ? (
                <div className="space-y-3">
                  <TextInput
                    value={editName}
                    onChange={(e) => setEditName(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleSaveEdit(tag.id)}
                  />
                  <div className="flex flex-wrap gap-2">
                    {tagColors.map((color) => (
                      <button
                        key={color.value}
                        onClick={() => setEditColor(color.value)}
                        className={`px-3 py-1 rounded-full text-sm font-medium transition-all ${
                          editColor === color.value
                            ? `bg-${color.value}-500 text-white`
                            : `bg-${color.value}-100 text-${color.value}-700`
                        }`}
                      >
                        {color.label}
                      </button>
                    ))}
                  </div>
                  <Flex justifyContent="end" className="space-x-2">
                    <Button
                      size="xs"
                      variant="secondary"
                      icon={X}
                      onClick={() => setEditingId(null)}
                    >
                      Cancel
                    </Button>
                    <Button
                      size="xs"
                      icon={Save}
                      onClick={() => handleSaveEdit(tag.id)}
                      disabled={!editName.trim()}
                    >
                      Save
                    </Button>
                  </Flex>
                </div>
              ) : (
                <Flex justifyContent="between" alignItems="center">
                  <Flex justifyContent="start" className="space-x-3">
                    <Badge color={tag.color as any}>{tag.name}</Badge>
                    <Text className="text-sm text-gray-500">
                      {tag.documentCount} documents
                    </Text>
                  </Flex>
                  <Flex justifyContent="end" className="space-x-2">
                    {onUpdateTag && (
                      <Button
                        size="xs"
                        variant="light"
                        icon={Edit2}
                        onClick={() => handleStartEdit(tag)}
                      >
                        Edit
                      </Button>
                    )}
                    {onDeleteTag && (
                      <Button
                        size="xs"
                        variant="light"
                        color="red"
                        icon={X}
                        onClick={() => handleDelete(tag.id)}
                      >
                        Delete
                      </Button>
                    )}
                  </Flex>
                </Flex>
              )}
            </Card>
          ))
        )}
      </div>
    </Card>
  );
}
