'use client';

import React from 'react';
import { useRouter } from 'next/navigation';

interface NodeDetailsProps {
  node: {
    id: string;
    label: string;
    properties: Record<string, any>;
    labels: string[];
  } | null;
  onClose: () => void;
}

export default function NodeDetails({ node, onClose }: NodeDetailsProps) {
  const router = useRouter();

  if (!node) {
    return (
      <div className="w-96 bg-gray-50 border-l p-4 flex items-center justify-center text-gray-500">
        Select a node to view details
      </div>
    );
  }

  const handleViewDocument = () => {
    if (node.properties.documentId) {
      router.push(`/documents/${node.properties.documentId}`);
    }
  };

  const handleEdit = async () => {
    // TODO: Implement edit functionality
    console.log('Edit node:', node);
  };

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this node?')) return;

    try {
      await fetch(`/api/graph/nodes/${node.id}`, {
        method: 'DELETE',
      });
      onClose();
      // Refresh graph
      window.location.reload();
    } catch (error) {
      console.error('Error deleting node:', error);
      alert('Failed to delete node');
    }
  };

  const formatValue = (value: any): string => {
    if (value === null || value === undefined) return 'N/A';
    if (typeof value === 'boolean') return value ? 'Yes' : 'No';
    if (typeof value === 'object') return JSON.stringify(value, null, 2);
    if (typeof value === 'number') return value.toLocaleString();
    return String(value);
  };

  return (
    <div className="w-96 bg-white border-l h-full overflow-y-auto">
      <div className="p-4 border-b flex items-center justify-between">
        <h2 className="text-lg font-semibold">Node Details</h2>
        <button
          onClick={onClose}
          className="text-gray-500 hover:text-gray-700"
          title="Close"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div className="p-4">
        {/* Labels */}
        <div className="mb-4">
          <h3 className="text-sm font-medium text-gray-700 mb-2">Labels</h3>
          <div className="flex flex-wrap gap-2">
            {node.labels.map(label => (
              <span
                key={label}
                className="px-2 py-1 text-xs bg-blue-100 text-blue-700 rounded"
              >
                {label}
              </span>
            ))}
          </div>
        </div>

        {/* Properties */}
        <div className="mb-4">
          <h3 className="text-sm font-medium text-gray-700 mb-2">Properties</h3>
          <div className="space-y-3">
            {Object.entries(node.properties).map(([key, value]) => (
              <div key={key}>
                <div className="text-xs font-medium text-gray-500 mb-1">
                  {key}
                </div>
                <div className="text-sm text-gray-900 break-words">
                  {formatValue(value)}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Connected Nodes */}
        <div className="mb-4">
          <h3 className="text-sm font-medium text-gray-700 mb-2">Connected Nodes</h3>
          <div className="text-sm text-gray-600">
            Click on connected nodes in the graph to explore relationships
          </div>
        </div>

        {/* Actions */}
        <div className="space-y-2">
          {node.properties.documentId && (
            <button
              onClick={handleViewDocument}
              className="w-full px-4 py-2 text-sm bg-blue-600 hover:bg-blue-700 text-white rounded"
            >
              View Document
            </button>
          )}
          <button
            onClick={handleEdit}
            className="w-full px-4 py-2 text-sm bg-gray-100 hover:bg-gray-200 text-gray-700 rounded"
          >
            Edit Node
          </button>
          <button
            onClick={handleDelete}
            className="w-full px-4 py-2 text-sm bg-red-100 hover:bg-red-200 text-red-700 rounded"
          >
            Delete Node
          </button>
        </div>

        {/* Metadata */}
        <div className="mt-6 pt-4 border-t">
          <h3 className="text-sm font-medium text-gray-700 mb-2">Metadata</h3>
          <div className="space-y-1 text-xs text-gray-600">
            <div>ID: {node.id}</div>
            {node.properties.created && (
              <div>Created: {new Date(node.properties.created).toLocaleString()}</div>
            )}
            {node.properties.updated && (
              <div>Updated: {new Date(node.properties.updated).toLocaleString()}</div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
