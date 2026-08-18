# ArchOS 3D Orb Navigation System

## Overview

A revolutionary **3D spatial interface** that replaces traditional menus with an interactive Orb system featuring voice control, hand/finger tracking, gesture recognition, and quantum security visualization.

## Features

### 🌐 Central Orb System
- **Interactive 3D Orb** with real-time animations
- **8 Mini Orbs** connected via energy tethers representing different modules:
  - 🔍 **Discover** - Ground scan and site intelligence
  - 🎨 **Design** - AI-powered design tools
  - ⚙️ **Build** - Code generation and LLM vault
  - 🚀 **Deploy** - Deployment pipeline management
  - 📊 **Monitor** - System monitoring and analytics
  - 🛡️ **Security** - Quantum encryption status
  - 🌐 **Languages** - 60+ programming language support
  - 🧠 **AI Vault** - LLM model management

### 🎤 Voice Control
- Natural language commands
- Real-time speech recognition
- Command history tracking
- Sensitivity adjustment

**Supported Commands:**
- "Switch to Design/Build/Deploy/Monitor"
- "Select Security/Languages/AI Vault"
- "Rotate left/right"
- "Zoom in/out"
- "Enable/disable security shield"

### ✋ Gesture Recognition
- **Pinch** - Activate/Process
- **Expand** - Zoom in
- **Swipe Left/Right** - Rotate orb
- **Tap** - Select/Confirm
- **Hover** - Preview

### 🛡️ Quantum Security Visualization
- **Quantum Shield Layer** - Visible when active (cyan glow)
- **Binary Encryption Ring** - Rotating ring showing AES-256 + ChaCha20
- **Real-time Threat Monitoring** - Color-coded status
- **Security Status Overlay** - Live encryption metrics

## Installation

```bash
npm install three @react-three/fiber @react-three/drei
```

## Quick Start

### 1. Import the Orb Navigation

```tsx
import { OrbNavigation } from '@/components/orb';

function App() {
  return <OrbNavigation />;
}
```

### 2. Use as Full-Screen Navigation

```tsx
import { OrbNavigation } from '@/components/orb';
import type { OrbMode } from '@/lib/archos/orb';

function Dashboard() {
  const handleModeChange = (mode: OrbMode) => {
    console.log('Current mode:', mode);
    // Switch your app's view based on mode
  };

  return (
    <div className="h-screen w-screen">
      <OrbNavigation onModeChange={handleModeChange} />
    </div>
  );
}
```

### 3. Access Orb System Directly

```tsx
import { useOrbSystem, Orb3D } from '@/lib/archos/orb';

function CustomOrbInterface() {
  const { state, setMode, selectMiniOrb, toggleQuantumShield } = useOrbSystem();

  return (
    <div>
      <Orb3D />
      <button onClick={() => setMode('DESIGN')}>Design Mode</button>
      <button onClick={toggleQuantumShield}>Toggle Security</button>
    </div>
  );
}
```

## API Reference

### `useOrbSystem()` Hook

Returns:
- `state` - Current orb system state
- `setMode(mode)` - Switch to a specific mode
- `selectMiniOrb(orbId)` - Select a mini orb
- `rotateOrb(pitch, yaw, roll)` - Rotate the central orb
- `setScale(scale)` - Zoom level (0.5 - 3)
- `toggleQuantumShield()` - Enable/disable quantum encryption
- `updatePosition(position)` - Update orb position
- `updateConfig(config)` - Update system configuration
- `startListening()` - Start voice recognition
- `stopListening()` - Stop voice recognition

### State Structure

```typescript
interface OrbSystemState {
  currentState: 'IDLE' | 'ACTIVE' | 'LISTENING' | 'PROCESSING' | 'ERROR' | 'SECURITY_ALERT';
  currentMode: 'DISCOVER' | 'DESIGN' | 'BUILD' | 'DEPLOY' | 'MONITOR';
  position: { x: number; y: number; z: number };
  rotation: { pitch: number; yaw: number; roll: number };
  scale: number;
  miniOrbs: MiniOrb[];
  selectedMiniOrb: string | null;
  voiceCommands: VoiceCommand[];
  handTracking: HandTrackingData | null;
  config: OrbSystemConfig;
  securityStatus: SecurityStatus;
  interactions: OrbInteractionEvent[];
}
```

## Configuration

```typescript
const config: OrbSystemConfig = {
  enableVoice: true,           // Enable voice recognition
  enableHandTracking: true,    // Enable hand/gesture tracking
  enableGestureControl: true,  // Enable gesture-based controls
  sensitivity: 0.75,           // Voice recognition sensitivity (0-1)
  securityLevel: 'QUANTUM',    // 'STANDARD' | 'ENHANCED' | 'QUANTUM'
  showSecurityIndicator: true, // Show security status overlay
};
```

## Integration with GroundScan

The Orb system integrates seamlessly with the ArchOS GroundScan layer:

```tsx
import { OrbNavigation } from '@/components/orb';
import { GroundScanMap } from '@/components/maps/GroundScanMap';
import type { OrbMode } from '@/lib/archos/orb';

function IntegratedDashboard() {
  const [currentMode, setCurrentMode] = React.useState<OrbMode>('DISCOVER');

  return (
    <div className="relative h-screen">
      {/* Orb Navigation Layer */}
      <OrbNavigation onModeChange={setCurrentMode} />
      
      {/* Mode-Specific Content */}
      {currentMode === 'DISCOVER' && <GroundScanMap locationId="site-001" />}
      {currentMode === 'DESIGN' && <DesignStudio />}
      {currentMode === 'BUILD' && <CodeGenerator />}
      {currentMode === 'DEPLOY' && <DeploymentPipeline />}
      {currentMode === 'MONITOR' && <SystemMonitor />}
    </div>
  );
}
```

## Security Features

### Quantum Encryption Indicators
- **Cyan Pulsing Shield** - Quantum key distribution active
- **Green Binary Ring** - AES-256-GCM + ChaCha20 encryption
- **Red Alert** - Security threat detected

### Encryption Layers
1. **Post-Quantum Cryptography** - CRYSTALS-Kyber, CRYSTALS-Dilithium
2. **Binary Encryption** - AES-256-GCM + ChaCha20-Poly1305
3. **Homomorphic Encryption** - For secure computation
4. **Crypto-shredding** - Instant data deletion capability

## Accessibility

- Keyboard navigation support (Arrow keys, +/- for zoom)
- Screen reader announcements for mode changes
- Alternative button controls for all voice/gesture actions
- Adjustable sensitivity settings

## Performance

- 60 FPS target with optimized Three.js rendering
- Lazy loading for voice recognition
- Efficient gesture detection using requestAnimationFrame
- Particle system limited to 500 particles

## Browser Support

- Chrome 90+ (Web Speech API, WebGL 2.0)
- Firefox 88+
- Safari 14+
- Edge 90+

**Note:** Hand tracking requires additional setup with MediaPipe Hands or Leap Motion SDK.

## Future Enhancements

- [ ] AR/VR headset support (WebXR)
- [ ] Multi-user collaborative orb sessions
- [ ] Haptic feedback integration
- [ ] Advanced gesture library
- [ ] Custom orb themes and skins
- [ ] Spatial audio positioning
- [ ] Eye-tracking integration

## Troubleshooting

### Voice Recognition Not Working
- Ensure microphone permissions are granted
- Check browser compatibility for Web Speech API
- Try adjusting sensitivity in config

### Orb Not Rendering
- Verify Three.js dependencies are installed
- Check WebGL support in browser
- Ensure container has defined height/width

### Gestures Not Detected
- Integrate MediaPipe Hands or Leap Motion SDK
- Calibrate hand tracking sensitivity
- Ensure proper lighting conditions

## License

MIT © ArchOS Development Team
