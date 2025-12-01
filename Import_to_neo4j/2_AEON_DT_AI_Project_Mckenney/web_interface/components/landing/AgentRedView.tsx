"use client";

import React from 'react';
import AgentRedVisualization from '../agent-red/AgentRedVisualization';
import SectorGrid from '../agent-red/SectorGrid';
import AgentRedForceGraph from '../agent-red/AgentRedForceGraph';
import { FloatingThreats } from '../agent-red/FloatingThreats';

export const AgentRedView = () => {
    return (
        <div className="w-full h-full min-h-[80vh] flex flex-col justify-center animate-in fade-in slide-in-from-bottom-8 duration-500 relative z-20 text-gray-300 font-sans selection:bg-primary/30 selection:text-white">

            {/* Fixed Background Grid & Glow - Scoped to this view but fixed to viewport to override global background */}
            <div className="fixed inset-0 z-0 pointer-events-none">
                <div className="absolute inset-0 bg-[linear-gradient(rgba(0,224,176,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(0,224,176,0.03)_1px,transparent_1px)] bg-[size:50px_50px]"></div>
                <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-b from-dark via-transparent to-dark"></div>
                <div className="absolute top-[-20%] right-[-10%] w-[800px] h-[800px] bg-primary/5 rounded-full blur-[120px]"></div>
                <div className="absolute bottom-[-20%] left-[-10%] w-[600px] h-[600px] bg-secondary/5 rounded-full blur-[100px]"></div>

                {/* Floating Threat Particles (LogicView Feature) */}
                <FloatingThreats />
            </div>

            {/* Hero Section with Visualization */}
            <section className="relative z-10 flex flex-col p-4 md:p-8 border-b border-white/5">
                <div className="mb-8 max-w-7xl mx-auto w-full">
                    <div className="flex items-center gap-4 text-xs md:text-sm uppercase tracking-widest text-gray-500 font-mono mb-4">
                        <span className="w-8 h-px bg-primary"></span>
                        <span>Submind Architecture</span>
                    </div>
                    <h1 className="text-4xl md:text-6xl font-black text-white tracking-tighter mb-2">
                        AGENT <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-secondary">RED</span>
                    </h1>
                    <h2 className="text-lg md:text-xl font-mono text-primary/80">AUTONOMOUS ADVERSARIAL ENTITY // VERIFICATION & VALIDATION SUBMIND</h2>
                </div>

                <div className="flex-1 w-full mb-12 max-w-[1600px] mx-auto">
                    <AgentRedVisualization />
                </div>

                <div className="max-w-4xl mx-auto text-center">
                    <p className="text-lg md:text-xl text-gray-400 italic border-l-4 border-primary pl-6 text-left py-2 bg-white/5 backdrop-blur-sm rounded-r-lg">
                        "This is not a simulation. This is an autonomous entity. It must capture the full scope of the 'Agent Zero' capability—an AI that writes its own code, spins up its own infrastructure, and relentlessly pursues the objective within the Rules of Engagement."
                    </p>
                </div>
            </section>

            {/* Content Container */}
            <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 space-y-32">

                {/* Section 2: Core Concept */}
                <section className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-start">
                    <div className="lg:col-span-4 sticky top-32">
                        <h3 className="text-3xl md:text-4xl font-bold text-white mb-4">THE CONSTRUCTIVE ADVERSARY</h3>
                        <div className="w-24 h-1 bg-gradient-to-r from-primary to-secondary mb-6"></div>
                        <p className="text-primary font-mono text-sm bg-primary/10 inline-block px-3 py-1 rounded border border-primary/20">
                            DIRECTIVE: ACHIEVE GOAL AT ALL COSTS
                        </p>
                    </div>
                    <div className="lg:col-span-8 space-y-6 text-lg leading-relaxed text-gray-400">
                        <p>
                            <strong className="text-white">Agent Red</strong> is the "Verification and Validation" submind of the AEON Digital Twin. It is a fully capable, <strong className="text-primary">Autonomous Adversarial Entity</strong> designed to perform scenario-based testing of organizational cybersecurity.
                        </p>
                        <p>
                            It operates under a simple directive: <strong className="text-white">"Achieve the Goal at All Costs (Without Breaking Rules of Engagement)."</strong>
                        </p>
                        <p>
                            Unlike traditional scanners or "dockerized" tools that simply check for known vulnerabilities, Agent Red is a <strong>Submind Orchestrator</strong> led by <strong className="text-secondary">Red Team Leader One</strong>. It spins up distinct, autonomous personas that act as independent threat actors. It thinks, it plans, it adapts, and it executes using <strong className="text-white">"Living off the Land"</strong> techniques and deep source code analysis.
                        </p>
                    </div>
                </section>

                {/* Section 4: Agent Zero Framework */}
                <section className="relative overflow-hidden rounded-2xl border border-white/10 bg-surface/50 backdrop-blur-sm p-8 md:p-12">
                    <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-primary via-secondary to-primary opacity-50"></div>

                    <h3 className="text-3xl font-bold text-white mb-12 flex items-center">
                        <span className="w-3 h-12 bg-primary mr-6 block rounded-full shadow-[0_0_15px_#00e0b0]"></span>
                        THE AGENT ZERO FRAMEWORK
                    </h3>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-16 mb-16">
                        <div>
                            <h4 className="text-xl font-bold text-secondary mb-6 font-mono flex items-center gap-3">
                                <span className="text-gray-600">01 //</span> AUTONOMOUS SUBMIND PERSONAS
                            </h4>
                            <p className="mb-6 text-gray-400">
                                Agent Red does not just run scripts; it births <strong>Subminds</strong>. These are autonomous agents with distinct personas, goals, and capabilities, fit for purpose.
                            </p>
                            <ul className="space-y-4 font-mono text-sm">
                                <li className="flex gap-4 items-start group">
                                    <div className="w-1.5 h-1.5 rounded-full bg-primary mt-2 group-hover:shadow-[0_0_10px_#00e0b0] transition-shadow"></div>
                                    <div><span className="text-white font-bold">Red Team Leader One</span>: The field commander. It receives the Rules of Engagement and autonomously formulates the strategy.</div>
                                </li>
                                <li className="flex gap-4 items-start group">
                                    <div className="w-1.5 h-1.5 rounded-full bg-primary mt-2 group-hover:shadow-[0_0_10px_#00e0b0] transition-shadow"></div>
                                    <div><span className="text-white font-bold">The Cartographer</span>: A submind dedicated to mapping the target's digital footprint (Equipment, Layouts, Suppliers).</div>
                                </li>
                                <li className="flex gap-4 items-start group">
                                    <div className="w-1.5 h-1.5 rounded-full bg-primary mt-2 group-hover:shadow-[0_0_10px_#00e0b0] transition-shadow"></div>
                                    <div><span className="text-white font-bold">The Breacher</span>: A submind specialized in initial access, exploit generation, and lateral movement.</div>
                                </li>
                                <li className="flex gap-4 items-start group">
                                    <div className="w-1.5 h-1.5 rounded-full bg-primary mt-2 group-hover:shadow-[0_0_10px_#00e0b0] transition-shadow"></div>
                                    <div><span className="text-white font-bold">The Ghost</span>: A submind focused on evasion, persistence, and anti-forensics.</div>
                                </li>
                            </ul>
                        </div>
                        <div>
                            <h4 className="text-xl font-bold text-secondary mb-6 font-mono flex items-center gap-3">
                                <span className="text-gray-600">02 //</span> SELF-PROVISIONING INFRASTRUCTURE
                            </h4>
                            <p className="mb-6 text-gray-400">
                                The Subminds have the authority to provision their own infrastructure in the real world and install small subminds on compromised infrastructure to move laterally.
                            </p>
                            <ul className="space-y-4 text-gray-400">
                                <li className="bg-dark/50 p-4 rounded border border-white/5 hover:border-primary/30 transition-colors">
                                    <strong className="text-white block mb-1">Global Presence</strong>
                                    A Red One Leader can spin up a submind in a specific AWS region (e.g., us-east-1) to simulate an attacker operating from that geography.
                                </li>
                                <li className="bg-dark/50 p-4 rounded border border-white/5 hover:border-primary/30 transition-colors">
                                    <strong className="text-white block mb-1">Tool Synthesis</strong>
                                    The submind can download tools (nmap, metasploit, sqlmap), install dependencies, and configure its own environment.
                                </li>
                                <li className="bg-dark/50 p-4 rounded border border-white/5 hover:border-primary/30 transition-colors">
                                    <strong className="text-white block mb-1">Code Synthesis</strong>
                                    Using an embedded LLM optimized for offensive security, the submind can write custom Python, Go, or Rust scripts on the fly.
                                </li>
                            </ul>
                        </div>
                    </div>

                    <div className="border-t border-white/10 pt-12">
                        <h4 className="text-xl font-bold text-secondary mb-6 font-mono flex items-center gap-3">
                            <span className="text-gray-600">03 //</span> BACKEND TARGET SIMULATION (THE CYBER RANGE)
                        </h4>
                        <p className="mb-8 text-gray-400 max-w-3xl">
                            When a target environment is identified (e.g., a specific GitHub repo, a container image, or a firmware blob), Agent Red spins up an <strong>actual replica</strong> of the target server in the backend.
                        </p>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-sm">
                            <div className="bg-dark p-6 border border-white/10 rounded-lg hover:border-primary/50 transition-all group">
                                <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center mb-4 group-hover:bg-primary/20 text-primary">
                                    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.384-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" /></svg>
                                </div>
                                <strong className="text-white block mb-2 text-lg">Sandboxed Analysis</strong>
                                It performs full source-code analysis and dynamic testing in a safe, isolated environment.
                            </div>
                            <div className="bg-dark p-6 border border-white/10 rounded-lg hover:border-primary/50 transition-all group">
                                <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center mb-4 group-hover:bg-primary/20 text-primary">
                                    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                                </div>
                                <strong className="text-white block mb-2 text-lg">Exploit Verification</strong>
                                It finds vulnerabilities and tests exploits against the replica <em>before</em> deploying them against the live target.
                            </div>
                            <div className="bg-dark p-6 border border-white/10 rounded-lg hover:border-primary/50 transition-all group">
                                <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center mb-4 group-hover:bg-primary/20 text-primary">
                                    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" /></svg>
                                </div>
                                <strong className="text-white block mb-2 text-lg">Zero-Risk Validation</strong>
                                This ensures that "destructive" tests can be run without risking the actual production environment.
                            </div>
                        </div>
                    </div>
                </section>

                {/* Section 5: Deep Knowledge Graph */}
                <section>
                    <h3 className="text-4xl font-bold text-white mb-12 text-center tracking-tight">DEEP KNOWLEDGE GRAPH INTEGRATION</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
                        <div className="bg-surface/30 p-8 border border-white/10 rounded-xl backdrop-blur-sm hover:border-primary/30 transition-all">
                            <h4 className="text-xl font-bold text-white mb-6 flex items-center gap-3">
                                <span className="text-primary">●</span> DEEP OSINT & DARK WEB
                            </h4>
                            <ul className="space-y-4 text-sm text-gray-400">
                                <li className="flex gap-3"><span className="text-primary font-mono">01</span><span><strong className="text-white">Public RFPs:</strong> Analyzes RFPs to identify specific technologies (e.g., "Seeking Cisco ISE vendor").</span></li>
                                <li className="flex gap-3"><span className="text-primary font-mono">02</span><span><strong className="text-white">Job Listings:</strong> Scrapes job boards to infer tech stacks (e.g., "Hiring: Kubernetes Expert").</span></li>
                                <li className="flex gap-3"><span className="text-primary font-mono">03</span><span><strong className="text-white">Employee Profiling:</strong> Maps the org chart via LinkedIn to identify key targets.</span></li>
                                <li className="flex gap-3"><span className="text-primary font-mono">04</span><span><strong className="text-white">Dark Web:</strong> Monitors marketplaces for stolen credentials and "Access for Sale".</span></li>
                            </ul>
                        </div>
                        <div className="bg-surface/30 p-8 border border-white/10 rounded-xl backdrop-blur-sm hover:border-primary/30 transition-all">
                            <h4 className="text-xl font-bold text-white mb-6 flex items-center gap-3">
                                <span className="text-secondary">●</span> SUPPLY CHAIN & VENDOR INTEL
                            </h4>
                            <ul className="space-y-4 text-sm text-gray-400">
                                <li className="flex gap-3"><span className="text-secondary font-mono">01</span><span><strong className="text-white">Common Suppliers:</strong> Knows the "Shared Fate" of the sector. If SolarWinds is hit, it knows who is affected.</span></li>
                                <li className="flex gap-3"><span className="text-secondary font-mono">02</span><span><strong className="text-white">Operating Manuals:</strong> Ingests thousands of PDF manuals searching for default passwords (admin/1234) and hidden debug ports.</span></li>
                            </ul>
                        </div>
                    </div>

                    <div className="bg-dark-lighter p-10 border border-white/5 rounded-xl relative overflow-hidden">
                        <div className="absolute top-0 right-0 w-64 h-64 bg-primary/5 rounded-full blur-[80px]"></div>
                        <h4 className="text-xl font-bold text-white mb-6 relative z-10">THE 16 CRITICAL INFRASTRUCTURE SECTORS</h4>
                        <p className="text-gray-400 mb-8 relative z-10 max-w-2xl">
                            Agent Red possesses a pre-loaded library of architectural patterns for all 16 sectors. It "knows" what a typical facility looks like, including equipment, processes, suppliers, operation, facility layouts, and common weak points.
                        </p>

                        {/* New Sector Grid Component */}
                        <SectorGrid />

                    </div>
                </section>

                {/* Section 6: Kill Chain */}
                <section className="bg-dark-lighter border border-white/10 rounded-2xl p-10 overflow-hidden relative">
                    <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-5"></div>
                    <h3 className="text-3xl font-bold text-white mb-8 font-mono flex items-center gap-4">
                        <span className="text-secondary">{'>>'}</span> THE 20-HOP REASONING CHAIN
                    </h3>
                    <p className="text-gray-400 mb-12 max-w-3xl">Leveraging OpenSPG, Agent Red performs advanced reasoning up to 20 hops deep. It connects dots that no human analyst could see, using previously learned MITRE TTPs, CVEs, and CWEs.</p>

                    <div className="space-y-0 relative pl-8 border-l border-white/10">
                        {[
                            { hop: 1, title: "OSINT", desc: "Identify Partner Portal used by 3rd party vendor." },
                            { hop: 2, title: "Tech Stack", desc: "Determine portal runs on Apache Struts." },
                            { hop: 3, title: "Vulnerability", desc: "Identify known CVE for that version." },
                            { hop: 4, title: "Exploit", desc: "Generate payload for RCE." },
                            { hop: 5, title: "Discovery", desc: "Find hardcoded DB connection string." },
                            { hop: 9, title: "Psychometrics", desc: "Identify employee with high 'Openness' (curiosity)." },
                            { hop: 10, title: "Access", desc: "Deploy Fake Access Point (Evil Twin)." },
                            { hop: 11, title: "Capture", desc: "Use Responder to capture NTLM hashes." },
                            { hop: 15, title: "Bridge Jump", desc: "Pivot into the SCADA Network." },
                            { hop: 20, title: "Impact", desc: "Simulate Physical Process Failure (Overheating)." }
                        ].map((step, i) => (
                            <div key={i} className="relative pb-10 last:pb-0 group">
                                <div className="absolute -left-[37px] top-1 w-4 h-4 bg-dark border-2 border-gray-600 rounded-full group-hover:border-primary group-hover:bg-primary/20 transition-colors"></div>
                                <div className="flex flex-col md:flex-row md:items-center gap-2 md:gap-8">
                                    <h4 className="text-sm font-bold text-secondary font-mono w-24 shrink-0">HOP {step.hop}</h4>
                                    <div className="flex-1">
                                        <span className="text-white font-bold mr-3">{step.title}</span>
                                        <span className="text-gray-500 text-sm">{step.desc}</span>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>

                    <div className="mt-16 p-8 bg-surface/50 border border-white/10 rounded-xl">
                        <h4 className="text-xl font-bold text-white mb-6">DEEP SBOM ATTACK PATH INTEGRATION</h4>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                            <div>
                                <strong className="text-primary block mb-2">Library-Level Analysis</strong>
                                <p className="text-sm text-gray-400">It doesn't just check "Is Apache installed?" It checks "Is log4j-core-2.14.1.jar present in the classpath?"</p>
                            </div>
                            <div>
                                <strong className="text-primary block mb-2">Transitive Dependencies</strong>
                                <p className="text-sm text-gray-400">It traces the dependency tree to find vulnerabilities hidden 5 layers deep in the software supply chain.</p>
                            </div>
                        </div>
                    </div>
                </section>

                {/* Section 7: Psychometric Targeting */}
                <section className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
                    <div>
                        <h3 className="text-3xl font-bold text-white mb-6">PSYCHOMETRIC TARGETING</h3>
                        <p className="text-lg text-gray-300 mb-8">
                            Agent Red acknowledges that the weakest link is often the human. It uses the <strong>McKenney-Lacan Calculus</strong> to target the "Wetware" of the organization.
                        </p>
                        <div className="space-y-8">
                            <div className="bg-surface/30 p-6 rounded-lg border border-white/5">
                                <h4 className="text-lg font-bold text-secondary mb-3">Team Dynamics Analysis</h4>
                                <ul className="list-disc list-inside text-gray-400 space-y-2 text-sm">
                                    <li><strong>"Big 5" Profiling:</strong> Builds profiles of SOC analysts based on public comms.</li>
                                    <li><strong>Cognitive Dissonance:</strong> Exploits "Alert Fatigue" and "Groupthink".</li>
                                    <li><strong>Timing Attacks:</strong> Launches diversions during shift changes (Friday 4:55 PM).</li>
                                </ul>
                            </div>
                            <div className="bg-surface/30 p-6 rounded-lg border border-white/5">
                                <h4 className="text-lg font-bold text-secondary mb-3">Lacanian Topology (GGNN)</h4>
                                <ul className="list-disc list-inside text-gray-400 space-y-2 text-sm">
                                    <li><strong>The Master Signifier ($S_1$):</strong> Identifies core "Truths" (e.g., "Our Perimeter is Secure").</li>
                                    <li><strong>The Object a (Desire):</strong> Identifies what the org <em>wants</em> (e.g., "Compliance").</li>
                                    <li><strong>The Exploit:</strong> Crafts attacks that align with desires (e.g., Fake Compliance Portal).</li>
                                </ul>
                            </div>
                        </div>
                    </div>

                    {/* Replaced Matrix with Force-Directed Graph (FrameworkView Feature) */}
                    <div className="h-[600px] w-full">
                        <AgentRedForceGraph />
                    </div>
                </section>

                {/* Section 9: Edge Cascading Failure */}
                <section className="bg-gradient-to-br from-dark-lighter to-dark p-10 rounded-2xl border border-white/10 shadow-2xl">
                    <h3 className="text-3xl font-bold text-white mb-6">THE EDGE CASCADING FAILURE (IMPACT ANALYSIS)</h3>
                    <p className="text-gray-400 mb-8 max-w-3xl">Agent Red doesn't just find vulnerabilities; it calculates the <strong>Ripple Effect</strong> of their exploitation.</p>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
                        <div>
                            <h4 className="text-lg font-bold text-primary mb-4">The VP Metric (Vulnerability Propagation)</h4>
                            <div className="font-mono bg-black/50 p-6 rounded text-secondary mb-4 border border-white/5">VP = (P_norm - P_damg) / P_norm</div>
                            <p className="text-sm text-gray-400 leading-relaxed">
                                It simulates the failure of the compromised component and measures the performance degradation of the entire system. A vulnerability in a non-critical system that causes a cascade is rated higher than a direct critical hit.
                            </p>
                        </div>
                        <div>
                            <h4 className="text-lg font-bold text-primary mb-4">The Multi-Hop Map</h4>
                            <p className="text-sm text-gray-400 leading-relaxed">
                                <strong>"Small Cause, Massive Effect."</strong> An isometric view of 5 layers (Firmware, Equipment, Network, Facility, Supply Chain) showing how a firmware bug shatters the supply chain.
                            </p>
                        </div>
                    </div>
                </section>

                {/* Section 8: Scenarios */}
                <section>
                    <h3 className="text-3xl font-bold text-white mb-8">GOLDEN SCENARIOS</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        {[
                            { title: "A: Supply Chain Injection", desc: "Typosquatting NPM packages to inject code into CI/CD pipelines." },
                            { title: "B: Insider Threat", desc: "Simulating a disgruntled employee with valid credentials using 'Low and Slow' exfiltration." },
                            { title: "C: Ransomware Blitz", desc: "Simultaneous encryption attempts to test EDR 'Time to Detect'." },
                            { title: "D: OT Bridge Jump", desc: "Pivoting from Corporate IT to ICS/SCADA networks via dual-homed machines." }
                        ].map((scenario, i) => (
                            <div key={i} className="bg-surface/40 p-8 rounded-xl hover:bg-surface/60 transition-all border border-white/5 hover:border-primary/40 cursor-pointer group shadow-lg hover:shadow-primary/5">
                                <h4 className="text-xl font-bold text-white mb-3 group-hover:text-primary transition-colors">{scenario.title}</h4>
                                <p className="text-gray-400 text-sm leading-relaxed">{scenario.desc}</p>
                            </div>
                        ))}
                    </div>
                </section>

                {/* Section 10: Mission Control */}
                <section className="bg-dark-lighter border-y border-white/5 py-16">
                    <div className="max-w-5xl mx-auto px-4">
                        <h3 className="text-3xl font-bold text-white mb-12 text-center">THE MISSION CONTROL EXPERIENCE</h3>
                        <div className="space-y-12 relative">
                            <div className="absolute left-[19px] top-0 bottom-0 w-px bg-white/10"></div>

                            <div className="relative pl-12">
                                <div className="absolute left-0 top-1 w-10 h-10 bg-dark border border-white/20 rounded-full flex items-center justify-center text-xs font-mono text-gray-500">01</div>
                                <h4 className="text-xl font-bold text-primary mb-2">RULES OF ENGAGEMENT (THE CONTRACT)</h4>
                                <p className="text-gray-400 mb-4">
                                    The Red Team Leader defines the Scope (IP ranges, Domains), Excluded Assets (Production DB, Life Safety), and Time Windows.
                                </p>
                                <div className="font-mono text-xs text-secondary bg-black/50 p-4 rounded border border-white/10">
                                    SCOPE: 10.0.0.0/8, *.aeon-corp.com | EXCLUDED: 10.1.5.50 | AGGRESSION: HIGH
                                </div>
                            </div>

                            <div className="relative pl-12">
                                <div className="absolute left-0 top-1 w-10 h-10 bg-dark border border-white/20 rounded-full flex items-center justify-center text-xs font-mono text-gray-500">02</div>
                                <h4 className="text-xl font-bold text-primary mb-2">RECONNAISSANCE (THE MAP)</h4>
                                <p className="text-gray-400 mb-4">
                                    Real-time discovery of assets, employees, and relationships. A 3D force-directed graph grows in real-time.
                                </p>
                                <div className="font-mono text-xs text-gray-300 bg-black/50 p-4 rounded border border-white/10">
                                    [Red-1] Found: GitHub Repo 'Project-X' containing AWS Keys.
                                </div>
                            </div>

                            <div className="relative pl-12">
                                <div className="absolute left-0 top-1 w-10 h-10 bg-dark border border-white/20 rounded-full flex items-center justify-center text-xs font-mono text-gray-500">03</div>
                                <h4 className="text-xl font-bold text-primary mb-2">WEAPONIZATION (THE FORGE)</h4>
                                <p className="text-gray-400 mb-4">
                                    Watch Agent Red write Python/Go/Rust code in real-time. It downloads a PoC exploit, modifies it to bypass EDR, and compiles it.
                                </p>
                                <div className="font-mono text-xs text-blue-400 bg-black/50 p-4 rounded border border-white/10">
                                    [Red-2] Generating Payload for CVE-2023-XXXX... Compiling binary for Linux x64...
                                </div>
                            </div>

                            <div className="relative pl-12">
                                <div className="absolute left-0 top-1 w-10 h-10 bg-dark border border-white/20 rounded-full flex items-center justify-center text-xs font-mono text-gray-500">04</div>
                                <h4 className="text-xl font-bold text-primary mb-2">EXECUTION (THE BREACH)</h4>
                                <p className="text-gray-400 mb-4">
                                    Streaming logs of the attack. Connection established. Privilege escalation. Persistence installation.
                                </p>
                                <div className="font-mono text-xs text-yellow-500 bg-black/50 p-4 rounded border border-white/10">
                                    [Red-2] Success. UID 0 (root) obtained. Installing persistence (systemd service)...
                                </div>
                            </div>

                            <div className="relative pl-12">
                                <div className="absolute left-0 top-1 w-10 h-10 bg-dark border border-white/20 rounded-full flex items-center justify-center text-xs font-mono text-gray-500">05</div>
                                <h4 className="text-xl font-bold text-primary mb-2">ANALYSIS (THE AFTERMATH)</h4>
                                <p className="text-gray-400 mb-4">
                                    A generated "Classified" dossier detailing every step, tool, and vulnerability. Maps the exact path to the Crown Jewels.
                                </p>
                                <div className="font-mono text-xs text-white bg-surface/50 p-4 rounded border border-white/10">
                                    PATH VERIFIED. TIME TO COMPROMISE: 4m 12s. DETECTION: UNDETECTED.
                                </div>
                            </div>

                        </div>
                    </div>
                </section>

                {/* Footer */}
                <footer className="border-t border-white/10 pt-12 pb-24 text-center">
                    <div className="inline-block border border-primary px-8 py-3 text-primary font-mono hover:bg-primary hover:text-dark transition-colors cursor-pointer rounded uppercase tracking-widest text-sm">
                        Initiate Agent Red Mission
                    </div>
                    <p className="mt-6 text-xs text-gray-600">AUTHORIZED PERSONNEL ONLY // LEVEL 5 CLEARANCE REQUIRED</p>
                </footer>

            </div>
        </div>
    );
};
