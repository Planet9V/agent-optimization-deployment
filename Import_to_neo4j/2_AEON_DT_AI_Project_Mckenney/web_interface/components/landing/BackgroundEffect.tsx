
import React, { useEffect, useRef } from 'react';

export const BackgroundEffect: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let width = canvas.width = window.innerWidth;
    let height = canvas.height = window.innerHeight;
    let time = 0;

    // Configuration
    const PARTICLE_COUNT = Math.min(window.innerWidth / 15, 150);
    const MAX_SYMBOL_COUNT = 40; // Increased max count slightly to allow for bursts
    const CONNECTION_DIST = 150;
    const MOUSE_DIST = 200;
    
    const mathSymbols = ['∫', '∮', '∑', '∏', '∆', '∇', '∂', 'λ', 'Ω', 'Ψ', 'μ', 'σ', 'dx', 'dt', 'P(x)', 'f(x)', 'lim', '∞', '∃', '∀'];

    // Mouse State
    const mouse = { x: -1000, y: -1000 };

    // Types
    interface Particle {
      x: number;
      y: number;
      vx: number;
      vy: number;
      size: number;
      pulseOffset: number;
    }

    interface Symbol {
      x: number;
      y: number;
      char: string;
      opacity: number;
      targetOpacity: number;
      life: number;
      maxLife: number;
      vx: number;
      vy: number;
      scale: number;
    }

    // Initialize State
    const particles: Particle[] = [];
    const symbols: Symbol[] = [];

    const init = () => {
      particles.length = 0;
      for (let i = 0; i < PARTICLE_COUNT; i++) {
        particles.push({
          x: Math.random() * width,
          y: Math.random() * height,
          vx: (Math.random() - 0.5) * 0.3,
          vy: (Math.random() - 0.5) * 0.3,
          size: Math.random() * 1.5 + 0.5,
          pulseOffset: Math.random() * Math.PI * 2
        });
      }

      symbols.length = 0;
      for (let i = 0; i < 15; i++) {
        spawnSymbol(undefined, undefined, true);
      }
    };

    const spawnSymbol = (x?: number, y?: number, randomStart = false) => {
      if (symbols.length >= MAX_SYMBOL_COUNT) return;

      const maxLife = Math.random() * 200 + 150;
      const startX = x !== undefined ? x : Math.random() * width;
      const startY = y !== undefined ? y : Math.random() * height;

      symbols.push({
        x: startX,
        y: startY,
        char: mathSymbols[Math.floor(Math.random() * mathSymbols.length)],
        opacity: 0,
        targetOpacity: Math.random() * 0.5 + 0.3, // Slightly more visible
        life: randomStart ? Math.random() * maxLife : maxLife,
        maxLife: maxLife,
        vx: (Math.random() - 0.5) * 0.5,
        vy: (Math.random() - 0.5) * 0.5 - 0.2, // Slight upward drift preference for spawned symbols
        scale: Math.random() * 0.5 + 0.8 
      });
    };

    const handleResize = () => {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
      init();
    };

    const handleMouseMove = (e: MouseEvent) => {
      mouse.x = e.clientX;
      mouse.y = e.clientY;
    };

    window.addEventListener('resize', handleResize);
    window.addEventListener('mousemove', handleMouseMove);
    init();

    // Animation Loop
    const animate = () => {
      if (!ctx) return;
      time += 0.01;
      
      // Clear with trail effect for subtle motion blur feeling
      ctx.fillStyle = 'rgba(10, 10, 10, 0.2)'; 
      ctx.fillRect(0, 0, width, height);

      // 1. Draw "Wave Functions" (Calculus representation)
      ctx.beginPath();
      for (let x = 0; x < width; x += 5) {
        const y1 = height * 0.3 + Math.sin(x * 0.005 + time) * 50 + Math.cos(x * 0.02 + time * 0.5) * 20;
        const y2 = height * 0.7 + Math.sin(x * 0.008 - time) * 60;
        
        ctx.fillStyle = `rgba(0, 224, 176, ${0.03 + Math.sin(x * 0.01 + time) * 0.02})`;
        ctx.fillRect(x, y1, 2, 2);
        
        ctx.fillStyle = `rgba(0, 170, 255, ${0.03 + Math.cos(x * 0.01 - time) * 0.02})`;
        ctx.fillRect(x, y2, 2, 2);
      }

      // 2. Update and Draw Particles (The Neural/Social Mesh)
      particles.forEach((p, i) => {
        p.x += p.vx;
        p.y += p.vy;

        const dx = mouse.x - p.x;
        const dy = mouse.y - p.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        
        if (dist < MOUSE_DIST) {
            const force = (MOUSE_DIST - dist) / MOUSE_DIST;
            p.x -= dx * force * 0.05;
            p.y -= dy * force * 0.05;
        }

        if (p.x < 0) p.x = width;
        if (p.x > width) p.x = 0;
        if (p.y < 0) p.y = height;
        if (p.y > height) p.y = 0;

        const pulse = Math.sin(time * 2 + p.pulseOffset);
        const currentSize = p.size + pulse * 0.3;

        ctx.beginPath();
        ctx.arc(p.x, p.y, Math.max(0, currentSize), 0, Math.PI * 2);
        ctx.fillStyle = `rgba(0, 224, 176, ${0.3 + pulse * 0.2})`;
        ctx.fill();

        for (let j = i + 1; j < particles.length; j++) {
          const p2 = particles[j];
          const dx = p.x - p2.x;
          const dy = p.y - p2.y;
          const dist = Math.sqrt(dx * dx + dy * dy);

          if (dist < CONNECTION_DIST) {
            const opacity = (1 - dist / CONNECTION_DIST) * 0.15;
            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(p2.x, p2.y);
            ctx.strokeStyle = `rgba(0, 224, 176, ${opacity})`;
            ctx.lineWidth = 1;
            ctx.stroke();

            // PROXIMITY SPAWNING LOGIC
            // If particles are very close, there's a chance to "spark" a math symbol
            // This represents emergent logic from neural connections
            if (dist < 20 && Math.random() > 0.98) {
                spawnSymbol((p.x + p2.x) / 2, (p.y + p2.y) / 2);
            }
          }
        }
      });

      // 3. Update and Draw Calculus Symbols (Complex Adaptive System)
      // Replenish population randomly if too low (background noise)
      if (symbols.length < 10 && Math.random() > 0.95) {
          spawnSymbol();
      }

      for (let i = symbols.length - 1; i >= 0; i--) {
        const s = symbols[i];
        
        // Erratic Movement (Brownian-like)
        s.vx += (Math.random() - 0.5) * 0.05;
        s.vy += (Math.random() - 0.5) * 0.05;
        
        // Damping to prevent exploding velocity
        s.vx *= 0.95;
        s.vy *= 0.95;
        
        s.x += s.vx;
        s.y += s.vy;
        s.life--;

        // Lifecycle Fade
        if (s.life > s.maxLife * 0.2) {
            // Fade In phase
            if (s.opacity < s.targetOpacity) s.opacity += 0.01;
        } else {
            // Fade Out phase
            s.opacity -= 0.01;
        }

        // Bounds Check (Wrap around)
        if (s.x < -50) s.x = width + 50;
        if (s.x > width + 50) s.x = -50;
        if (s.y < -50) s.y = height + 50;
        if (s.y > height + 50) s.y = -50;

        // Death
        if (s.life <= 0 || s.opacity <= 0) {
            symbols.splice(i, 1);
            continue;
        }

        ctx.font = `${14 * s.scale}px 'Roboto Mono', monospace`;
        ctx.fillStyle = `rgba(0, 170, 255, ${s.opacity})`;
        ctx.fillText(s.char, s.x, s.y);
      }

      requestAnimationFrame(animate);
    };

    const animId = requestAnimationFrame(animate);

    return () => {
      window.removeEventListener('resize', handleResize);
      window.removeEventListener('mousemove', handleMouseMove);
      cancelAnimationFrame(animId);
    };
  }, []);

  return <canvas ref={canvasRef} className="fixed inset-0 pointer-events-none z-0" />;
};
