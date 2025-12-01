import React from 'react';
import { motion, Variants } from 'framer-motion';

interface AnimatedCardProps {
  children: React.ReactNode;
  className?: string;
  delay?: number;
  variant?: 'default' | 'hover-lift' | 'hover-glow' | 'pulse';
  onClick?: () => void;
}

const cardVariants: Record<string, Variants> = {
  default: {
    initial: { opacity: 0, y: 20 },
    animate: { opacity: 1, y: 0 },
    exit: { opacity: 0, y: -20 }
  },
  'hover-lift': {
    initial: { opacity: 0, y: 20 },
    animate: { opacity: 1, y: 0 },
    hover: {
      y: -5,
      scale: 1.02,
      transition: { duration: 0.2 }
    }
  },
  'hover-glow': {
    initial: { opacity: 0, scale: 0.95 },
    animate: { opacity: 1, scale: 1 },
    hover: {
      boxShadow: '0 0 20px rgba(59, 130, 246, 0.5)',
      transition: { duration: 0.3 }
    }
  },
  pulse: {
    initial: { opacity: 0 },
    animate: {
      opacity: 1,
      scale: [1, 1.02, 1],
      transition: {
        scale: {
          duration: 2,
          repeat: Infinity,
          ease: 'easeInOut'
        }
      }
    }
  }
};

export const AnimatedCard: React.FC<AnimatedCardProps> = ({
  children,
  className = '',
  delay = 0,
  variant = 'default',
  onClick
}) => {
  return (
    <motion.div
      className={`${className}`}
      variants={cardVariants[variant]}
      initial="initial"
      animate="animate"
      exit="exit"
      whileHover="hover"
      transition={{
        duration: 0.3,
        delay,
        ease: 'easeOut'
      }}
      onClick={onClick}
      style={{ cursor: onClick ? 'pointer' : 'default' }}
    >
      {children}
    </motion.div>
  );
};

// Stagger container for multiple cards
export const AnimatedCardGrid: React.FC<{
  children: React.ReactNode;
  className?: string;
}> = ({ children, className = '' }) => {
  const containerVariants: Variants = {
    initial: {},
    animate: {
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  return (
    <motion.div
      className={className}
      variants={containerVariants}
      initial="initial"
      animate="animate"
    >
      {children}
    </motion.div>
  );
};

// Animated metric card with pulsing indicator
export const MetricCard: React.FC<{
  title: string;
  value: string | number;
  subtitle?: string;
  status?: 'success' | 'warning' | 'error' | 'info';
  pulse?: boolean;
}> = ({ title, value, subtitle, status = 'info', pulse = false }) => {
  const statusColors = {
    success: 'bg-green-500',
    warning: 'bg-yellow-500',
    error: 'bg-red-500',
    info: 'bg-blue-500'
  };

  return (
    <AnimatedCard variant="hover-lift" className="relative">
      <div className="bg-gray-800/50 backdrop-blur-sm border border-gray-700 rounded-lg p-6 hover:border-gray-600 transition-colors">
        {pulse && (
          <motion.div
            className={`absolute top-3 right-3 w-2 h-2 ${statusColors[status]} rounded-full`}
            animate={{
              scale: [1, 1.5, 1],
              opacity: [1, 0.5, 1]
            }}
            transition={{
              duration: 2,
              repeat: Infinity,
              ease: 'easeInOut'
            }}
          />
        )}

        <h3 className="text-gray-400 text-sm font-medium mb-2">{title}</h3>
        <motion.div
          className="text-3xl font-bold text-white mb-1"
          initial={{ scale: 0.5, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ delay: 0.2 }}
        >
          {value}
        </motion.div>
        {subtitle && (
          <p className="text-gray-500 text-xs">{subtitle}</p>
        )}
      </div>
    </AnimatedCard>
  );
};

// Animated button with ripple effect
export const AnimatedButton: React.FC<{
  children: React.ReactNode;
  onClick?: () => void;
  variant?: 'primary' | 'secondary' | 'danger';
  disabled?: boolean;
  className?: string;
}> = ({ children, onClick, variant = 'primary', disabled = false, className = '' }) => {
  const variants = {
    primary: 'bg-blue-600 hover:bg-blue-700 text-white',
    secondary: 'bg-gray-700 hover:bg-gray-600 text-white',
    danger: 'bg-red-600 hover:bg-red-700 text-white'
  };

  return (
    <motion.button
      className={`px-4 py-2 rounded-lg font-medium transition-colors ${variants[variant]} ${className} disabled:opacity-50 disabled:cursor-not-allowed`}
      whileHover={!disabled ? { scale: 1.05 } : {}}
      whileTap={!disabled ? { scale: 0.95 } : {}}
      onClick={onClick}
      disabled={disabled}
      transition={{ duration: 0.2 }}
    >
      {children}
    </motion.button>
  );
};

export default AnimatedCard;
