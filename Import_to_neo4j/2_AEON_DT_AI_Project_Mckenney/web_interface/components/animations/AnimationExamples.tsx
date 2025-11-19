import React from 'react';
import { WaveBackground, SimpleWaveBackground } from './WaveBackground';
import { AnimatedCard, AnimatedCardGrid, MetricCard, AnimatedButton } from './AnimatedCard';
import { useWaveAnimation, useScrollAnimation, useRipple } from '../../hooks/useWaveAnimation';

/**
 * Example Dashboard Layout with Wave Background
 */
export const DashboardWithWaves: React.FC = () => {
  const { isAnimating, toggle } = useWaveAnimation();

  return (
    <div className="relative min-h-screen bg-gray-900">
      {/* Canvas-based wave background */}
      <WaveBackground
        color="#3b82f6"
        opacity={0.15}
        speed={30}
        waveCount={5}
      />

      {/* Or use the simpler CSS-based version */}
      {/* <SimpleWaveBackground variant="primary" /> */}

      {/* Your dashboard content */}
      <div className="relative z-10 p-8">
        <h1 className="text-4xl font-bold text-white mb-8">
          AEON Digital Twin Dashboard
        </h1>

        <AnimatedButton onClick={toggle} className="mb-8">
          {isAnimating ? 'Pause' : 'Resume'} Animations
        </AnimatedButton>

        {/* Animated metrics grid */}
        <AnimatedCardGrid className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <MetricCard
            title="Active Threats"
            value={23}
            subtitle="Last 24 hours"
            status="warning"
            pulse
          />
          <MetricCard
            title="System Health"
            value="98%"
            subtitle="All systems operational"
            status="success"
          />
          <MetricCard
            title="Network Load"
            value="2.4 GB/s"
            subtitle="Current throughput"
            status="info"
          />
        </AnimatedCardGrid>
      </div>
    </div>
  );
};

/**
 * Example Card List with Scroll Animations
 */
export const AnimatedCardList: React.FC = () => {
  const { elementRef, isVisible } = useScrollAnimation(0.2);

  return (
    <div className="space-y-4">
      {[1, 2, 3, 4, 5].map((item, index) => (
        <AnimatedCard
          key={item}
          variant="hover-lift"
          delay={index * 0.1}
          className="bg-gray-800/50 backdrop-blur-sm border border-gray-700 rounded-lg p-6"
        >
          <h3 className="text-xl font-semibold text-white mb-2">
            Card Item {item}
          </h3>
          <p className="text-gray-400">
            This card animates on render with hover effects
          </p>
        </AnimatedCard>
      ))}
    </div>
  );
};

/**
 * Example Interactive Button with Ripple Effect
 */
export const RippleButton: React.FC = () => {
  const { ripples, addRipple } = useRipple();

  return (
    <button
      className="relative overflow-hidden px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
      onClick={addRipple}
    >
      Click me for ripple effect
      {ripples.map((ripple) => (
        <span
          key={ripple.id}
          className="absolute bg-white/30 rounded-full animate-ripple"
          style={{
            left: ripple.x,
            top: ripple.y,
            width: ripple.size,
            height: ripple.size,
          }}
        />
      ))}
    </button>
  );
};

/**
 * Example Multi-Status Dashboard
 */
export const StatusDashboard: React.FC = () => {
  return (
    <div className="relative min-h-screen bg-gray-900">
      <SimpleWaveBackground variant="primary" />

      <div className="relative z-10 p-8">
        <h1 className="text-3xl font-bold text-white mb-8">System Status</h1>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Critical alerts with pulse */}
          <AnimatedCard variant="pulse" className="bg-red-900/30 border border-red-500/50 rounded-lg p-6">
            <div className="flex items-center gap-4">
              <div className="w-4 h-4 bg-red-500 rounded-full status-pulse" />
              <div>
                <h3 className="text-xl font-semibold text-white">Critical Alert</h3>
                <p className="text-gray-300">Suspicious activity detected</p>
              </div>
            </div>
          </AnimatedCard>

          {/* Normal status with glow effect */}
          <AnimatedCard variant="hover-glow" className="bg-gray-800/50 border border-gray-700 rounded-lg p-6">
            <div className="flex items-center gap-4">
              <div className="w-4 h-4 bg-green-500 rounded-full" />
              <div>
                <h3 className="text-xl font-semibold text-white">System Healthy</h3>
                <p className="text-gray-300">All services running normally</p>
              </div>
            </div>
          </AnimatedCard>
        </div>

        {/* Action buttons */}
        <div className="flex gap-4 mt-8">
          <AnimatedButton variant="primary">
            Investigate
          </AnimatedButton>
          <AnimatedButton variant="secondary">
            View Details
          </AnimatedButton>
          <AnimatedButton variant="danger">
            Shutdown
          </AnimatedButton>
        </div>
      </div>
    </div>
  );
};

/**
 * Example Usage in Main App Component
 */
export const AppWithAnimations: React.FC = () => {
  return (
    <>
      {/* Import the animations CSS */}
      <link rel="stylesheet" href="/styles/animations.css" />

      {/* Use any of the example components */}
      <DashboardWithWaves />
    </>
  );
};

export default DashboardWithWaves;
