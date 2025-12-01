
import React, { useState } from 'react';
import { Brain, Radio, Database, ShieldAlert, Globe, Activity, ChevronRight, Zap, Lock, Server, Layers, ArrowUpRight } from 'lucide-react';
import { ViewState } from './types';

const layers = [
    {
        level: 5,
        title: "GEOPOLITICAL",
        subtitle: "Contextual Superstructure",
        description: "The macro-environment where cyber threats originate. International tensions, media narratives, and societal fear factors act as the primary forcing function.",
        icon: <Globe size={24} />,
        stats: { latency: "24h+", throughput: "Macro", type: "Abstract" },
        color: "text-blue-400",
        bg: "bg-blue-500",
        border: "border-blue-400",
        shadow: "shadow-blue-500"
    },
    {
        level: 4,
        title: "ORG PSYCHOLOGY",
        subtitle: "The Cultural Filter",
        description: "The internal reality distortion field. Biases, cognitive dissonance, and organizational culture filter external signals, suppressing warnings.",
        icon: <Brain size={24} />,
        stats: { latency: "Real-time", throughput: "High", type: "Cognitive" },
        color: "text-purple-400",
        bg: "bg-purple-500",
        border: "border-purple-400",
        shadow: "shadow-purple-500"
    },
    {
        level: 3,
        title: "INFO STREAMS",
        subtitle: "The Nervous System",
        description: "The sensory inputs. CVE feeds, SIEM alerts, and threat intelligence that must traverse the psychological filters.",
        icon: <Radio size={24} />,
        stats: { latency: "<100ms", throughput: "10GB/s", type: "Digital" },
        color: "text-green-400",
        bg: "bg-green-500",
        border: "border-green-400",
        shadow: "shadow-green-500"
    },
    {
        level: 2,
        title: "THREAT ACTOR",
        subtitle: "The Adversarial Mind",
        description: "The intent behind the attack. Modeling 'Why' using MICE frameworks (Money, Ideology, Coercion, Ego) vs just 'How'.",
        icon: <ShieldAlert size={24} />,
        stats: { latency: "Variable", throughput: "Targeted", type: "Behavioral" },
        color: "text-orange-400",
        bg: "bg-orange-500",
        border: "border-orange-400",
        shadow: "shadow-orange-500"
    },
    {
        level: 1,
        title: "TECH LAYER",
        subtitle: "The Physical Substrate",
        description: "The raw attack surface. Unpatched libraries, misconfigurations. Potential energy waiting for a kinetic trigger.",
        icon: <Database size={24} />,
        stats: { latency: "Static", throughput: "N/A", type: "Physical" },
        color: "text-cyan-400",
        bg: "bg-cyan-500",
        border: "border-cyan-400",
        shadow: "shadow-cyan-500"
    }
];

interface ArchitectureProps {
    onNavigate: (view: ViewState) => void;
}

export const Architecture: React.FC<ArchitectureProps> = ({ onNavigate }) => {
    const [activeLevel, setActiveLevel] = useState<number>(3);
    const activeLayer = layers.find(l => l.level === activeLevel) || layers[2];

    return (
        <div className="w-full h-full flex flex-col lg:flex-row items-center justify-center gap-12 lg:gap-24 p-4 lg:p-12 relative perspective-1000">

            {/* LEFT: THE STACK (Stable Exploded Isometric) */}
            <div className="relative w-[300px] md:w-[350px] h-[500px] md:h-[600px] flex flex-col justify-between z-10 transform-style-3d rotate-x-12 group">
                {/* Central Axis Line */}
                <div className="absolute left-1/2 top-0 bottom-0 w-px bg-gradient-to-b from-transparent via-gray-700 to-transparent -translate-x-1/2 z-0"></div>

                {layers.map((layer, i) => {
                    const isActive = layer.level === activeLevel;

                    return (
                        <div
                            key={layer.level}
                            className={`
                        relative w-full h-[80px] md:h-[100px] 
                        backdrop-blur-sm transition-all duration-700 ease-out
                        cursor-pointer flex items-center px-6 gap-4
                        hover:backdrop-blur-md
                        animate-float
                        ${isActive
                                    ? `z-20 opacity-100 translate-x-6`
                                    : 'z-10 opacity-50 hover:opacity-90 hover:translate-x-2 grayscale-[0.5] hover:grayscale-0'
                                }
                    `}
                            style={{
                                animationDelay: `${i * 0.3}s`, // Staggered float
                                // Sophisticated Isometric Tilt & 3D Transform
                                transform: isActive
                                    ? 'perspective(1500px) rotateY(-5deg) rotateX(2deg) scale(1.05)'
                                    : 'perspective(1500px) rotateY(0deg) rotateX(0deg) scale(1)',
                            }}
                            onClick={() => setActiveLevel(layer.level)}
                            onMouseEnter={() => setActiveLevel(layer.level)}
                        >
                            {/* Glass Block Background */}
                            <div className={`
                        absolute inset-0 rounded-sm border border-l-4 shadow-2xl transition-all duration-500
                        ${isActive
                                    ? `bg-gradient-to-br from-gray-900/90 via-gray-800/90 to-black/90 ${layer.border} border-l-${layer.color.split('-')[1]}-500`
                                    : 'bg-gray-900/40 border-gray-800 border-l-gray-600'
                                }
                    `}>
                                {/* Internal Circuit Pattern Overlay */}
                                <div className="absolute inset-0 opacity-10 bg-[url('https://www.transparenttextures.com/patterns/diagmonds-light.png')] mix-blend-overlay"></div>

                                {/* Active Laser Scan Effect */}
                                {isActive && (
                                    <div className={`absolute inset-0 w-full h-full bg-gradient-to-b from-transparent via-${layer.color.split('-')[1]}-500/20 to-transparent animate-scan-vertical pointer-events-none`}></div>
                                )}
                            </div>

                            {/* Icon Block with depth */}
                            <div className={`
                        relative z-10 p-3 rounded-sm border transition-all duration-500 shadow-lg
                        ${isActive
                                    ? `${layer.color} border-${layer.color.split('-')[1]}-500/50 bg-white/5 shadow-[0_0_15px_rgba(0,0,0,0.5)] scale-110`
                                    : 'text-gray-500 border-gray-700 bg-transparent scale-100'}
                    `}>
                                {layer.icon}
                            </div>

                            {/* Text Info */}
                            <div className="relative z-10 flex flex-col">
                                <span className={`text-[10px] font-mono uppercase tracking-widest mb-1 transition-colors duration-300 ${isActive ? layer.color : 'text-gray-600'}`}>
                                    Layer 0{layer.level}
                                </span>
                                <span className={`font-bold font-mono uppercase text-sm md:text-base transition-colors duration-300 ${isActive ? 'text-white' : 'text-gray-500'}`}>
                                    {layer.title}
                                </span>
                            </div>

                            {/* Connector Line to Axis */}
                            <div className={`
                        absolute right-full top-1/2 h-px transition-all duration-500 origin-right
                        ${isActive ? `w-12 ${layer.bg} opacity-100 shadow-[0_0_10px_currentColor]` : 'w-6 bg-gray-800 opacity-50'}
                    `}>
                                <div className={`absolute left-0 top-1/2 -translate-y-1/2 w-1 h-1 rounded-full ${isActive ? layer.bg : 'bg-gray-800'}`}></div>
                            </div>

                            {/* Active Indicator Dot */}
                            {isActive && (
                                <div className={`absolute right-4 top-1/2 -translate-y-1/2 w-1.5 h-1.5 rounded-full ${layer.bg} animate-pulse shadow-[0_0_10px_currentColor]`}></div>
                            )}
                        </div>
                    );
                })}
            </div>

            {/* RIGHT: ANALYSIS MODULE (Dynamic Detail View) */}
            <div className="w-full max-w-md relative z-20 animate-in slide-in-from-right-8 fade-in duration-700">
                <div className="bg-dark/80 backdrop-blur-xl border border-white/10 p-8 relative overflow-hidden shadow-[0_0_50px_rgba(0,0,0,0.5)] min-h-[450px] group">

                    {/* Dynamic Top Border */}
                    <div className={`absolute top-0 left-0 w-full h-0.5 transition-colors duration-500 ${activeLayer.bg}`}></div>

                    {/* Header Area */}
                    <div className="flex items-start justify-between mb-8 relative z-10">
                        <div>
                            <div className="overflow-hidden">
                                <h2 key={activeLevel} className="text-3xl md:text-4xl font-bold text-white font-mono mb-2 tracking-tight animate-in slide-in-from-bottom-4 duration-500">
                                    {activeLayer.title}
                                </h2>
                            </div>
                            <p className={`text-sm font-mono uppercase tracking-widest transition-colors duration-500 ${activeLayer.color}`}>
                                {activeLayer.subtitle}
                            </p>
                        </div>
                        <div className={`p-3 rounded border bg-white/5 transition-all duration-500 ${activeLayer.border} ${activeLayer.color} shadow-[0_0_20px_rgba(0,0,0,0.3)]`}>
                            {activeLayer.icon}
                        </div>
                    </div>

                    {/* Description with Typing Effect Simulation */}
                    <div className="mb-8 relative z-10">
                        <div className="flex items-center gap-2 mb-3 text-gray-500 text-xs font-bold uppercase tracking-wider">
                            <Activity size={12} className="animate-pulse" />
                            <span>System Function</span>
                        </div>
                        <p key={activeLevel} className="text-gray-300 leading-relaxed text-sm border-l-2 border-gray-800 pl-4 py-1 animate-in fade-in duration-700">
                            {activeLayer.description}
                        </p>

                        <button
                            onClick={() => onNavigate(ViewState.LOGIC)}
                            className="mt-6 inline-flex items-center gap-2 px-3 py-1.5 border border-white/10 bg-white/5 hover:bg-white/10 hover:border-primary/50 text-[10px] text-gray-400 hover:text-primary uppercase tracking-wider font-mono rounded-sm transition-all group"
                        >
                            <Brain size={12} />
                            <span>Analyze Logic</span>
                            <ArrowUpRight size={12} className="group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform opacity-50 group-hover:opacity-100" />
                        </button>
                    </div>

                    {/* Stats Grid */}
                    <div className="grid grid-cols-2 gap-4 mb-8 relative z-10">
                        <div className="bg-black/50 border border-white/5 p-3 hover:border-white/10 transition-colors">
                            <div className="text-[10px] uppercase text-gray-500 mb-1 flex items-center gap-2">
                                <Zap size={10} /> Latency
                            </div>
                            <div className="font-mono text-white">{activeLayer.stats.latency}</div>
                        </div>
                        <div className="bg-black/50 border border-white/5 p-3 hover:border-white/10 transition-colors">
                            <div className="text-[10px] uppercase text-gray-500 mb-1 flex items-center gap-2">
                                <Server size={10} /> Throughput
                            </div>
                            <div className="font-mono text-white">{activeLayer.stats.throughput}</div>
                        </div>
                        <div className="col-span-2 bg-black/50 border border-white/5 p-3 hover:border-white/10 transition-colors">
                            <div className="text-[10px] uppercase text-gray-500 mb-1 flex items-center gap-2">
                                <Lock size={10} /> Classification
                            </div>
                            <div className={`font-mono transition-colors duration-500 ${activeLayer.color}`}>{activeLayer.stats.type} Security Domain</div>
                        </div>
                    </div>

                    {/* Footer with ID */}
                    <div className="flex items-center justify-between pt-6 border-t border-white/5 relative z-10">
                        <div className="text-[10px] font-mono text-gray-600">
                            ID: LAYER_0{activeLayer.level}_V1.0
                        </div>
                        <div className={`flex items-center gap-2 text-xs font-bold uppercase ${activeLayer.color}`}>
                            <div className={`w-2 h-2 rounded-full ${activeLayer.bg} animate-pulse`}></div>
                            <span>Online</span>
                        </div>
                    </div>

                    {/* Ambient Glow Background */}
                    <div className={`absolute -right-20 -bottom-20 w-64 h-64 ${activeLayer.bg} opacity-10 blur-[80px] pointer-events-none transition-all duration-1000`}></div>

                    {/* Scanline Overlay */}
                    <div className="absolute inset-0 pointer-events-none opacity-5 bg-[linear-gradient(transparent_50%,_rgba(0,0,0,1)_50%)] bg-[length:100%_4px]"></div>
                </div>
            </div>

        </div>
    );
};
