"use client";

import React, { useState, useEffect } from 'react';

interface LogEntry {
    message: string;
    timestamp: string;
}

const AgentRedVisualization = () => {
    const [logs, setLogs] = useState<LogEntry[]>([]);
    const [code, setCode] = useState("");

    useEffect(() => {
        const logStream = [
            "[Red One Leader] Initializing Global Swarm Protocol...",
            "[Red One Leader] Spawning Submind 'Cartographer-Alpha' in AWS us-east-1...",
            "[Cartographer] Mapping digital footprint of target 'Aeon Corp'...",
            "[Cartographer] Found: 142 exposed assets. 3 Critical.",
            "[Red One Leader] Spawning Submind 'Breacher-9' for target 10.1.1.5...",
            "[Breacher-9] Synthesizing custom exploit for CVE-2024-XXXX...",
            "[Breacher-9] Compiling payload for MIPS architecture...",
            "[Breacher-9] Launching 'Zero-Day' variant...",
            "[Target] Connection established.",
            "[Breacher-9] Escalating privileges to Root...",
            "[Red One Leader] Spawning Submind 'Ghost-7' for persistence...",
            "[Ghost-7] Installing kernel-level rootkit...",
            "[Ghost-7] Cleaning logs. Anti-forensics active.",
            "[Red One Leader] Mission Objective Achieved. Awaiting orders."
        ];

        let logIndex = 0;
        const logInterval = setInterval(() => {
            if (logIndex < logStream.length) {
                const message = logStream[logIndex];
                if (message) {
                    setLogs(prev => [...prev.slice(-10), {
                        message,
                        timestamp: new Date().toLocaleTimeString()
                    }]);
                }
                logIndex++;
            } else {
                logIndex = 0;
                setLogs([]);
            }
        }, 1500);

        const codeSnippet = `
# SUBMIND: BREACHER-9
# DIRECTIVE: AUTONOMOUS EXPLOIT GENERATION
# TARGET_ARCH: MIPS_BE

class ExploitGenerator:
    def __init__(self, target):
        self.target = target
        self.llm = AgentZeroLLM()

    def synthesize(self):
        vuln = self.scan_sbom(self.target)
        payload = self.llm.generate_payload(vuln)
        return self.compile(payload)

# EXECUTING SYNTHESIS...
    `;

        let charIndex = 0;
        const codeInterval = setInterval(() => {
            if (charIndex < codeSnippet.length) {
                setCode(prev => prev + codeSnippet[charIndex]);
                charIndex++;
            } else {
                charIndex = 0;
                setCode("");
            }
        }, 50);

        return () => {
            clearInterval(logInterval);
            clearInterval(codeInterval);
        };
    }, []);

    return (
        <div className="w-full h-[80vh] bg-dark/80 backdrop-blur-md text-primary font-mono p-6 grid grid-cols-12 grid-rows-6 gap-6 border border-white/10 rounded-xl shadow-[0_0_40px_rgba(0,224,176,0.1)] relative overflow-hidden">

            {/* Background Grid Effect */}
            <div className="absolute inset-0 pointer-events-none opacity-20 bg-[linear-gradient(rgba(0,224,176,0.1)_1px,transparent_1px),linear-gradient(90deg,rgba(0,224,176,0.1)_1px,transparent_1px)] bg-[size:20px_20px]"></div>

            {/* Header / Status Bar */}
            <div className="col-span-12 row-span-1 flex justify-between items-center border-b border-white/10 px-4 bg-white/5 rounded-t-lg relative z-10">
                <div className="flex items-center gap-3">
                    <div className="w-3 h-3 bg-primary rounded-full animate-pulse shadow-[0_0_10px_#00e0b0]"></div>
                    <h1 className="text-xl font-bold tracking-widest text-white">AGENT RED // SUBMIND ORCHESTRATOR</h1>
                </div>
                <div className="flex gap-8 text-xs font-bold text-gray-400">
                    <span className="flex items-center gap-2"><span className="text-primary">STATUS:</span> AUTONOMOUS</span>
                    <span className="flex items-center gap-2"><span className="text-secondary">ACTIVE SUBMINDS:</span> 142</span>
                    <span className="flex items-center gap-2"><span className="text-white">GLOBAL REACH:</span> 100%</span>
                </div>
            </div>

            {/* The Globe (Placeholder) */}
            <div className="col-span-4 row-span-3 border border-white/10 relative overflow-hidden bg-black/40 rounded-lg group hover:border-primary/30 transition-colors">
                <div className="absolute inset-0 flex items-center justify-center">
                    <div className="w-48 h-48 rounded-full border border-primary/30 animate-[spin_10s_linear_infinite] opacity-50 shadow-[0_0_30px_rgba(0,224,176,0.2)]"></div>
                    <div className="w-64 h-64 rounded-full border border-secondary/20 absolute animate-[spin_15s_linear_infinite_reverse] opacity-30"></div>
                    <div className="absolute text-center z-10">
                        <div className="text-4xl font-bold text-white tracking-tighter">GLOBAL</div>
                        <div className="text-xs text-primary tracking-widest">SWARM VIEW</div>
                    </div>
                </div>
                {/* Mock Agents */}
                <div className="absolute top-1/4 left-1/4 w-2 h-2 bg-primary rounded-full animate-ping shadow-[0_0_10px_#00e0b0]"></div>
                <div className="absolute bottom-1/3 right-1/3 w-2 h-2 bg-secondary rounded-full animate-ping delay-75 shadow-[0_0_10px_#00aaff]"></div>
                <div className="absolute top-1/2 right-1/4 w-2 h-2 bg-white rounded-full animate-ping delay-150"></div>
            </div>

            {/* The Code Forge */}
            <div className="col-span-4 row-span-3 border border-white/10 bg-black/60 p-4 overflow-hidden rounded-lg hover:border-primary/30 transition-colors relative">
                <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-primary to-transparent opacity-50"></div>
                <div className="text-xs text-gray-500 mb-3 border-b border-white/5 pb-2 flex justify-between">
                    <span>{`>>`} SUBMIND_SYNTHESIS_ENGINE.py</span>
                    <span className="text-primary animate-pulse">● LIVE</span>
                </div>
                <pre className="text-xs text-primary/90 whitespace-pre-wrap font-mono leading-tight">
                    {code}
                    <span className="animate-pulse bg-primary text-black ml-1"> </span>
                </pre>
            </div>

            {/* The Kill Chain */}
            <div className="col-span-4 row-span-5 border border-white/10 p-4 flex flex-col gap-3 bg-white/5 rounded-lg">
                <h3 className="text-xs font-bold border-b border-white/10 pb-2 text-gray-400 tracking-wider">KILL CHAIN PROGRESS</h3>
                {['RECONNAISSANCE', 'WEAPONIZATION', 'DELIVERY', 'EXPLOITATION', 'INSTALLATION', 'C2', 'ACTIONS'].map((step, i) => (
                    <div key={step} className="flex items-center gap-3 group">
                        <div className={`w-1 h-full transition-all duration-300 ${i < 4 ? 'bg-primary shadow-[0_0_10px_#00e0b0]' : 'bg-gray-800'}`}></div>
                        <div className={`flex-1 p-2 border border-white/5 rounded text-xs transition-all duration-300 ${i < 4 ? 'bg-primary/10 text-white border-primary/30' : 'text-gray-600'}`}>
                            {step}
                        </div>
                    </div>
                ))}
            </div>

            {/* The Terminal Logs */}
            <div className="col-span-8 row-span-2 border border-white/10 bg-black/80 p-4 overflow-hidden font-mono text-sm rounded-lg hover:border-primary/30 transition-colors">
                <div className="text-xs text-gray-500 mb-2 flex items-center gap-2">
                    <span className="text-secondary">{'>>'}</span> SUBMIND_LOGS
                </div>
                <div className="flex flex-col justify-end h-full space-y-1">
                    {logs.map((log, i) => (
                        <div key={i} className="text-gray-300 hover:text-white transition-colors flex gap-3 border-l-2 border-transparent hover:border-primary pl-2">
                            <span className="text-gray-600 text-xs whitespace-nowrap">[{log.timestamp}]</span>
                            <span className={log.message.includes("Red One Leader") ? "text-primary font-bold" : log.message.includes("Submind") ? "text-secondary" : "text-gray-400"}>
                                {log.message}
                            </span>
                        </div>
                    ))}
                </div>
            </div>

        </div>
    );
};

export default AgentRedVisualization;
