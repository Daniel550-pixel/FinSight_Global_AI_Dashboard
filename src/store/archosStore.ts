import { create } from 'zustand';
import { GroundScanLayer, SiteIntelligence } from '@/lib/archos/types';

interface ArchOSState {
  // UI State
  activeLocationId: string;
  visibleLayers: string[];
  selectedEntityId: string | null;
  intelligence: SiteIntelligence | null;
  layers: GroundScanLayer[];
  
  // Connection State
  wsConnected: boolean;
  lastSyncTimestamp: number | null;

  // Actions
  setActiveLocation: (id: string) => void;
  toggleLayer: (layerId: string) => void;
  setSelectedEntity: (id: string | null) => void;
  setIntelligence: (data: SiteIntelligence | null) => void;
  setLayers: (layers: GroundScanLayer[]) => void;
  setWsConnected: (connected: boolean) => void;
  updateSyncTimestamp: () => void;
}

export const useArchOSStore = create<ArchOSState>((set) => ({
  activeLocationId: 'loc-dxb-downtown-01',
  visibleLayers: ['terrain', 'planning', 'constraints'],
  selectedEntityId: null,
  intelligence: null,
  layers: [],
  wsConnected: false,
  lastSyncTimestamp: null,

  setActiveLocation: (id) => set({ activeLocationId: id }),
  toggleLayer: (layerId) => set((state) => ({
    visibleLayers: state.visibleLayers.includes(layerId)
      ? state.visibleLayers.filter(l => l !== layerId)
      : [...state.visibleLayers, layerId]
  })),
  setSelectedEntity: (id) => set({ selectedEntityId: id }),
  setIntelligence: (data) => set({ intelligence: data }),
  setLayers: (layers) => set({ layers }),
  setWsConnected: (connected) => set({ wsConnected: connected }),
  updateSyncTimestamp: () => set({ lastSyncTimestamp: Date.now() }),
}));
