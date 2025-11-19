"use client";

import { Select, SelectItem } from "@tremor/react";

interface SectorClassifierProps {
  sector: string;
  subsector: string;
  onSectorChange: (sector: string) => void;
  onSubsectorChange: (subsector: string) => void;
}

const SECTORS = {
  Infrastructure: ["Water", "Transportation", "Power Grid", "Telecommunications"],
  "Industrial Controls": ["SCADA", "PLC", "DCS", "HMI"],
  Healthcare: ["Medical Devices", "Patient Data", "Lab Systems", "Pharmaceuticals"],
  Energy: ["Oil & Gas", "Nuclear", "Renewable", "Distribution"],
  Financial: ["Banking", "Trading", "Payment Systems", "Insurance"],
  Government: ["Federal", "State", "Local", "Military"],
} as const;

export default function SectorClassifier({
  sector,
  subsector,
  onSectorChange,
  onSubsectorChange,
}: SectorClassifierProps) {
  const handleSectorChange = (value: string) => {
    onSectorChange(value);
    onSubsectorChange("");
  };

  const subsectorOptions = sector && SECTORS[sector as keyof typeof SECTORS] 
    ? SECTORS[sector as keyof typeof SECTORS] 
    : [];

  return (
    <div className="space-y-4">
      <h3 className="text-tremor-default font-medium text-tremor-content-strong dark:text-dark-tremor-content-strong">
        Classify Document Sector
      </h3>

      <div className="space-y-3">
        <div>
          <label className="text-tremor-default font-medium text-tremor-content dark:text-dark-tremor-content mb-1.5 block">
            Select Sector <span className="text-red-500">*</span>
          </label>
          <Select
            value={sector}
            onValueChange={handleSectorChange}
            placeholder="Select Sector"
          >
            {Object.keys(SECTORS).map((sectorName) => (
              <SelectItem key={sectorName} value={sectorName}>
                {sectorName}
              </SelectItem>
            ))}
          </Select>
        </div>

        {sector && subsectorOptions.length > 0 && (
          <div>
            <label className="text-tremor-default font-medium text-tremor-content dark:text-dark-tremor-content mb-1.5 block">
              Select Subsector (Optional)
            </label>
            <Select
              value={subsector}
              onValueChange={onSubsectorChange}
              placeholder="Select Subsector (Optional)"
            >
              {subsectorOptions.map((subsectorName) => (
                <SelectItem key={subsectorName} value={subsectorName}>
                  {subsectorName}
                </SelectItem>
              ))}
            </Select>
          </div>
        )}
      </div>
    </div>
  );
}
