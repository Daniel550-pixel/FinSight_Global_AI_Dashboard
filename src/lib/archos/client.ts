import { ArchOSClient, GroundScanLayer, SiteIntelligence, LayerType, Scale } from './types';
import * as turf from '@turf/turf';

// ── MODE SWITCHING ──
type ClientMode = 'MOCK' | 'LIVE';
const MODE: ClientMode = (import.meta.env.VITE_ARCHOS_CLIENT_MODE as ClientMode) || 'MOCK';

export const isMock = () => MODE === 'MOCK';

// ── REAL CLIENT (Stub) ──
class RealArchOSClient implements ArchOSClient {
  private baseUrl: string;
  private token?: string;

  constructor() {
    this.baseUrl = import.meta.env.VITE_ARCHOS_API_URL?.replace(/\/$/, '') || '';
    this.token = import.meta.env.VITE_ARCHOS_API_TOKEN;
  }

  private async fetch<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const headers: Record<string, string> = { 'Content-Type': 'application/json' };
    if (this.token) headers['Authorization'] = `Bearer ${this.token}`;
    const res = await fetch(`${this.baseUrl}${endpoint}`, { ...options, headers });
    if (!res.ok) throw new Error(`ArchOS API ${res.status}: ${res.statusText}`);
    return res.json();
  }

  async getGroundScanLayers(locationId: string, types?: LayerType[]): Promise<GroundScanLayer[]> {
    const params = new URLSearchParams();
    if (types?.length) params.set('types', types.join(','));
    return this.fetch(`/v1/groundscan/${locationId}/layers?${params}`);
  }

  async getSiteIntelligence(locationId: string): Promise<SiteIntelligence> {
    return this.fetch(`/v1/intelligence/site/${locationId}`);
  }

  async querySpatial(filter: GeoJSON.Geometry, scale: Scale): Promise<SiteIntelligence[]> {
    return this.fetch('/v1/intelligence/query-spatial', {
      method: 'POST',
      body: JSON.stringify({ filter, scale })
    });
  }
}

// ── MOCK CLIENT ──
class MockArchOSClient implements ArchOSClient {
  private delay = (ms: number) => new Promise(res => setTimeout(res, ms));

  async getGroundScanLayers(locationId: string, types?: LayerType[]): Promise<GroundScanLayer[]> {
    await this.delay(450);
    const all: GroundScanLayer[] = [
      { id: 'terrain', type: 'TERRAIN', name: 'Elevation & Topography', features: [], provenance: { source: 'OBSERVATION', timestamp: '2026-08-10T08:00:00Z' }, confidence: 0.94, lastUpdated: '2026-08-10' },
      { id: 'infra', type: 'INFRASTRUCTURE', name: 'Roads & Transit Corridors', features: [], provenance: { source: 'OBSERVATION', timestamp: '2026-08-09T14:20:00Z' }, confidence: 0.98, lastUpdated: '2026-08-09' },
      { id: 'utils', type: 'UTILITIES', name: 'Subsurface Utilities', features: [], provenance: { source: 'INFERENCE', timestamp: '2026-08-08T11:00:00Z', modelVersion: 'v2.4' }, confidence: 0.76, lastUpdated: '2026-08-08' },
      { id: 'planning', type: 'PLANNING', name: 'Zoning & FAR Limits', features: [], provenance: { source: 'OBSERVATION', timestamp: '2026-07-15T09:00:00Z' }, confidence: 1.0, lastUpdated: '2026-07-15' },
      { id: 'constraints', type: 'CONSTRAINTS', name: 'Development Constraints', features: [], provenance: { source: 'PREDICTION', timestamp: '2026-08-11T07:30:00Z', agentId: 'compliance-agent' }, confidence: 0.88, lastUpdated: '2026-08-11' },
    ];
    return types ? all.filter(l => types.includes(l.type)) : all;
  }

  async getSiteIntelligence(locationId: string): Promise<SiteIntelligence> {
    await this.delay(600);
    return {
      locationId,
      emirate: 'Dubai',
      scale: 'SITE',
      constraints: [
        { id: 'c1', type: 'SETBACK', severity: 'HIGH', description: '15m front setback from main corridor per RTA masterplan', regulatoryReference: 'RTA-2024-SEC4' },
        { id: 'c2', type: 'UTILITY_EASEMENT', severity: 'MEDIUM', description: '2.5m clearance required over DEWA fiber corridor', geometry: turf.buffer(turf.point([55.27, 25.20]), 0.0002, { units: 'kilometers' }) }
      ],
      opportunities: [
        { id: 'o1', type: 'TRANSIT_ORIENTED', score: 0.91, description: 'High footfall zone within 400m of Metro Blue Line station', recommendedAction: 'Prioritize mixed-use ground floor retail + F&B' },
        { id: 'o2', type: 'SOLAR_POTENTIAL', score: 0.84, description: 'South-facing roof exposure > 70% annual yield', recommendedAction: 'Allocate 40% roof area for PV integration' }
      ],
      generativeHints: { maxHeight: '120m', preferredOrientation: 'North-South', suggestedFAR: 4.2, windMitigation: 'Aerodynamic corner tapering recommended' },
      provenance: { source: 'SIMULATION', timestamp: '2026-08-12T10:15:00Z', agentId: 'uae-urban-intelligence-agent' }
    };
  }

  async querySpatial(filter: GeoJSON.Geometry, scale: Scale): Promise<SiteIntelligence[]> {
    await this.delay(800);
    return [await this.getSiteIntelligence('mock-parcel-001')];
  }
}

// ── EXPORTED INSTANCE ──
export const client: ArchOSClient = MODE === 'MOCK' ? new MockArchOSClient() : new RealArchOSClient();
