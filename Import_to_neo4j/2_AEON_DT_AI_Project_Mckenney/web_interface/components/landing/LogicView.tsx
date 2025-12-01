
import React, { useState, useEffect, useRef } from 'react';
import { Activity, Cpu, Eye } from 'lucide-react';

const SOCIOLOGICAL_CONCEPTS = [
  { text: "Confirmation Bias", type: "BIAS" },
  { text: "Openness", type: "BIG5" },
  { text: "Dominance", type: "DISC" },
  { text: "Normalcy Bias", type: "BIAS" },
  { text: "Neuroticism", type: "BIG5" },
  { text: "Compliance", type: "DISC" },
  { text: "Groupthink", type: "SOC" },
  { text: "Authority Bias", type: "BIAS" },
  { text: "Anchoring", type: "BIAS" },
  { text: "Conscientiousness", type: "BIG5" },
  { text: "Influence", type: "DISC" },
  { text: "Sunk Cost", type: "BIAS" },
  { text: "Agreeableness", type: "BIG5" },
  { text: "Mimetic Desire", type: "SOC" },
  { text: "Steadiness", type: "DISC" }
];

export const LogicView: React.FC = () => {
  const [hoveredRing, setHoveredRing] = useState<'real' | 'symbolic' | 'imaginary' | 'center' | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  
  // Refs for particle animation updates
  const particlesRef = useRef(SOCIOLOGICAL_CONCEPTS.map(() => ({
    x: 0, 
    y: 0, 
    vx: (Math.random() - 0.5) * 0.2,
    vy: (Math.random() - 0.5) * 0.2,
    angle: Math.random() * Math.PI * 2,
    orbitRadius: 120 + Math.random() * 180,
    speed: 0.001 + Math.random() * 0.003,
    phase: Math.random() * Math.PI * 2
  })));

  useEffect(() => {
    let animationFrame: number;
    let time = 0;

    const animate = () => {
      time += 0.01;
      
      // 1. Update Particles (Floating Concepts)
      particlesRef.current.forEach((p, i) => {
        // Complex Orbit Logic
        p.angle += p.speed;
        
        // Lissajous-style variation for organic movement
        const r = p.orbitRadius + Math.sin(time + p.phase) * 20;
        
        // Calculate target position relative to center
        const targetX = Math.cos(p.angle) * r;
        const targetY = Math.sin(p.angle * 0.8) * (r * 0.8); // Slightly elliptical

        // Smoothly interpolate current pos to orbit pos (Soft follow)
        p.x += (targetX - p.x) * 0.05;
        p.y += (targetY - p.y) * 0.05;

        // Update DOM Element directly for performance
        const el = document.getElementById(`concept-${i}`);
        if (el) {
            // Add some floaty noise
            const noiseX = Math.sin(time * 2 + p.phase) * 5;
            const noiseY = Math.cos(time * 1.5 + p.phase) * 5;
            el.style.transform = `translate(${p.x + noiseX}px, ${p.y + noiseY}px)`;
            el.style.opacity = `${0.2 + Math.sin(time + p.phase) * 0.15}`; // Breathing opacity
        }
      });

      // 2. Calculate Topological Distortion (The Ring Jitter)
      // The "swarm" of concepts exerts a pull on the structure
      let pullX = 0;
      let pullY = 0;
      particlesRef.current.forEach(p => {
          pullX += p.x * 0.0005; // Scale down influence
          pullY += p.y * 0.0005;
      });

      if (containerRef.current) {
          // We update CSS variables that the rings use in their transform
          // Adding noise (Math.sin) to simulate the "flexing" described
          const noiseRealX = Math.sin(time * 1.2) * 3 + pullX * -1;
          const noiseRealY = Math.cos(time * 1.1) * 3 + pullY * -1;
          
          const noiseSymX = Math.cos(time * 0.9) * 3 + pullX;
          const noiseSymY = Math.sin(time * 0.8) * 3 + pullY;
          
          const noiseImgX = Math.sin(time * 1.5) * 3 + pullX * 0.5;
          const noiseImgY = Math.cos(time * 1.4) * 3 + pullY * 0.5;

          containerRef.current.style.setProperty('--jitter-real-x', `${noiseRealX.toFixed(2)}px`);
          containerRef.current.style.setProperty('--jitter-real-y', `${noiseRealY.toFixed(2)}px`);
          
          containerRef.current.style.setProperty('--jitter-sym-x', `${noiseSymX.toFixed(2)}px`);
          containerRef.current.style.setProperty('--jitter-sym-y', `${noiseSymY.toFixed(2)}px`);
          
          containerRef.current.style.setProperty('--jitter-img-x', `${noiseImgX.toFixed(2)}px`);
          containerRef.current.style.setProperty('--jitter-img-y', `${noiseImgY.toFixed(2)}px`);
      }

      animationFrame = requestAnimationFrame(animate);
    };

    animationFrame = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(animationFrame);
  }, []);

  return (
    <div ref={containerRef} className="w-full h-full flex flex-col lg:flex-row items-center justify-center relative overflow-hidden p-4 lg:p-12">
      
      {/* Abstract Background Elements */}
      <div className="absolute top-20 left-20 w-64 h-64 bg-primary/5 rounded-full blur-3xl animate-pulse"></div>
      <div className="absolute bottom-20 right-20 w-96 h-96 bg-secondary/5 rounded-full blur-3xl animate-pulse delay-700"></div>

      {/* Floating Sociological Concepts Layer */}
      <div className="absolute inset-0 pointer-events-none flex items-center justify-center z-0">
          {SOCIOLOGICAL_CONCEPTS.map((concept, i) => (
              <div 
                key={i} 
                id={`concept-${i}`}
                className={`absolute text-[10px] font-mono whitespace-nowrap transition-colors duration-1000
                    ${concept.type === 'BIAS' ? 'text-red-300/40' : 
                      concept.type === 'BIG5' ? 'text-blue-300/40' : 
                      concept.type === 'DISC' ? 'text-yellow-300/40' : 'text-purple-300/40'}
                `}
                style={{ willChange: 'transform, opacity' }}
              >
                  {concept.text}
              </div>
          ))}
      </div>

      {/* Main Visual: The Borromean Knot of Cyber-Psychology */}
      <div className="relative z-10 w-full max-w-5xl grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
        
        {/* Left Column: The Abstract Visualization */}
        <div className="relative h-[400px] lg:h-[500px] flex items-center justify-center perspective-1000">
          
          {/* The Rings Container */}
          <div className="relative w-[300px] h-[300px] md:w-[400px] md:h-[400px]">
            
            {/* THE SYMBOLIC (Code/Structure) */}
            <div 
               className={`absolute top-0 left-1/2 w-48 h-48 md:w-64 md:h-64 border-2 rounded-full transition-all duration-500 ease-out 
               ${hoveredRing === 'symbolic' ? 'scale-110 border-primary shadow-[0_0_30px_rgba(0,224,176,0.3)] z-20 bg-black/80' : 
                 hoveredRing === 'center' ? 'scale-105 border-primary/80 shadow-[0_0_15px_rgba(0,224,176,0.2)] z-20 bg-black/40' : 
                 'border-primary/40 z-10 bg-black/10'}
               ${hoveredRing && hoveredRing !== 'symbolic' && hoveredRing !== 'center' ? 'opacity-20 blur-sm' : 'opacity-100'}
               `}
               style={{ 
                   transform: `translate(calc(-50% + var(--jitter-sym-x, 0px)), var(--jitter-sym-y, 0px))` 
               }}
               onMouseEnter={() => setHoveredRing('symbolic')}
               onMouseLeave={() => setHoveredRing(null)}
            >
               <div className="absolute inset-0 flex items-center justify-center">
                  <Cpu className={`text-primary transition-all duration-500 ${hoveredRing === 'symbolic' || hoveredRing === 'center' ? 'opacity-100 scale-100' : 'opacity-0 scale-50'}`} size={48} strokeWidth={1} />
               </div>
               <span className="absolute -top-8 left-1/2 -translate-x-1/2 text-primary font-mono text-xs tracking-[0.2em] uppercase">The Symbolic</span>
            </div>

            {/* THE IMAGINARY (Fear/Image) */}
            <div 
               className={`absolute bottom-0 right-0 w-48 h-48 md:w-64 md:h-64 border-2 rounded-full transition-all duration-500 ease-out
               ${hoveredRing === 'imaginary' ? 'scale-110 border-purple-500 shadow-[0_0_30px_rgba(168,85,247,0.3)] z-20 bg-black/80' : 
                 hoveredRing === 'center' ? 'scale-105 border-purple-500/80 shadow-[0_0_15px_rgba(168,85,247,0.2)] z-20 bg-black/40' : 
                 'border-purple-500/40 z-10 bg-black/10'}
               ${hoveredRing && hoveredRing !== 'imaginary' && hoveredRing !== 'center' ? 'opacity-20 blur-sm' : 'opacity-100'}
               `}
               style={{ 
                   transform: hoveredRing === 'center' 
                    ? 'translate(calc(-8% + var(--jitter-img-x, 0px)), calc(-8% + var(--jitter-img-y, 0px))) scale(1.05)' 
                    : 'translate(calc(-10% + var(--jitter-img-x, 0px)), calc(-10% + var(--jitter-img-y, 0px)))' 
               }}
               onMouseEnter={() => setHoveredRing('imaginary')}
               onMouseLeave={() => setHoveredRing(null)}
            >
                <div className="absolute inset-0 flex items-center justify-center">
                  <Eye className={`text-purple-500 transition-all duration-500 ${hoveredRing === 'imaginary' || hoveredRing === 'center' ? 'opacity-100 scale-100' : 'opacity-0 scale-50'}`} size={48} strokeWidth={1} />
               </div>
               <span className="absolute -bottom-8 right-1/2 translate-x-1/2 text-purple-500 font-mono text-xs tracking-[0.2em] uppercase">The Imaginary</span>
            </div>

            {/* THE REAL (Trauma/Hard Kernel) */}
            <div 
               className={`absolute bottom-0 left-0 w-48 h-48 md:w-64 md:h-64 border-2 rounded-full transition-all duration-500 ease-out
               ${hoveredRing === 'real' ? 'scale-110 border-white shadow-[0_0_30px_rgba(255,255,255,0.3)] z-20 bg-black/80' : 
                 hoveredRing === 'center' ? 'scale-105 border-white/80 shadow-[0_0_15px_rgba(255,255,255,0.2)] z-20 bg-black/40' : 
                 'border-white/40 z-10 bg-black/10'}
               ${hoveredRing && hoveredRing !== 'real' && hoveredRing !== 'center' ? 'opacity-20 blur-sm' : 'opacity-100'}
               `}
               style={{ 
                   transform: hoveredRing === 'center' 
                   ? 'translate(calc(8% + var(--jitter-real-x, 0px)), calc(-8% + var(--jitter-real-y, 0px))) scale(1.05)' 
                   : 'translate(calc(10% + var(--jitter-real-x, 0px)), calc(-10% + var(--jitter-real-y, 0px)))' 
               }}
               onMouseEnter={() => setHoveredRing('real')}
               onMouseLeave={() => setHoveredRing(null)}
            >
                <div className="absolute inset-0 flex items-center justify-center">
                  <Activity className={`text-white transition-all duration-500 ${hoveredRing === 'real' || hoveredRing === 'center' ? 'opacity-100 scale-100' : 'opacity-0 scale-50'}`} size={48} strokeWidth={1} />
               </div>
               <span className="absolute -bottom-8 left-1/2 -translate-x-1/2 text-white font-mono text-xs tracking-[0.2em] uppercase">The Real</span>
            </div>

            {/* Central Intersection - The Object a */}
            <div 
                className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-24 h-24 z-30 cursor-pointer group"
                onMouseEnter={() => setHoveredRing('center')}
                onMouseLeave={() => setHoveredRing(null)}
            >
                <div className={`absolute inset-0 rounded-full bg-gradient-to-tr from-transparent via-white/20 to-transparent blur-md transition-all duration-500 ${hoveredRing === 'center' ? 'scale-150 opacity-100' : 'scale-100 opacity-50'}`}></div>
                <div className={`absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-2 h-2 bg-white rounded-full animate-ping ${hoveredRing === 'center' ? 'opacity-100' : 'opacity-0'}`}></div>
            </div>
          </div>
        </div>

        {/* Right Column: The Logic Text */}
        <div className="relative z-20 space-y-12 text-left pl-0 lg:pl-8">
          
          {/* Header */}
          <div>
            <h2 className="text-4xl md:text-5xl font-bold text-white uppercase tracking-tighter mb-2">
              Lacanian <br/>
              <span className="text-gradient">Topography</span>
            </h2>
            <p className="text-gray-500 font-mono text-sm max-w-md border-l-2 border-primary/30 pl-4">
              Mapping the dissonance between organizational perception and cybersecurity reality.
            </p>
          </div>

          {/* Interactive Content Area based on Hover */}
          <div className="min-h-[240px] relative">
            
            {/* DEFAULT / INTRO / CENTER VIEW */}
            <div className={`absolute inset-0 transition-all duration-500 ${hoveredRing && hoveredRing !== 'center' ? 'opacity-0 translate-x-8 pointer-events-none' : 'opacity-100 translate-x-0'}`}>
               <div className="space-y-8">
                  <div className="flex gap-4 items-start group">
                    <div className="mt-1 p-2 border border-gray-800 bg-surface/50 rounded-sm group-hover:border-primary/50 transition-colors">
                        <Activity size={20} className="text-gray-400 group-hover:text-primary" />
                    </div>
                    <div>
                        <h4 className="text-white font-bold uppercase text-sm tracking-wider">The Disconnect</h4>
                        <p className="text-gray-400 text-sm mt-1 leading-relaxed max-w-md">
                            Organizations allocate 80% of budgets to <span className="text-purple-400">Imaginary</span> fears (APTs) while ignoring <span className="text-white">Real</span> threats (Patching).
                        </p>
                    </div>
                  </div>
                  
                   <div className="bg-gradient-to-r from-primary/10 to-transparent border border-primary/20 p-6 flex justify-between items-center cursor-pointer group backdrop-blur-sm">
                        <div>
                            <h4 className="text-primary font-bold font-mono text-xs uppercase tracking-widest mb-1">Projection ROI</h4>
                            <p className="text-[10px] text-gray-400">Preventive intervention vs Breach cost</p>
                        </div>
                        <div className="text-4xl font-black text-white font-mono group-hover:scale-110 transition-transform">150x</div>
                    </div>
               </div>
            </div>

            {/* SYMBOLIC VIEW */}
            <div className={`absolute inset-0 transition-all duration-500 ${hoveredRing === 'symbolic' ? 'opacity-100 translate-x-0' : 'opacity-0 translate-x-8 pointer-events-none'}`}>
                <div className="border-l-2 border-primary pl-6 space-y-4">
                    <h3 className="text-2xl font-bold text-primary uppercase tracking-widest">The Symbolic</h3>
                    <div className="text-xs font-mono text-gray-500 uppercase tracking-widest">The Official Narrative</div>
                    <p className="text-2xl font-light text-white italic">
                        "We have Zero Trust Architecture."
                    </p>
                    <p className="text-gray-400 text-sm leading-relaxed">
                        The language, protocols, and compliance structures an organization uses to maintain order. It is often disconnected from operational reality.
                    </p>
                </div>
            </div>

            {/* IMAGINARY VIEW */}
            <div className={`absolute inset-0 transition-all duration-500 ${hoveredRing === 'imaginary' ? 'opacity-100 translate-x-0' : 'opacity-0 translate-x-8 pointer-events-none'}`}>
                <div className="border-l-2 border-purple-500 pl-6 space-y-4">
                    <h3 className="text-2xl font-bold text-purple-500 uppercase tracking-widest">The Imaginary</h3>
                    <div className="text-xs font-mono text-gray-500 uppercase tracking-widest">The Feared Phantom</div>
                    <p className="text-2xl font-light text-white italic">
                        "Nation-State APTs."
                    </p>
                    <div className="flex items-center gap-4 mt-2">
                         <div className="bg-purple-500/10 border border-purple-500/30 px-3 py-1">
                            <span className="text-[10px] text-purple-300 uppercase">Perceived Risk: 9.8/10</span>
                         </div>
                         <div className="bg-gray-800 border border-gray-700 px-3 py-1">
                            <span className="text-[10px] text-gray-400 uppercase">Actual Risk: 3.2/10</span>
                         </div>
                    </div>
                    <p className="text-gray-400 text-sm leading-relaxed mt-2">
                        The domain of ego and image. Organizations obsess over sophisticated enemies to validate their own importance, ignoring mundane threats.
                    </p>
                </div>
            </div>

            {/* REAL VIEW */}
            <div className={`absolute inset-0 transition-all duration-500 ${hoveredRing === 'real' ? 'opacity-100 translate-x-0' : 'opacity-0 translate-x-8 pointer-events-none'}`}>
                 <div className="border-l-2 border-white pl-6 space-y-4">
                    <h3 className="text-2xl font-bold text-white uppercase tracking-widest">The Real</h3>
                    <div className="text-xs font-mono text-gray-500 uppercase tracking-widest">The Traumatic Truth</div>
                    <p className="text-2xl font-light text-white italic">
                        "Ransomware & Unpatched Libraries."
                    </p>
                     <div className="flex items-center gap-4 mt-2">
                         <div className="bg-white/10 border border-white/30 px-3 py-1">
                            <span className="text-[10px] text-white uppercase">Actual Risk: 8.7/10</span>
                         </div>
                    </div>
                    <p className="text-gray-400 text-sm leading-relaxed mt-2">
                        That which resists symbolization. The unpatched vulnerability, the burnt-out employee, the entropy that cannot be talked away by compliance reports.
                    </p>
                </div>
            </div>

          </div>

        </div>

      </div>

    </div>
  );
};
