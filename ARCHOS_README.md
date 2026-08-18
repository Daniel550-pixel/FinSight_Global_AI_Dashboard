# ArchOS DISCOVER/ GroundScan Implementation

## ✅ Production-Ready Frontend Architecture

This implementation provides a complete, type-safe frontend for the ArchOS World Model with:

### 🏗️ Architecture Components

1. **Swappable Client** (`src/lib/archos/client.ts`)
   - Zero-code-change switching between MOCK and LIVE modes
   - Environment-driven via `VITE_ARCHOS_CLIENT_MODE`
   - Mock client returns realistic UAE urban intelligence data
   - Real client stub ready for API gateway integration

2. **Unified Command Bus** (`src/lib/archos/commandBus.ts`)
   - Event-driven architecture for UI, voice, and gesture commands
   - Audit logging for compliance (LIVE mode only)
   - Never mutates state directly - routes through store

3. **Zustand Store** (`src/store/archosStore.ts`)
   - Type-safe global state management
   - Tracks layers, intelligence, connection status
   - Atomic updates with full TypeScript inference

4. **Real-Time Sync Hook** (`src/hooks/useWorldModelSync.ts`)
   - WebSocket subscription with exponential backoff
   - Auto-reconnect on connection loss
   - Routes events to store based on type

5. **GroundScan Hook** (`src/hooks/useGroundScan.ts`)
   - Fetches layers and intelligence via swappable client
   - Syncs results to Zustand store
   - Loading and error states included

### 🎨 UI Components

- **LayerController** - Toggle GroundScan layers with confidence indicators
- **SiteIntelligencePanel** - View constraints, opportunities, and generative hints
- **GroundScanView** - Main map view integrating all components

### 📁 File Structure

```
src/
├── lib/
│   └── archos/
│       ├── types.ts          # TypeScript contracts
│       ├── client.ts         # Swappable MOCK/LIVE client
│       └── commandBus.ts     # Event routing system
├── store/
│   └── archosStore.ts        # Global state management
├── hooks/
│   ├── useGroundScan.ts      # Data fetching hook
│   └── useWorldModelSync.ts  # WebSocket sync hook
└── components/
    └── discover/
        ├── LayerController.tsx
        ├── SiteIntelligencePanel.tsx
        └── GroundScanView.tsx
```

### 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   npm install zustand @turf/turf react-leaflet leaflet lucide-react
   npm install -D @types/geojson
   ```

2. **Configure environment:**
   - Edit `.env.local` to switch between MOCK and LIVE modes

3. **Use in your app:**
   ```tsx
   import { GroundScanView } from '@/components/discover/GroundScanView';

   function App() {
     return <GroundScanView locationId="loc-dxb-downtown-01" />;
   }
   ```

### 🔐 Security & Compliance

- **Zero-Trust**: Auth headers passed to all API/WS calls
- **Audit Trail**: Commands logged to `/api/v1/audit/command` in LIVE mode
- **Provenance Tracking**: Every data item includes source, timestamp, and agent ID
- **Confidence Scoring**: All layers and predictions include confidence metrics

### 🔄 Mode Switching

| Mode | Use Case | Data Source |
|------|----------|-------------|
| `MOCK` | Development, demos, testing | Simulated UAE intelligence |
| `LIVE` | Production deployment | Real ArchOS API gateway |

To switch: Change `VITE_ARCHOS_CLIENT_MODE` in `.env.local` and restart dev server.

### 📊 Data Contracts

All types enforce ArchOS principles:
- **Provenance**: Source (OBSERVATION/INFERENCE/PREDICTION/SIMULATION)
- **Confidence**: 0.0-1.0 score on all predictions
- **Scale Continuity**: CITY → DISTRICT → SITE → PARCEL
- **Lifecycle Awareness**: Timestamps and version tracking

### 🎯 Next Steps

1. **Backend Integration**: Deploy ArchOS API gateway and update `.env.local`
2. **3D Visualization**: Swap Leaflet for Three.js using same data contracts
3. **Voice/Gesture**: Wire Web Speech API and MediaPipe to command bus
4. **Real-Time Telemetry**: Connect IoT sensors to WebSocket stream

---

**Status**: ✅ Production-ready for MOCK mode, awaiting backend handshake for LIVE.
