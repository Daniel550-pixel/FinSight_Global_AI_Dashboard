import { useState, useEffect, useCallback } from 'react';
import { client } from '@/lib/archos/client';
import { GroundScanLayer, SiteIntelligence, LayerType, Scale } from '@/lib/archos/types';
import { useArchOSStore } from '@/store/archosStore';

export function useGroundScan(locationId: string, layerTypes?: LayerType[], scale: Scale = 'SITE') {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  const { setLayers, setIntelligence } = useArchOSStore();

  const refresh = useCallback(() => {
    if (!locationId) return;
    setLoading(true);
    setError(null);

    Promise.all([
      client.getGroundScanLayers(locationId, layerTypes),
      client.getSiteIntelligence(locationId)
    ])
      .then(([layers, intelligence]) => { 
        setLayers(layers); 
        setIntelligence(intelligence);
      })
      .catch(e => setError(e as Error))
      .finally(() => setLoading(false));
  }, [locationId, layerTypes?.join(','), scale, setLayers, setIntelligence]);

  useEffect(() => { refresh(); }, [refresh]);

  return { loading, error, refresh };
}
