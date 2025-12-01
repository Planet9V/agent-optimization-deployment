'use client';

import { Select, SelectItem, Text } from '@tremor/react';

const SECTORS: Record<string, string[]> = {
  'Infrastructure': ['Water', 'Transportation', 'Power Grid'],
  'Industrial Controls': ['SCADA', 'PLC', 'DCS', 'HMI'],
  'Healthcare': ['Medical Devices', 'Patient Data', 'Lab Systems'],
  'Energy': ['Oil & Gas', 'Nuclear', 'Renewable'],
  'Financial': ['Banking', 'Trading', 'Payment Systems'],
  'Government': ['Federal', 'State', 'Local', 'Military']
};

interface Props {
  sector: string;
  subsector: string;
  onSectorChange: (s: string) => void;
  onSubsectorChange: (s: string) => void;
}

export default function SectorClassifier({ sector, subsector, onSectorChange, onSubsectorChange }: Props) {
  return (
    <div className="space-y-4">
      <div>
        <Text>Sector *</Text>
        <Select value={sector} onValueChange={onSectorChange} className="mt-2">
          {Object.keys(SECTORS).map(s => (
            <SelectItem key={s} value={s}>{s}</SelectItem>
          ))}
        </Select>
      </div>

      {sector && (
        <div>
          <Text>Subsector (Optional)</Text>
          <Select value={subsector} onValueChange={onSubsectorChange} className="mt-2">
            {SECTORS[sector].map(sub => (
              <SelectItem key={sub} value={sub}>{sub}</SelectItem>
            ))}
          </Select>
        </div>
      )}
    </div>
  );
}
