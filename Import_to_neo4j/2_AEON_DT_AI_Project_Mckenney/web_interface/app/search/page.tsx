'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { Checkbox } from '@/components/ui/checkbox';
import { SearchResults } from '@/components/search/SearchResults';
import { Search, Filter, X, Loader2, AlertCircle } from 'lucide-react';
import { Alert, AlertDescription } from '@/components/ui/alert';
import type { SearchResult } from '@/lib/hybrid-search';
import { ErrorBoundary, DatabaseConnectionError } from '@/components/error-boundary';

function SearchPageContent() {
  // Search state
  const [query, setQuery] = useState('');
  const [mode, setMode] = useState<'fulltext' | 'semantic' | 'hybrid'>('hybrid');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [searchPerformed, setSearchPerformed] = useState(false);
  const [dbConnected, setDbConnected] = useState<boolean | null>(null);

  // Filter state
  const [showFilters, setShowFilters] = useState(false);
  const [selectedCustomer, setSelectedCustomer] = useState<string>('');
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [dateFrom, setDateFrom] = useState('');
  const [dateTo, setDateTo] = useState('');

  // Cybersecurity filters
  const [selectedNodeTypes, setSelectedNodeTypes] = useState<string[]>([]);
  const [cvssSeverityMin, setCvssSeverityMin] = useState<number>(0);
  const [cvssSeverityMax, setCvssSeverityMax] = useState<number>(10);
  const [selectedMitreTactic, setSelectedMitreTactic] = useState<string>('');

  // VulnCheck-style severity and type facets
  const [selectedSeverities, setSelectedSeverities] = useState<string[]>([]);
  const [selectedTypes, setSelectedTypes] = useState<string[]>([]);

  // Pagination state
  const [limit, setLimit] = useState(10);
  const [currentPage, setCurrentPage] = useState(1);

  // Available filter options (these would typically come from API)
  const availableCustomers = ['ACME Corp', 'TechStart Inc', 'Global Solutions', 'Innovation Labs'];
  const availableTags = ['requirements', 'specification', 'design', 'architecture', 'testing', 'deployment'];

  // Cybersecurity filter options
  const availableNodeTypes = ['CVE', 'CWE', 'ThreatActor', 'Campaign', 'Malware', 'AttackTechnique', 'ICS_Asset'];
  const availableMitreTactics = [
    'Initial Access', 'Execution', 'Persistence', 'Privilege Escalation',
    'Defense Evasion', 'Credential Access', 'Discovery', 'Lateral Movement',
    'Collection', 'Exfiltration', 'Impact'
  ];

  // VulnCheck-style facet options
  const availableSeverities = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'];
  const availableTypes = ['CVE', 'CWE', 'Threat Actor', 'Malware', 'ICS Asset'];

  // Health check on mount
  useEffect(() => {
    checkHealth();
  }, []);

  const checkHealth = async () => {
    try {
      const response = await fetch('/api/search/health');
      const data = await response.json();

      if (data.status === 'healthy') {
        setDbConnected(true);
      } else {
        setDbConnected(false);
        console.warn('Search services degraded:', data.services);
      }
    } catch (error) {
      console.error('Health check failed:', error);
      setDbConnected(false);
    }
  };

  const executeSearch = async (e?: React.FormEvent) => {
    e?.preventDefault();

    if (!query.trim()) {
      setError('Please enter a search query');
      return;
    }

    setLoading(true);
    setError(null);
    setSearchPerformed(true);

    try {
      const requestBody: any = {
        query: query.trim(),
        mode,
        limit,
      };

      // Add filters
      if (selectedCustomer) {
        requestBody.customer = selectedCustomer;
      }

      if (selectedTags.length > 0) {
        requestBody.tags = selectedTags;
      }

      if (dateFrom) {
        requestBody.dateFrom = dateFrom;
      }

      if (dateTo) {
        requestBody.dateTo = dateTo;
      }

      // Add cybersecurity filters
      if (selectedNodeTypes.length > 0) {
        requestBody.nodeTypes = selectedNodeTypes;
      }

      if (cvssSeverityMin > 0 || cvssSeverityMax < 10) {
        requestBody.cvssSeverity = {
          min: cvssSeverityMin,
          max: cvssSeverityMax
        };
      }

      if (selectedMitreTactic) {
        requestBody.mitreTactic = selectedMitreTactic;
      }

      // Add VulnCheck-style severity and type filters
      if (selectedSeverities.length > 0) {
        requestBody.severities = selectedSeverities;
      }

      if (selectedTypes.length > 0) {
        requestBody.types = selectedTypes;
      }

      const response = await fetch('/api/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Search failed');
      }

      const data = await response.json();
      setResults(data.results);
      setCurrentPage(1);
    } catch (error) {
      console.error('Search error:', error);
      setError(error instanceof Error ? error.message : 'Search failed');
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  const clearFilters = () => {
    setSelectedCustomer('');
    setSelectedTags([]);
    setDateFrom('');
    setDateTo('');
    setSelectedNodeTypes([]);
    setCvssSeverityMin(0);
    setCvssSeverityMax(10);
    setSelectedMitreTactic('');
    setSelectedSeverities([]);
    setSelectedTypes([]);
  };

  const handleTagToggle = (tag: string) => {
    setSelectedTags(prev =>
      prev.includes(tag) ? prev.filter(t => t !== tag) : [...prev, tag]
    );
  };

  const handleNodeTypeToggle = (nodeType: string) => {
    setSelectedNodeTypes(prev =>
      prev.includes(nodeType) ? prev.filter(t => t !== nodeType) : [...prev, nodeType]
    );
  };

  const handleSeverityToggle = (severity: string) => {
    setSelectedSeverities(prev =>
      prev.includes(severity) ? prev.filter(s => s !== severity) : [...prev, severity]
    );
  };

  const handleTypeToggle = (type: string) => {
    setSelectedTypes(prev =>
      prev.includes(type) ? prev.filter(t => t !== type) : [...prev, type]
    );
  };

  const handleResultClick = (result: SearchResult) => {
    console.log('Result clicked:', result);
    // Navigate to document detail page or open modal
  };

  const activeFilterCount = [
    selectedCustomer,
    selectedTags.length > 0,
    dateFrom,
    dateTo,
    selectedNodeTypes.length > 0,
    cvssSeverityMin > 0 || cvssSeverityMax < 10,
    selectedMitreTactic,
    selectedSeverities.length > 0,
    selectedTypes.length > 0,
  ].filter(Boolean).length;

  // Show connection error if database is not available
  if (dbConnected === false) {
    return <DatabaseConnectionError serviceName="Neo4j/Qdrant" onRetry={checkHealth} />;
  }

  // Show loading state while checking connection
  if (dbConnected === null) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
      </div>
    );
  }

  return (
    <div className="container mx-auto p-6 max-w-7xl">
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-2" style={{ color: 'var(--text-primary)' }}>Hybrid Search</h1>
        <p style={{ color: 'var(--text-secondary)' }}>
          Search across documents using full-text, semantic, or hybrid search
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Filters Sidebar */}
        <div className={`lg:col-span-1 space-y-4 ${!showFilters ? 'hidden lg:block' : ''}`}>
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="text-lg">Filters</CardTitle>
                {activeFilterCount > 0 && (
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={clearFilters}
                    className="h-8"
                  >
                    <X className="h-4 w-4 mr-1" />
                    Clear
                  </Button>
                )}
              </div>
              {activeFilterCount > 0 && (
                <CardDescription>
                  {activeFilterCount} filter{activeFilterCount !== 1 ? 's' : ''} active
                </CardDescription>
              )}
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Customer filter */}
              <div className="space-y-2">
                <Label>Customer</Label>
                <Select value={selectedCustomer} onChange={(e) => setSelectedCustomer(e.target.value)}>
                  <SelectItem value="">All customers</SelectItem>
                  {availableCustomers.map(customer => (
                    <SelectItem key={customer} value={customer}>
                      {customer}
                    </SelectItem>
                  ))}
                </Select>
              </div>

              {/* Tags filter */}
              <div className="space-y-2">
                <Label>Tags</Label>
                <div className="space-y-2">
                  {availableTags.map(tag => (
                    <div key={tag} className="flex items-center space-x-2">
                      <Checkbox
                        id={`tag-${tag}`}
                        checked={selectedTags.includes(tag)}
                        onCheckedChange={() => handleTagToggle(tag)}
                      />
                      <label
                        htmlFor={`tag-${tag}`}
                        className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                      >
                        {tag}
                      </label>
                    </div>
                  ))}
                </div>
              </div>

              {/* Date range filter */}
              <div className="space-y-2">
                <Label>Date Range</Label>
                <div className="space-y-2">
                  <Input
                    type="date"
                    value={dateFrom}
                    onChange={(e) => setDateFrom(e.target.value)}
                    placeholder="From"
                  />
                  <Input
                    type="date"
                    value={dateTo}
                    onChange={(e) => setDateTo(e.target.value)}
                    placeholder="To"
                  />
                </div>
              </div>

              {/* VulnCheck-Style Facets */}
              <div className="border-t pt-4 mt-4">
                <h3 className="text-sm font-semibold text-gray-900 dark:text-slate-200 mb-3">Quick Filters</h3>

                {/* Severity Filter */}
                <div className="space-y-2 mb-4">
                  <Label className="text-xs font-medium text-gray-700 dark:text-slate-300">Severity</Label>
                  <div className="space-y-2 bg-slate-900/80 dark:bg-slate-900/80 p-3 rounded-lg">
                    {availableSeverities.map(severity => (
                      <div key={severity} className="flex items-center space-x-2">
                        <Checkbox
                          id={`severity-${severity}`}
                          checked={selectedSeverities.includes(severity)}
                          onCheckedChange={() => handleSeverityToggle(severity)}
                        />
                        <label
                          htmlFor={`severity-${severity}`}
                          className="text-xs font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 text-slate-400 cursor-pointer"
                        >
                          {severity}
                        </label>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Type Filter */}
                <div className="space-y-2 mb-4">
                  <Label className="text-xs font-medium text-gray-700 dark:text-slate-300">Type</Label>
                  <div className="space-y-2 bg-slate-900/80 dark:bg-slate-900/80 p-3 rounded-lg">
                    {availableTypes.map(type => (
                      <div key={type} className="flex items-center space-x-2">
                        <Checkbox
                          id={`type-${type}`}
                          checked={selectedTypes.includes(type)}
                          onCheckedChange={() => handleTypeToggle(type)}
                        />
                        <label
                          htmlFor={`type-${type}`}
                          className="text-xs font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 text-slate-400 cursor-pointer"
                        >
                          {type}
                        </label>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* Cybersecurity Filters Section */}
              <div className="border-t pt-4 mt-4">
                <h3 className="text-sm font-semibold text-gray-900 dark:text-slate-200 mb-3">Advanced Filters</h3>

                {/* Node Type filter */}
                <div className="space-y-2 mb-4">
                  <Label className="text-xs font-medium text-gray-700">Node Type</Label>
                  <div className="space-y-2">
                    {availableNodeTypes.map(nodeType => (
                      <div key={nodeType} className="flex items-center space-x-2">
                        <Checkbox
                          id={`node-${nodeType}`}
                          checked={selectedNodeTypes.includes(nodeType)}
                          onCheckedChange={() => handleNodeTypeToggle(nodeType)}
                        />
                        <label
                          htmlFor={`node-${nodeType}`}
                          className="text-xs font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                        >
                          {nodeType}
                        </label>
                      </div>
                    ))}
                  </div>
                </div>

                {/* CVSS Severity Range */}
                <div className="space-y-2 mb-4">
                  <Label className="text-xs font-medium text-gray-700">
                    CVSS Severity: {cvssSeverityMin.toFixed(1)} - {cvssSeverityMax.toFixed(1)}
                  </Label>
                  <div className="space-y-2">
                    <input
                      type="range"
                      min="0"
                      max="10"
                      step="0.1"
                      value={cvssSeverityMin}
                      onChange={(e) => setCvssSeverityMin(parseFloat(e.target.value))}
                      className="w-full"
                    />
                    <input
                      type="range"
                      min="0"
                      max="10"
                      step="0.1"
                      value={cvssSeverityMax}
                      onChange={(e) => setCvssSeverityMax(parseFloat(e.target.value))}
                      className="w-full"
                    />
                    <div className="flex justify-between text-xs text-gray-500">
                      <span>Min: {cvssSeverityMin.toFixed(1)}</span>
                      <span>Max: {cvssSeverityMax.toFixed(1)}</span>
                    </div>
                  </div>
                </div>

                {/* MITRE Tactic filter */}
                <div className="space-y-2">
                  <Label className="text-xs font-medium text-gray-700">MITRE ATT&CK Tactic</Label>
                  <select
                    value={selectedMitreTactic}
                    onChange={(e) => setSelectedMitreTactic(e.target.value)}
                    className="w-full px-3 py-2 text-sm border border-gray-300 rounded bg-white"
                  >
                    <option value="">All tactics</option>
                    {availableMitreTactics.map(tactic => (
                      <option key={tactic} value={tactic}>
                        {tactic}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Main Search Area */}
        <div className="lg:col-span-3 space-y-6">
          {/* Search Form */}
          <Card>
            <CardContent className="pt-6">
              <form onSubmit={executeSearch} className="space-y-4">
                {/* Search input */}
                <div className="flex gap-2">
                  <div className="flex-1">
                    <Input
                      type="text"
                      placeholder="Search documents, entities, requirements..."
                      value={query}
                      onChange={(e) => setQuery(e.target.value)}
                      className="text-lg"
                      disabled={loading}
                    />
                  </div>
                  <Button type="submit" disabled={loading || !query.trim()}>
                    {loading ? (
                      <Loader2 className="h-4 w-4 animate-spin" />
                    ) : (
                      <Search className="h-4 w-4" />
                    )}
                  </Button>
                </div>

                {/* Search mode and options */}
                <div className="flex flex-wrap items-center gap-4">
                  <div className="flex items-center gap-2">
                    <Label htmlFor="mode">Mode:</Label>
                    <Select id="mode" value={mode} onChange={(e) => setMode(e.target.value as "fulltext" | "semantic" | "hybrid")} className="w-32">
                      <SelectItem value="hybrid">Hybrid</SelectItem>
                      <SelectItem value="fulltext">Full-text</SelectItem>
                      <SelectItem value="semantic">Semantic</SelectItem>
                    </Select>
                  </div>

                  <div className="flex items-center gap-2">
                    <Label htmlFor="limit">Results:</Label>
                    <Select id="limit" value={limit.toString()} onChange={(e) => setLimit(parseInt(e.target.value))} className="w-20">
                      <SelectItem value="10">10</SelectItem>
                      <SelectItem value="25">25</SelectItem>
                      <SelectItem value="50">50</SelectItem>
                      <SelectItem value="100">100</SelectItem>
                    </Select>
                  </div>

                  <Button
                    type="button"
                    variant="outline"
                    size="sm"
                    onClick={() => setShowFilters(!showFilters)}
                    className="lg:hidden"
                  >
                    <Filter className="h-4 w-4 mr-2" />
                    Filters
                    {activeFilterCount > 0 && (
                      <Badge variant="secondary" className="ml-2">
                        {activeFilterCount}
                      </Badge>
                    )}
                  </Button>
                </div>

                {/* Mode descriptions */}
                <div className="text-sm text-muted-foreground">
                  {mode === 'hybrid' && (
                    <p>Combines full-text and semantic search for best results</p>
                  )}
                  {mode === 'fulltext' && (
                    <p>Traditional keyword-based search in Neo4j</p>
                  )}
                  {mode === 'semantic' && (
                    <p>AI-powered meaning-based search in Qdrant</p>
                  )}
                </div>
              </form>
            </CardContent>
          </Card>

          {/* Error display */}
          {error && (
            <Alert variant="destructive">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          {/* Results */}
          {searchPerformed && !loading && (
            <SearchResults
              results={results}
              query={query}
              onResultClick={handleResultClick}
            />
          )}

          {/* Loading state */}
          {loading && (
            <div className="flex items-center justify-center py-12">
              <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
            </div>
          )}

          {/* Initial state */}
          {!searchPerformed && !loading && (
            <div className="text-center py-12">
              <Search className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
              <p className="text-muted-foreground text-lg">
                Enter a search query to get started
              </p>
              <p className="text-sm text-muted-foreground mt-2">
                Try searching for documents, entities, or requirements
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function SearchPage() {
  return (
    <ErrorBoundary fallbackMessage="Search page encountered an error. The database may be unavailable.">
      <SearchPageContent />
    </ErrorBoundary>
  );
}
