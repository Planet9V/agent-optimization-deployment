import { useState, useEffect, useCallback, useRef } from 'react';

interface WaveConfig {
  speed: number;
  amplitude: number;
  frequency: number;
  opacity: number;
}

interface UseWaveAnimationReturn {
  isAnimating: boolean;
  start: () => void;
  stop: () => void;
  toggle: () => void;
  updateConfig: (config: Partial<WaveConfig>) => void;
  config: WaveConfig;
}

/**
 * Custom hook for controlling wave animations
 * Provides start/stop controls and configuration updates
 */
export const useWaveAnimation = (
  initialConfig: Partial<WaveConfig> = {}
): UseWaveAnimationReturn => {
  const [isAnimating, setIsAnimating] = useState(true);
  const [config, setConfig] = useState<WaveConfig>({
    speed: 30,
    amplitude: 40,
    frequency: 0.01,
    opacity: 0.15,
    ...initialConfig
  });

  const start = useCallback(() => {
    setIsAnimating(true);
  }, []);

  const stop = useCallback(() => {
    setIsAnimating(false);
  }, []);

  const toggle = useCallback(() => {
    setIsAnimating((prev) => !prev);
  }, []);

  const updateConfig = useCallback((newConfig: Partial<WaveConfig>) => {
    setConfig((prev) => ({ ...prev, ...newConfig }));
  }, []);

  return {
    isAnimating,
    start,
    stop,
    toggle,
    updateConfig,
    config
  };
};

/**
 * Hook for scroll-based animation triggers
 * Detects when elements enter viewport
 */
export const useScrollAnimation = (threshold: number = 0.1) => {
  const [isVisible, setIsVisible] = useState(false);
  const elementRef = useRef<HTMLElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
          // Optionally unobserve after first trigger
          // observer.unobserve(entry.target);
        }
      },
      { threshold }
    );

    const currentElement = elementRef.current;
    if (currentElement) {
      observer.observe(currentElement);
    }

    return () => {
      if (currentElement) {
        observer.unobserve(currentElement);
      }
    };
  }, [threshold]);

  return { elementRef, isVisible };
};

/**
 * Hook for staggered animation delays
 * Useful for animating lists of items
 */
export const useStaggerAnimation = (count: number, baseDelay: number = 0.1) => {
  const getDelay = useCallback(
    (index: number) => index * baseDelay,
    [baseDelay]
  );

  return { getDelay };
};

/**
 * Hook for performance-aware animations
 * Reduces animation complexity on low-end devices
 */
export const usePerformanceAnimation = () => {
  const [reducedMotion, setReducedMotion] = useState(false);
  const [performanceLevel, setPerformanceLevel] = useState<'high' | 'medium' | 'low'>('high');

  useEffect(() => {
    // Check for user's motion preference
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    setReducedMotion(mediaQuery.matches);

    const handleChange = (e: MediaQueryListEvent) => {
      setReducedMotion(e.matches);
    };

    mediaQuery.addEventListener('change', handleChange);

    // Detect device performance
    const detectPerformance = () => {
      const connection = (navigator as any).connection;
      if (connection) {
        if (connection.effectiveType === '4g' && navigator.hardwareConcurrency > 4) {
          setPerformanceLevel('high');
        } else if (connection.effectiveType === '3g' || navigator.hardwareConcurrency <= 4) {
          setPerformanceLevel('medium');
        } else {
          setPerformanceLevel('low');
        }
      }
    };

    detectPerformance();

    return () => {
      mediaQuery.removeEventListener('change', handleChange);
    };
  }, []);

  const shouldAnimate = !reducedMotion;
  const animationQuality = reducedMotion ? 'low' : performanceLevel;

  return {
    shouldAnimate,
    animationQuality,
    reducedMotion,
    performanceLevel
  };
};

/**
 * Hook for mouse-following particle effects
 */
export const useMouseParticles = () => {
  const [particles, setParticles] = useState<Array<{
    id: number;
    x: number;
    y: number;
    timestamp: number;
  }>>([]);

  const addParticle = useCallback((x: number, y: number) => {
    const newParticle = {
      id: Date.now(),
      x,
      y,
      timestamp: Date.now()
    };

    setParticles((prev) => [...prev, newParticle]);

    // Remove particle after animation
    setTimeout(() => {
      setParticles((prev) => prev.filter((p) => p.id !== newParticle.id));
    }, 2000);
  }, []);

  const handleMouseMove = useCallback((e: React.MouseEvent) => {
    // Throttle particle creation
    if (Math.random() > 0.9) {
      addParticle(e.clientX, e.clientY);
    }
  }, [addParticle]);

  return { particles, handleMouseMove };
};

/**
 * Hook for element entrance animations
 */
export const useEntranceAnimation = (delay: number = 0) => {
  const [hasEntered, setHasEntered] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => {
      setHasEntered(true);
    }, delay);

    return () => clearTimeout(timer);
  }, [delay]);

  return hasEntered;
};

/**
 * Hook for ripple effect on click
 */
export const useRipple = () => {
  const [ripples, setRipples] = useState<Array<{
    id: number;
    x: number;
    y: number;
    size: number;
  }>>([]);

  const addRipple = useCallback((e: React.MouseEvent<HTMLElement>) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = e.clientX - rect.left - size / 2;
    const y = e.clientY - rect.top - size / 2;

    const newRipple = {
      id: Date.now(),
      x,
      y,
      size
    };

    setRipples((prev) => [...prev, newRipple]);

    setTimeout(() => {
      setRipples((prev) => prev.filter((r) => r.id !== newRipple.id));
    }, 600);
  }, []);

  return { ripples, addRipple };
};

export default useWaveAnimation;
