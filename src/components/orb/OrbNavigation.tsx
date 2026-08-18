/**
 * OrbNavigation Component
 * Main navigation interface using the 3D Orb system
 * Replaces traditional menus with voice, gesture, and orb-based navigation
 * 
 * FIXED: Now uses shared Zustand store for unified state across all components
 */

import React from 'react';
import { Orb3D } from '@/lib/archos/orb';
import { useOrbSystemStore } from '@/store/orbSystemStore';
import type { OrbMode } from '@/lib/archos/orb/types';

interface OrbNavigationProps {
  onModeChange?: (mode: OrbMode) => void;
  className?: string;
}

export function OrbNavigation({ onModeChange, className = '' }: OrbNavigationProps) {
  // Use shared store - same instance as Orb3D and VoiceToggleButton
  const { 
    currentMode, 
    selectedMiniOrb, 
    miniOrbs, 
    setMode, 
    selectMiniOrb 
  } = useOrbSystemStore();

  React.useEffect(() => {
    if (onModeChange) {
      onModeChange(currentMode);
    }
  }, [currentMode, onModeChange]);

  return (
    <div className={`relative h-screen w-full bg-gradient-to-br from-gray-950 via-blue-950 to-gray-950 ${className}`}>
      {/* 3D Orb Canvas - now shares the same store instance */}
      <Orb3D className="absolute inset-0" showControls={true} />

      {/* Quick Action Buttons (Alternative to Voice/Gesture) */}
      <div className="absolute bottom-8 left-1/2 -translate-x-1/2 flex gap-4">
        {miniOrbs.map((orb) => (
          <button
            key={orb.id}
            onClick={() => selectMiniOrb(orb.id)}
            className={`
              px-4 py-3 rounded-xl backdrop-blur-md border transition-all duration-300
              flex items-center gap-2 group
              ${selectedMiniOrb === orb.id || currentMode === orb.mode
                ? 'bg-white/20 border-white/40 scale-105'
                : 'bg-black/40 border-white/10 hover:bg-white/10 hover:border-white/20'
              }
            `}
            style={{ borderColor: selectedMiniOrb === orb.id ? orb.color : undefined }}
          >
            <span className="text-xl">{orb.icon}</span>
            <span className="text-sm font-medium text-white hidden group-hover:block transition-all">
              {orb.name}
            </span>
          </button>
        ))}
      </div>

      {/* Voice Activation Button - also uses shared store */}
      <div className="absolute top-4 right-4">
        <VoiceToggleButton />
      </div>

      {/* Help Tooltip */}
      <div className="absolute bottom-4 right-4 bg-black/60 backdrop-blur-md rounded-lg p-4 border border-white/10 max-w-sm">
        <h3 className="text-sm font-bold text-white mb-2">🎮 Navigation Controls</h3>
        <ul className="text-xs text-gray-400 space-y-1">
          <li>🎤 <strong>Voice:</strong> "Switch to Design", "Select Security"</li>
          <li>✋ <strong>Gestures:</strong> Pinch, Swipe, Tap on mini-orbs</li>
          <li>🖱️ <strong>Mouse:</strong> Click orbs, scroll to zoom, drag to rotate</li>
          <li>⌨️ <strong>Keyboard:</strong> Arrow keys to rotate, +/- to zoom</li>
        </ul>
      </div>
    </div>
  );
}

function VoiceToggleButton() {
  // Uses the SAME shared store - state changes are reflected everywhere
  const { currentState, setCurrentState, addVoiceCommand } = useOrbSystemStore();
  const isListening = currentState === 'LISTENING';

  const handleToggle = () => {
    if (isListening) {
      setCurrentState('IDLE');
      // In a real implementation, this would stop the actual voice recognition
    } else {
      setCurrentState('LISTENING');
      addVoiceCommand({
        command: 'Voice activated',
        confidence: 1.0,
        timestamp: new Date().toISOString(),
        action: 'VOICE_START',
        parameters: {},
      });
    }
  };

  return (
    <button
      onClick={handleToggle}
      className={`
        p-3 rounded-full backdrop-blur-md border transition-all duration-300
        flex items-center justify-center w-12 h-12
        ${isListening
          ? 'bg-green-500/30 border-green-400 animate-pulse'
          : 'bg-black/60 border-white/20 hover:border-white/40'
        }
      `}
      title={isListening ? 'Stop Listening' : 'Start Voice Control'}
    >
      <svg
        className={`w-6 h-6 ${isListening ? 'text-green-400' : 'text-gray-400'}`}
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={2}
          d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"
        />
      </svg>
    </button>
  );
}

export default OrbNavigation;
