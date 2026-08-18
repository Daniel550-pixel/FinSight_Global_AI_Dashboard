import { useEffect, useRef } from 'react';
import { useArchOSStore } from '@/store/archosStore';

export function useWorldModelSync() {
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout>();
  const { setWsConnected, updateSyncTimestamp } = useArchOSStore();
  const isLive = import.meta.env.VITE_ARCHOS_CLIENT_MODE === 'LIVE';

  useEffect(() => {
    if (!isLive) return;

    let cancelled = false;
    let reconnectAttempts = 0;

    const connect = () => {
      if (cancelled) return;

      const token = import.meta.env.VITE_ARCHOS_API_TOKEN;
      const url = `${import.meta.env.VITE_ARCHOS_API_URL}/ws/world-model?token=${token}`;
      
      wsRef.current = new WebSocket(url);

      wsRef.current.onopen = () => {
        reconnectAttempts = 0; // Reset on successful connection
        setWsConnected(true);
        console.log('[ArchOS] World Model WebSocket connected');
      };

      wsRef.current.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          // Route to store or command bus based on event type
          if (data.type === 'LAYER_UPDATE') {
            useArchOSStore.getState().setLayers(data.payload.layers);
          } else if (data.type === 'INTELLIGENCE_UPDATE') {
            useArchOSStore.getState().setIntelligence(data.payload.intelligence);
          }
          updateSyncTimestamp();
        } catch (err) {
          console.error('[ArchOS] WS message parse error:', err);
        }
      };

      wsRef.current.onclose = () => {
        if (cancelled) return; // Don't reconnect if intentionally closed
        
        setWsConnected(false);
        
        // Only reconnect on unexpected closes (not intentional teardown)
        const delay = Math.min(1000 * Math.pow(2, reconnectAttempts), 30000);
        reconnectAttempts++;
        reconnectTimeoutRef.current = setTimeout(connect, delay);
      };

      wsRef.current.onerror = (err) => {
        console.error('[ArchOS] WebSocket error:', err);
        if (!cancelled) {
          wsRef.current?.close();
        }
      };
    };

    connect();

    return () => {
      cancelled = true;
      if (reconnectTimeoutRef.current) clearTimeout(reconnectTimeoutRef.current);
      wsRef.current?.close();
      wsRef.current = null;
    };
  }, [isLive, setWsConnected, updateSyncTimestamp]);

  return { wsConnected: useArchOSStore(state => state.wsConnected) };
}
