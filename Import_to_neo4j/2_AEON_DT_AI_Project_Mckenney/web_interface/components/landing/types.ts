
export enum ViewState {
  CONTEXT = 'CONTEXT',
  ARCHITECTURE = 'ARCHITECTURE',
  CALCULUS = 'CALCULUS',
  LOGIC = 'LOGIC',
  FRAMEWORK = 'FRAMEWORK',
  TIMELINE = 'TIMELINE',
  AGENT_RED = 'AGENT_RED'
}

export interface SimulationParams {
  // Represents the resistance of the population to change (Mass)
  socialInertia: number;
  // Represents the chaos/randomness in the system (Heat)
  systemEntropy: number;
  // Represents the friction of organizational culture (Viscosity)
  culturalViscosity: number;
  // Represents the speed of technical adaptation (Velocity)
  adaptationRate: number;
}

export interface NodeData {
  id: string;
  label: string;
  description: string;
  x: number;
  y: number;
  status: 'active' | 'latent' | 'critical';
}

export interface ArchitectureLayerProps {
  level: number;
  title: string;
  description: string;
  details: string[];
}

export interface DataFeedItem {
  id: string;
  source: 'NVD' | 'REUTERS' | 'INT' | 'DARKWEB';
  timestamp: string;
  content: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  impactParameter: keyof SimulationParams | 'general';
}