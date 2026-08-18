/**
 * ArchOS Orb System Store
 * Shared Zustand store for unified orb state management across all components
 * Fixes the issue where OrbNavigation, Orb3D, and VoiceToggleButton had separate state instances
 */

import { create } from 'zustand';
import type { OrbSystemState, OrbMode, OrbInteractionEvent, OrbPosition, OrbRotation } from './types';

const INITIAL_MINI_ORBS = [
  { id: 'discover', name: 'Discover', icon: '🔍', mode: 'DISCOVER' as OrbMode, position: { x: 2, y: 0, z: 0 }, color: '#00e5ff', glowIntensity: 0.8, connected: true },
  { id: 'design', name: 'Design', icon: '🎨', mode: 'DESIGN' as OrbMode, position: { x: 1.414, y: 1.414, z: 0 }, color: '#ff6b35', glowIntensity: 0.6, connected: true },
  { id: 'build', name: 'Build', icon: '⚙️', mode: 'BUILD' as OrbMode, position: { x: 0, y: 2, z: 0 }, color: '#00ff88', glowIntensity: 0.6, connected: true },
  { id: 'deploy', name: 'Deploy', icon: '🚀', mode: 'DEPLOY' as OrbMode, position: { x: -1.414, y: 1.414, z: 0 }, color: '#a855f7', glowIntensity: 0.6, connected: true },
  { id: 'monitor', name: 'Monitor', icon: '📊', mode: 'MONITOR' as OrbMode, position: { x: -2, y: 0, z: 0 }, color: '#fbbf24', glowIntensity: 0.6, connected: true },
  { id: 'security', name: 'Security', icon: '🛡️', mode: 'MONITOR' as OrbMode, position: { x: -1.414, y: -1.414, z: 0 }, color: '#ef4444', glowIntensity: 0.9, connected: true },
  { id: 'languages', name: 'Languages', icon: '🌐', mode: 'BUILD' as OrbMode, position: { x: 0, y: -2, z: 0 }, color: '#3b82f6', glowIntensity: 0.7, connected: true },
  { id: 'ai-vault', name: 'AI Vault', icon: '🧠', mode: 'DESIGN' as OrbMode, position: { x: 1.414, y: -1.414, z: 0 }, color: '#ec4899', glowIntensity: 0.85, connected: true },
];

interface OrbSystemStore extends OrbSystemState {
  // Actions
  setMode: (mode: OrbMode) => void;
  selectMiniOrb: (orbId: string) => void;
  rotateOrb: (pitch: number, yaw: number, roll: number) => void;
  setScale: (scale: number) => void;
  toggleQuantumShield: () => void;
  updatePosition: (position: OrbPosition) => void;
  updateRotation: (rotation: OrbRotation) => void;
  setCurrentState: (state: OrbSystemState['currentState']) => void;
  addVoiceCommand: (command: any) => void;
  addInteraction: (event: OrbInteractionEvent) => void;
  updateHandTracking: (handData: any) => void;
  reset: () => void;
}

const initialState: Omit<OrbSystemStore, keyof OrbSystemStore> = {
  currentState: 'IDLE',
  currentMode: 'DISCOVER',
  position: { x: 0, y: 0, z: 0 },
  rotation: { pitch: 0, yaw: 0, roll: 0 },
  scale: 1,
  miniOrbs: INITIAL_MINI_ORBS,
  selectedMiniOrb: null,
  voiceCommands: [],
  handTracking: null,
  config: {
    enableVoice: true,
    enableHandTracking: true,
    enableGestureControl: true,
    sensitivity: 0.75,
    securityLevel: 'QUANTUM',
    showSecurityIndicator: true,
  },
  securityStatus: {
    encryptionActive: true,
    quantumShieldEnabled: true,
    binaryEncryptionLevel: 256,
    threatLevel: 'NONE',
    lastSecurityScan: new Date().toISOString(),
  },
  interactions: [],
};

export const useOrbSystemStore = create<OrbSystemStore>((set, get) => ({
  ...initialState,

  setMode: (mode) => {
    const previousMode = get().currentMode;
    set((state) => ({
      currentMode: mode,
      currentState: 'ACTIVE',
      miniOrbs: state.miniOrbs.map((orb) => ({
        ...orb,
        glowIntensity: orb.mode === mode ? 0.9 : 0.6,
      })),
    }));
    
    get().addInteraction({
      type: 'MODE_CHANGED',
      timestamp: new Date().toISOString(),
      data: { previousMode, newMode: mode },
    });
  },

  selectMiniOrb: (orbId) => {
    const orb = get().miniOrbs.find((o) => o.id === orbId);
    if (!orb) return;

    set((state) => ({
      selectedMiniOrb: orbId,
      currentMode: orb.mode,
      currentState: 'ACTIVE',
    }));

    get().addInteraction({
      type: 'MINI_ORB_SELECTED',
      timestamp: new Date().toISOString(),
      data: { orbId, orbName: orb.name },
    });
  },

  rotateOrb: (pitch, yaw, roll) => {
    set((state) => ({
      rotation: {
        pitch: (state.rotation.pitch + pitch) % (Math.PI * 2),
        yaw: (state.rotation.yaw + yaw) % (Math.PI * 2),
        roll: (state.rotation.roll + roll) % (Math.PI * 2),
      },
      currentState: 'ACTIVE',
    }));

    get().addInteraction({
      type: 'ORBIT_ROTATED',
      timestamp: new Date().toISOString(),
      data: { pitch, yaw, roll },
    });
  },

  setScale: (scale) => {
    set(() => ({
      scale: Math.max(0.5, Math.min(scale, 3)),
      currentState: 'ACTIVE',
    }));
  },

  toggleQuantumShield: () => {
    const wasEnabled = get().securityStatus.quantumShieldEnabled;
    
    set((state) => ({
      securityStatus: {
        ...state.securityStatus,
        quantumShieldEnabled: !state.securityStatus.quantumShieldEnabled,
      },
      currentState: wasEnabled ? 'ACTIVE' : 'SECURITY_ALERT',
    }));

    get().addInteraction({
      type: 'VOICE_COMMAND',
      timestamp: new Date().toISOString(),
      data: { action: 'TOGGLE_SECURITY', enabled: !wasEnabled },
    });
  },

  updatePosition: (position) => {
    set(() => ({ position }));
  },

  updateRotation: (rotation) => {
    set(() => ({ rotation }));
  },

  setCurrentState: (currentState) => {
    set(() => ({ currentState }));
  },

  addVoiceCommand: (command) => {
    set((state) => ({
      voiceCommands: [...state.voiceCommands.slice(-9), command],
    }));
  },

  addInteraction: (event) => {
    set((state) => ({
      interactions: [...state.interactions.slice(-19), event],
    }));
  },

  updateHandTracking: (handData) => {
    set(() => ({ handTracking: handData }));
  },

  reset: () => {
    set(initialState);
  },
}));
