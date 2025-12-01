import React, { useEffect, useRef } from 'react';
import { motion } from 'framer-motion';

interface WaveBackgroundProps {
  color?: string;
  opacity?: number;
  speed?: number;
  waveCount?: number;
}

export const WaveBackground: React.FC<WaveBackgroundProps> = ({
  color = '#3b82f6',
  opacity = 0.15,
  speed = 30,
  waveCount = 5
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Set canvas size
    const resizeCanvas = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    // Wave properties
    const waves: Array<{
      y: number;
      length: number;
      amplitude: number;
      frequency: number;
      phase: number;
    }> = [];

    for (let i = 0; i < waveCount; i++) {
      waves.push({
        y: canvas.height * (0.5 + i * 0.15),
        length: 0.01 + i * 0.001,
        amplitude: 40 + i * 20,
        frequency: 0.01 + i * 0.005,
        phase: i * Math.PI / 4
      });
    }

    let animationFrame: number;
    let increment = 0;

    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Create gradient for fade effect
      const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
      gradient.addColorStop(0, 'rgba(0, 0, 0, 0)');
      gradient.addColorStop(0.3, `${color}${Math.round(opacity * 255).toString(16).padStart(2, '0')}`);
      gradient.addColorStop(0.7, `${color}${Math.round(opacity * 255).toString(16).padStart(2, '0')}`);
      gradient.addColorStop(1, 'rgba(0, 0, 0, 0)');

      waves.forEach((wave, index) => {
        ctx.beginPath();
        ctx.strokeStyle = gradient;
        ctx.lineWidth = 2 + index * 0.5;

        for (let i = 0; i < canvas.width; i++) {
          const y = wave.y +
            Math.sin(i * wave.length + increment * wave.frequency + wave.phase) * wave.amplitude;

          if (i === 0) {
            ctx.moveTo(i, y);
          } else {
            ctx.lineTo(i, y);
          }
        }

        ctx.stroke();
      });

      increment += speed / 1000;
      animationFrame = requestAnimationFrame(animate);
    };

    animate();

    return () => {
      window.removeEventListener('resize', resizeCanvas);
      cancelAnimationFrame(animationFrame);
    };
  }, [color, opacity, speed, waveCount]);

  return (
    <canvas
      ref={canvasRef}
      className="fixed inset-0 pointer-events-none z-0"
      style={{ opacity }}
    />
  );
};

// Alternative simpler CSS-based wave animation
export const SimpleWaveBackground: React.FC<{
  variant?: 'primary' | 'secondary' | 'accent';
}> = ({ variant = 'primary' }) => {
  const colors = {
    primary: 'from-blue-500/20 via-blue-400/10 to-transparent',
    secondary: 'from-purple-500/20 via-purple-400/10 to-transparent',
    accent: 'from-cyan-500/20 via-cyan-400/10 to-transparent'
  };

  return (
    <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
      {[...Array(3)].map((_, i) => (
        <motion.div
          key={i}
          className={`absolute inset-0 bg-gradient-to-b ${colors[variant]}`}
          initial={{ y: '100%' }}
          animate={{
            y: ['-100%', '100%'],
          }}
          transition={{
            duration: 20 + i * 5,
            repeat: Infinity,
            ease: 'linear',
            delay: i * 2
          }}
          style={{
            maskImage: 'linear-gradient(to bottom, transparent 0%, black 20%, black 80%, transparent 100%)',
            WebkitMaskImage: 'linear-gradient(to bottom, transparent 0%, black 20%, black 80%, transparent 100%)',
          }}
        />
      ))}
    </div>
  );
};

export default WaveBackground;
