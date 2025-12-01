'use client';

import React, { useState, useEffect } from 'react';
import { Navigation } from './Navigation';
import { CalculusPanel } from './CalculusPanel';
import { SimulationGraph } from './SimulationGraph';
import { Architecture } from './Architecture';
import { LogicView } from './LogicView';
import { FrameworkView } from './FrameworkView';
import { TimelineView } from './TimelineView';
import { BackgroundEffect } from './BackgroundEffect';
import { PsychoHistorySphere } from './PsychoHistorySphere';
import { AgentRedView } from './AgentRedView';
import { ViewState, SimulationParams } from './types';
import { ArrowUpRight } from 'lucide-react';
import Link from 'next/link';

// Define types locally if not yet migrated
// import { ViewState, SimulationParams } from './types'; 
// For now, let's assume we copy types.ts to components/landing/types.ts or similar.
// But wait, the original import was from './types'. I should copy types.ts too.

const DEFAULT_PARAMS: SimulationParams = {
    socialInertia: 0.75,
    systemEntropy: 0.42,
    culturalViscosity: 0.89,
    adaptationRate: 45
};

export default function LandingPage() {
    const [currentView, setCurrentView] = useState<ViewState>(ViewState.CONTEXT);
    const [simParams, setSimParams] = useState<SimulationParams>(DEFAULT_PARAMS);
    const [mounted, setMounted] = useState(false);

    useEffect(() => {
        setMounted(true);
    }, []);

    const handleReset = () => {
        setSimParams(DEFAULT_PARAMS);
    };

    if (!mounted) return null;

    return (
        <div className="relative w-full min-h-screen flex flex-col items-center overflow-hidden bg-dark selection:bg-primary/30 selection:text-white font-sans">

            {/* Layer 0: Complex Calculus & Algorithms Background */}
            <BackgroundEffect />

            {/* Layer 1: Interactive PsychoHistory Sphere */}
            <div className={`fixed inset-0 pointer-events-none z-0 overflow-hidden flex items-center justify-center transition-all duration-1000 ease-in-out ${currentView === ViewState.CONTEXT
                ? 'opacity-100 scale-100 translate-y-0'
                : 'opacity-10 scale-150 translate-y-32 blur-sm'
                }`}>
                <div className={`transition-all duration-1000 ease-in-out pointer-events-auto ${currentView === ViewState.CONTEXT
                    ? 'w-[22rem] h-[22rem] md:w-[40rem] md:h-[40rem]'
                    : 'w-[50rem] h-[50rem]'
                    }`}>
                    <PsychoHistorySphere />
                </div>
            </div>

            <Navigation currentView={currentView} onNavigate={setCurrentView} />

            {/* Dashboard Link (New Addition) */}
            <div className="fixed top-6 right-6 z-50">
                <Link href="/dashboard" className="modern-button flex items-center gap-2">
                    <span>Enter System</span>
                    <ArrowUpRight className="w-4 h-4" />
                </Link>
            </div>

            <main className="flex-grow w-full z-10 pt-24 md:pt-32 px-4 md:px-8 pb-32 flex flex-col justify-center">

                {/* VIEW: CONTEXT (Hero) */}
                {currentView === ViewState.CONTEXT && (
                    <div className="max-w-7xl mx-auto w-full relative animate-in fade-in slide-in-from-bottom-8 duration-700 min-h-[60vh] flex flex-col justify-center">
                        <div className="mb-8 pl-1">
                            <div className="flex items-center gap-4 text-xs md:text-sm uppercase tracking-widest text-gray-500 font-mono">
                                <span className="w-8 h-px bg-primary"></span>
                                <span>Owner: Jim McKenney</span>
                            </div>
                        </div>

                        <h2 className="text-5xl md:text-7xl lg:text-9xl font-bold uppercase tracking-tighter leading-none text-white mix-blend-screen relative z-10">
                            Predictive Threat
                        </h2>
                        <h2 className="text-5xl md:text-7xl lg:text-9xl font-bold uppercase tracking-tighter leading-none mb-12 relative z-10">
                            <span className="text-gradient-cyber">Intelligence</span>
                        </h2>

                        <div className="flex flex-col md:flex-row justify-between items-start gap-12 border-t border-gray-800 pt-8 relative z-10 bg-dark/30 backdrop-blur-sm p-4 rounded-sm border border-white/5">
                            <p className="max-w-xl text-lg md:text-xl text-gray-400 leading-relaxed font-light">
                                "Predictive threat intelligence combining technical vulnerabilities, human psychology, organizational culture, and geopolitical context."
                            </p>

                            <div className="grid grid-cols-2 gap-x-12 gap-y-4 text-xs uppercase tracking-wider text-gray-500 font-mono">
                                <div className="flex flex-col gap-1">
                                    <span>Horizon</span>
                                    <span className="text-white text-base">90 Days</span>
                                </div>
                                <div className="flex flex-col gap-1">
                                    <span>Model</span>
                                    <span className="text-white text-base">Neural Physics</span>
                                </div>
                                <div className="flex flex-col gap-1">
                                    <span>Status</span>
                                    <span className="text-primary text-base">Active</span>
                                </div>
                                <div className="flex flex-col gap-1">
                                    <span>Confidence</span>
                                    <span className="text-white text-base">89.4%</span>
                                </div>
                            </div>
                        </div>

                        {/* Interactive Nodes Overlay */}
                        <div className="absolute inset-0 pointer-events-none hidden lg:block">
                            {/* Node 1: Technical Vulnerabilities -> CALCULUS */}
                            <button
                                onClick={() => setCurrentView(ViewState.CALCULUS)}
                                className="absolute top-[20%] right-[15%] group pointer-events-auto focus:outline-none"
                                aria-label="Explore Technical Vulnerabilities"
                            >
                                <div className="relative flex items-center justify-end gap-4">
                                    <div className="opacity-0 group-hover:opacity-100 transition-all duration-300 -translate-x-4 group-hover:translate-x-0 flex flex-col items-end">
                                        <div className="bg-dark/90 border border-primary/50 p-4 backdrop-blur-md shadow-[0_0_30px_rgba(0,224,176,0.15)]">
                                            <h4 className="text-primary font-bold text-sm font-mono uppercase mb-1 text-right">Technical Vulnerabilities</h4>
                                            <p className="text-[10px] text-gray-400 font-mono max-w-[180px] text-right leading-tight">
                                                Real-time CVE & exploit data streams integrated into the calculus.
                                            </p>
                                        </div>
                                        {/* Connector Line */}
                                        <div className="h-px w-8 bg-primary/50 mt-[-1px] mr-[-32px] opacity-0 group-hover:opacity-100 transition-opacity delay-100"></div>
                                    </div>

                                    <div className="relative transition-transform duration-300 group-hover:scale-125 group-active:scale-95">
                                        {/* Inner Pulse on Hover */}
                                        <div className="absolute inset-0 -m-1 border border-primary/60 rounded-full opacity-0 group-hover:opacity-100 group-hover:animate-ping"></div>
                                        <div className="w-3 h-3 bg-primary rounded-full shadow-[0_0_20px_#00e0b0] group-hover:shadow-[0_0_40px_#00e0b0] transition-shadow duration-300 animate-pulse"></div>
                                        <div className="absolute inset-0 w-3 h-3 border border-primary rounded-full animate-ping opacity-40"></div>
                                        <div className="absolute inset-0 -m-2 border border-dashed border-primary/30 rounded-full w-7 h-7 animate-spin-slow opacity-0 group-hover:opacity-100 transition-opacity"></div>
                                    </div>
                                </div>
                            </button>

                            {/* Node 2: Human Psychology -> LOGIC */}
                            <button
                                onClick={() => setCurrentView(ViewState.LOGIC)}
                                className="absolute top-[50%] right-[25%] group pointer-events-auto focus:outline-none"
                                aria-label="Explore Human Psychology"
                            >
                                <div className="relative flex items-center gap-4">
                                    <div className="relative transition-transform duration-300 group-hover:scale-125 group-active:scale-[1.4]">
                                        <div className="w-3 h-3 bg-secondary rounded-full shadow-[0_0_20px_#00aaff] group-hover:shadow-[0_0_40px_#00aaff] transition-shadow duration-300 animate-pulse"></div>
                                        <div className="absolute inset-0 w-3 h-3 border border-secondary rounded-full animate-ping opacity-40"></div>
                                        <div className="absolute inset-0 -m-2 border border-dashed border-secondary/30 rounded-full w-7 h-7 animate-spin-slow opacity-0 group-hover:opacity-100 transition-opacity"></div>
                                    </div>

                                    <div className="opacity-0 group-hover:opacity-100 transition-all duration-300 translate-x-4 group-hover:translate-x-0 flex flex-col items-start">
                                        <div className="h-px w-8 bg-secondary/50 mb-[-1px] ml-[-32px] opacity-0 group-hover:opacity-100 transition-opacity delay-100"></div>
                                        <div className="bg-dark/90 border border-secondary/50 p-4 backdrop-blur-md shadow-[0_0_30px_rgba(0,170,255,0.15)]">
                                            <h4 className="text-secondary font-bold text-sm font-mono uppercase mb-1">Human Psychology</h4>
                                            <p className="text-[10px] text-gray-400 font-mono max-w-[180px] leading-tight">
                                                Analysis of behavioral patterns and cognitive biases.
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            </button>

                            {/* Background Network Lines Connecting Nodes */}
                            <svg className="absolute inset-0 w-full h-full opacity-30 pointer-events-none">
                                <line x1="85%" y1="21%" x2="75%" y2="51%" stroke="currentColor" strokeWidth="1" strokeDasharray="4 4" className="text-gray-500 animate-dash animate-pulse" />
                                <circle cx="85%" cy="21%" r="2" fill="#00e0b0" className="opacity-50" />
                                <circle cx="75%" cy="51%" r="2" fill="#00aaff" className="opacity-50" />
                            </svg>
                        </div>
                    </div>
                )}

                {/* VIEW: ARCHITECTURE */}
                {currentView === ViewState.ARCHITECTURE && (
                    <div className="w-full h-full animate-in fade-in zoom-in-95 duration-500 relative z-20">
                        <Architecture onNavigate={setCurrentView} />
                    </div>
                )}

                {/* VIEW: CALCULUS */}
                {currentView === ViewState.CALCULUS && (
                    <div className="w-full h-full max-w-[1600px] mx-auto flex flex-col items-start gap-8 animate-in fade-in slide-in-from-right-8 duration-500 relative z-20">

                        {/* Wide Main Visualization */}
                        <div className="w-full pr-0 lg:pr-[440px] transition-all duration-500">
                            <SimulationGraph params={simParams} />
                        </div>

                        {/* The Calculus Panel is position: fixed on the right, so we leave padding for it in the layout */}
                    </div>
                )}

                {/* VIEW: LOGIC */}
                {currentView === ViewState.LOGIC && (
                    <div className="w-full h-full min-h-[60vh] flex flex-col justify-center animate-in fade-in slide-in-from-bottom-8 duration-500 relative z-20">
                        <LogicView />
                    </div>
                )}

                {/* VIEW: FRAMEWORK */}
                {currentView === ViewState.FRAMEWORK && (
                    <div className="w-full h-full min-h-[80vh] flex flex-col justify-center animate-in fade-in slide-in-from-bottom-8 duration-500 relative z-20">
                        <FrameworkView />
                    </div>
                )}

                {/* VIEW: TIMELINE (NEW) */}
                {currentView === ViewState.TIMELINE && (
                    <div className="w-full h-full min-h-[80vh] flex flex-col justify-center animate-in fade-in zoom-in duration-1000 relative z-20">
                        <TimelineView />
                    </div>
                )}

                {/* VIEW: AGENT RED (NEW) */}
                {currentView === ViewState.AGENT_RED && (
                    <div className="w-full h-full min-h-[80vh] flex flex-col justify-center animate-in fade-in slide-in-from-bottom-8 duration-500 relative z-20">
                        <AgentRedView />
                    </div>
                )}

            </main>

            {/* Global Elements */}
            <CalculusPanel
                params={simParams}
                setParams={setSimParams}
                onReset={handleReset}
            />
        </div>
    );
};
