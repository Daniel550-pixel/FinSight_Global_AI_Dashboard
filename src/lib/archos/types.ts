export type Emirate = 'Abu Dhabi' | 'Dubai' | 'Sharjah' | 'Ajman' | 'Umm Al Quwain' | 'Ras Al Khaimah' | 'Fujairah';
export type LayerType = 'TERRAIN' | 'INFRASTRUCTURE' | 'UTILITIES' | 'PLANNING' | 'CONSTRAINTS' | 'OPPORTUNITIES';
export type ProvenanceSource = 'OBSERVATION' | 'INFERENCE' | 'PREDICTION' | 'SIMULATION';
export type Scale = 'CITY' | 'DISTRICT' | 'SITE' | 'PARCEL';

export interface GroundScanFeature {
  id: string;
  geometry: GeoJSON.Geometry;
  properties: Record<string, any>;
}

export interface GroundScanLayer {
  id: string;
  type: LayerType;
  name: string;
  features: GroundScanFeature[];
  provenance: { source: ProvenanceSource; timestamp: string; modelVersion?: string };
  confidence: number; // 0.0 to 1.0
  lastUpdated: string;
}

export interface SiteConstraint {
  id: string;
  type: string;
  severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  description: string;
  geometry?: GeoJSON.Geometry;
  regulatoryReference?: string;
}

export interface SiteOpportunity {
  id: string;
  type: string;
  score: number; // 0.0 to 1.0
  description: string;
  recommendedAction?: string;
}

export interface SiteIntelligence {
  locationId: string;
  emirate: Emirate;
  scale: Scale;
  constraints: SiteConstraint[];
  opportunities: SiteOpportunity[];
  generativeHints: Record<string, any>;
  provenance: { source: ProvenanceSource; timestamp: string; agentId?: string };
}

export interface ArchOSClient {
  getGroundScanLayers(locationId: string, types?: LayerType[]): Promise<GroundScanLayer[]>;
  getSiteIntelligence(locationId: string): Promise<SiteIntelligence>;
  querySpatial(filter: GeoJSON.Geometry, scale: Scale): Promise<SiteIntelligence[]>;
}
