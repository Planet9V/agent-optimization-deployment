import React, { useState } from 'react';
import { ViewState, SimulationParams } from './types';
import { RefreshCw, Activity, Sliders, Server, ChevronDown, ChevronUp, Settings2 } from 'lucide-react';

interface CalculusPanelProps {
    params: SimulationParams;
    setParams: React.Dispatch<React.SetStateAction<SimulationParams>>;
    onReset: () => void;
}

export const CalculusPanel: React.FC<CalculusPanelProps> = ({ params, setParams, onReset }) => {
    const [isOpen, setIsOpen] = useState(true);

    const handleChange = (key: keyof SimulationParams, value: number) => {
        setParams(prev => ({ ...prev, [key]: value }));
    };

    return (
        <aside className="fixed bottom-0 right-0 z-40 w-full md:w-auto flex flex-col items-end pointer-events-none p-4 md:p-8 gap-3 transition-all duration-500">

            {/* Toggle / Status Bar */}
            <div className="pointer-events-auto flex items-center gap-2">
                {!isOpen && (
                    <div className="bg-dark/90 border border-primary/30 px-4 py-2 text-[10px] text-primary font-mono uppercase flex items-center gap-2 tracking-widest backdrop-blur-md animate-in fade-in slide-in-from-right-8 shadow-[0_0_15px_rgba(0,224,176,0.1)] rounded-sm">
                        <span className="w-1.5 h-1.5 rounded-full bg-primary animate-pulse"></span>
                        Systems Nominal
                    </div>
                )}

                <button
                    onClick={() => setIsOpen(!isOpen)}
                    className={`pointer - events - auto bg - dark / 90 border border - gray - 700 hover: border - primary / 50 p - 2 text - primary backdrop - blur - md transition - all duration - 300 shadow - lg rounded - sm group ${!isOpen ? 'bg-primary/10 border-primary/30' : ''} `}
                    title={isOpen ? "Retract Controls" : "Expand Controls"}
                >
                    {isOpen ? (
                        <ChevronDown size={18} className="group-hover:translate-y-0.5 transition-transform" />
                    ) : (
                        <Settings2 size={18} className="animate-[spin_4s_linear_infinite]" />
                    )}
                </button>
            </div>

            {/* Main Panel Container */}
            <div className={`
pointer - events - auto
w - full md: w - [420px]
bg - dark / 95 backdrop - blur - xl border border - gray - 800
shadow - [0_0_50px_rgba(0, 0, 0, 0.8)] 
          relative overflow - hidden clip - path - polygon
transition - all duration - 500 ease - [cubic - bezier(0.34, 1.56, 0.64, 1)] origin - bottom - right
          ${isOpen ? 'opacity-100 translate-x-0 translate-y-0 scale-100' : 'opacity-0 translate-x-8 translate-y-8 scale-95 pointer-events-none h-0'}
`}>
                {/* Top Tech Border */}
                <div className="h-1 w-full bg-gradient-to-r from-primary/20 via-primary to-primary/20"></div>

                <div className="p-6 space-y-6">

                    {/* Header */}
                    <div className="flex justify-between items-center border-b border-gray-800 pb-4">
                        <div className="flex items-center gap-3 text-white">
                            <div className="p-1.5 bg-primary/10 border border-primary/30 rounded-sm">
                                <Sliders size={14} className="text-primary" />
                            </div>
                            <h3 className="text-sm font-bold uppercase tracking-widest font-mono">
                                Psychohistory Controls
                            </h3>
                        </div>
                        <button
                            onClick={onReset}
                            className="flex items-center gap-2 text-[10px] uppercase text-gray-500 hover:text-primary transition-colors group border border-transparent hover:border-primary/30 px-2 py-1 rounded"
                        >
                            <RefreshCw size={12} className="group-hover:rotate-180 transition-transform duration-500" />
                            <span>Reset Params</span>
                        </button>
                    </div>

                    {/* Live Equation Visualizer */}
                    <div className="bg-black border border-gray-800 p-4 font-mono relative overflow-hidden group">
                        <div className="absolute top-0 right-0 p-1">
                            <div className="flex gap-1">
                                <span className="w-1 h-1 bg-red-500 animate-pulse"></span>
                                <span className="w-1 h-1 bg-yellow-500 animate-pulse delay-75"></span>
                                <span className="w-1 h-1 bg-green-500 animate-pulse delay-150"></span>
                            </div>
                        </div>
                        <div className="text-[10px] text-gray-500 mb-1">DIFFERENTIAL ENGINE</div>
                        <div className="flex items-center justify-center gap-3 text-xs md:text-sm py-2">
                            <span className="text-gray-400 italic">d</span>
                            <span className="text-primary font-bold text-lg">Ψ</span>
                            <span className="text-gray-400 italic">/dt</span>
                            <span className="mx-1 text-gray-600">=</span>
                            <span className="text-secondary">∇</span>
                            <span>(S - μ)</span>
                            <span className="mx-1 text-gray-600">+</span>
                            <span className="text-white font-bold">Q</span>
                            <span className="align-super text-[8px] text-primary">k</span>
                        </div>
                        {/* Scanline */}
                        <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-b from-transparent via-white/5 to-transparent opacity-0 group-hover:opacity-100 animate-scan pointer-events-none"></div>
                    </div>

                    {/* Sliders Grid */}
                    <div className="grid grid-cols-1 gap-5 font-mono">
                        {/* Social Inertia */}
                        <div className="space-y-2">
                            <div className="flex justify-between text-[10px] text-gray-400">
                                <label className="flex items-center gap-2 uppercase tracking-wider">
                                    <div className="w-1.5 h-1.5 bg-primary rotate-45"></div>
                                    Social Inertia (Mass)
                                </label>
                                <span className="text-primary font-bold">{params.socialInertia.toFixed(2)}</span>
                            </div>
                            <div className="relative h-4 flex items-center">
                                <div className="absolute w-full h-0.5 bg-gray-800"></div>
                                <input
                                    type="range"
                                    min="0"
                                    max="1"
                                    step="0.01"
                                    value={params.socialInertia}
                                    onChange={(e) => handleChange('socialInertia', parseFloat(e.target.value))}
                                    className="w-full z-10 opacity-0 cursor-pointer h-full"
                                />
                                {/* Custom Thumb Track Visual */}
                                <div className="absolute h-1 bg-primary pointer-events-none transition-all duration-100" style={{ width: `${params.socialInertia * 100}% ` }}></div>
                                <div className="absolute w-3 h-3 bg-black border-2 border-primary pointer-events-none transition-all duration-100 transform -translate-x-1/2" style={{ left: `${params.socialInertia * 100}% ` }}></div>
                            </div>
                        </div>

                        {/* System Entropy */}
                        <div className="space-y-2">
                            <div className="flex justify-between text-[10px] text-gray-400">
                                <label className="flex items-center gap-2 uppercase tracking-wider">
                                    <div className="w-1.5 h-1.5 bg-red-500 rotate-45"></div>
                                    System Entropy (Chaos)
                                </label>
                                <span className="text-red-400 font-bold">{params.systemEntropy.toFixed(2)}</span>
                            </div>
                            <div className="relative h-4 flex items-center">
                                <div className="absolute w-full h-0.5 bg-gray-800"></div>
                                <input
                                    type="range"
                                    min="0"
                                    max="1"
                                    step="0.01"
                                    value={params.systemEntropy}
                                    onChange={(e) => handleChange('systemEntropy', parseFloat(e.target.value))}
                                    className="w-full z-10 opacity-0 cursor-pointer h-full"
                                />
                                <div className="absolute h-1 bg-red-500 pointer-events-none transition-all duration-100" style={{ width: `${params.systemEntropy * 100}% ` }}></div>
                                <div className="absolute w-3 h-3 bg-black border-2 border-red-500 pointer-events-none transition-all duration-100 transform -translate-x-1/2" style={{ left: `${params.systemEntropy * 100}% ` }}></div>
                            </div>
                        </div>

                        {/* Cultural Viscosity */}
                        <div className="space-y-2">
                            <div className="flex justify-between text-[10px] text-gray-400">
                                <label className="flex items-center gap-2 uppercase tracking-wider">
                                    <div className="w-1.5 h-1.5 bg-secondary rotate-45"></div>
                                    Cultural Viscosity
                                </label>
                                <span className="text-secondary font-bold">{params.culturalViscosity.toFixed(2)}</span>
                            </div>
                            <div className="relative h-4 flex items-center">
                                <div className="absolute w-full h-0.5 bg-gray-800"></div>
                                <input
                                    type="range"
                                    min="0"
                                    max="1"
                                    step="0.01"
                                    value={params.culturalViscosity}
                                    onChange={(e) => handleChange('culturalViscosity', parseFloat(e.target.value))}
                                    className="w-full z-10 opacity-0 cursor-pointer h-full"
                                />
                                <div className="absolute h-1 bg-secondary pointer-events-none transition-all duration-100" style={{ width: `${params.culturalViscosity * 100}% ` }}></div>
                                <div className="absolute w-3 h-3 bg-black border-2 border-secondary pointer-events-none transition-all duration-100 transform -translate-x-1/2" style={{ left: `${params.culturalViscosity * 100}% ` }}></div>
                            </div>
                        </div>

                        {/* Adaptation Rate */}
                        <div className="space-y-2">
                            <div className="flex justify-between text-[10px] text-gray-400">
                                <label className="flex items-center gap-2 uppercase tracking-wider">
                                    <div className="w-1.5 h-1.5 bg-yellow-500 rotate-45"></div>
                                    Adaptation Rate
                                </label>
                                <span className="text-yellow-400 font-bold">{params.adaptationRate.toFixed(0)}%</span>
                            </div>
                            <div className="relative h-4 flex items-center">
                                <div className="absolute w-full h-0.5 bg-gray-800"></div>
                                <input
                                    type="range"
                                    min="1"
                                    max="100"
                                    step="1"
                                    value={params.adaptationRate}
                                    onChange={(e) => handleChange('adaptationRate', parseFloat(e.target.value))}
                                    className="w-full z-10 opacity-0 cursor-pointer h-full"
                                />
                                <div className="absolute h-1 bg-yellow-500 pointer-events-none transition-all duration-100" style={{ width: `${params.adaptationRate}% ` }}></div>
                                <div className="absolute w-3 h-3 bg-black border-2 border-yellow-500 pointer-events-none transition-all duration-100 transform -translate-x-1/2" style={{ left: `${params.adaptationRate}% ` }}></div>
                            </div>
                        </div>

                    </div>

                    {/* Footer Status */}
                    <div className="flex justify-between items-center pt-4 border-t border-gray-800 text-[10px] font-mono text-gray-500">
                        <div className="flex items-center gap-2">
                            <Server size={12} className="text-gray-600" />
                            <span>HOST: <span className="text-gray-300">US-EAST-2A</span></span>
                        </div>
                        <div className="flex items-center gap-1">
                            <div className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse"></div>
                            <span className="text-green-500">ONLINE</span>
                        </div>
                    </div>
                </div>
            </div>
        </aside>
    );
};
