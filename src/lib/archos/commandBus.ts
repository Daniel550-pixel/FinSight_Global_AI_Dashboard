import { EventEmitter } from 'events';
import { client } from './client';
import { useArchOSStore } from '@/store/archosStore';

export type CommandType = 
  | 'SELECT_ENTITY'
  | 'TOGGLE_LAYER'
  | 'UPDATE_VIEWPORT'
  | 'REFRESH_INTELLIGENCE'
  | 'VOICE_COMMAND'
  | 'GESTURE_INTERACTION';

export interface ArchOSCommand {
  type: CommandType;
  payload: Record<string, any>;
  source: 'ui' | 'voice' | 'gesture' | 'system';
  timestamp: number;
}

class CommandBus extends EventEmitter {
  private client = client;
  private store = useArchOSStore.getState;

  constructor() {
    super();
    this.initialize();
  }

  private initialize() {
    this.on('TOGGLE_LAYER', this.handleToggleLayer);
    this.on('SELECT_ENTITY', this.handleSelectEntity);
    this.on('REFRESH_INTELLIGENCE', this.handleRefreshIntelligence);
  }

  dispatch(command: Omit<ArchOSCommand, 'timestamp'>) {
    const fullCommand: ArchOSCommand = { ...command, timestamp: Date.now() };
    this.emit(fullCommand.type, fullCommand);
    // Audit log (sent to backend when live)
    if (import.meta.env.VITE_ARCHOS_CLIENT_MODE === 'LIVE') {
      fetch('/api/v1/audit/command', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(fullCommand)
      }).catch(console.error);
    }
  }

  private handleToggleLayer = ({ payload }: ArchOSCommand) => {
    this.store().toggleLayer(payload.layerId);
  };

  private handleSelectEntity = ({ payload }: ArchOSCommand) => {
    this.store().setSelectedEntity(payload.entityId);
    // Trigger intelligence fetch if needed
    if (payload.entityId && !this.store().intelligence) {
      this.dispatch({ type: 'REFRESH_INTELLIGENCE', payload: { locationId: payload.entityId }, source: 'system' });
    }
  };

  private handleRefreshIntelligence = async ({ payload }: ArchOSCommand) => {
    try {
      const intelligence = await this.client.getSiteIntelligence(payload.locationId);
      this.store().setIntelligence(intelligence);
    } catch (err) {
      console.error('Failed to refresh intelligence:', err);
    }
  };
}

export const commandBus = new CommandBus();
