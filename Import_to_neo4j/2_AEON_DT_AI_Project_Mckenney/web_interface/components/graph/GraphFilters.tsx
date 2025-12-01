'use client';

import React, { useState, useEffect } from 'react';

interface GraphFiltersProps {
  onFilterChange: (filters: {
    nodeTypes: string[];
    relationshipTypes: string[];
    customers: string[];
    tags: string[];
    confidenceMin: number;
    dateRange: { start: string; end: string } | null;
  }) => void;
  onLayoutChange: (layout: 'force' | 'hierarchical') => void;
}

const NODE_TYPES = [
  'Document',
  'Entity',
  'Topic',
  'Person',
  'Organization',
  'Location',
  'Project',
];

const RELATIONSHIP_TYPES = [
  'MENTIONS',
  'RELATED_TO',
  'HAS_TOPIC',
  'WORKS_FOR',
  'LOCATED_IN',
  'CONTAINS',
  'BELONGS_TO',
];

export default function GraphFilters({ onFilterChange, onLayoutChange }: GraphFiltersProps) {
  const [nodeTypes, setNodeTypes] = useState<string[]>([]);
  const [relationshipTypes, setRelationshipTypes] = useState<string[]>([]);
  const [customers, setCustomers] = useState<string[]>([]);
  const [availableCustomers, setAvailableCustomers] = useState<string[]>([]);
  const [tags, setTags] = useState<string[]>([]);
  const [availableTags, setAvailableTags] = useState<string[]>([]);
  const [confidenceMin, setConfidenceMin] = useState(0);
  const [dateRange, setDateRange] = useState<{ start: string; end: string } | null>(null);
  const [layout, setLayout] = useState<'force' | 'hierarchical'>('force');

  useEffect(() => {
    // Fetch available customers and tags
    fetchCustomers();
    fetchTags();
  }, []);

  useEffect(() => {
    onFilterChange({
      nodeTypes,
      relationshipTypes,
      customers,
      tags,
      confidenceMin,
      dateRange,
    });
  }, [nodeTypes, relationshipTypes, customers, tags, confidenceMin, dateRange]);

  const fetchCustomers = async () => {
    try {
      const response = await fetch('/api/customers');
      const data = await response.json();
      setAvailableCustomers(data.customers || []);
    } catch (error) {
      console.error('Error fetching customers:', error);
    }
  };

  const fetchTags = async () => {
    try {
      const response = await fetch('/api/tags');
      const data = await response.json();
      setAvailableTags(data.tags || []);
    } catch (error) {
      console.error('Error fetching tags:', error);
    }
  };

  const toggleNodeType = (type: string) => {
    setNodeTypes(prev =>
      prev.includes(type) ? prev.filter(t => t !== type) : [...prev, type]
    );
  };

  const toggleRelationshipType = (type: string) => {
    setRelationshipTypes(prev =>
      prev.includes(type) ? prev.filter(t => t !== type) : [...prev, type]
    );
  };

  const toggleCustomer = (customer: string) => {
    setCustomers(prev =>
      prev.includes(customer) ? prev.filter(c => c !== customer) : [...prev, customer]
    );
  };

  const toggleTag = (tag: string) => {
    setTags(prev =>
      prev.includes(tag) ? prev.filter(t => t !== tag) : [...prev, tag]
    );
  };

  const handleLayoutChange = (newLayout: 'force' | 'hierarchical') => {
    setLayout(newLayout);
    onLayoutChange(newLayout);
  };

  const clearFilters = () => {
    setNodeTypes([]);
    setRelationshipTypes([]);
    setCustomers([]);
    setTags([]);
    setConfidenceMin(0);
    setDateRange(null);
  };

  return (
    <div className="w-80 bg-white border-r h-full overflow-y-auto">
      <div className="p-4">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold">Filters</h2>
          <button
            onClick={clearFilters}
            className="text-sm text-blue-600 hover:text-blue-700"
          >
            Clear All
          </button>
        </div>

        {/* Layout Selection */}
        <div className="mb-6">
          <h3 className="text-sm font-medium text-gray-700 mb-2">Layout</h3>
          <div className="flex gap-2">
            <button
              onClick={() => handleLayoutChange('force')}
              className={`flex-1 px-3 py-2 text-sm rounded ${
                layout === 'force'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              Force
            </button>
            <button
              onClick={() => handleLayoutChange('hierarchical')}
              className={`flex-1 px-3 py-2 text-sm rounded ${
                layout === 'hierarchical'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              Hierarchical
            </button>
          </div>
        </div>

        {/* Node Types */}
        <div className="mb-6">
          <h3 className="text-sm font-medium text-gray-700 mb-2">Node Types</h3>
          <div className="space-y-2">
            {NODE_TYPES.map(type => (
              <label key={type} className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={nodeTypes.includes(type)}
                  onChange={() => toggleNodeType(type)}
                  className="rounded border-gray-300"
                />
                <span className="text-sm">{type}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Relationship Types */}
        <div className="mb-6">
          <h3 className="text-sm font-medium text-gray-700 mb-2">Relationships</h3>
          <div className="space-y-2">
            {RELATIONSHIP_TYPES.map(type => (
              <label key={type} className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={relationshipTypes.includes(type)}
                  onChange={() => toggleRelationshipType(type)}
                  className="rounded border-gray-300"
                />
                <span className="text-sm">{type}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Customers */}
        <div className="mb-6">
          <h3 className="text-sm font-medium text-gray-700 mb-2">Customers</h3>
          <div className="space-y-2 max-h-40 overflow-y-auto">
            {availableCustomers.map(customer => (
              <label key={customer} className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={customers.includes(customer)}
                  onChange={() => toggleCustomer(customer)}
                  className="rounded border-gray-300"
                />
                <span className="text-sm">{customer}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Tags */}
        <div className="mb-6">
          <h3 className="text-sm font-medium text-gray-700 mb-2">Tags</h3>
          <div className="space-y-2 max-h-40 overflow-y-auto">
            {availableTags.map(tag => (
              <label key={tag} className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={tags.includes(tag)}
                  onChange={() => toggleTag(tag)}
                  className="rounded border-gray-300"
                />
                <span className="text-sm">{tag}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Confidence Threshold */}
        <div className="mb-6">
          <h3 className="text-sm font-medium text-gray-700 mb-2">
            Confidence Threshold: {confidenceMin.toFixed(2)}
          </h3>
          <input
            type="range"
            min="0"
            max="1"
            step="0.05"
            value={confidenceMin}
            onChange={(e) => setConfidenceMin(parseFloat(e.target.value))}
            className="w-full"
          />
          <div className="flex justify-between text-xs text-gray-500 mt-1">
            <span>0.0</span>
            <span>1.0</span>
          </div>
        </div>

        {/* Date Range */}
        <div className="mb-6">
          <h3 className="text-sm font-medium text-gray-700 mb-2">Date Range</h3>
          <div className="space-y-2">
            <input
              type="date"
              value={dateRange?.start || ''}
              onChange={(e) =>
                setDateRange(prev => ({ start: e.target.value, end: prev?.end || '' }))
              }
              className="w-full px-3 py-2 text-sm border border-gray-300 rounded"
              placeholder="Start date"
            />
            <input
              type="date"
              value={dateRange?.end || ''}
              onChange={(e) =>
                setDateRange(prev => ({ start: prev?.start || '', end: e.target.value }))
              }
              className="w-full px-3 py-2 text-sm border border-gray-300 rounded"
              placeholder="End date"
            />
            {dateRange && (
              <button
                onClick={() => setDateRange(null)}
                className="text-sm text-red-600 hover:text-red-700"
              >
                Clear dates
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
