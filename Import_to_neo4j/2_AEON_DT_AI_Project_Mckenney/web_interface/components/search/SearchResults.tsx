'use client';

import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { ExternalLink, Tag, Calendar, Building2 } from 'lucide-react';
import type { SearchResult } from '@/lib/hybrid-search';

interface SearchResultsProps {
  results: SearchResult[];
  query: string;
  onResultClick?: (result: SearchResult) => void;
}

export function SearchResults({ results, query, onResultClick }: SearchResultsProps) {
  // Highlight matching terms in text
  const highlightText = (text: string, query: string): React.ReactNode => {
    if (!query || !text) return text;

    const terms = query.toLowerCase().split(/\s+/).filter(Boolean);
    const regex = new RegExp(`(${terms.join('|')})`, 'gi');
    const parts = text.split(regex);

    return parts.map((part, index) => {
      const isMatch = terms.some(term => part.toLowerCase() === term.toLowerCase());
      return isMatch ? (
        <mark key={index} className="bg-yellow-200 dark:bg-yellow-800 font-semibold">
          {part}
        </mark>
      ) : (
        <span key={index}>{part}</span>
      );
    });
  };

  // Format relevance score for display
  const formatScore = (score: number, source: string): string => {
    if (source === 'hybrid') {
      return `${(score * 100).toFixed(1)}% (RRF)`;
    }
    return `${(score * 100).toFixed(1)}%`;
  };

  // Get badge color based on source
  const getSourceBadgeColor = (source: string): string => {
    switch (source) {
      case 'neo4j':
        return 'bg-blue-500';
      case 'qdrant':
        return 'bg-purple-500';
      case 'hybrid':
        return 'bg-green-500';
      default:
        return 'bg-gray-500';
    }
  };

  // Get type badge color
  const getTypeBadgeColor = (type: string): string => {
    switch (type) {
      case 'document':
        return 'bg-orange-500';
      case 'entity':
        return 'bg-indigo-500';
      case 'requirement':
        return 'bg-pink-500';
      default:
        return 'bg-gray-500';
    }
  };

  if (results.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-muted-foreground text-lg">No results found for &quot;{query}&quot;</p>
        <p className="text-sm text-muted-foreground mt-2">Try adjusting your search terms or filters</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="text-sm text-muted-foreground mb-4">
        Found {results.length} result{results.length !== 1 ? 's' : ''} for &quot;{query}&quot;
      </div>

      {results.map((result) => (
        <Card
          key={result.id}
          className="hover:shadow-lg transition-shadow cursor-pointer"
          onClick={() => onResultClick?.(result)}
        >
          <CardHeader>
            <div className="flex items-start justify-between gap-4">
              <div className="flex-1 space-y-2">
                <CardTitle className="text-lg">
                  {highlightText(result.title, query)}
                </CardTitle>

                <div className="flex flex-wrap gap-2">
                  {/* Source badge */}
                  <Badge className={`${getSourceBadgeColor(result.source)} text-white`}>
                    {result.source.toUpperCase()}
                  </Badge>

                  {/* Type badge */}
                  <Badge className={`${getTypeBadgeColor(result.type)} text-white`}>
                    {result.type}
                  </Badge>

                  {/* Relevance score */}
                  <Badge variant="outline">
                    {formatScore(result.score, result.source)}
                  </Badge>
                </div>
              </div>

              <Button
                variant="ghost"
                size="sm"
                onClick={(e) => {
                  e.stopPropagation();
                  onResultClick?.(result);
                }}
              >
                <ExternalLink className="h-4 w-4" />
              </Button>
            </div>
          </CardHeader>

          <CardContent className="space-y-4">
            {/* Content preview with highlights */}
            <CardDescription className="line-clamp-3">
              {highlightText(result.content, query)}
            </CardDescription>

            {/* Metadata */}
            <div className="flex flex-wrap gap-4 text-sm text-muted-foreground">
              {result.metadata.customer && (
                <div className="flex items-center gap-1">
                  <Building2 className="h-4 w-4" />
                  <span>{result.metadata.customer}</span>
                </div>
              )}

              {result.metadata.date && (
                <div className="flex items-center gap-1">
                  <Calendar className="h-4 w-4" />
                  <span>{new Date(result.metadata.date).toLocaleDateString()}</span>
                </div>
              )}

              {result.metadata.tags && result.metadata.tags.length > 0 && (
                <div className="flex items-center gap-1">
                  <Tag className="h-4 w-4" />
                  <div className="flex gap-1">
                    {result.metadata.tags.slice(0, 3).map((tag) => (
                      <Badge key={tag} variant="secondary" className="text-xs">
                        {tag}
                      </Badge>
                    ))}
                    {result.metadata.tags.length > 3 && (
                      <Badge variant="secondary" className="text-xs">
                        +{result.metadata.tags.length - 3}
                      </Badge>
                    )}
                  </div>
                </div>
              )}
            </div>

            {/* Document ID if available */}
            {result.metadata.documentId && (
              <div className="text-xs text-muted-foreground">
                Document ID: {result.metadata.documentId}
              </div>
            )}
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
