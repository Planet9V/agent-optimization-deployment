import React, { useMemo, useState, useEffect, useRef } from 'react';
import {
    ComposedChart, Line, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine
} from 'recharts';
import { SimulationParams, DataFeedItem } from './types';
import { GitCommit, AlertTriangle, Database, Globe, Shield, Terminal, Cpu, Activity } from 'lucide-react';

interface SimulationGraphProps {
    params: SimulationParams;
}

// Mock Data Generators
const CYPHER_QUERIES = [
    "MATCH (t:ThreatActor)-[:TARGETS]->(s:Sector {name: 'Energy'}) RETURN t.probability",
    "CALL gds.pageRank.stream('PsychGraph') YIELD nodeId, score",
    "MATCH (v:Vulnerability) WHERE v.cvss > 9.0 DETACH DELETE v",
    "MERGE (e:Event {type: 'Geopolitical'})-[:IMPACTS]->(m:Market)",
    "CALCULATE d(Psi)/dt WHERE entropy > threshold"
];

const NEWS_FRAGMENTS = [
    { source: 'NVD', content: 'CVE-2025-8921: Remote Code Execution in OpenSSL', severity: 'critical' },
    { source: 'REUTERS', content: 'Tensions rise in Strait of Hormuz, shipping impacted', severity: 'high' },
    { source: 'INT', content: 'Intercepted chatter regarding water utility SCADA', severity: 'high' },
    { source: 'DARKWEB', content: 'New exploit kit "Vortex" selling for 50BTC', severity: 'medium' },
    { source: 'INT', content: 'Employee sentiment analysis: "Burnout" detected', severity: 'medium' },
    { source: 'NVD', content: 'CVE-2025-9912: Minor buffer overflow in legacy stack', severity: 'low' },
];

export const SimulationGraph: React.FC<SimulationGraphProps> = ({ params }) => {
    const [feeds, setFeeds] = useState<DataFeedItem[]>([]);
    const [activeQuery, setActiveQuery] = useState("");
    const [timeStep, setTimeStep] = useState(0);
    const feedScrollRef = useRef<HTMLDivElement>(null);

    // Simulation Data Calculation
    const data = useMemo(() => {
        const points = [];
        const days = 90;

        let currentRealist = 0.2;
        let currentOptimistic = 0.2;
        let currentPessimistic = 0.2;

        // Seed randomness based on params to keep it stable-ish but reactive
        const seed = params.systemEntropy * 100;

        for (let day = 0; day <= days; day++) {
            const timeNoise = Math.sin(day * 0.1 + seed) * 0.05;
            const entropyNoise = (Math.random() - 0.5) * params.systemEntropy * 0.15;

            // Equations
            // dP/dt = (Entropy * Viscosity) / Inertia
            const riskDelta = (params.systemEntropy * params.culturalViscosity) / (params.socialInertia + 0.1) * 0.03;
            const mitigation = (params.adaptationRate / 100) * 0.025;

            currentRealist = currentRealist + riskDelta - mitigation + entropyNoise + (timeNoise * 0.2);
            currentRealist = Math.max(0.05, Math.min(0.95, currentRealist));

            // Optimistic (Seldon Path)
            currentOptimistic = currentOptimistic + (0.05 * 0.02) - 0.03; // Natural decay of risk
            currentOptimistic = Math.max(0.02, Math.min(currentRealist - 0.1, currentOptimistic));

            // Pessimistic (Collapse)
            currentPessimistic = currentPessimistic + 0.015 + entropyNoise; // Accumulating risk
            currentPessimistic = Math.max(currentRealist + 0.1, Math.min(1.0, currentPessimistic));

            // Calculate "Range" for the Area chart
            // We want to fill between Pessimistic and Optimistic

            points.push({
                day: day,
                label: `T + ${day} `,
                optimistic: currentOptimistic.toFixed(3),
                realist: currentRealist.toFixed(3),
                pessimistic: currentPessimistic.toFixed(3),
                // For Area Chart 'range' visual
                range: [currentOptimistic, currentPessimistic],
                divergence: Math.abs(currentPessimistic - currentOptimistic).toFixed(3),
                threshold: 0.8
            });
        }
        return points;
    }, [params]);

    // Live Feed Effect
    useEffect(() => {
        const interval = setInterval(() => {
            const newItem = NEWS_FRAGMENTS[Math.floor(Math.random() * NEWS_FRAGMENTS.length)];
            const feedItem: DataFeedItem = {
                id: Math.random().toString(36).substring(7),
                source: newItem.source as any,
                timestamp: new Date().toLocaleTimeString([], { hour12: false }),
                content: newItem.content,
                severity: newItem.severity as any,
                impactParameter: 'general'
            };
            // Limit buffer to 10 items to prevent endless visualization
            setFeeds(prev => [feedItem, ...prev].slice(0, 10));

            // Randomly switch query
            if (Math.random() > 0.7) {
                setActiveQuery(CYPHER_QUERIES[Math.floor(Math.random() * CYPHER_QUERIES.length)]);
            }

            setTimeStep(t => t + 1);

        }, 2000);

        return () => clearInterval(interval);
    }, []);

    const currentRisk = parseFloat(data[data.length - 1].realist);
    const isCrisis = currentRisk > 0.8;
    const riskColor = isCrisis ? '#ef4444' : currentRisk > 0.5 ? '#eab308' : '#00e0b0';

    return (
        <div className="w-full h-full min-h-[600px] flex flex-col lg:flex-row gap-6 perspective-1000">

            {/* LEFT: THE PRIME RADIANT (Main Visualization) */}
            <div className="flex-grow relative group bg-dark/40 border border-gray-800 backdrop-blur-sm overflow-hidden flex flex-col transform transition-transform duration-700 hover:rotate-y-1 hover:scale-[1.01] shadow-2xl">

                {/* Background: Cypher Matrix */}
                <div className="absolute inset-0 overflow-hidden opacity-10 pointer-events-none font-mono text-[10px] leading-4 text-primary select-none">
                    {Array.from({ length: 20 }).map((_, i) => (
                        <div key={i} className="whitespace-nowrap animate-pulse" style={{ animationDelay: `${i * 0.5} s`, transform: `translateY(${timeStep % 10}px)` }}>
                            {CYPHER_QUERIES[i % CYPHER_QUERIES.length]}
                        </div>
                    ))}
                </div>

                {/* Header */}
                <div className="relative z-10 flex justify-between items-start p-6 border-b border-gray-800/50 bg-gradient-to-b from-black/40 to-transparent">
                    <div>
                        <div className="flex items-center gap-3 mb-1">
                            <Activity className="text-primary animate-pulse" size={16} />
                            <h3 className="text-sm font-bold font-mono text-white tracking-[0.2em] uppercase">Prime Radiant Visualization</h3>
                        </div>
                        <div className="text-xs text-gray-500 font-mono flex items-center gap-4">
                            <span>MODEL: PSYCHOHISTORY_V4</span>
                            <span>LATENCY: 12ms</span>
                            <span className="text-primary">SYNCED</span>
                        </div>
                    </div>
                    <div className="text-right">
                        <div className="text-4xl font-black font-mono tracking-tighter" style={{ color: riskColor, textShadow: `0 0 20px ${riskColor} 40` }}>
                            {(currentRisk * 100).toFixed(1)}%
                        </div>
                        <div className="text-[10px] uppercase tracking-widest text-gray-500">Collapse Probability (Ψ)</div>
                    </div>
                </div>

                {/* Graph Area */}
                <div className="relative flex-grow p-2">
                    <ResponsiveContainer width="100%" height="100%">
                        <ComposedChart data={data} margin={{ top: 20, right: 30, left: 0, bottom: 0 }}>
                            <defs>
                                <linearGradient id="colorPessimistic" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="5%" stopColor="#ef4444" stopOpacity={0.1} />
                                    <stop offset="95%" stopColor="#ef4444" stopOpacity={0} />
                                </linearGradient>
                                <linearGradient id="colorOptimistic" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="5%" stopColor="#00e0b0" stopOpacity={0.1} />
                                    <stop offset="95%" stopColor="#00e0b0" stopOpacity={0} />
                                </linearGradient>
                                <filter id="glow">
                                    <feGaussianBlur stdDeviation="2.5" result="coloredBlur" />
                                    <feMerge>
                                        <feMergeNode in="coloredBlur" />
                                        <feMergeNode in="SourceGraphic" />
                                    </feMerge>
                                </filter>
                            </defs>

                            <CartesianGrid strokeDasharray="3 3" stroke="#222" vertical={false} />
                            <XAxis dataKey="label" tick={{ fill: '#444', fontSize: 10, fontFamily: 'monospace' }} tickLine={false} axisLine={{ stroke: '#333' }} interval={14} />
                            <YAxis domain={[0, 1.1]} hide />

                            <Tooltip
                                contentStyle={{ backgroundColor: '#0a0a0a', border: '1px solid #333', fontFamily: 'monospace' }}
                                itemStyle={{ fontSize: '12px' }}
                            />

                            <ReferenceLine y={0.8} stroke="#ef4444" strokeDasharray="3 3" opacity={0.5} label={{ value: "CRITICAL THRESHOLD", fill: "#ef4444", fontSize: 10, position: "insideTopRight" }} />

                            {/* Uncertainty Range Area */}
                            <Area
                                type="monotone"
                                dataKey="pessimistic"
                                stroke="transparent"
                                fill="url(#colorPessimistic)"
                            />
                            <Area
                                type="monotone"
                                dataKey="optimistic"
                                stroke="transparent"
                                fill="url(#colorOptimistic)"
                            />

                            {/* Trajectories */}
                            <Line
                                type="monotone"
                                dataKey="pessimistic"
                                stroke="#ef4444"
                                strokeWidth={1}
                                strokeDasharray="4 4"
                                dot={false}
                                opacity={0.6}
                                name="Collapse Vector"
                            />
                            <Line
                                type="monotone"
                                dataKey="optimistic"
                                stroke="#00e0b0"
                                strokeWidth={1}
                                strokeDasharray="4 4"
                                dot={false}
                                opacity={0.6}
                                name="Seldon Path"
                            />
                            <Line
                                type="monotone"
                                dataKey="realist"
                                stroke={riskColor}
                                strokeWidth={3}
                                dot={false}
                                filter="url(#glow)"
                                name="Current Projection"
                                animationDuration={1000}
                            />
                        </ComposedChart>
                    </ResponsiveContainer>

                    {/* Overlay Math Symbols */}
                    <div className="absolute top-[20%] left-[30%] text-primary/20 font-mono text-2xl pointer-events-none select-none">∫</div>
                    <div className="absolute bottom-[30%] right-[20%] text-secondary/20 font-mono text-4xl pointer-events-none select-none">∂x</div>
                </div>

                {/* Footer Query Line */}
                <div className="h-8 bg-black border-t border-gray-800 flex items-center px-4 gap-2">
                    <Terminal size={12} className="text-primary" />
                    <span className="font-mono text-[10px] text-gray-500 truncate w-full animate-pulse">
                        {activeQuery}
                    </span>
                </div>
            </div>

            {/* RIGHT: LIVE DATA INGESTION (The Feed) */}
            <div className="w-full lg:w-[320px] flex flex-col gap-4 h-full min-h-[400px]">

                {/* Stats Box */}
                <div className="grid grid-cols-2 gap-2">
                    <div className="bg-surface/60 border border-gray-800 p-3 backdrop-blur-sm">
                        <div className="flex items-center gap-2 text-gray-500 mb-1">
                            <Database size={12} />
                            <span className="text-[10px] uppercase font-mono">Data Points</span>
                        </div>
                        <div className="text-white font-mono font-bold text-xl">42.8M</div>
                    </div>
                    <div className="bg-surface/60 border border-gray-800 p-3 backdrop-blur-sm">
                        <div className="flex items-center gap-2 text-gray-500 mb-1">
                            <Cpu size={12} />
                            <span className="text-[10px] uppercase font-mono">Compute Load</span>
                        </div>
                        <div className="text-primary font-mono font-bold text-xl">8%</div>
                    </div>
                </div>

                {/* The Feed List */}
                <div className="flex-grow bg-black/80 border border-gray-800 flex flex-col overflow-hidden relative">
                    <div className="p-3 border-b border-gray-800 bg-gray-900/50 flex justify-between items-center">
                        <h4 className="text-xs font-bold font-mono text-gray-400 uppercase tracking-wider">Live Ingestion Stream</h4>
                        <div className="w-2 h-2 rounded-full bg-primary animate-ping"></div>
                    </div>

                    <div className="flex-grow overflow-y-hidden relative p-2 space-y-2" ref={feedScrollRef}>
                        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-black/90 pointer-events-none z-10"></div>

                        {feeds.map((feed, idx) => (
                            <div key={feed.id} className={`p - 3 border border - gray - 800 bg - gray - 900 / 30 backdrop - blur - sm transition - all duration - 500 animate -in slide -in -from - top - 2 fade -in ${idx === 0 ? 'border-primary/50 bg-primary/5' : ''} `}>
                                <div className="flex justify-between items-start mb-1">
                                    <div className="flex items-center gap-2">
                                        {feed.source === 'NVD' && <Shield size={10} className="text-red-400" />}
                                        {feed.source === 'REUTERS' && <Globe size={10} className="text-blue-400" />}
                                        {feed.source === 'INT' && <Activity size={10} className="text-yellow-400" />}
                                        {feed.source === 'DARKWEB' && <Terminal size={10} className="text-purple-400" />}
                                        <span className={`text - [10px] font - mono font - bold ${feed.source === 'NVD' ? 'text-red-400' :
                                            feed.source === 'REUTERS' ? 'text-blue-400' :
                                                feed.source === 'INT' ? 'text-yellow-400' : 'text-purple-400'
                                            } `}>{feed.source}</span>
                                    </div>
                                    <span className="text-[9px] text-gray-600 font-mono">{feed.timestamp}</span>
                                </div>
                                <p className="text-[10px] text-gray-300 font-mono leading-tight">
                                    {feed.content}
                                </p>
                                <div className="mt-2 flex items-center justify-between">
                                    <span className="text-[8px] uppercase text-gray-600 font-mono">Impact: {feed.impactParameter}</span>
                                    <div className="flex gap-0.5">
                                        {[1, 2, 3, 4, 5].map(i => (
                                            <div key={i} className={`w - 0.5 h - 2 ${i <= (feed.severity === 'critical' ? 5 : feed.severity === 'high' ? 4 : feed.severity === 'medium' ? 3 : 1) ? 'bg-primary' : 'bg-gray-800'} `}></div>
                                        ))}
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

            </div>
        </div>
    );
};
