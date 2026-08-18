import React, { useState } from 'react';
import { AlertCircle, TrendingUp, ChevronRight, Box, ShieldCheck, Zap } from 'lucide-react';
import { SiteIntelligence, SiteConstraint, SiteOpportunity } from '@/lib/archos/types';

interface SiteIntelligencePanelProps {
  intelligence: SiteIntelligence | null;
  onClose: () => void;
}

function ConstraintCard({ constraint }: { constraint: SiteConstraint }) {
  const severityColor = 
    constraint.severity === 'CRITICAL' ? 'text-red-400 border-red-500/30 bg-red-500/10' :
    constraint.severity === 'HIGH' ? 'text-orange-400 border-orange-500/30 bg-orange-500/10' :
    'text-amber-400 border-amber-500/30 bg-amber-500/10';

  return (
    <div className="p-3 rounded-lg border border-[#ffffff]/10 bg-[#0c0c0c]/50 mb-2 group hover:border-[#ff006e]/30 transition-all">
      <div className="flex items-start justify-between mb-1">
        <div className="flex items-center gap-2">
          <AlertCircle size={14} className="text-[#ff006e]" />
          <span className="text-xs font-mono font-bold text-[#f0f4f4]">{constraint.type}</span>
        </div>
        <span className={`px-1.5 py-0.5 rounded text-[9px] font-mono border ${severityColor}`}>
          {constraint.severity}
        </span>
      </div>
      <p className="text-[10px] text-[#5a6478] font-mono leading-tight mb-2">{constraint.description}</p>
      {constraint.regulatoryReference && (
        <div className="flex items-center gap-1 text-[9px] text-[#00e5ff] font-mono opacity-70">
          <ShieldCheck size={10} /> {constraint.regulatoryReference}
        </div>
      )}
    </div>
  );
}

function OpportunityCard({ opportunity }: { opportunity: SiteOpportunity }) {
  return (
    <div className="p-3 rounded-lg border border-[#ffffff]/10 bg-[#0c0c0c]/50 mb-2 group hover:border-[#ffd700]/30 transition-all">
      <div className="flex items-start justify-between mb-1">
        <div className="flex items-center gap-2">
          <TrendingUp size={14} className="text-[#ffd700]" />
          <span className="text-xs font-mono font-bold text-[#f0f4f4]">{opportunity.type}</span>
        </div>
        <span className="text-[9px] font-mono text-[#ffd700]">
          SCORE: {Math.round(opportunity.score * 100)}
        </span>
      </div>
      <p className="text-[10px] text-[#5a6478] font-mono leading-tight mb-2">{opportunity.description}</p>
      {opportunity.recommendedAction && (
        <div className="flex items-start gap-1 text-[9px] text-[#00ff88] font-mono opacity-80">
          <ChevronRight size={10} className="mt-0.5 flex-shrink-0" />
          <span>RECOMMEND: {opportunity.recommendedAction}</span>
        </div>
      )}
    </div>
  );
}

export function SiteIntelligencePanel({ intelligence, onClose }: SiteIntelligencePanelProps) {
  const [activeTab, setActiveTab] = useState<'CONSTRAINTS' | 'OPPORTUNITIES' | 'HINTS'>('CONSTRAINTS');

  if (!intelligence) return null;

  return (
    <div className="absolute top-4 right-4 w-80 max-h-[85vh] overflow-hidden z-10 rounded-xl border border-[#00e5ff]/30 bg-[#0c0c0c]/90 backdrop-blur-xl shadow-[0_0_20px_rgba(0,229,255,0.1)] flex flex-col">
      {/* Header */}
      <div className="p-3 border-b border-[#00e5ff]/20 flex items-center justify-between">
        <div className="flex flex-col">
          <span className="text-xs font-mono font-bold tracking-wider text-[#f0f4f4]">SITE INTELLIGENCE</span>
          <span className="text-[9px] text-[#00e5ff] font-mono">{intelligence.locationId} • {intelligence.scale}</span>
        </div>
        <button onClick={onClose} className="text-[#5a6478] hover:text-[#ff006e]"></button>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-[#ffffff]/10">
        {(['CONSTRAINTS', 'OPPORTUNITIES', 'HINTS'] as const).map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`flex-1 py-2 text-[9px] font-mono font-bold tracking-wider transition-colors ${
              activeTab === tab ? 'text-[#00e5ff] bg-[#00e5ff]/10' : 'text-[#5a6478] hover:text-[#f0f4f4]'
            }`}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-3">
        {activeTab === 'CONSTRAINTS' && (
          <div>
            <div className="text-[9px] text-[#5a6478] font-mono mb-2 uppercase tracking-wide">Detected Constraints ({intelligence.constraints.length})</div>
            {intelligence.constraints.map(c => <ConstraintCard key={c.id} constraint={c} />)}
            {intelligence.constraints.length === 0 && <div className="text-xs text-[#5a6478] font-mono text-center py-4">No critical constraints found.</div>}
          </div>
        )}

        {activeTab === 'OPPORTUNITIES' && (
          <div>
            <div className="text-[9px] text-[#5a6478] font-mono mb-2 uppercase tracking-wide">Value Opportunities ({intelligence.opportunities.length})</div>
            {intelligence.opportunities.map(o => <OpportunityCard key={o.id} opportunity={o} />)}
          </div>
        )}

        {activeTab === 'HINTS' && (
          <div>
            <div className="text-[9px] text-[#5a6478] font-mono mb-2 uppercase tracking-wide">Generative Design Hints</div>
            <div className="p-3 rounded-lg border border-[#ffd700]/20 bg-[#ffd700]/5">
              {Object.entries(intelligence.generativeHints).map(([key, value]) => (
                <div key={key} className="flex items-start gap-2 mb-2 last:mb-0">
                  <Box size={12} className="text-[#ffd700] mt-0.5 flex-shrink-0" />
                  <div>
                    <span className="text-[10px] text-[#f0f4f4] font-mono font-bold">{key.replace(/([A-Z])/g, ' $1').toUpperCase()}</span>
                    <span className="text-[10px] text-[#ffd700] font-mono block">: {String(value)}</span>
                  </div>
                </div>
              ))}
            </div>
            <div className="mt-3 pt-3 border-t border-[#ffffff]/10 text-[9px] text-[#5a6478] font-mono">
              PROVENANCE: {intelligence.provenance.agentId || 'SYSTEM'}<br/>
              TIMESTAMP: {new Date(intelligence.provenance.timestamp).toLocaleTimeString()}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
