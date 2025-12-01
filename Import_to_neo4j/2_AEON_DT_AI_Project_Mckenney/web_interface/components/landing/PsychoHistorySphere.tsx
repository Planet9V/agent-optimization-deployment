
import React, { useEffect, useRef } from 'react';

export const PsychoHistorySphere: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const container = containerRef.current;
    if (!canvas || !container) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Configuration
    const SYMBOLS = ['∂', 'dt', '∫', 'Ψ', '∑', '∇', '∅', '∞', 'Ω'];
    let width = 0;
    let height = 0;
    let animationId: number;

    // State
    const state = {
      time: 0,
      rotation: { x: 0, y: 0 },
      targetRotation: { x: 0, y: 0 },
      isHovered: false,
      jouissance: 0, // Intensity factor
    };

    // Entity Definition
    interface Entity {
      x: number;
      y: number;
      z: number;
      layer: 'REAL' | 'SYMBOLIC' | 'IMAGINARY' | 'CALCULUS';
      val: string | number;
      phase: number;
      baseR: number;
    }

    const entities: Entity[] = [];

    // Initialize Sphere Data
    const initEntities = () => {
      entities.length = 0;
      const radius = Math.min(width, height) * 0.35;

      // 1. The REAL (Core) - Dense, chaotic, unrepresentable
      // Represented by a dense cloud of points
      for (let i = 0; i < 150; i++) {
        const theta = Math.random() * Math.PI * 2;
        const phi = Math.acos(Math.random() * 2 - 1);
        const r = radius * 0.4 * Math.cbrt(Math.random()); // Volume distribution
        
        entities.push({
          x: r * Math.sin(phi) * Math.cos(theta),
          y: r * Math.sin(phi) * Math.sin(theta),
          z: r * Math.cos(phi),
          layer: 'REAL',
          val: '.',
          phase: Math.random() * 10,
          baseR: r
        });
      }

      // 2. The SYMBOLIC (Structure) - Ordered network
      // Points on a sphere surface
      const symbolicCount = 60;
      for (let i = 0; i < symbolicCount; i++) {
        const phi = Math.acos(1 - 2 * (i + 0.5) / symbolicCount);
        const theta = Math.PI * (1 + Math.sqrt(5)) * i; // Golden angle
        const r = radius * 0.75;

        entities.push({
          x: r * Math.sin(phi) * Math.cos(theta),
          y: r * Math.sin(phi) * Math.sin(theta),
          z: r * Math.cos(phi),
          layer: 'SYMBOLIC',
          val: 'o',
          phase: i,
          baseR: r
        });
      }

      // 3. The IMAGINARY (Halo/Mirror) - Outer glow/illusion
      // Larger sparse rings
      for (let i = 0; i < 3; i++) { // 3 Rings
        const ringTiltX = Math.random() * Math.PI;
        const ringTiltY = Math.random() * Math.PI;
        for (let j = 0; j < 20; j++) {
            const angle = (j / 20) * Math.PI * 2;
            const r = radius * 1.0;
            // Flat ring coords
            let x = r * Math.cos(angle);
            let y = r * Math.sin(angle);
            let z = 0;
            
            // Rotate ring
            let tempY = y * Math.cos(ringTiltX) - z * Math.sin(ringTiltX);
            let tempZ = y * Math.sin(ringTiltX) + z * Math.cos(ringTiltX);
            y = tempY; z = tempZ;

            let tempX = x * Math.cos(ringTiltY) + z * Math.sin(ringTiltY);
            z = -x * Math.sin(ringTiltY) + z * Math.cos(ringTiltY);
            x = tempX;

            entities.push({
                x, y, z,
                layer: 'IMAGINARY',
                val: '',
                phase: Math.random() * Math.PI,
                baseR: r
            });
        }
      }

      // 4. CALCULUS (Time Derivatives) - Floating symbols
      for (let i = 0; i < 25; i++) {
        const theta = Math.random() * Math.PI * 2;
        const phi = Math.acos(Math.random() * 2 - 1);
        const r = radius * 1.3 + Math.random() * radius * 0.4;
        
        entities.push({
          x: r * Math.sin(phi) * Math.cos(theta),
          y: r * Math.sin(phi) * Math.sin(theta),
          z: r * Math.cos(phi),
          layer: 'CALCULUS',
          val: SYMBOLS[Math.floor(Math.random() * SYMBOLS.length)],
          phase: Math.random() * 10,
          baseR: r
        });
      }
    };

    const handleResize = () => {
      if (!container) return;
      width = canvas.width = container.clientWidth;
      height = canvas.height = container.clientHeight;
      initEntities();
    };

    const handleMouseMove = (e: MouseEvent) => {
      const rect = canvas.getBoundingClientRect();
      const cx = rect.left + rect.width / 2;
      const cy = rect.top + rect.height / 2;
      
      // Update target rotation based on mouse position relative to center
      state.targetRotation.y = (e.clientX - cx) * 0.001;
      state.targetRotation.x = (e.clientY - cy) * 0.001;
      state.isHovered = true;
    };

    const handleMouseLeave = () => {
      state.isHovered = false;
      state.targetRotation.x = 0;
      state.targetRotation.y = 0;
    };

    // Initial Setup
    handleResize();
    window.addEventListener('resize', handleResize);
    container.addEventListener('mousemove', handleMouseMove);
    container.addEventListener('mouseleave', handleMouseLeave);

    // Loop
    const animate = () => {
      state.time += 0.015;
      
      // Smooth Rotation Logic
      const autoSpeed = 0.003;
      if (!state.isHovered) {
          state.targetRotation.y = autoSpeed;
          state.targetRotation.x = Math.sin(state.time * 0.5) * 0.001;
      }
      
      // Interpolate rotation
      state.rotation.x += (state.targetRotation.x - state.rotation.x) * 0.05;
      state.rotation.y += (state.targetRotation.y - state.rotation.y) * 0.05;

      // Jouissance (Intensity) Logic
      const targetJouissance = state.isHovered ? 1.0 : 0.0;
      state.jouissance += (targetJouissance - state.jouissance) * 0.05;

      // Clear
      ctx.clearRect(0, 0, width, height);
      
      const cx = width / 2;
      const cy = height / 2;

      // Process Entities
      const projected: any[] = [];
      const perspective = 800;

      entities.forEach(p => {
        // 1. Apply Base Rotation
        let x = p.x; let y = p.y; let z = p.z;

        // Rotate Y
        let tx = x * Math.cos(state.rotation.y) - z * Math.sin(state.rotation.y);
        let tz = x * Math.sin(state.rotation.y) + z * Math.cos(state.rotation.y);
        x = tx; z = tz;

        // Rotate X
        let ty = y * Math.cos(state.rotation.x) - z * Math.sin(state.rotation.x);
        tz = y * Math.sin(state.rotation.x) + z * Math.cos(state.rotation.x);
        y = ty; z = tz;

        // 2. Apply "Jouissance" (Pulsation/Distortion)
        // The Real beats faster/more erratically
        const pulseSpeed = p.layer === 'REAL' ? 5 : 2;
        const pulseAmount = p.layer === 'REAL' ? 0.1 : 0.05;
        const pulse = 1 + Math.sin(state.time * pulseSpeed + p.phase) * (pulseAmount + state.jouissance * 0.05);
        
        x *= pulse;
        y *= pulse;
        z *= pulse;

        // 3. Perspective Projection
        // CLIP POINTS BEHIND CAMERA to prevent negative scale/radius errors
        if (z < -perspective + 50) return;

        const scale = perspective / (perspective + z);
        
        if (!Number.isFinite(scale) || scale <= 0) return;

        projected.push({
          x: x * scale + cx,
          y: y * scale + cy,
          z: z,
          scale: scale,
          layer: p.layer,
          val: p.val,
          alpha: (z + width * 0.2) / (width * 0.4) // rough depth fading
        });
      });

      // Z-Sort
      projected.sort((a, b) => b.z - a.z);

      // Draw Lines for Symbolic Layer (Structure)
      // We only connect a few close neighbors to avoid mess
      ctx.strokeStyle = `rgba(0, 224, 176, 0.15)`;
      ctx.lineWidth = 1;
      
      // Draw Rings (Lacanian Borromean Knot implication)
      const ringRadius = Math.min(width, height) * 0.35 * 0.9;
      const drawRing = (rotationOffset: number, color: string) => {
          ctx.beginPath();
          let started = false;
          for(let i=0; i<=60; i++) {
              const theta = (i/60) * Math.PI * 2;
              let rx = ringRadius * Math.cos(theta);
              let ry = ringRadius * Math.sin(theta);
              let rz = 0;

              // Rotate ring itself
              let tx = rx;
              let ty = ry * Math.cos(rotationOffset) - rz * Math.sin(rotationOffset);
              let tz = ry * Math.sin(rotationOffset) + rz * Math.cos(rotationOffset);
              
              // Apply Sphere Rotation
              let ftx = tx * Math.cos(state.rotation.y + state.time * 0.2) - tz * Math.sin(state.rotation.y + state.time * 0.2);
              let ftz = tx * Math.sin(state.rotation.y + state.time * 0.2) + tz * Math.cos(state.rotation.y + state.time * 0.2);
              
              // Clipping check for ring segment
              if (ftz < -perspective + 50) {
                  started = false;
                  continue;
              }

              // Projection
              const scale = perspective / (perspective + ftz);
              if (!Number.isFinite(scale) || scale <= 0) {
                  started = false;
                  continue;
              }

              const px = ftx * scale + cx;
              const py = ty * scale + cy;
              
              if (!Number.isFinite(px) || !Number.isFinite(py)) {
                  started = false;
                  continue;
              }

              if (!started) {
                  ctx.moveTo(px, py);
                  started = true;
              } else {
                  ctx.lineTo(px, py);
              }
          }
          ctx.strokeStyle = color;
          ctx.stroke();
      };

      // Draw Dynamic Borromean Rings
      ctx.globalAlpha = 0.3 + state.jouissance * 0.2;
      drawRing(0, '#00e0b0'); // Real/Symbolic Intersection
      drawRing(Math.PI/2, '#00aaff'); // Symbolic/Imaginary
      drawRing(Math.PI/4, '#ffffff'); // Imaginary/Real

      // Render Points
      projected.forEach(p => {
        if (p.alpha <= 0) return;

        ctx.globalAlpha = Math.max(0, Math.min(1, p.alpha));
        
        // Safeguard against negative or Infinite radius
        const safeScale = Number.isFinite(p.scale) ? Math.max(0, p.scale) : 0;
        
        if (!Number.isFinite(p.x) || !Number.isFinite(p.y)) return;

        if (p.layer === 'REAL') {
            ctx.fillStyle = '#ffffff';
            const size = 1.5 * safeScale;
            if (size > 0) {
                ctx.beginPath();
                ctx.arc(p.x, p.y, size, 0, Math.PI*2);
                ctx.fill();
            }
        } else if (p.layer === 'SYMBOLIC') {
            ctx.fillStyle = '#00e0b0'; // Primary
            const size = 2 * safeScale;
            if (size > 0) {
                ctx.beginPath();
                ctx.arc(p.x, p.y, size, 0, Math.PI*2);
                ctx.fill();
                // Glow
                if (Math.random() > 0.98) {
                    ctx.fillStyle = 'rgba(0, 224, 176, 0.5)';
                    ctx.beginPath();
                    ctx.arc(p.x, p.y, size * 4, 0, Math.PI*2);
                    ctx.fill();
                }
            }
        } else if (p.layer === 'IMAGINARY') {
            ctx.fillStyle = 'rgba(255, 255, 255, 0.5)';
            const size = 1 * safeScale;
            if (size > 0) {
                ctx.beginPath();
                ctx.arc(p.x, p.y, size, 0, Math.PI*2);
                ctx.fill();
            }
        } else if (p.layer === 'CALCULUS') {
            ctx.font = `${Math.max(1, 12 * safeScale)}px 'Roboto Mono'`;
            ctx.fillStyle = '#00aaff'; // Secondary
            ctx.fillText(p.val as string, p.x, p.y);
        }
      });

      // Center "Jouissance" Core Glow
      // Check finite inputs for gradient
      if (Number.isFinite(cx) && Number.isFinite(cy) && width > 0) {
        try {
            const corePulse = 1 + Math.sin(state.time * 10) * 0.1;
            const radius = Math.max(0, width * 0.15 * corePulse);
            const grd = ctx.createRadialGradient(cx, cy, 0, cx, cy, radius);
            grd.addColorStop(0, `rgba(0, 224, 176, ${0.2 + state.jouissance * 0.2})`);
            grd.addColorStop(1, 'rgba(0,0,0,0)');
            ctx.globalAlpha = 1;
            ctx.fillStyle = grd;
            ctx.fillRect(0,0, width, height);
        } catch(e) {}
      }

      animationId = requestAnimationFrame(animate);
    };

    animate();

    return () => {
      window.removeEventListener('resize', handleResize);
      container.removeEventListener('mousemove', handleMouseMove);
      container.removeEventListener('mouseleave', handleMouseLeave);
      cancelAnimationFrame(animationId);
    };
  }, []);

  return (
    <div ref={containerRef} className="w-full h-full relative">
      <canvas ref={canvasRef} className="absolute inset-0 w-full h-full" />
      {/* Overlay to ensure it blends well with dark background */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_transparent_20%,_#0a0a0a_90%)] pointer-events-none"></div>
    </div>
  );
};
