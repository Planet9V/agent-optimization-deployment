import React, { useEffect, useRef } from 'react';

const THREAT_CONCEPTS = [
    { text: "CVE-2024-3094", type: "CRITICAL" },
    { text: "Log4Shell", type: "CRITICAL" },
    { text: "SQL Injection", type: "VECTOR" },
    { text: "Zero-Day", type: "CRITICAL" },
    { text: "Privilege Escalation", type: "TACTIC" },
    { text: "RCE", type: "VECTOR" },
    { text: "XSS", type: "VECTOR" },
    { text: "Brute Force", type: "TACTIC" },
    { text: "Mimikatz", type: "TOOL" },
    { text: "Cobalt Strike", type: "TOOL" },
    { text: "EternalBlue", type: "CRITICAL" },
    { text: "Phishing", type: "VECTOR" },
    { text: "Lateral Movement", type: "TACTIC" },
    { text: "Data Exfiltration", type: "GOAL" },
    { text: "Ransomware", type: "PAYLOAD" }
];

export const FloatingThreats: React.FC = () => {
    // Refs for particle animation updates
    const particlesRef = useRef(THREAT_CONCEPTS.map(() => ({
        x: 0,
        y: 0,
        vx: (Math.random() - 0.5) * 0.2,
        vy: (Math.random() - 0.5) * 0.2,
        angle: Math.random() * Math.PI * 2,
        orbitRadius: 150 + Math.random() * 200,
        speed: 0.0005 + Math.random() * 0.002,
        phase: Math.random() * Math.PI * 2
    })));

    useEffect(() => {
        let animationFrame: number;
        let time = 0;

        const animate = () => {
            time += 0.01;

            particlesRef.current.forEach((p, i) => {
                // Complex Orbit Logic
                p.angle += p.speed;

                // Lissajous-style variation for organic movement
                const r = p.orbitRadius + Math.sin(time + p.phase) * 30;

                // Calculate target position relative to center (assuming center is 0,0 relative to container)
                // We'll translate this to screen coordinates in the render
                const targetX = Math.cos(p.angle) * r;
                const targetY = Math.sin(p.angle * 0.7) * (r * 0.7);

                // Smoothly interpolate
                p.x += (targetX - p.x) * 0.05;
                p.y += (targetY - p.y) * 0.05;

                // Update DOM Element directly for performance
                const el = document.getElementById(`threat-${i}`);
                if (el) {
                    const noiseX = Math.sin(time * 2 + p.phase) * 10;
                    const noiseY = Math.cos(time * 1.5 + p.phase) * 10;
                    el.style.transform = `translate(${p.x + noiseX}px, ${p.y + noiseY}px)`;
                    el.style.opacity = `${0.1 + Math.max(0, Math.sin(time + p.phase)) * 0.3}`; // Breathing opacity
                }
            });

            animationFrame = requestAnimationFrame(animate);
        };

        animationFrame = requestAnimationFrame(animate);
        return () => cancelAnimationFrame(animationFrame);
    }, []);

    return (
        <div className="absolute inset-0 pointer-events-none flex items-center justify-center overflow-hidden z-0">
            {THREAT_CONCEPTS.map((concept, i) => (
                <div
                    key={i}
                    id={`threat-${i}`}
                    className={`absolute text-[10px] font-mono whitespace-nowrap transition-colors duration-1000
                  ${concept.type === 'CRITICAL' ? 'text-red-500/40 font-bold' :
                            concept.type === 'VECTOR' ? 'text-primary/30' :
                                concept.type === 'TOOL' ? 'text-secondary/30' : 'text-gray-500/30'}
              `}
                    style={{ willChange: 'transform, opacity' }}
                >
                    {concept.text}
                </div>
            ))}
        </div>
    );
};
