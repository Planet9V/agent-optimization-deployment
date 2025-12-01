'use client';

import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { Plus, Edit2, Trash2, Tag as TagIcon, Loader2 } from 'lucide-react';
import { ErrorBoundary, DatabaseConnectionError } from '@/components/error-boundary';

interface Tag {
  name: string;
  category: string;
  color: string;
  description?: string;
  createdAt: Date;
  usageCount: number;
}

const CATEGORIES = [
  'general',
  'document-type',
  'project',
  'priority',
  'status',
  'department',
  'client',
  'custom'
];

const PRESET_COLORS = [
  '#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A',
  '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E2',
  '#F8B739', '#52B788', '#E76F51', '#2A9D8F'
];

function TagManagementPageContent() {
  const [tags, setTags] = useState<Tag[]>([]);
  const [filteredTags, setFilteredTags] = useState<Tag[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [dbConnected, setDbConnected] = useState<boolean | null>(null);

  // Dialog states
  const [createDialogOpen, setCreateDialogOpen] = useState(false);
  const [editDialogOpen, setEditDialogOpen] = useState(false);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);

  // Form states
  const [currentTag, setCurrentTag] = useState<Tag | null>(null);
  const [formData, setFormData] = useState({
    name: '',
    category: 'general',
    color: PRESET_COLORS[0],
    description: ''
  });

  // Fetch all tags
  const fetchTags = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/tags');

      if (!response.ok) {
        setDbConnected(false);
        return;
      }

      const result = await response.json();

      if (result.success) {
        setDbConnected(true);
        setTags(result.data);
        filterTags(result.data, selectedCategory, searchTerm);
      } else {
        setDbConnected(false);
      }
    } catch (error) {
      console.error('Error fetching tags:', error);
      setDbConnected(false);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTags();
  }, []);

  // Filter tags
  const filterTags = (allTags: Tag[], category: string, search: string) => {
    let filtered = [...allTags];

    if (category !== 'all') {
      filtered = filtered.filter(tag => tag.category === category);
    }

    if (search) {
      filtered = filtered.filter(tag =>
        tag.name.toLowerCase().includes(search.toLowerCase()) ||
        tag.description?.toLowerCase().includes(search.toLowerCase())
      );
    }

    setFilteredTags(filtered);
  };

  useEffect(() => {
    filterTags(tags, selectedCategory, searchTerm);
  }, [selectedCategory, searchTerm, tags]);

  // Create tag
  const handleCreate = async () => {
    try {
      const response = await fetch('/api/tags', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });

      const result = await response.json();

      if (result.success) {
        setCreateDialogOpen(false);
        resetForm();
        fetchTags();
      } else {
        alert(`Error: ${result.message}`);
      }
    } catch (error) {
      console.error('Error creating tag:', error);
      alert('Failed to create tag');
    }
  };

  // Update tag
  const handleUpdate = async () => {
    if (!currentTag) return;

    try {
      const response = await fetch(`/api/tags/${encodeURIComponent(currentTag.name)}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          category: formData.category,
          color: formData.color,
          description: formData.description
        })
      });

      const result = await response.json();

      if (result.success) {
        setEditDialogOpen(false);
        setCurrentTag(null);
        resetForm();
        fetchTags();
      } else {
        alert(`Error: ${result.message}`);
      }
    } catch (error) {
      console.error('Error updating tag:', error);
      alert('Failed to update tag');
    }
  };

  // Delete tag
  const handleDelete = async () => {
    if (!currentTag) return;

    try {
      const response = await fetch(`/api/tags/${encodeURIComponent(currentTag.name)}`, {
        method: 'DELETE'
      });

      const result = await response.json();

      if (result.success) {
        setDeleteDialogOpen(false);
        setCurrentTag(null);
        fetchTags();
      } else {
        alert(`Error: ${result.message}`);
      }
    } catch (error) {
      console.error('Error deleting tag:', error);
      alert('Failed to delete tag');
    }
  };

  const resetForm = () => {
    setFormData({
      name: '',
      category: 'general',
      color: PRESET_COLORS[0],
      description: ''
    });
  };

  const openEditDialog = (tag: Tag) => {
    setCurrentTag(tag);
    setFormData({
      name: tag.name,
      category: tag.category,
      color: tag.color,
      description: tag.description || ''
    });
    setEditDialogOpen(true);
  };

  const openDeleteDialog = (tag: Tag) => {
    setCurrentTag(tag);
    setDeleteDialogOpen(true);
  };

  // Group tags by category
  const tagsByCategory = filteredTags.reduce((acc, tag) => {
    if (!acc[tag.category]) {
      acc[tag.category] = [];
    }
    acc[tag.category].push(tag);
    return acc;
  }, {} as Record<string, Tag[]>);

  // Show connection error if database is not available
  if (dbConnected === false) {
    return <DatabaseConnectionError serviceName="Neo4j" onRetry={fetchTags} />;
  }

  // Show loading state while checking connection
  if (dbConnected === null && loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
      </div>
    );
  }

  return (
    <div className="container mx-auto py-8 px-4">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold">Tag Management</h1>
          <p className="text-muted-foreground mt-2">
            Organize and manage tags for your documents and entities
          </p>
        </div>
        <Button onClick={() => setCreateDialogOpen(true)}>
          <Plus className="mr-2 h-4 w-4" />
          Create Tag
        </Button>
      </div>

      {/* Filters */}
      <Card className="mb-6">
        <CardContent className="pt-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label>Search Tags</Label>
              <Input
                placeholder="Search by name or description..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
            <div>
              <Label>Filter by Category</Label>
              <Select value={selectedCategory} onChange={(e) => setSelectedCategory(e.target.value)}>
                <SelectItem value="all">All Categories</SelectItem>
                {CATEGORIES.map(cat => (
                  <SelectItem key={cat} value={cat}>
                    {cat.charAt(0).toUpperCase() + cat.slice(1)}
                  </SelectItem>
                ))}
              </Select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Tags Display */}
      {loading ? (
        <div className="text-center py-12">Loading tags...</div>
      ) : filteredTags.length === 0 ? (
        <Card>
          <CardContent className="py-12 text-center">
            <TagIcon className="mx-auto h-12 w-12 text-muted-foreground mb-4" />
            <p className="text-muted-foreground">No tags found</p>
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-6">
          {Object.entries(tagsByCategory).map(([category, categoryTags]) => (
            <Card key={category}>
              <CardHeader>
                <CardTitle className="text-lg capitalize">{category}</CardTitle>
                <CardDescription>{categoryTags.length} tag(s)</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-3">
                  {categoryTags.map(tag => (
                    <div
                      key={tag.name}
                      className="flex items-center gap-2 p-3 border rounded-lg bg-card hover:bg-accent transition-colors"
                    >
                      <Badge
                        style={{
                          backgroundColor: tag.color,
                          color: '#fff'
                        }}
                      >
                        {tag.name}
                      </Badge>
                      <span className="text-sm text-muted-foreground">
                        ({tag.usageCount} uses)
                      </span>
                      <div className="flex gap-1 ml-2">
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => openEditDialog(tag)}
                        >
                          <Edit2 className="h-3 w-3" />
                        </Button>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => openDeleteDialog(tag)}
                        >
                          <Trash2 className="h-3 w-3" />
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {/* Create Dialog */}
      <Dialog open={createDialogOpen} onOpenChange={setCreateDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Create New Tag</DialogTitle>
            <DialogDescription>
              Add a new tag to organize your documents
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4 py-4">
            <div>
              <Label htmlFor="name">Tag Name *</Label>
              <Input
                id="name"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                placeholder="Enter tag name"
              />
            </div>
            <div>
              <Label htmlFor="category">Category *</Label>
              <Select
                value={formData.category}
                onChange={(e) => setFormData({ ...formData, category: e.target.value })}
              >
                {CATEGORIES.map(cat => (
                  <SelectItem key={cat} value={cat}>
                    {cat.charAt(0).toUpperCase() + cat.slice(1)}
                  </SelectItem>
                ))}
              </Select>
            </div>
            <div>
              <Label>Color *</Label>
              <div className="flex flex-wrap gap-2 mt-2">
                {PRESET_COLORS.map(color => (
                  <button
                    key={color}
                    className={`w-8 h-8 rounded-full border-2 transition-all ${
                      formData.color === color ? 'border-primary scale-110' : 'border-transparent'
                    }`}
                    style={{ backgroundColor: color }}
                    onClick={() => setFormData({ ...formData, color })}
                  />
                ))}
              </div>
            </div>
            <div>
              <Label htmlFor="description">Description</Label>
              <Input
                id="description"
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                placeholder="Optional description"
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setCreateDialogOpen(false)}>
              Cancel
            </Button>
            <Button onClick={handleCreate}>Create Tag</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Edit Dialog */}
      <Dialog open={editDialogOpen} onOpenChange={setEditDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Edit Tag</DialogTitle>
            <DialogDescription>
              Update tag properties (name cannot be changed)
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4 py-4">
            <div>
              <Label>Tag Name</Label>
              <Input value={formData.name} disabled />
            </div>
            <div>
              <Label htmlFor="edit-category">Category</Label>
              <Select
                value={formData.category}
                onChange={(e) => setFormData({ ...formData, category: e.target.value })}
              >
                {CATEGORIES.map(cat => (
                  <SelectItem key={cat} value={cat}>
                    {cat.charAt(0).toUpperCase() + cat.slice(1)}
                  </SelectItem>
                ))}
              </Select>
            </div>
            <div>
              <Label>Color</Label>
              <div className="flex flex-wrap gap-2 mt-2">
                {PRESET_COLORS.map(color => (
                  <button
                    key={color}
                    className={`w-8 h-8 rounded-full border-2 transition-all ${
                      formData.color === color ? 'border-primary scale-110' : 'border-transparent'
                    }`}
                    style={{ backgroundColor: color }}
                    onClick={() => setFormData({ ...formData, color })}
                  />
                ))}
              </div>
            </div>
            <div>
              <Label htmlFor="edit-description">Description</Label>
              <Input
                id="edit-description"
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                placeholder="Optional description"
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setEditDialogOpen(false)}>
              Cancel
            </Button>
            <Button onClick={handleUpdate}>Update Tag</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Delete Confirmation Dialog */}
      <Dialog open={deleteDialogOpen} onOpenChange={setDeleteDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Delete Tag</DialogTitle>
            <DialogDescription>
              Are you sure you want to delete this tag? This will remove all HAS_TAG relationships.
            </DialogDescription>
          </DialogHeader>
          {currentTag && (
            <div className="py-4">
              <Badge style={{ backgroundColor: currentTag.color, color: '#fff' }}>
                {currentTag.name}
              </Badge>
              <p className="mt-2 text-sm text-muted-foreground">
                Currently used {currentTag.usageCount} time(s)
              </p>
            </div>
          )}
          <DialogFooter>
            <Button variant="outline" onClick={() => setDeleteDialogOpen(false)}>
              Cancel
            </Button>
            <Button variant="destructive" onClick={handleDelete}>
              Delete Tag
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}

export default function TagManagementPage() {
  return (
    <ErrorBoundary fallbackMessage="Tag management page encountered an error. The database may be unavailable.">
      <TagManagementPageContent />
    </ErrorBoundary>
  );
}
