# AEON DT UI Components

Production-ready React components built with Tremor React and Tailwind CSS for the AEON Digital Twin dashboard.

## Components Overview

### Dashboard Components

#### MetricsCard
Display key performance metrics with optional delta indicators.

```tsx
import { MetricsCard } from '@/components';
import { Users } from 'lucide-react';

<MetricsCard
  title="Total Documents"
  metric="1,234"
  delta="+12.5%"
  deltaType="increase"
  icon={Users}
  iconColor="text-blue-500"
  loading={false}
/>
```

#### QuickActions
Grid of quick action buttons for common tasks.

```tsx
import { QuickActions } from '@/components';

<QuickActions />
```

#### RecentActivity
Live activity feed showing recent system events.

```tsx
import { RecentActivity } from '@/components';

const activities = [
  {
    id: '1',
    type: 'upload',
    title: 'Document uploaded',
    description: 'contract.pdf',
    timestamp: new Date(),
    user: 'john@example.com'
  }
];

<RecentActivity
  activities={activities}
  maxItems={10}
  loading={false}
/>
```

#### SystemHealth
Real-time service health monitoring.

```tsx
import { SystemHealth } from '@/components';

const services = [
  {
    name: 'Neo4j',
    status: 'healthy',
    responseTime: 45,
    uptime: '99.9%',
    icon: <Database className="h-5 w-5" />
  }
];

<SystemHealth
  services={services}
  loading={false}
  onRefresh={() => console.log('Refresh')}
/>
```

### Customer Components

#### CustomerCard
Display customer information with actions.

```tsx
import { CustomerCard } from '@/components';

const customer = {
  id: '1',
  name: 'Acme Corp',
  email: 'contact@acme.com',
  phone: '+1 (555) 123-4567',
  address: '123 Main St, City, State',
  status: 'active',
  documentCount: 42,
  createdAt: new Date(),
  lastActivity: new Date()
};

<CustomerCard
  customer={customer}
  onEdit={(customer) => console.log('Edit', customer)}
  onDelete={(customer) => console.log('Delete', customer)}
  onView={(customer) => console.log('View', customer)}
  compact={false}
/>
```

#### CustomerForm
Create or edit customer information.

```tsx
import { CustomerForm } from '@/components';

<CustomerForm
  mode="create"
  initialData={{
    name: 'Acme Corp',
    email: 'contact@acme.com',
    status: 'active'
  }}
  onSubmit={async (data) => {
    console.log('Submit', data);
  }}
  onCancel={() => console.log('Cancel')}
  loading={false}
/>
```

### Tag Components

#### TagManager
Full tag management interface with create, edit, delete.

```tsx
import { TagManager } from '@/components';

const tags = [
  {
    id: '1',
    name: 'Contract',
    color: 'blue',
    documentCount: 25,
    createdAt: new Date()
  }
];

<TagManager
  tags={tags}
  onCreateTag={async (name, color) => {
    console.log('Create', name, color);
  }}
  onUpdateTag={async (id, name, color) => {
    console.log('Update', id, name, color);
  }}
  onDeleteTag={async (id) => {
    console.log('Delete', id);
  }}
  loading={false}
/>
```

#### TagSelector
Multi-tag selection with search and optional creation.

```tsx
import { TagSelector } from '@/components';

const availableTags = [
  { id: '1', name: 'Contract', color: 'blue' },
  { id: '2', name: 'Invoice', color: 'green' }
];

<TagSelector
  availableTags={availableTags}
  selectedTags={['1']}
  onTagsChange={(tagIds) => console.log('Tags changed', tagIds)}
  allowCreate={true}
  onCreateTag={async (name) => {
    return { id: '3', name, color: 'blue' };
  }}
  maxTags={5}
  placeholder="Search or add tags..."
  label="Document Tags"
/>
```

### Upload Components

#### FileUpload
Drag-and-drop file upload with validation.

```tsx
import { FileUpload } from '@/components';

<FileUpload
  onFilesSelected={(files) => {
    console.log('Files selected', files);
  }}
  onUpload={async (files) => {
    console.log('Uploading', files);
  }}
  acceptedFileTypes={['.pdf', '.doc', '.docx']}
  maxFileSize={50}
  maxFiles={10}
  multiple={true}
/>
```

#### UploadProgress
Real-time upload progress tracking.

```tsx
import { UploadProgress } from '@/components';

const tasks = [
  {
    id: '1',
    fileName: 'document.pdf',
    status: 'uploading',
    progress: 45,
    message: 'Uploading...',
    startedAt: new Date()
  }
];

<UploadProgress
  tasks={tasks}
  onCancel={(taskId) => console.log('Cancel', taskId)}
  onRetry={(taskId) => console.log('Retry', taskId)}
  compact={false}
/>
```

## Features

### Built-in Features
- TypeScript support with full type safety
- Responsive design (mobile, tablet, desktop)
- Loading states for all components
- Error handling and validation
- Accessibility (ARIA labels, keyboard navigation)
- Dark mode ready (via Tremor)
- Animation and transitions

### Dependencies
- **Tremor React**: UI component library
- **Tailwind CSS**: Utility-first styling
- **Lucide React**: Icon library
- **date-fns**: Date formatting utilities

## Component Guidelines

### Styling
All components use:
- Tremor React components for consistency
- Tailwind CSS for custom styling
- Consistent spacing and color schemes
- Hover states and transitions

### State Management
Components follow React best practices:
- Local state with `useState`
- Callback props for parent communication
- Optional controlled/uncontrolled modes

### Error Handling
- Form validation with error messages
- Try-catch blocks for async operations
- User-friendly error displays

### Performance
- Optimized re-renders with React hooks
- Efficient list rendering
- Lazy loading where appropriate

## Usage Tips

### Import Components
```tsx
// Individual imports
import MetricsCard from '@/components/dashboard/MetricsCard';

// Batch imports
import {
  MetricsCard,
  QuickActions,
  CustomerCard
} from '@/components';
```

### Customization
All components accept standard React props and can be extended:

```tsx
<MetricsCard
  className="custom-class"
  style={{ background: 'red' }}
  {...otherProps}
/>
```

### Type Safety
Import types for TypeScript projects:

```tsx
import type { UploadTask } from '@/components/upload/UploadProgress';
```

## Testing

Components are designed to be easily testable:

```tsx
import { render, fireEvent, screen } from '@testing-library/react';
import { FileUpload } from '@/components';

test('renders file upload', () => {
  render(<FileUpload />);
  expect(screen.getByText('Drag & drop files here')).toBeInTheDocument();
});
```

## Browser Support

- Chrome/Edge (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)
- Mobile browsers (iOS Safari, Chrome Android)

## License

Part of the AEON DT project.
