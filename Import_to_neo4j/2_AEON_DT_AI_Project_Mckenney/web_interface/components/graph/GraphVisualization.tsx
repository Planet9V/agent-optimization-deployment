'use client';

import React, { useEffect, useRef, useState } from 'react';
import NeoVis from 'neovis.js';

interface GraphVisualizationProps {
  filters: {
    nodeTypes: string[];
    relationshipTypes: string[];
    customers: string[];
    tags: string[];
    confidenceMin: number;
    dateRange: { start: string; end: string } | null;
  };
  layout: 'force' | 'hierarchical';
  onNodeClick: (node: any) => void;
}

export default function GraphVisualization({ filters, layout, onNodeClick }: GraphVisualizationProps) {
  const vizRef = useRef<HTMLDivElement>(null);
  const neovisRef = useRef<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!vizRef.current) return;

    try {
      // Build Cypher query based on filters
      const nodeFilter = filters.nodeTypes.length > 0
        ? `WHERE ANY(label IN labels(n) WHERE label IN [${filters.nodeTypes.map(t => `'${t}'`).join(',')}])`
        : '';

      const relFilter = filters.relationshipTypes.length > 0
        ? `AND type(r) IN [${filters.relationshipTypes.map(t => `'${t}'`).join(',')}]`
        : '';

      const customerFilter = filters.customers.length > 0
        ? `AND n.customer IN [${filters.customers.map(c => `'${c}'`).join(',')}]`
        : '';

      const tagFilter = filters.tags.length > 0
        ? `AND ANY(tag IN n.tags WHERE tag IN [${filters.tags.map(t => `'${t}'`).join(',')}])`
        : '';

      const confidenceFilter = `AND (r.confidence IS NULL OR r.confidence >= ${filters.confidenceMin})`;

      const dateFilter = filters.dateRange
        ? `AND n.created >= datetime('${filters.dateRange.start}') AND n.created <= datetime('${filters.dateRange.end}')`
        : '';

      const initialCypher = `
        MATCH (n)-[r]->(m)
        ${nodeFilter}
        ${relFilter}
        ${customerFilter}
        ${tagFilter}
        ${confidenceFilter}
        ${dateFilter}
        RETURN n, r, m
        LIMIT 500
      `;

      const config = {
        containerId: vizRef.current.id,
        neo4j: {
          serverUrl: process.env.NEXT_PUBLIC_NEO4J_URI || 'bolt://localhost:7687',
          serverUser: process.env.NEXT_PUBLIC_NEO4J_USER || 'neo4j',
          serverPassword: process.env.NEXT_PUBLIC_NEO4J_PASSWORD || 'password',
        },
        visConfig: {
          nodes: {
            shape: 'dot',
            size: 25,
            font: {
              size: 14,
              color: '#000000',
            },
            borderWidth: 2,
          },
          edges: {
            arrows: {
              to: { enabled: true, scaleFactor: 0.5 },
            },
            smooth: {
              enabled: true,
              type: 'continuous',
            },
            font: {
              size: 10,
              align: 'middle',
            },
          },
          physics: {
            enabled: layout === 'force',
            barnesHut: {
              gravitationalConstant: -20000,
              centralGravity: 0.3,
              springLength: 200,
              springConstant: 0.04,
            },
            stabilization: {
              iterations: 150,
            },
          },
          layout: layout === 'hierarchical' ? {
            hierarchical: {
              enabled: true,
              direction: 'UD',
              sortMethod: 'directed',
              levelSeparation: 150,
              nodeSpacing: 200,
            },
          } : undefined,
        },
        labels: {
          Document: {
            label: 'title',
            value: 'confidence',
            group: 'Document',
            [NeoVis.NEOVIS_ADVANCED_CONFIG]: {
              static: {
                color: '#4A90E2',
              },
            },
          },
          Entity: {
            label: 'name',
            group: 'Entity',
            [NeoVis.NEOVIS_ADVANCED_CONFIG]: {
              static: {
                color: '#50C878',
              },
            },
          },
          Topic: {
            label: 'name',
            group: 'Topic',
            [NeoVis.NEOVIS_ADVANCED_CONFIG]: {
              static: {
                color: '#F7B731',
              },
            },
          },
          Person: {
            label: 'name',
            group: 'Person',
            [NeoVis.NEOVIS_ADVANCED_CONFIG]: {
              static: {
                color: '#E74C3C',
              },
            },
          },
          Organization: {
            label: 'name',
            group: 'Organization',
            [NeoVis.NEOVIS_ADVANCED_CONFIG]: {
              static: {
                color: '#9B59B6',
              },
            },
          },
          Location: {
            label: 'name',
            group: 'Location',
            [NeoVis.NEOVIS_ADVANCED_CONFIG]: {
              static: {
                color: '#3498DB',
              },
            },
          },
          Project: {
            label: 'name',
            group: 'Project',
            [NeoVis.NEOVIS_ADVANCED_CONFIG]: {
              static: {
                color: '#1ABC9C',
              },
            },
          },
        },
        relationships: {
          MENTIONS: {
            label: 'type',
            [NeoVis.NEOVIS_ADVANCED_CONFIG]: {
              static: {
                color: '#999999',
              },
            },
          },
          RELATED_TO: {
            label: 'type',
            [NeoVis.NEOVIS_ADVANCED_CONFIG]: {
              static: {
                color: '#666666',
              },
            },
          },
          HAS_TOPIC: {
            label: 'type',
            [NeoVis.NEOVIS_ADVANCED_CONFIG]: {
              static: {
                color: '#F7B731',
              },
            },
          },
          WORKS_FOR: {
            label: 'type',
            [NeoVis.NEOVIS_ADVANCED_CONFIG]: {
              static: {
                color: '#9B59B6',
              },
            },
          },
          LOCATED_IN: {
            label: 'type',
            [NeoVis.NEOVIS_ADVANCED_CONFIG]: {
              static: {
                color: '#3498DB',
              },
            },
          },
        },
        initialCypher,
      };

      // Create new NeoVis instance
      const viz = new NeoVis(config as any);

      // Add click event handler
      (viz as any).registerOnEvent('clickNode', (event: any) => {
        const nodeData = event.node;
        onNodeClick({
          id: nodeData.id,
          label: nodeData.label,
          properties: nodeData.raw.properties,
          labels: nodeData.raw.labels,
        });
      });

      // Render the visualization
      viz.render();
      neovisRef.current = viz;
      setLoading(false);
      setError(null);
    } catch (err) {
      console.error('Error initializing NeoVis:', err);
      setError(err instanceof Error ? err.message : 'Failed to initialize graph');
      setLoading(false);
    }

    // Cleanup
    return () => {
      if (neovisRef.current) {
        neovisRef.current = null;
      }
    };
  }, [filters, layout, onNodeClick]);

  const exportGraph = (format: 'png' | 'svg') => {
    if (!vizRef.current) return;

    const canvas = vizRef.current.querySelector('canvas');
    if (!canvas) return;

    if (format === 'png') {
      const url = canvas.toDataURL('image/png');
      const link = document.createElement('a');
      link.download = `graph-${new Date().toISOString()}.png`;
      link.href = url;
      link.click();
    } else if (format === 'svg') {
      // SVG export would require additional library or manual canvas-to-svg conversion
      alert('SVG export not yet implemented');
    }
  };

  const stabilize = () => {
    if (neovisRef.current && neovisRef.current._network) {
      neovisRef.current._network.stabilize();
    }
  };

  const fitToView = () => {
    if (neovisRef.current && neovisRef.current._network) {
      neovisRef.current._network.fit();
    }
  };

  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center justify-between p-4 bg-white border-b">
        <div className="flex items-center gap-2">
          {loading && (
            <div className="flex items-center gap-2">
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600"></div>
              <span className="text-sm text-gray-600">Loading graph...</span>
            </div>
          )}
          {error && (
            <div className="text-sm text-red-600">
              Error: {error}
            </div>
          )}
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={stabilize}
            className="px-3 py-1 text-sm bg-gray-100 hover:bg-gray-200 rounded"
            title="Stabilize layout"
          >
            Stabilize
          </button>
          <button
            onClick={fitToView}
            className="px-3 py-1 text-sm bg-gray-100 hover:bg-gray-200 rounded"
            title="Fit to view"
          >
            Fit
          </button>
          <button
            onClick={() => exportGraph('png')}
            className="px-3 py-1 text-sm bg-blue-600 hover:bg-blue-700 text-white rounded"
            title="Export as PNG"
          >
            Export PNG
          </button>
        </div>
      </div>
      <div
        id="neo4j-viz"
        ref={vizRef}
        className="flex-1 bg-white"
        style={{ height: 'calc(100vh - 200px)' }}
      />
    </div>
  );
}
