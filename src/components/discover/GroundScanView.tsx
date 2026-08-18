import React, { useEffect } from 'react';
import { useGroundScan } from '@/hooks/useGroundScan';
import { useWorldModelSync } from '@/hooks/useWorldModelSync';
import { useArchOSStore } from '@/store/archosStore';
import { commandBus } from '@/lib/archos/commandBus';
import { LayerController } from './LayerController';
import { SiteIntelligencePanel } from './SiteIntelligencePanel';
import { MapContainer, TileLayer, GeoJSON } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

export function GroundScanView({ locationId }: { locationId?: string }) {
  const { activeLocationId, visibleLayers, intelligence, layers, setLayers, setIntelligence } = useArchOSStore();
  const { wsConnected } = useWorldModelSync();
  const targetId = locationId || activeLocationId;

  // Fetch initial data via swappable client
  const { loading, error, refresh } = useGroundScan(targetId, undefined, 'SITE');

  // Sync store with fetched data
  useEffect(() => {
    if (layers.length) setLayers(layers);
    if (intelligence) setIntelligence(intelligence);
  }, [layers, intelligence, setLayers, setIntelligence]);

  const handleToggleLayer = (layerId: string) => {
    commandBus.dispatch({ type: 'TOGGLE_LAYER', payload: { layerId }, source: 'ui' });
  };

  const handleRetry = () => {
    commandBus.dispatch({ type: 'REFRESH_INTELLIGENCE', payload: { locationId: targetId }, source: 'ui' });
  };

  if (error) {
    return (
      <div className="flex items-center justify-center h-full bg-[#0a0e1a] text-[#ff006e] font-mono">
        <div className="text-center">
          <p className="text-lg font-bold mb-2">INTELLIGENCE FEED ERROR</p>
          <p className="text-xs text-[#5a6478]">{error.message}</p>
          <button onClick={handleRetry} 
            className="mt-4 px-4 py-2 bg-[#00e5ff]/20 text-[#00e5ff] rounded hover:bg-[#00e5ff]/30">
            RETRY SYNC
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="relative w-full h-full bg-[#0a0e1a]">
      {/* Connection Status Indicator */}
      {import.meta.env.VITE_ARCHOS_CLIENT_MODE === 'LIVE' && (
        <div className={`absolute top-2 right-2 z-50 px-2 py-1 rounded text-[9px] font-mono ${
          wsConnected ? 'bg-[#00ff88]/20 text-[#00ff88] border border-[#00ff88]/40' : 'bg-[#ff006e]/20 text-[#ff006e] border border-[#ff006e]/40'
        }`}>
          {wsConnected ? '● WS LIVE' : '○ WS OFFLINE'}
        </div>
      )}

      <MapContainer 
        center={[25.1972, 55.2744]} 
        zoom={15} 
        className="w-full h-full z-0"
        zoomControl={false}
      >
        <TileLayer 
          url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
          attribution='&copy; OSM &copy; CARTO'
        />
        {layers.filter(l => visibleLayers.includes(l.id)).map(layer => (
          <GeoJSON 
            key={layer.id} 
            data={{ type: 'FeatureCollection', features: layer.features }}
            style={{ 
              color: layer.type === 'CONSTRAINTS' ? '#ff006e' : '#00e5ff',
              weight: 2,
              opacity: layer.confidence,
              dashArray: layer.type === 'UTILITIES' ? '5, 5' : undefined
            }}
          />
        ))}
      </MapContainer>

      <LayerController 
        layers={layers} 
        visibleLayers={visibleLayers} 
        onToggleLayer={handleToggleLayer} 
      />

      {intelligence && (
        <SiteIntelligencePanel intelligence={intelligence} onClose={() => useArchOSStore.getState().setSelectedEntity(null)} />
      )}

      {loading && (
        <div className="absolute inset-0 z-50 bg-[#0a0e1a]/60 backdrop-blur-sm flex items-center justify-center pointer-events-none">
          <div className="text-[#00e5ff] font-mono text-xs animate-pulse">
            SYNCING WORLD MODEL...
          </div>
        </div>
      )}
    </div>
  );
}
