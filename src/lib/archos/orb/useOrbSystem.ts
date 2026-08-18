/**
 * ArchOS 3D Orb System - React Hook
 * Manages voice control, hand tracking, gesture recognition, and quantum security visualization
 */

import { useState, useEffect, useCallback, useRef } from 'react';
import {
  OrbSystemState,
  OrbState,
  OrbMode,
  MiniOrb,
  VoiceCommand,
  HandTrackingData,
  GestureType,
  SecurityStatus,
  OrbSystemConfig,
  OrbInteractionEvent,
  OrbPosition,
  OrbRotation,
} from './types';

const DEFAULT_CONFIG: OrbSystemConfig = {
  enableVoice: true,
  enableHandTracking: true,
  enableGestureControl: true,
  sensitivity: 0.75,
  securityLevel: 'QUANTUM',
  showSecurityIndicator: true,
};

const INITIAL_MINI_ORBS: MiniOrb[] = [
  { id: 'discover', name: 'Discover', icon: '🔍', mode: 'DISCOVER', position: { x: 2, y: 0, z: 0 }, color: '#00e5ff', glowIntensity: 0.8, connected: true },
  { id: 'design', name: 'Design', icon: '🎨', mode: 'DESIGN', position: { x: 1.414, y: 1.414, z: 0 }, color: '#ff6b35', glowIntensity: 0.6, connected: true },
  { id: 'build', name: 'Build', icon: '⚙️', mode: 'BUILD', position: { x: 0, y: 2, z: 0 }, color: '#00ff88', glowIntensity: 0.6, connected: true },
  { id: 'deploy', name: 'Deploy', icon: '🚀', mode: 'DEPLOY', position: { x: -1.414, y: 1.414, z: 0 }, color: '#a855f7', glowIntensity: 0.6, connected: true },
  { id: 'monitor', name: 'Monitor', icon: '📊', mode: 'MONITOR', position: { x: -2, y: 0, z: 0 }, color: '#fbbf24', glowIntensity: 0.6, connected: true },
  { id: 'security', name: 'Security', icon: '🛡️', mode: 'MONITOR', position: { x: -1.414, y: -1.414, z: 0 }, color: '#ef4444', glowIntensity: 0.9, connected: true },
  { id: 'languages', name: 'Languages', icon: '🌐', mode: 'BUILD', position: { x: 0, y: -2, z: 0 }, color: '#3b82f6', glowIntensity: 0.7, connected: true },
  { id: 'ai-vault', name: 'AI Vault', icon: '🧠', mode: 'DESIGN', position: { x: 1.414, y: -1.414, z: 0 }, color: '#ec4899', glowIntensity: 0.85, connected: true },
];

const INITIAL_SECURITY: SecurityStatus = {
  encryptionActive: true,
  quantumShieldEnabled: true,
  binaryEncryptionLevel: 256,
  threatLevel: 'NONE',
  lastSecurityScan: new Date().toISOString(),
};

export function useOrbSystem() {
  const [state, setState] = useState<OrbSystemState>({
    currentState: 'IDLE',
    currentMode: 'DISCOVER',
    position: { x: 0, y: 0, z: 0 },
    rotation: { pitch: 0, yaw: 0, roll: 0 },
    scale: 1,
    miniOrbs: INITIAL_MINI_ORBS,
    selectedMiniOrb: null,
    voiceCommands: [],
    handTracking: null,
    config: DEFAULT_CONFIG,
    securityStatus: INITIAL_SECURITY,
    interactions: [],
  });

  const voiceRecognitionRef = useRef<any>(null);
  const handTrackingRef = useRef<any>(null);
  const animationFrameRef = useRef<number>();

  // Initialize Voice Recognition
  useEffect(() => {
    if (!state.config.enableVoice || typeof window === 'undefined') return;

    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (SpeechRecognition) {
      voiceRecognitionRef.current = new SpeechRecognition();
      voiceRecognitionRef.current.continuous = true;
      voiceRecognitionRef.current.interimResults = true;
      voiceRecognitionRef.current.lang = 'en-US';

      voiceRecognitionRef.current.onresult = (event: any) => {
        const transcript = Array.from(event.results)
          .map((result: any) => result[0].transcript)
          .join('');
        
        const confidence = event.results[0]?.confidence || 0.8;
        
        if (confidence > state.config.sensitivity) {
          const command = parseVoiceCommand(transcript);
          addVoiceCommand(command);
          executeVoiceCommand(command);
        }
      };

      voiceRecognitionRef.current.onerror = (event: any) => {
        console.error('Voice recognition error:', event.error);
        setState(prev => ({ ...prev, currentState: prev.currentState === 'LISTENING' ? 'ACTIVE' : prev.currentState }));
      };

      voiceRecognitionRef.current.start();
      setState(prev => ({ ...prev, currentState: 'LISTENING' }));
    }

    return () => {
      if (voiceRecognitionRef.current) {
        voiceRecognitionRef.current.stop();
      }
    };
  }, [state.config.enableVoice, state.config.sensitivity]);

  // Initialize Hand Tracking (placeholder for MediaPipe/Leap Motion)
  useEffect(() => {
    if (!state.config.enableHandTracking) return;

    // Simulated hand tracking - replace with actual implementation
    const simulateHandTracking = () => {
      const now = Date.now();
      const handData: HandTrackingData = {
        handId: 'right-hand-1',
        isLeftHand: false,
        confidence: 0.95,
        fingers: {
          thumb: { x: Math.sin(now / 1000) * 0.5, y: 0.2, z: 0.1 },
          index: { x: Math.sin(now / 1000 + 0.5) * 0.5, y: 0.4, z: 0.2 },
          middle: { x: Math.sin(now / 1000 + 1) * 0.5, y: 0.5, z: 0.2 },
          ring: { x: Math.sin(now / 1000 + 1.5) * 0.5, y: 0.4, z: 0.2 },
          pinky: { x: Math.sin(now / 1000 + 2) * 0.5, y: 0.2, z: 0.1 },
          palm: { x: 0, y: 0, z: 0 },
        },
      };

      // Detect gestures based on finger positions
      const gesture = detectGesture(handData);
      if (gesture && gesture !== handData.gesture) {
        handData.gesture = gesture;
        handleGesture(gesture);
      }

      setState(prev => ({ ...prev, handTracking: handData }));
      animationFrameRef.current = requestAnimationFrame(simulateHandTracking);
    };

    animationFrameRef.current = requestAnimationFrame(simulateHandTracking);

    return () => {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
    };
  }, [state.config.enableHandTracking]);

  // Quantum Security Status Monitor
  useEffect(() => {
    const interval = setInterval(() => {
      setState(prev => ({
        ...prev,
        securityStatus: {
          ...prev.securityStatus,
          threatLevel: Math.random() > 0.95 ? 'LOW' : 'NONE',
          lastSecurityScan: new Date().toISOString(),
        },
      }));
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  const parseVoiceCommand = (transcript: string): VoiceCommand => {
    const lowerTranscript = transcript.toLowerCase();
    let action = 'UNKNOWN';
    let parameters: Record<string, any> = {};

    if (lowerTranscript.includes('switch to') || lowerTranscript.includes('go to')) {
      if (lowerTranscript.includes('discover')) action = 'SWITCH_MODE';
      else if (lowerTranscript.includes('design')) action = 'SWITCH_MODE';
      else if (lowerTranscript.includes('build')) action = 'SWITCH_MODE';
      else if (lowerTranscript.includes('deploy')) action = 'SWITCH_MODE';
      else if (lowerTranscript.includes('monitor')) action = 'SWITCH_MODE';
      parameters.mode = lowerTranscript.split(' ').pop()?.toUpperCase() as OrbMode;
    } else if (lowerTranscript.includes('select') || lowerTranscript.includes('open')) {
      action = 'SELECT_MINI_ORB';
      parameters.orbId = lowerTranscript.replace(/select|open|the/gi, '').trim();
    } else if (lowerTranscript.includes('rotate') || lowerTranscript.includes('spin')) {
      action = 'ROTATE_ORB';
      parameters.direction = lowerTranscript.includes('left') ? 'left' : 'right';
    } else if (lowerTranscript.includes('zoom') || lowerTranscript.includes('scale')) {
      action = 'ZOOM';
      parameters.factor = lowerTranscript.includes('in') ? 1.2 : 0.8;
    } else if (lowerTranscript.includes('security') || lowerTranscript.includes('shield')) {
      action = 'TOGGLE_SECURITY';
    }

    return {
      command: transcript,
      confidence: 0.9,
      timestamp: new Date().toISOString(),
      action,
      parameters,
    };
  };

  const addVoiceCommand = (command: VoiceCommand) => {
    setState(prev => ({
      ...prev,
      voiceCommands: [...prev.voiceCommands.slice(-9), command],
    }));
  };

  const executeVoiceCommand = (command: VoiceCommand) => {
    switch (command.action) {
      case 'SWITCH_MODE':
        if (command.parameters.mode) {
          setMode(command.parameters.mode);
        }
        break;
      case 'SELECT_MINI_ORB':
        const orb = state.miniOrbs.find(o => o.name.toLowerCase().includes(command.parameters.orbId));
        if (orb) selectMiniOrb(orb.id);
        break;
      case 'ROTATE_ORB':
        rotateOrb(command.parameters.direction === 'left' ? -0.1 : 0.1, 0, 0);
        break;
      case 'ZOOM':
        setScale(state.scale * command.parameters.factor);
        break;
      case 'TOGGLE_SECURITY':
        toggleQuantumShield();
        break;
    }
  };

  const detectGesture = (handData: HandTrackingData): GestureType | undefined => {
    const { index, middle, thumb } = handData.fingers;
    
    // Pinch detection
    const pinchDistance = Math.sqrt(
      Math.pow(index.x - thumb.x, 2) + Math.pow(index.y - thumb.y, 2)
    );
    if (pinchDistance < 0.15) return 'PINCH';

    // Expand detection
    if (pinchDistance > 0.4) return 'EXPAND';

    // Swipe detection based on palm movement
    if (Math.abs(handData.fingers.palm.x) > 0.3) {
      return handData.fingers.palm.x > 0 ? 'SWIPE_RIGHT' : 'SWIPE_LEFT';
    }

    // Tap detection
    if (index.y > 0.6 && middle.y < 0.4) return 'TAP';

    return undefined;
  };

  const handleGesture = (gesture: GestureType) => {
    addInteraction({
      type: 'GESTURE_DETECTED',
      timestamp: new Date().toISOString(),
      data: { gesture },
    });

    switch (gesture) {
      case 'PINCH':
        setState(prev => ({ ...prev, currentState: 'PROCESSING' }));
        break;
      case 'EXPAND':
        setScale(Math.min(state.scale * 1.2, 3));
        break;
      case 'SWIPE_LEFT':
      case 'SWIPE_RIGHT':
        rotateOrb(0, gesture === 'SWIPE_LEFT' ? -0.2 : 0.2, 0);
        break;
      case 'TAP':
        if (state.selectedMiniOrb) {
          const orb = state.miniOrbs.find(o => o.id === state.selectedMiniOrb);
          if (orb) setMode(orb.mode);
        }
        break;
    }

    setTimeout(() => {
      setState(prev => ({ ...prev, currentState: prev.currentState === 'PROCESSING' ? 'ACTIVE' : prev.currentState }));
    }, 500);
  };

  const addInteraction = (event: OrbInteractionEvent) => {
    setState(prev => ({
      ...prev,
      interactions: [...prev.interactions.slice(-19), event],
    }));
  };

  const setMode = useCallback((mode: OrbMode) => {
    setState(prev => {
      const updatedOrbs = prev.miniOrbs.map(orb => ({
        ...orb,
        glowIntensity: orb.mode === mode ? 0.9 : 0.6,
      }));

      addInteraction({
        type: 'MODE_CHANGED',
        timestamp: new Date().toISOString(),
        data: { previousMode: prev.currentMode, newMode: mode },
      });

      return {
        ...prev,
        currentMode: mode,
        miniOrbs: updatedOrbs,
        currentState: 'ACTIVE',
      };
    });
  }, []);

  const selectMiniOrb = useCallback((orbId: string) => {
    setState(prev => {
      const orb = prev.miniOrbs.find(o => o.id === orbId);
      if (!orb) return prev;

      addInteraction({
        type: 'MINI_ORB_SELECTED',
        timestamp: new Date().toISOString(),
        data: { orbId, orbName: orb.name },
      });

      return {
        ...prev,
        selectedMiniOrb: orbId,
        currentMode: orb.mode,
        currentState: 'ACTIVE',
      };
    });
  }, []);

  const rotateOrb = useCallback((pitch: number, yaw: number, roll: number) => {
    setState(prev => ({
      ...prev,
      rotation: {
        pitch: (prev.rotation.pitch + pitch) % (Math.PI * 2),
        yaw: (prev.rotation.yaw + yaw) % (Math.PI * 2),
        roll: (prev.rotation.roll + roll) % (Math.PI * 2),
      },
      currentState: 'ACTIVE',
    }));

    addInteraction({
      type: 'ORBIT_ROTATED',
      timestamp: new Date().toISOString(),
      data: { pitch, yaw, roll },
    });
  }, []);

  const setScale = useCallback((scale: number) => {
    setState(prev => ({
      ...prev,
      scale: Math.max(0.5, Math.min(scale, 3)),
      currentState: 'ACTIVE',
    }));
  }, []);

  const toggleQuantumShield = useCallback(() => {
    setState(prev => ({
      ...prev,
      securityStatus: {
        ...prev.securityStatus,
        quantumShieldEnabled: !prev.securityStatus.quantumShieldEnabled,
      },
      currentState: prev.securityStatus.quantumShieldEnabled ? 'ACTIVE' : 'SECURITY_ALERT',
    }));

    addInteraction({
      type: 'VOICE_COMMAND',
      timestamp: new Date().toISOString(),
      data: { action: 'TOGGLE_SECURITY', enabled: !state.securityStatus.quantumShieldEnabled },
    });
  }, [state.securityStatus.quantumShieldEnabled]);

  const updatePosition = useCallback((position: OrbPosition) => {
    setState(prev => ({ ...prev, position }));
  }, []);

  const updateConfig = useCallback((config: Partial<OrbSystemConfig>) => {
    setState(prev => ({ ...prev, config: { ...prev.config, ...config } }));
  }, []);

  return {
    state,
    setMode,
    selectMiniOrb,
    rotateOrb,
    setScale,
    toggleQuantumShield,
    updatePosition,
    updateConfig,
    startListening: () => voiceRecognitionRef.current?.start(),
    stopListening: () => voiceRecognitionRef.current?.stop(),
  };
}
