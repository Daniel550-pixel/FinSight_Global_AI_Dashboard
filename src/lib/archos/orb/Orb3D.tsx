/**
 * ArchOS 3D Orb Component
 * Interactive Three.js orb with voice, gesture, and quantum security visualization
 */

import React, { useRef, useMemo } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { Sphere, OrbitControls, Text } from '@react-three/drei';
import * as THREE from 'three';
import { useOrbSystem } from './useOrbSystem';
import type { MiniOrb, OrbState } from './types';

interface OrbMaterialProps {
  color: string;
  state: OrbState;
  quantumShieldEnabled: boolean;
  glowIntensity: number;
}

function OrbMaterial({ color, state, quantumShieldEnabled, glowIntensity }: OrbMaterialProps) {
  const meshRef = useRef<THREE.Mesh>(null);
  const shieldRef = useRef<THREE.Mesh>(null);

  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.rotation.y += 0.002;
      meshRef.current.rotation.x += 0.001;
      
      // Pulse effect based on state
      const pulse = Math.sin(state.clock.elapsedTime * 2) * 0.1 + 1;
      meshRef.current.scale.setScalar(pulse * glowIntensity);
    }

    if (shieldRef.current && quantumShieldEnabled) {
      shieldRef.current.rotation.y -= 0.005;
      shieldRef.current.rotation.z += 0.003;
    }
  });

  const getStateColor = () => {
    switch (state) {
      case 'LISTENING': return '#00ff88';
      case 'PROCESSING': return '#fbbf24';
      case 'ERROR': return '#ef4444';
      case 'SECURITY_ALERT': return '#dc2626';
      default: return color;
    }
  };

  return (
    <>
      {/* Main Orb */}
      <Sphere ref={meshRef} args={[1, 64, 64]}>
        <meshStandardMaterial
          color={getStateColor()}
          emissive={getStateColor()}
          emissiveIntensity={0.5}
          transparent
          opacity={0.9}
          roughness={0.2}
          metalness={0.8}
        />
      </Sphere>

      {/* Quantum Shield Layer */}
      {quantumShieldEnabled && (
        <Sphere ref={shieldRef} args={[1.3, 32, 32]}>
          <meshPhysicalMaterial
            color="#00e5ff"
            emissive="#00e5ff"
            emissiveIntensity={0.3}
            transparent
            opacity={0.15}
            roughness={0.1}
            metalness={0.9}
            side={THREE.DoubleSide}
          />
        </Sphere>
      )}

      {/* Binary Encryption Ring */}
      {quantumShieldEnabled && (
        <mesh rotation={[Math.PI / 2, 0, 0]}>
          <torusGeometry args={[1.5, 0.02, 16, 100]} />
          <meshStandardMaterial
            color="#00ff88"
            emissive="#00ff88"
            emissiveIntensity={0.8}
            transparent
            opacity={0.6}
          />
        </mesh>
      )}
    </>
  );
}

interface MiniOrbComponentProps {
  orb: MiniOrb;
  isSelected: boolean;
  onClick: () => void;
}

function MiniOrbComponent({ orb, isSelected, onClick }: MiniOrbComponentProps) {
  const meshRef = useRef<THREE.Mesh>(null);

  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.position.x = orb.position.x + Math.sin(state.clock.elapsedTime + orb.position.y) * 0.1;
      meshRef.current.position.y = orb.position.y + Math.cos(state.clock.elapsedTime + orb.position.x) * 0.1;
      meshRef.current.rotation.y += 0.01;
    }
  });

  return (
    <group>
      {/* Connection Line to Central Orb */}
      {orb.connected && (
        <line>
          <bufferGeometry>
            <float32BufferAttribute
              attach="attributes-position"
              count={2}
              array={new Float32Array([0, 0, 0, orb.position.x, orb.position.y, orb.position.z])}
              itemSize={3}
            />
          </bufferGeometry>
          <lineBasicMaterial
            color={orb.color}
            transparent
            opacity={isSelected ? 0.8 : 0.3}
            linewidth={isSelected ? 2 : 1}
          />
        </line>
      )}

      {/* Mini Orb */}
      <Sphere
        ref={meshRef}
        args={[0.2, 32, 32]}
        position={[orb.position.x, orb.position.y, orb.position.z]}
        onClick={onClick}
        onPointerOver={() => (document.body.style.cursor = 'pointer')}
        onPointerOut={() => (document.body.style.cursor = 'auto')}
      >
        <meshStandardMaterial
          color={orb.color}
          emissive={orb.color}
          emissiveIntensity={orb.glowIntensity}
          transparent
          opacity={0.95}
          roughness={0.3}
          metalness={0.7}
        />
      </Sphere>

      {/* Label */}
      <Text
        position={[orb.position.x, orb.position.y + 0.4, orb.position.z]}
        fontSize={0.15}
        color={orb.color}
        anchorX="center"
        anchorY="middle"
        outlineWidth={0.02}
        outlineColor="#000000"
      >
        {orb.icon}
      </Text>
    </group>
  );
}

export interface Orb3DProps {
  className?: string;
  showControls?: boolean;
}

export function Orb3D({ className = '', showControls = true }: Orb3DProps) {
  const { state, selectMiniOrb, rotateOrb, setScale } = useOrbSystem();

  const handleWheel = (e: React.WheelEvent) => {
    e.preventDefault();
    setScale(state.scale + e.deltaY * 0.001);
  };

  return (
    <div className={`relative w-full h-full ${className}`} onWheel={handleWheel}>
      <Canvas camera={{ position: [0, 0, 6], fov: 50 }}>
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} intensity={1} />
        <pointLight position={[-10, -10, -10]} intensity={0.5} color="#00e5ff" />
        
        {/* Central Orb */}
        <OrbMaterial
          color="#3b82f6"
          state={state.currentState}
          quantumShieldEnabled={state.securityStatus.quantumShieldEnabled}
          glowIntensity={state.miniOrbs.find(o => o.mode === state.currentMode)?.glowIntensity || 0.7}
        />

        {/* Mini Orbs */}
        {state.miniOrbs.map((orb) => (
          <MiniOrbComponent
            key={orb.id}
            orb={orb}
            isSelected={state.selectedMiniOrb === orb.id}
            onClick={() => selectMiniOrb(orb.id)}
          />
        ))}

        {/* Controls */}
        {showControls && (
          <OrbitControls
            enableZoom={true}
            enablePan={false}
            minDistance={3}
            maxDistance={10}
            onChange={(e) => {
              const target = e.target as any;
              rotateOrb(target.rotation.x, target.rotation.y, 0);
            }}
          />
        )}

        {/* Particle System Background */}
        <Particles />
      </Canvas>

      {/* Security Status Overlay */}
      {state.config.showSecurityIndicator && (
        <div className="absolute top-4 right-4 bg-black/60 backdrop-blur-md rounded-lg p-3 border border-cyan-500/30">
          <div className="flex items-center gap-2">
            <div
              className={`w-3 h-3 rounded-full ${
                state.securityStatus.quantumShieldEnabled
                  ? 'bg-cyan-400 animate-pulse'
                  : 'bg-red-500'
              }`}
            />
            <span className="text-xs text-cyan-100 font-mono">
              {state.securityStatus.quantumShieldEnabled ? 'QUANTUM SHIELD ACTIVE' : 'SHIELD DISABLED'}
            </span>
          </div>
          <div className="mt-2 text-xs text-gray-400">
            <div>Encryption: AES-256-GCM + ChaCha20</div>
            <div>Threat Level: {state.securityStatus.threatLevel}</div>
          </div>
        </div>
      )}

      {/* Voice Command History */}
      {state.voiceCommands.length > 0 && (
        <div className="absolute bottom-4 left-4 bg-black/60 backdrop-blur-md rounded-lg p-3 border border-purple-500/30 max-w-xs">
          <div className="text-xs text-purple-200 font-mono mb-2">VOICE COMMANDS</div>
          {state.voiceCommands.slice(-3).map((cmd, idx) => (
            <div key={idx} className="text-xs text-gray-400 truncate">
              {cmd.command}
            </div>
          ))}
        </div>
      )}

      {/* Current Mode Indicator */}
      <div className="absolute top-4 left-4 bg-black/60 backdrop-blur-md rounded-lg p-3 border border-blue-500/30">
        <div className="text-xs text-blue-200 font-mono">CURRENT MODE</div>
        <div className="text-lg text-white font-bold">{state.currentMode}</div>
      </div>
    </div>
  );
}

function Particles() {
  const particlesRef = useRef<THREE.Points>(null);
  const particleCount = 500;

  const positions = useMemo(() => {
    const pos = new Float32Array(particleCount * 3);
    for (let i = 0; i < particleCount * 3; i++) {
      pos[i] = (Math.random() - 0.5) * 20;
    }
    return pos;
  }, []);

  useFrame((state) => {
    if (particlesRef.current) {
      particlesRef.current.rotation.y = state.clock.elapsedTime * 0.05;
      particlesRef.current.rotation.x = state.clock.elapsedTime * 0.02;
    }
  });

  return (
    <points ref={particlesRef}>
      <bufferGeometry>
        <float32BufferAttribute
          attach="attributes-position"
          count={particleCount}
          array={positions}
          itemSize={3}
        />
      </bufferGeometry>
      <pointsMaterial
        size={0.05}
        color="#00e5ff"
        transparent
        opacity={0.6}
        sizeAttenuation
      />
    </points>
  );
}

export default Orb3D;
