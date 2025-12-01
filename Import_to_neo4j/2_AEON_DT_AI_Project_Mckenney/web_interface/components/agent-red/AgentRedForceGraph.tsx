import React, { useEffect, useRef, useState } from 'react';
import { Move, Info, MousePointer2, ShieldAlert, Terminal, Network } from 'lucide-react';

/**
 * AGENT RED FORCE GRAPH
 * 
 * Adapted from FrameworkView.tsx (Force-Directed Dialectic).
 * Visualizes the "Submind Swarm" and their interaction with Target Assets.
 */

export const AgentRedForceGraph: React.FC = () => {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const containerRef = useRef<HTMLDivElement>(null);
    const [selectedNode, setSelectedNode] = useState<string | null>(null);

    const simulation = useRef<{
        nodes: any[];
        edges: any[];
        particles: any[];
        draggingNode: any | null;
        hoveredNode: any | null;
        time: number;
        shocks: number[];
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
    const NODE_RADIUS = 35;
    const SYMBOLS = ['1', '0', 'X', '!', '>', '#', '{', '}'];

    // Initialize Graph Data
    const initGraph = (width: number, height: number) => {
        const cx = width / 2;
        const cy = height / 2;
        const scale = Math.min(width, height) * 0.35;

        // Define Nodes (Subminds & Targets)
        const nodes = [
            // The Commander
            { id: 'red_leader', label: 'RED LEADER', x: cx, y: cy, color: '#00e0b0', type: 'CORE', mass: 80, desc: "The strategic mastermind. Orchestrates the campaign and defines Rules of Engagement." },

            // The Subminds
            { id: 'cartographer', label: 'Cartographer', x: cx - scale, y: cy - scale * 0.5, color: '#00aaff', type: 'SUBMIND', mass: 30, desc: "Maps the digital footprint. Scans ports, identifies services, and enumerates assets." },
            { id: 'breacher', label: 'Breacher', x: cx + scale, y: cy - scale * 0.5, color: '#f59e0b', type: 'SUBMIND', mass: 30, desc: "The offensive engine. Generates exploits, cracks passwords, and gains initial access." },
            { id: 'ghost', label: 'Ghost', x: cx, y: cy + scale * 0.8, color: '#a855f7', type: 'SUBMIND', mass: 30, desc: "Persistence and evasion. Installs backdoors and cleans logs to remain undetected." },

            // The Targets (Simulated)
            { id: 'target_db', label: 'Target: DB', x: cx - scale * 0.8, y: cy + scale * 0.5, color: '#ef4444', type: 'TARGET', mass: 20, desc: "Critical Database Server (SQL Injection Vector)." },
            { id: 'target_web', label: 'Target: Web', x: cx + scale * 0.8, y: cy + scale * 0.5, color: '#ef4444', type: 'TARGET', mass: 20, desc: "Public Web Portal (RCE Vulnerability)." },
            { id: 'target_human', label: 'Target: HR', x: cx + scale * 0.5, y: cy - scale * 0.8, color: '#ef4444', type: 'TARGET', mass: 20, desc: "HR Department (Phishing/Social Engineering)." },
        ];

        nodes.forEach((n, i) => {
            (n as any).vx = (Math.random() - 0.5) * 0.5;
            (n as any).vy = (Math.random() - 0.5) * 0.5;
            (n as any).fx = 0;
            (n as any).fy = 0;
            (n as any).phase = Math.random() * Math.PI * 2;
        });

        // Define Edges (Command & Attack Paths)
        const edges = [
            // Command Links
            { source: 'red_leader', target: 'cartographer', len: scale * 0.8, type: 'COMMAND' },
            { source: 'red_leader', target: 'breacher', len: scale * 0.8, type: 'COMMAND' },
            { source: 'red_leader', target: 'ghost', len: scale * 0.8, type: 'COMMAND' },

            // Submind Coordination
            { source: 'cartographer', target: 'breacher', len: scale * 1.2, type: 'DATA' },
            { source: 'breacher', target: 'ghost', len: scale * 1.2, type: 'HANDOFF' },

            // Attack Vectors
            { source: 'cartographer', target: 'target_web', len: scale * 0.6, type: 'SCAN' },
            { source: 'cartographer', target: 'target_db', len: scale * 0.6, type: 'SCAN' },
            { source: 'cartographer', target: 'target_human', len: scale * 0.6, type: 'SCAN' },

            { source: 'breacher', target: 'target_web', len: scale * 0.4, type: 'ATTACK' },
            { source: 'breacher', target: 'target_db', len: scale * 0.4, type: 'ATTACK' },

            { source: 'ghost', target: 'target_db', len: scale * 0.3, type: 'PERSIST' },
        ];

        const edgeObjs = edges.map(e => ({
            source: nodes.find(n => n.id === e.source),
            target: nodes.find(n => n.id === e.target),
            len: e.len,
            type: e.type
        })).filter(e => e.source && e.target);

        // Particles
        const particles = [];
        for (const edge of edgeObjs) {
            const count = edge.type === 'COMMAND' ? 20 : edge.type === 'ATTACK' ? 40 : 10;
            for (let i = 0; i < count; i++) {
                particles.push({
                    edge: edge,
                    progress: Math.random(),
                    baseSpeed: 0.002 + Math.random() * 0.003,
                    char: SYMBOLS[Math.floor(Math.random() * SYMBOLS.length)],
                    offset: (Math.random() - 0.5) * 10,
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
            for (const node of nodes) {
                const dx = x - node.x;
                const dy = y - node.y;
                if (dx * dx + dy * dy < NODE_RADIUS * NODE_RADIUS) {
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
                draggingNode.vx = (x - draggingNode.x) * 0.2;
                draggingNode.vy = (y - draggingNode.y) * 0.2;
                draggingNode.x = x;
                draggingNode.y = y;
            }

            let hover = null;
            for (const node of nodes) {
                const dx = x - node.x;
                const dy = y - node.y;
                if (dx * dx + dy * dy < NODE_RADIUS * NODE_RADIUS) {
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

        const animate = () => {
            if (width <= 0 || height <= 0) {
                animationId = requestAnimationFrame(animate);
                return;
            }

            simulation.current.time += 0.01;
            const { nodes, edges, particles, draggingNode, time } = simulation.current;

            // Random Shocks (Network Spikes)
            if (Math.random() > 0.98) {
                simulation.current.shocks.push(0);
            }

            // Physics
            const REPULSION = 1000;
            const SPRING_K = 0.00015;
            const DAMPING = 0.95;
            const CENTER_GRAVITY = 0.00008;
            const MAX_VELOCITY = 5.0;

            for (let i = 0; i < nodes.length; i++) {
                const node = nodes[i];
                if (node === draggingNode) continue;

                let fx = 0;
                let fy = 0;

                for (let j = 0; j < nodes.length; j++) {
                    if (i === j) continue;
                    const other = nodes[j];
                    const dx = node.x - other.x;
                    const dy = node.y - other.y;
                    const distSq = dx * dx + dy * dy || 1;
                    const dist = Math.sqrt(distSq);

                    if (dist < 800) {
                        const force = REPULSION / (distSq + 50);
                        fx += (dx / dist) * force;
                        fy += (dy / dist) * force;
                    }
                }

                const dxC = (width / 2) - node.x;
                const dyC = (height / 2) - node.y;
                fx += dxC * CENTER_GRAVITY * node.mass;
                fy += dyC * CENTER_GRAVITY * node.mass;

                fx += Math.sin(time * 0.5 + node.phase) * 0.03;
                fy += Math.cos(time * 0.4 + node.phase) * 0.03;

                node.fx = fx;
                node.fy = fy;
            }

            edges.forEach(edge => {
                const source = edge.source;
                const target = edge.target;
                if (!source || !target) return;

                const dx = target.x - source.x;
                const dy = target.y - source.y;
                const dist = Math.sqrt(dx * dx + dy * dy) || 1;
                const displacement = dist - edge.len;
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

            nodes.forEach(node => {
                if (node === draggingNode) return;
                node.vx = (node.vx + node.fx) * DAMPING;
                node.vy = (node.vy + node.fy) * DAMPING;
                const speed = Math.sqrt(node.vx * node.vx + node.vy * node.vy);
                if (speed > MAX_VELOCITY) {
                    node.vx = (node.vx / speed) * MAX_VELOCITY;
                    node.vy = (node.vy / speed) * MAX_VELOCITY;
                }
                node.x += node.vx;
                node.y += node.vy;

                const MARGIN = NODE_RADIUS;
                if (node.x < MARGIN) { node.x = MARGIN; node.vx *= -0.5; }
                if (node.x > width - MARGIN) { node.x = width - MARGIN; node.vx *= -0.5; }
                if (node.y < MARGIN) { node.y = MARGIN; node.vy *= -0.5; }
                if (node.y > height - MARGIN) { node.y = height - MARGIN; node.vy *= -0.5; }
            });

            // Render
            ctx.clearRect(0, 0, width, height);

            // Background Shockwaves
            const cx = width / 2;
            const cy = height / 2;
            simulation.current.shocks = simulation.current.shocks.map(t => t + 0.5).filter(t => t < 120);
            simulation.current.shocks.forEach(t => {
                const r = t * 8;
                const alpha = Math.max(0, 1 - t / 100) * 0.2;
                ctx.beginPath();
                ctx.arc(cx, cy, Math.max(0, r), 0, Math.PI * 2);
                ctx.strokeStyle = `rgba(0, 224, 176, ${alpha})`;
                ctx.lineWidth = 1;
                ctx.stroke();
            });

            // Edges & Particles
            ctx.font = "10px 'Roboto Mono'";
            ctx.textAlign = "center";
            ctx.textBaseline = "middle";

            particles.forEach(p => {
                const { source, target } = p.edge;
                if (!source || !target) return;

                const dx = target.x - source.x;
                const dy = target.y - source.y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                const stretchRatio = dist / p.edge.len;
                const isStretched = stretchRatio > 1.2;

                p.progress += p.baseSpeed * (isStretched ? 2.0 : 1.0);
                if (p.progress > 1) p.progress = 0;

                const x = source.x + (target.x - source.x) * p.progress;
                const y = source.y + (target.y - source.y) * p.progress;

                const angle = Math.atan2(dy, dx);
                const perpX = -Math.sin(angle) * p.offset;
                const perpY = Math.cos(angle) * p.offset;

                if (Number.isFinite(x) && Number.isFinite(y)) {
                    ctx.fillStyle = p.edge.type === 'ATTACK' ? '#ef4444' + '90' : '#00e0b0' + '60';
                    ctx.fillText(p.char, x + perpX, y + perpY);
                }
            });

            // Nodes
            nodes.forEach(node => {
                if (!Number.isFinite(node.x) || !Number.isFinite(node.y)) return;
                const isSelected = node.id === selectedNode;

                // Glow
                ctx.beginPath();
                ctx.arc(node.x, node.y, NODE_RADIUS * (isSelected ? 1.4 : 1.1), 0, Math.PI * 2);
                ctx.fillStyle = node.color + '15';
                ctx.fill();

                // Body
                ctx.beginPath();
                ctx.arc(node.x, node.y, NODE_RADIUS, 0, Math.PI * 2);
                ctx.fillStyle = '#0a0a0a';
                ctx.strokeStyle = node.color;
                ctx.lineWidth = isSelected ? 2 : 1;
                ctx.fill();
                ctx.stroke();

                // Label
                ctx.fillStyle = node.color;
                ctx.font = `bold ${node.type === 'CORE' ? '11px' : '9px'} 'Inter'`;
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

    const activeNodeDesc = simulation.current.nodes.find(n => n.id === selectedNode);

    return (
        <div ref={containerRef} className="relative w-full h-[600px] bg-dark-lighter/50 border border-white/10 rounded-xl overflow-hidden group">
            <canvas ref={canvasRef} className="absolute inset-0 w-full h-full z-0 cursor-grab active:cursor-grabbing" />

            {/* Overlay UI */}
            <div className="absolute top-6 left-6 pointer-events-none opacity-70 group-hover:opacity-100 transition-opacity">
                <div className="flex items-center gap-2 text-primary font-mono text-xs uppercase tracking-widest mb-2">
                    <Network size={14} />
                    <span>Submind Swarm Topology</span>
                </div>
                <p className="text-[10px] text-gray-500 max-w-xs">
                    Drag nodes to reconfigure the attack swarm. Observe data flow between subminds and targets.
                </p>
            </div>

            {/* Detail Panel (LogicView Style) */}
            {selectedNode && activeNodeDesc && (
                <div className="absolute bottom-6 right-6 w-80 bg-black/90 border border-gray-800 backdrop-blur-md p-6 border-l-2 animate-in slide-in-from-bottom-4 fade-in duration-300 shadow-2xl" style={{ borderLeftColor: activeNodeDesc.color }}>
                    <div className="flex items-center justify-between mb-2">
                        <h3 className="text-lg font-bold text-white">{activeNodeDesc.label}</h3>
                        <div className="px-2 py-0.5 bg-white/10 rounded text-[10px] font-mono text-gray-300">{activeNodeDesc.type}</div>
                    </div>
                    <p className="text-sm text-gray-400 leading-relaxed">
                        {activeNodeDesc.desc}
                    </p>
                    <div className="mt-4 flex items-center gap-2 text-[10px] text-gray-600 font-mono">
                        <Terminal size={12} />
                        <span>ID: {activeNodeDesc.id.toUpperCase()}</span>
                    </div>
                </div>
            )}

            {!selectedNode && (
                <div className="absolute bottom-6 right-6 flex items-center gap-3 text-gray-600 animate-pulse pointer-events-none">
                    <MousePointer2 size={16} />
                    <span className="text-xs font-mono uppercase tracking-widest">Select a node to inspect</span>
                </div>
            )}

        </div>
    );
};

export default AgentRedForceGraph;
