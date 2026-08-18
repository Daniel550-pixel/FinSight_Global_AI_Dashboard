/**
 * ArchOS 3D Orb System Types
 * Central navigation orb with satellite mini-orbs, voice control, and gesture tracking
 */

export type OrbState = 'IDLE' | 'ACTIVE' | 'LISTENING' | 'PROCESSING' | 'ERROR' | 'SECURITY_ALERT';
export type OrbMode = 'DISCOVER' | 'DESIGN' | 'BUILD' | 'DEPLOY' | 'MONITOR';
export type GestureType = 'TAP' | 'SWIPE_LEFT' | 'SWIPE_RIGHT' | 'PINCH' | 'EXPAND' | 'ROTATE' | 'HOVER';

export interface OrbPosition {
  x: number;
  y: number;
  z: number;
}

export interface OrbRotation {
  pitch: number;
  yaw: number;
  roll: number;
}

export interface MiniOrb {
  id: string;
  name: string;
  icon: string;
  mode: OrbMode;
  position: OrbPosition;
  color: string;
  glowIntensity: number;
  connected: boolean;
  data?: Record<string, any>;
}

export interface VoiceCommand {
  command: string;
  confidence: number;
  timestamp: string;
  action: string;
  parameters?: Record<string, any>;
}

export interface HandTrackingData {
  handId: string;
  isLeftHand: boolean;
  confidence: number;
  fingers: {
    thumb: OrbPosition;
    index: OrbPosition;
    middle: OrbPosition;
    ring: OrbPosition;
    pinky: OrbPosition;
    palm: OrbPosition;
  };
  gesture?: GestureType;
}

export interface OrbSystemConfig {
  enableVoice: boolean;
  enableHandTracking: boolean;
  enableGestureControl: boolean;
  sensitivity: number;
  securityLevel: 'STANDARD' | 'ENHANCED' | 'QUANTUM';
  showSecurityIndicator: boolean;
}

export interface OrbInteractionEvent {
  type: 'VOICE_COMMAND' | 'GESTURE_DETECTED' | 'ORBIT_ROTATED' | 'MINI_ORB_SELECTED' | 'MODE_CHANGED';
  timestamp: string;
  data: any;
}

export interface SecurityStatus {
  encryptionActive: boolean;
  quantumShieldEnabled: boolean;
  binaryEncryptionLevel: number;
  threatLevel: 'NONE' | 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  lastSecurityScan: string;
}

export interface OrbSystemState {
  currentState: OrbState;
  currentMode: OrbMode;
  position: OrbPosition;
  rotation: OrbRotation;
  scale: number;
  miniOrbs: MiniOrb[];
  selectedMiniOrb: string | null;
  voiceCommands: VoiceCommand[];
  handTracking: HandTrackingData | null;
  config: OrbSystemConfig;
  securityStatus: SecurityStatus;
  interactions: OrbInteractionEvent[];
}
