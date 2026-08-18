import React, { useState } from 'react';
import { Eye, EyeOff, AlertTriangle, Shield, Zap, Globe, Layers, ChevronDown, ChevronUp } from 'lucide-react';
import { GroundScanLayer } from '@/lib/archos/types';

interface LayerControllerProps {
  layers: GroundScanLayer[];
  visibleLayers: string[];
  onToggleLayer: (layerId: string) => void;
}

const LAYER_ICONS = {
  TERRAIN: Globe,
  INFRASTRUCTURE: Layers,
  UTILITIES: Zap,
  PLANNING: Shield,
  CONSTRAINTS: AlertTriangle,
};

const CONFIDENCE_COLOR = (c: number) => {
  if (c >= 0.9) return 'bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.5)]';
  if (c >= 0.7) return 'bg-amber-500 shadow-[0_0_8px_rgba(245,158,11,0.5)]';
  return 'bg-red-500 shadow-[0_0_8px_rgba(239,68,68,0.5)]';
};

export function LayerController({ layers, visibleLayers, onToggleLayer }: LayerControllerProps) {
  const [isCollapsed, setIsCollapsed] = useState(false);

  if (isCollapsed) {
    return (
      <button
        onClick={() => setIsCollapsed(false)}
        className="absolute top-4 left-4 z-10 w-10 h-10 rounded-full bg-[#0c0c0c]/80 border border-[#00e5ff]/30 backdrop-blur-md flex items-center justify-center text-[#00e5ff] hover:bg-[#00e5ff]/20 transition-all"
      >
        <Layers size={18} />
      </button>
    );
  }

  return (
    <div className="absolute top-4 left-4 w-72 max-h-[80vh] overflow-y-auto z-10 rounded-xl border border-[#00e5ff]/30 bg-[#0c0c0c]/90 backdrop-blur-xl shadow-[0_0_20px_rgba(0,229,255,0.1)]">
      {/* Header */}
      <div className="flex items-center justify-between p-3 border-b border-[#00e5ff]/20">
        <div className="flex items-center gap-2">
          <Layers size={16} className="text-[#00e5ff]" />
          <span className="text-xs font-mono font-bold tracking-wider text-[#f0f4f4]">GROUNDSCAN LAYERS</span>
        </div>
        <button onClick={() => setIsCollapsed(true)} className="text-[#5a6478] hover:text-[#00e5ff]">
          <ChevronUp size={14} />
        </button>
      </div>

      {/* Layer List */}
      <div className="p-2 space-y-1">
        {layers.map((layer) => {
          const Icon = LAYER_ICONS[layer.type] || Layers;
          const isVisible = visibleLayers.includes(layer.id);
          return (
            <div
              key={layer.id}
              onClick={() => onToggleLayer(layer.id)}
              className={`group flex items-center justify-between p-2 rounded-lg cursor-pointer transition-all duration-200 ${
                isVisible ? 'bg-[#00e5ff]/10 border border-[#00e5ff]/30' : 'border border-transparent hover:bg-[#ffffff]/5'
              }`}
            >
              <div className="flex items-center gap-3">
                <div className={`w-8 h-8 rounded-md flex items-center justify-center ${isVisible ? 'bg-[#00e5ff]/20 text-[#00e5ff]' : 'bg-[#ffffff]/5 text-[#5a6478]'}`}>
                  <Icon size={14} />
                </div>
                <div className="flex flex-col">
                  <span className={`text-xs font-mono font-bold ${isVisible ? 'text-[#f0f4f4]' : 'text-[#5a6478]'}`}>
                    {layer.name}
                  </span>
                  <span className="text-[9px] text-[#5a6478]">
                    {layer.provenance.source} • {Math.round(layer.confidence * 100)}%
                  </span>
                </div>
              </div>
              
              {/* Visibility Toggle & Confidence Dot */}
              <div className="flex items-center gap-2">
                <div className={`w-1.5 h-1.5 rounded-full ${CONFIDENCE_COLOR(layer.confidence)}`} />
                {isVisible ? <Eye size={14} className="text-[#00e5ff]" /> : <EyeOff size={14} className="text-[#5a6478]" />}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
