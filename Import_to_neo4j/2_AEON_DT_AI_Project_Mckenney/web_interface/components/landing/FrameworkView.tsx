
import React, { useEffect, useRef, useState } from 'react';
import { Move, Info, MousePointer2 } from 'lucide-react';

/**
 * FRAMEWORK VIEW
 * 
 * This component visualizes a "Force-Directed Graph" (Dialectic).
 * Unlike standard graph libraries (D3, Cytoscape), this is a custom implementation
 * focused on visual aesthetics (Neon/Cyber) and specific physics behaviors (Fluidity).
 * 
 * CORE CONCEPTS:
 * 1. Nodes: Physical bodies that repel each other (Coulomb's Law).
 * 2. Edges: Springs that attract connected nodes (Hooke's Law).
 * 3. Particles: Visual symbols that flow along the edges to show direction/tension.
 */

export const FrameworkView: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [selectedNode, setSelectedNode] = useState<string | null>(null);

  // REF PATTERN: We use a ref for simulation state to avoid React re-renders
  // triggering on every single frame (60fps). This ensures high performance.
  const simulation = useRef<{
    nodes: any[];
    edges: any[];
    particles: any[];
    draggingNode: any | null;
    hoveredNode: any | null;
    time: number;
    shocks: number[]; // For geopolitical ripple effects
  }>({
    nodes: [],
    edges: [],
    particles: [],
    draggingNode: null,
    hoveredNode: null,
    time: 0,
    shocks: []
  });

  // Configuration Constants
  const NODE_RADIUS = 30;
  const SYMBOLS = ['∂', '∫', 'Ψ', '∑', '∇', '∆', 'λ', 'Ω', 'μ', '∅'];

  // Initialize Graph Data
  const initGraph = (width: number, height: number) => {
    const cx = width / 2;
    const cy = height / 2;
    const scale = Math.min(width, height) * 0.3;

    // Define Nodes (Lacanian Topology)
    const nodes = [
      { id: 'real', label: 'REAL', x: cx, y: cy, color: '#ffffff', type: 'CORE', mass: 60, desc: "The impossible kernel. That which resists symbolization." },
      
      // The Square
      { id: 'desire', label: 'Desire', x: cx - scale, y: cy - scale, color: '#fb7185', type: 'OUTER', mass: 25, desc: "The driving force, always seeking the lost object." },
      { id: 'law', label: 'Law', x: cx + scale, y: cy - scale, color: '#94a3b8', type: 'OUTER', mass: 25, desc: "The prohibitions that structure social reality." },
      { id: 'eros', label: 'Eros', x: cx - scale, y: cy + scale, color: '#fb7185', type: 'OUTER', mass: 25, desc: "Life drive. Binding, unification, preservation." },
      { id: 'thanatos', label: 'Thanatos', x: cx + scale, y: cy + scale, color: '#94a3b8', type: 'OUTER', mass: 25, desc: "Death drive. Repetition, aggression, unbinding." },
      
      // The Registers
      { id: 'imaginary', label: 'Imaginary', x: cx, y: cy - scale * 0.6, color: '#c084fc', type: 'REGISTER', mass: 20, desc: "The realm of images, ego, and identification." },
      { id: 'symbolic', label: 'Symbolic', x: cx, y: cy + scale * 0.6, color: '#3b82f6', type: 'REGISTER', mass: 20, desc: "The realm of language, law, and structure." },
      
      // Axis Points
      { id: 'ego', label: 'Ego', x: cx - scale * 0.5, y: cy + scale * 0.2, color: '#c084fc', type: 'NODE', mass: 15, desc: "The projection of the self." },
      { id: 'other', label: 'Other', x: cx + scale * 0.5, y: cy + scale * 0.2, color: '#3b82f6', type: 'NODE', mass: 15, desc: "The locus of speech and the Law." },
    ];

    // Initialize physics props
    nodes.forEach((n, i) => {
        (n as any).vx = (Math.random() - 0.5) * 0.5; // Slight initial velocity
        (n as any).vy = (Math.random() - 0.5) * 0.5;
        (n as any).fx = 0;
        (n as any).fy = 0;
        (n as any).phase = Math.random() * Math.PI * 2; // For ambient motion
    });

    // Define Edges (The Topology)
    const edges = [
      { source: 'desire', target: 'law', len: scale * 2 },
      { source: 'law', target: 'thanatos', len: scale * 2 },
      { source: 'thanatos', target: 'eros', len: scale * 2 },
      { source: 'eros', target: 'desire', len: scale * 2 },
      
      // Connecting to Real - Slightly longer to show the "impossible distance" or "pull"
      { source: 'desire', target: 'real', len: scale * 1.6 },
      { source: 'law', target: 'real', len: scale * 1.6 },
      { source: 'eros', target: 'real', len: scale * 1.6 },
      { source: 'thanatos', target: 'real', len: scale * 1.6 },
      
      { source: 'imaginary', target: 'real', len: scale * 0.8 },
      { source: 'symbolic', target: 'real', len: scale * 0.8 },
      
      { source: 'ego', target: 'imaginary', len: scale * 0.8 },
      { source: 'other', target: 'symbolic', len: scale * 0.8 },
      { source: 'ego', target: 'other', len: scale }
    ];

    // Map IDs to objects
    const edgeObjs = edges.map(e => ({
        source: nodes.find(n => n.id === e.source),
        target: nodes.find(n => n.id === e.target),
        len: e.len
    })).filter(e => e.source && e.target);

    // Particles for edges (The Symbol Streams)
    const particles = [];
    // Create roughly 40 particles per edge
    for (const edge of edgeObjs) {
        for(let i=0; i<40; i++) {
            particles.push({
                edge: edge,
                progress: Math.random(), // 0 to 1 position along edge
                baseSpeed: 0.0005 + Math.random() * 0.002, 
                char: SYMBOLS[Math.floor(Math.random() * SYMBOLS.length)],
                offset: (Math.random() - 0.5) * 15, // wider stream width for fluidity
                phase: Math.random() * Math.PI * 2
            });
        }
    }

    simulation.current = {
        nodes,
        edges: edgeObjs,
        particles,
        draggingNode: null,
        hoveredNode: null,
        time: 0,
        shocks: []
    };
  };

  useEffect(() => {
    const canvas = canvasRef.current;
    const container = containerRef.current;
    if (!canvas || !container) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let width = canvas.width = container.clientWidth;
    let height = canvas.height = container.clientHeight;
    let animationId: number;

    initGraph(width, height);

    // Use ResizeObserver to handle window resizing robustly
    const handleResize = () => {
         const newWidth = container.clientWidth;
         const newHeight = container.clientHeight;
         if (newWidth > 0 && newHeight > 0) {
            width = canvas.width = newWidth;
            height = canvas.height = newHeight;
         }
    };

    const resizeObserver = new ResizeObserver(handleResize);
    resizeObserver.observe(container);

    // Input Handling Logic
    const getMousePos = (e: MouseEvent) => {
        const rect = canvas.getBoundingClientRect();
        return {
            x: e.clientX - rect.left,
            y: e.clientY - rect.top
        };
    };

    const handleMouseDown = (e: MouseEvent) => {
        const { x, y } = getMousePos(e);
        const nodes = simulation.current.nodes;
        
        // Hit detection for nodes
        for (const node of nodes) {
            const dx = x - node.x;
            const dy = y - node.y;
            if (dx*dx + dy*dy < NODE_RADIUS*NODE_RADIUS) {
                simulation.current.draggingNode = node;
                setSelectedNode(node.id);
                return;
            }
        }
        setSelectedNode(null);
    };

    const handleMouseMove = (e: MouseEvent) => {
        const { x, y } = getMousePos(e);
        const { draggingNode, nodes } = simulation.current;

        if (draggingNode) {
            // Smooth drag interpolation
            draggingNode.vx = (x - draggingNode.x) * 0.2;
            draggingNode.vy = (y - draggingNode.y) * 0.2;
            draggingNode.x = x;
            draggingNode.y = y;
        }

        // Check hover for cursor change
        let hover = null;
        for (const node of nodes) {
            const dx = x - node.x;
            const dy = y - node.y;
            if (dx*dx + dy*dy < NODE_RADIUS*NODE_RADIUS) {
                hover = node;
                break;
            }
        }
        simulation.current.hoveredNode = hover;
        canvas.style.cursor = hover ? 'grab' : draggingNode ? 'grabbing' : 'default';
    };

    const handleMouseUp = () => {
        simulation.current.draggingNode = null;
    };

    canvas.addEventListener('mousedown', handleMouseDown);
    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('mouseup', handleMouseUp);

    // --- PHYSICS & RENDER LOOP ---
    const animate = () => {
        // Safety check for dimensions
        if (width <= 0 || height <= 0) {
             animationId = requestAnimationFrame(animate);
             return;
        }

        simulation.current.time += 0.01;
        const { nodes, edges, particles, draggingNode, time } = simulation.current;
        
        // Randomly add Geopolitical Shocks (Ripples)
        if (Math.random() > 0.99) {
            simulation.current.shocks.push(0); // Start a new shockwave at t=0
        }

        // PHYSICS PARAMETERS
        // Tip: Adjust these to change the "feel" of the graph
        const REPULSION = 800;      // How strongly nodes push apart
        const SPRING_K = 0.0002;    // Spring stiffness (Low = Stretchy)
        const DAMPING = 0.96;       // Friction (High = slippery/fluid)
        const CENTER_GRAVITY = 0.00005; // Pull to center
        const MAX_VELOCITY = 4.0;   // Speed limit to prevent glitching

        // 1. Apply Forces
        for (let i = 0; i < nodes.length; i++) {
            const node = nodes[i];
            if (node === draggingNode) continue;

            let fx = 0;
            let fy = 0;

            // Repulsion (Coulomb)
            for (let j = 0; j < nodes.length; j++) {
                if (i === j) continue;
                const other = nodes[j];
                const dx = node.x - other.x;
                const dy = node.y - other.y;
                const distSq = dx*dx + dy*dy || 1;
                const dist = Math.sqrt(distSq);
                
                if (dist < 600) {
                    const force = REPULSION / (distSq + 50);
                    fx += (dx / dist) * force;
                    fy += (dy / dist) * force;
                }
            }

            // Center Gravity
            const dxC = (width / 2) - node.x;
            const dyC = (height / 2) - node.y;
            fx += dxC * CENTER_GRAVITY * node.mass;
            fy += dyC * CENTER_GRAVITY * node.mass;

            // Ambient Fluid Drift (Perlin-ish noise)
            fx += Math.sin(time * 0.5 + node.phase) * 0.02;
            fy += Math.cos(time * 0.4 + node.phase) * 0.02;

            node.fx = fx;
            node.fy = fy;
        }

        // Spring Forces (Hooke's Law)
        edges.forEach(edge => {
            const source = edge.source;
            const target = edge.target;
            if (!source || !target) return;

            const dx = target.x - source.x;
            const dy = target.y - source.y;
            const dist = Math.sqrt(dx*dx + dy*dy) || 1;
            
            const displacement = dist - edge.len;
            
            // Lenient spring: force prop to displacement * K
            const force = displacement * SPRING_K;
            
            const fx = (dx / dist) * force;
            const fy = (dy / dist) * force;

            if (source !== draggingNode) {
                source.fx += fx;
                source.fy += fy;
            }
            if (target !== draggingNode) {
                target.fx -= fx;
                target.fy -= fy;
            }
        });

        // Update Positions via Velocity (Euler Integration)
        nodes.forEach(node => {
            if (node === draggingNode) return;
            
            node.vx = (node.vx + node.fx) * DAMPING;
            node.vy = (node.vy + node.fy) * DAMPING;

            // Clamp Velocity
            const speed = Math.sqrt(node.vx*node.vx + node.vy*node.vy);
            if (speed > MAX_VELOCITY) {
                node.vx = (node.vx / speed) * MAX_VELOCITY;
                node.vy = (node.vy / speed) * MAX_VELOCITY;
            }

            node.x += node.vx;
            node.y += node.vy;

            // Bounds Collision (Bounce)
            const MARGIN = NODE_RADIUS;
            if (node.x < MARGIN) { node.x = MARGIN; node.vx *= -0.5; }
            if (node.x > width - MARGIN) { node.x = width - MARGIN; node.vx *= -0.5; }
            if (node.y < MARGIN) { node.y = MARGIN; node.vy *= -0.5; }
            if (node.y > height - MARGIN) { node.y = height - MARGIN; node.vy *= -0.5; }
        });

        // 2. Render Scene
        
        // CLEAR instead of FILL to allow Global Background to show through
        ctx.clearRect(0, 0, width, height);

        // --- BACKGROUND LAYER: LACANIAN MIRROR & RIPPLES ---
        const cx = width / 2;
        const cy = height / 2;
        
        // Draw expanding shockwaves
        simulation.current.shocks = simulation.current.shocks.map(t => t + 0.5).filter(t => t < 100);
        
        simulation.current.shocks.forEach(t => {
            const r = t * 10;
            const alpha = Math.max(0, 1 - t / 80) * 0.3;
            
            ctx.beginPath();
            ctx.arc(cx, cy, Math.max(0, r), 0, Math.PI * 2); // SAFE RADIUS
            ctx.strokeStyle = `rgba(255, 255, 255, ${alpha})`;
            ctx.lineWidth = 1;
            ctx.stroke();
            
            // "Jouissance" Spike
            if (t % 10 < 1) {
                 ctx.beginPath();
                 ctx.arc(cx, cy, Math.max(0, r * 1.05), 0, Math.PI * 2); // SAFE RADIUS
                 ctx.strokeStyle = `rgba(0, 224, 176, ${alpha * 0.5})`;
                 ctx.stroke();
            }
        });

        // Draw Concentric "Dialectic" Rings (The Mirror)
        // These pulsate slowly to breathe with the graph
        const ringCount = 4;
        for (let i = 0; i < ringCount; i++) {
            const baseR = Math.min(width, height) * (0.1 + i * 0.15);
            const breath = Math.sin(time * 0.5 + i) * 15;
            const r = Math.max(0, baseR + breath); // SAFE RADIUS
            
            // Main Ring
            if (r > 0) {
                ctx.beginPath();
                ctx.arc(cx, cy, r, 0, Math.PI * 2);
                ctx.strokeStyle = `rgba(0, 224, 176, 0.05)`; // Teal faint
                ctx.lineWidth = 2;
                ctx.stroke();
            }

            // Mirror Reflection (Inverse Pulse)
            const mirrorR = Math.max(0, baseR - breath * 0.5); // SAFE RADIUS
            if (mirrorR > 0) {
                ctx.beginPath();
                ctx.arc(cx, cy, mirrorR, 0, Math.PI * 2);
                ctx.strokeStyle = `rgba(168, 85, 247, 0.03)`; // Purple faint (Imaginary)
                ctx.lineWidth = 10;
                ctx.stroke();
            }
        }

        // Draw Edges (The flowing symbol streams)
        ctx.font = "10px 'Roboto Mono'";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";

        particles.forEach(p => {
            const { source, target } = p.edge;
            if (!source || !target) return;

            // Calculate Tension Visuals
            const dx = target.x - source.x;
            const dy = target.y - source.y;
            const dist = Math.sqrt(dx*dx + dy*dy);
            const stretchRatio = dist / p.edge.len;
            const isStretched = stretchRatio > 1.2;

            // Move particle along line
            const currentSpeed = p.baseSpeed * (isStretched ? 2.5 : 1.0);
            p.progress += currentSpeed;
            if (p.progress > 1) p.progress = 0;

            const x = source.x + (target.x - source.x) * p.progress;
            const y = source.y + (target.y - source.y) * p.progress;

            // Add visual "Sag" and "Jitter" based on tension
            const angle = Math.atan2(target.y - source.y, target.x - source.x);
            const freq = isStretched ? 10 : 4;
            const amp = isStretched ? 2 : 5;
            const flowOffset = Math.sin(p.progress * Math.PI * freq + time * (isStretched ? 5 : 2) + p.phase) * amp;
            
            const perpX = -Math.sin(angle) * (p.offset + flowOffset);
            const perpY = Math.cos(angle) * (p.offset + flowOffset);

            if (Number.isFinite(x) && Number.isFinite(y)) {
                ctx.fillStyle = isStretched ? '#ff4444' + '80' : source.color + '60';
                ctx.fillText(p.char, x + perpX, y + perpY);
            }
        });

        // Draw Nodes
        nodes.forEach(node => {
            if (!Number.isFinite(node.x) || !Number.isFinite(node.y)) return;

            const isSelected = node.id === selectedNode;
            
            // Outer Glow
            ctx.beginPath();
            ctx.arc(node.x, node.y, NODE_RADIUS * (isSelected ? 1.5 : 1.2), 0, Math.PI * 2);
            ctx.fillStyle = node.color + '10';
            ctx.fill();

            // Solid Body
            ctx.beginPath();
            ctx.arc(node.x, node.y, NODE_RADIUS, 0, Math.PI * 2);
            ctx.fillStyle = '#0a0a0a';
            ctx.strokeStyle = node.color;
            ctx.lineWidth = isSelected ? 2 : 1;
            ctx.fill();
            ctx.stroke();

            // Label
            ctx.fillStyle = node.color;
            ctx.font = `bold ${node.type === 'CORE' ? '12px' : '10px'} 'Inter'`;
            ctx.fillText(node.label, node.x, node.y);
        });

        animationId = requestAnimationFrame(animate);
    };

    animate();

    return () => {
        resizeObserver.disconnect();
        cancelAnimationFrame(animationId);
        canvas.removeEventListener('mousedown', handleMouseDown);
        window.removeEventListener('mousemove', handleMouseMove);
        window.removeEventListener('mouseup', handleMouseUp);
    };
  }, [selectedNode]);

  // Get description for the UI panel
  const activeNodeDesc = simulation.current.nodes.find(n => n.id === selectedNode);

  return (
    <div ref={containerRef} className="relative w-full h-full min-h-[800px] flex items-center justify-center bg-transparent overflow-hidden group">
      <canvas ref={canvasRef} className="absolute inset-0 w-full h-full z-0 cursor-grab active:cursor-grabbing" />

      {/* Instructions Overlay */}
      <div className="absolute top-8 left-8 pointer-events-none select-none opacity-50 group-hover:opacity-100 transition-opacity">
         <div className="flex items-center gap-2 text-primary font-mono text-xs uppercase tracking-widest mb-2">
            <Move size={14} />
            <span>Force-Directed Dialectic</span>
         </div>
         <p className="text-[10px] text-gray-500 max-w-xs">
            The diagram is not static. Drag nodes to reshape the tensions between Lacanian registers.
         </p>
      </div>

      {/* Detail Panel */}
      {selectedNode && activeNodeDesc && (
        <div className="absolute bottom-8 right-8 w-80 bg-black/80 border border-gray-800 backdrop-blur-md p-6 border-l-2 animate-in slide-in-from-bottom-4 fade-in duration-300" style={{ borderLeftColor: activeNodeDesc.color }}>
            <div className="flex items-center justify-between mb-2">
                <h3 className="text-lg font-bold text-white">{activeNodeDesc.label}</h3>
                <div className="px-2 py-0.5 bg-white/10 rounded text-[10px] font-mono text-gray-300">{activeNodeDesc.type}</div>
            </div>
            <p className="text-sm text-gray-400 leading-relaxed">
                {activeNodeDesc.desc}
            </p>
            <div className="mt-4 flex items-center gap-2 text-[10px] text-gray-600 font-mono">
                <MousePointer2 size={12} />
                <span>NODE_ID: {activeNodeDesc.id.toUpperCase()}</span>
            </div>
        </div>
      )}
      
      {!selectedNode && (
         <div className="absolute bottom-8 right-8 flex items-center gap-3 text-gray-600 animate-pulse pointer-events-none">
            <MousePointer2 size={16} />
            <span className="text-xs font-mono uppercase tracking-widest">Select a node to analyze</span>
         </div>
      )}

    </div>
  );
};
