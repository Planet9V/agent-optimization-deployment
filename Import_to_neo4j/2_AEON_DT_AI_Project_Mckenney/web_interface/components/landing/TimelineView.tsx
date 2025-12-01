
import React, { useEffect, useRef } from 'react';
import { Timer, Zap } from 'lucide-react';

/**
 * TIMELINE VIEW
 * 
 * This component renders a "4D Time Vortex".
 * It uses a raw Canvas 2D implementation of a 3D tunnel effect.
 * 
 * MATH EXPLAINED:
 * 1. World Space: Objects have x (angle), y (radius), z (depth).
 * 2. Projection: We convert (x, y, z) to (screenX, screenY) using perspective divide:
 *    scale = PERSPECTIVE / (PERSPECTIVE + z)
 * 
 * PERFORMANCE NOTE:
 * We use strict input sanitization (Number.isFinite) because division by zero
 * in the projection math can cause the Canvas rendering to crash.
 */

export const TimelineView: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const container = containerRef.current;
    if (!canvas || !container) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // --- CONFIGURATION ---
    // Initialize with safe defaults to prevent immediate NaN
    let width = canvas.width = container.clientWidth || window.innerWidth || 800;
    let height = canvas.height = container.clientHeight || window.innerHeight || 600;
    let cx = width / 2;
    let cy = height / 2;

    const SYMBOLS = ['0', '1', '∂', '∫', 'Ψ', '∑', '∇', '∆', 'λ', 'Ω', 'μ', '∅', '∞'];
    const YEARS = Array.from({ length: 50 }, (_, i) => 2010 + i); // 2010 to 2060
    
    const PERSPECTIVE = 300; // Lower = more extreme fisheye
    const NEAR_PLANE = -200; // Clip particles before they hit the camera (avoid divide by zero)
    const SPEED = 4; // Base travel speed
    const MAX_Z = 4000; // How far into the distance
    
    // --- STATE ---
    let frame = 0;
    const mouse = { x: 0, y: 0 };
    const camera = { x: 0, y: 0, rotation: 0 };

    // --- ENTITY DEFINITIONS ---

    // 1. The Tunnel Particles (The Walls of Time)
    interface Particle {
        x: number; // initial angle relative to center (we map polar to cartesian)
        y: number; // radius
        z: number;
        char: string;
        color: string;
        jitterSpeed: number;
    }
    
    const particles: Particle[] = [];
    const initParticles = () => {
        particles.length = 0;
        for(let i=0; i<800; i++) {
            particles.push({
                x: Math.random() * Math.PI * 2, // Angle
                y: 200 + Math.random() * 600,   // Radius from center tunnel
                z: Math.random() * MAX_Z,
                char: SYMBOLS[Math.floor(Math.random() * SYMBOLS.length)],
                color: Math.random() > 0.9 ? '#ef4444' : Math.random() > 0.5 ? '#00e0b0' : '#00aaff',
                jitterSpeed: Math.random() * 0.1
            });
        }
    };

    // 2. The Milestones (Years)
    interface Milestone {
        year: number;
        z: number;
        type: 'PAST' | 'PRESENT' | 'FUTURE';
        label: string;
    }
    
    const milestones: Milestone[] = [];
    const initMilestones = () => {
        milestones.length = 0;
        // Space them out every 500 units
        for(let i=0; i<YEARS.length; i++) {
            milestones.push({
                year: YEARS[i],
                z: i * 800 - 2000, // Start behind camera
                type: 'FUTURE',
                label: YEARS[i].toString()
            });
        }
    };

    // 3. The "Black Swans" (Anomalies)
    interface Anomaly {
        x: number; y: number; z: number;
        size: number;
        life: number;
    }
    const anomalies: Anomaly[] = [];

    // --- INITIALIZATION ---
    initParticles();
    initMilestones();

    const handleResize = () => {
        if (!container || !canvas) return;
        const newWidth = container.clientWidth;
        const newHeight = container.clientHeight;
        
        // Prevent setting 0 dimensions
        if (newWidth > 0 && newHeight > 0) {
            width = canvas.width = newWidth;
            height = canvas.height = newHeight;
            cx = width / 2;
            cy = height / 2;
        }
    };

    // Use ResizeObserver for robust dimension tracking
    const resizeObserver = new ResizeObserver(handleResize);
    resizeObserver.observe(container);

    const handleMouseMove = (e: MouseEvent) => {
        const rect = canvas.getBoundingClientRect();
        if (cx > 0 && cy > 0) {
            const rawX = (e.clientX - rect.left - cx) / cx;
            const rawY = (e.clientY - rect.top - cy) / cy;
            // Clamp values to prevent Infinity
            if (Number.isFinite(rawX) && Number.isFinite(rawY)) {
                mouse.x = rawX;
                mouse.y = rawY;
            }
        }
    };

    window.addEventListener('mousemove', handleMouseMove);

    // --- RENDER LOOP ---
    let animId: number;
    const animate = () => {
        // Safety Check: Don't render if dimensions are invalid or NaN
        if (width <= 0 || height <= 0 || cx <= 0 || cy <= 0 || !Number.isFinite(width) || !Number.isFinite(height)) {
             animId = requestAnimationFrame(animate);
             return;
        }

        frame++;
        
        // Camera Movement (Parallax based on mouse)
        // Double check finite values before logic
        const targetX = Number.isFinite(mouse.x) ? mouse.x * 200 : 0;
        const targetY = Number.isFinite(mouse.y) ? mouse.y * 200 : 0;
        
        if (Number.isFinite(targetX)) camera.x += (targetX - camera.x) * 0.05;
        if (Number.isFinite(targetY)) camera.y += (targetY - camera.y) * 0.05;
        camera.rotation += 0.002;

        // Clear Screen
        ctx.fillStyle = '#0a0a0a';
        ctx.fillRect(0,0, width, height);

        // Draw "Singularity" Glow at center
        const gradX = cx + camera.x * 0.5;
        const gradY = cy + camera.y * 0.5;
        const gradRadius = Math.max(0.1, width); // Ensure positive radius

        // STRICT CHECK for createRadialGradient
        // All parameters must be finite
        if (
            Number.isFinite(gradX) && 
            Number.isFinite(gradY) && 
            Number.isFinite(cx) && 
            Number.isFinite(cy) && 
            Number.isFinite(gradRadius) &&
            gradRadius >= 0
        ) {
            try {
                const gradient = ctx.createRadialGradient(gradX, gradY, 0, cx, cy, gradRadius);
                gradient.addColorStop(0, 'rgba(255, 255, 255, 0.1)');
                gradient.addColorStop(0.2, 'rgba(0, 224, 176, 0.05)');
                gradient.addColorStop(1, 'rgba(0,0,0,0)');
                ctx.fillStyle = gradient;
                ctx.fillRect(0,0, width, height);
            } catch (e) {
                // Silently fail gradient if browser complains
            }
        }

        // --- RENDER PARTICLES (TUNNEL) ---
        ctx.font = "12px 'Roboto Mono'";
        ctx.textAlign = "center";
        
        particles.forEach(p => {
            // Move forward
            p.z -= SPEED;
            
            // Respawn at back
            if (p.z < NEAR_PLANE) {
                p.z = MAX_Z;
                p.char = SYMBOLS[Math.floor(Math.random() * SYMBOLS.length)];
            }

            // 3D Projection Math
            const angle = p.x + camera.rotation + (p.z * 0.001); 
            
            const rx = Math.cos(angle) * p.y; // polar to cartesian
            const ry = Math.sin(angle) * p.y;

            // Clipping: Don't divide by zero or negative numbers close to 0
            const depth = PERSPECTIVE + p.z;
            if (depth < 1) return; // Clip

            const scale = PERSPECTIVE / depth;
            const x2d = (rx - camera.x) * scale + cx;
            const y2d = (ry - camera.y) * scale + cy;
            
            const alpha = Math.max(0, Math.min(1, (MAX_Z - p.z) / 1000)); 
            
            if (alpha > 0 && scale > 0 && Number.isFinite(x2d) && Number.isFinite(y2d)) {
                let color = p.color;
                if (p.z > 2000) color = '#ffffff';
                else if (p.z < 0) color = '#333333';
                
                ctx.fillStyle = color;
                ctx.globalAlpha = alpha * (p.z < 0 ? 0.2 : 1);
                
                const size = Math.max(0.5, 14 * scale);
                ctx.font = `${size}px 'Roboto Mono'`;
                ctx.fillText(p.char, x2d, y2d);
            }
        });

        // --- RENDER MILESTONES (YEARS) ---
        milestones.forEach(m => {
            m.z -= SPEED;
            
            if (m.z < NEAR_PLANE) {
                m.z = milestones.length * 800 + NEAR_PLANE; 
                m.type = 'FUTURE';
            }

            if (m.z < 100 && m.z > -100) m.type = 'PRESENT';
            else if (m.z < -100) m.type = 'PAST';
            else m.type = 'FUTURE';

            const depth = PERSPECTIVE + m.z;
            if (depth < 1) return;

            const scale = PERSPECTIVE / depth;
            const x2d = cx - camera.x * scale;
            const y2d = cy - camera.y * scale;

            if (scale > 0 && m.z < MAX_Z && Number.isFinite(x2d) && Number.isFinite(y2d)) {
                ctx.globalAlpha = Math.max(0, Math.min(1, (MAX_Z - m.z) / 1000));
                
                if (m.type === 'PRESENT') {
                    ctx.fillStyle = '#00e0b0';
                    ctx.font = `bold ${60 * scale}px 'Inter'`;
                    ctx.shadowColor = '#00e0b0';
                    ctx.shadowBlur = 20;
                    ctx.fillText(m.year.toString(), x2d, y2d);
                    
                    ctx.font = `${14 * scale}px 'Roboto Mono'`;
                    ctx.fillStyle = '#ffffff';
                    ctx.shadowBlur = 0;
                    ctx.fillText("CURRENT_EPOCH", x2d, y2d + 40 * scale);

                } else if (m.type === 'PAST') {
                    ctx.fillStyle = '#444';
                    ctx.font = `${40 * scale}px 'Inter'`;
                    ctx.shadowBlur = 0;
                    ctx.fillText(m.year.toString(), x2d, y2d);
                
                } else {
                    const isFar = m.z > 1500;
                    const txt = isFar && Math.random() > 0.8 ? (Math.floor(Math.random()*10000)).toString() : m.year.toString();
                    
                    ctx.fillStyle = isFar ? '#555' : '#fff';
                    ctx.font = `${40 * scale}px 'Inter'`;
                    ctx.shadowBlur = isFar ? 0 : 10;
                    ctx.shadowColor = 'white';
                    ctx.fillText(txt, x2d, y2d);
                }
            }
        });
        ctx.shadowBlur = 0;

        // --- RENDER ANOMALIES (BLACK SWANS) ---
        // Randomly spawn red anomalies
        if (Math.random() > 0.98) {
            anomalies.push({
                x: (Math.random() - 0.5) * width,
                y: (Math.random() - 0.5) * height,
                z: MAX_Z,
                size: Math.random() * 20 + 10,
                life: 1.0
            });
        }

        for (let i = anomalies.length - 1; i >= 0; i--) {
            const a = anomalies[i];
            a.z -= SPEED * 3;
            
            const depth = PERSPECTIVE + a.z;
            if (depth < 1 || a.z < NEAR_PLANE) {
                anomalies.splice(i, 1);
                continue;
            }
            
            const scale = PERSPECTIVE / depth;
            const x2d = (a.x * 0.1) * scale + cx - (camera.x * scale);
            const y2d = (a.y * 0.1) * scale + cy - (camera.y * scale);

            if (scale > 0 && Number.isFinite(x2d) && Number.isFinite(y2d)) {
                ctx.beginPath();
                ctx.arc(x2d, y2d, Math.max(0, a.size * scale), 0, Math.PI * 2);
                ctx.fillStyle = '#ef4444';
                ctx.globalAlpha = 0.8;
                ctx.fill();
                
                ctx.strokeStyle = '#ef4444';
                ctx.lineWidth = 2 * scale;
                ctx.beginPath();
                ctx.moveTo(x2d, y2d);
                ctx.lineTo(x2d + (Math.random()-0.5)*20, y2d + (Math.random()-0.5)*20);
                ctx.stroke();
            }
        }

        animId = requestAnimationFrame(animate);
    };

    // Start Animation
    animId = requestAnimationFrame(animate);

    return () => {
        resizeObserver.disconnect();
        window.removeEventListener('mousemove', handleMouseMove);
        cancelAnimationFrame(animId);
    };
  }, []);

  return (
    <div ref={containerRef} className="w-full h-full min-h-[80vh] relative flex items-center justify-center bg-black overflow-hidden">
        
        <canvas ref={canvasRef} className="absolute inset-0 w-full h-full z-0" />
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,transparent_0%,#000_90%)] pointer-events-none"></div>

        {/* HUD Overlay */}
        <div className="absolute top-8 left-8 z-10 animate-in fade-in duration-1000">
            <div className="flex items-center gap-3 mb-2">
                <Timer className="text-primary animate-spin-slow" size={20} />
                <h2 className="text-white font-bold font-mono uppercase tracking-widest">Temporal Calculus</h2>
            </div>
            <p className="text-[10px] text-gray-400 font-mono max-w-xs leading-relaxed">
                Visualizing the collapse of probabilistic future timelines into the deterministic present.
                <br/>
                <span className="text-red-400 mt-1 block">WARNING: Black Swan anomalies detected in sector 2027.</span>
            </p>
        </div>

        <div className="absolute bottom-8 right-8 z-10 text-right animate-in fade-in slide-in-from-bottom-4 duration-1000 delay-500">
             <div className="flex items-center justify-end gap-2 text-xs font-mono text-gray-500 uppercase tracking-widest mb-1">
                <span>Velocity</span>
                <Zap size={12} className="text-yellow-400" />
             </div>
             <div className="text-3xl font-black text-white font-mono">1.00 Y/S</div>
        </div>

    </div>
  );
};
