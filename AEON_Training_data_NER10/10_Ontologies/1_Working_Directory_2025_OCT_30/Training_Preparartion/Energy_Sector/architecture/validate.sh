#!/bin/bash
echo "=== VALIDATION REPORT ==="
echo ""
for file in *.md; do
  echo "FILE: $file"
  words=$(wc -w < "$file")
  sections=$(grep -c "^## Section" "$file")
  vendors=$(grep -Eo "ABB|GE|Siemens|Schneider|Emerson|Honeywell|Yokogawa|Allen-Bradley|Rockwell|Mitsubishi|Schweitzer|SEL|Cisco|Palo Alto|Fortinet|Dell|HP|Intel|Oracle|Microsoft|IBM|Caterpillar|Cummins|OSIsoft|Ruggedcom|Moxa|Meinberg|Veritas|Vaisala|Sulzer|Flowserve|Pentair|Graver|Toshiba|Grundfos|Eaton|ASCO|Woodward|Bently Nevada|Kistler|Rosemount|Fisher|Spirax Sarco|Endress\+Hauser|Belimo|Alfa Laval|Highland|Garnet|Tenable|McAfee|BeyondTrust|Splunk|AspenTech|EPRI|Landis\+Gyr|Cooper Power|Verizon|AT\&T|CenturyLink|Ciena|Sierra Wireless|Aviat|Matrikon|SAP|Power BI" "$file" | wc -l)
  equipment=$(grep -Eo "Mark VIe|AC800M|PowerFlex|ControlLogix|DCS|SCADA|RTU|PLC|HMI|MCC|VFD|UPS|ATS|switchgear|transformer|generator|turbine|HRSG|relay|breaker|CT|VT|PMU|PDC|merging unit|recloser|capacitor bank|voltage regulator|diesel genset" "$file" | wc -l)
  arch_patterns=$(grep -Eio "architecture|topology|redundan[ct]|configuration|network|protocol|system|design|infrastructure|implementation|failover|hot standby|N\+1|TMR|IEC [0-9]|IEEE [0-9]|NERC CIP" "$file" | wc -l)
  
  echo "  Words: $words"
  echo "  Sections: $sections"
  echo "  Vendor mentions: $vendors"
  echo "  Equipment mentions: $equipment"
  echo "  Architecture patterns: $arch_patterns"
  echo ""
done
