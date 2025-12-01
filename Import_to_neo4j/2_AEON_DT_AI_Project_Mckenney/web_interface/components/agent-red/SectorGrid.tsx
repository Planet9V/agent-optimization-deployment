"use client";

import React from 'react';

const sectors = [
    {
        id: 1,
        name: "Chemical",
        icon: (
            <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.384-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
            </svg>
        ),
        details: "Honeywell/Emerson PLCs, SIS (Safety Instrumented Systems), Batch Processing Units. Vulnerable to logic modification causing thermal runaway."
    },
    {
        id: 2,
        name: "Commercial Facilities",
        icon: (
            <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
            </svg>
        ),
        details: "BMS (Building Management), HVAC Controllers (Johnson Controls), Access Control. Weak points: Default credentials on IoT gateways."
    },
    {
        id: 3,
        name: "Communications",
        icon: (
            <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M8.111 16.404a5.5 5.5 0 017.778 0M12 20h.01m-7.08-7.071c3.904-3.905 10.236-3.905 14.141 0M1.394 9.393c5.857-5.857 15.355-5.857 21.213 0" />
            </svg>
        ),
        details: "BGP Routing, MPLS Backbones, 5G Core, Tower Infrastructure. Targets: HLR/HSS databases and undersea cable landing stations."
    },
    {
        id: 4,
        name: "Critical Manufacturing",
        icon: (
            <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
        ),
        details: "Robotics (Fanuc, ABB), MES Systems, CNC Machines. Impact: Micro-defects in production line causing product recall or failure."
    },
    {
        id: 5,
        name: "Dams",
        icon: (
            <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
        ),
        details: "Spillway Gate Controllers, Water Level Sensors, Hydro-turbines. Risk: Catastrophic flooding via remote SCADA manipulation."
    },
    {
        id: 6,
        name: "Defense Industrial Base",
        icon: (
            <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
        ),
        details: "CMMC Compliance, Air-gapped Networks, CAD/CAM Design Files. Threat: Exfiltration of classified weapon system schematics."
    },
    {
        id: 7,
        name: "Emergency Services",
        icon: (
            <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
        ),
        details: "CAD (Computer Aided Dispatch), P25 Radio Systems, NG911. Attack Vector: TDoS (Telephony Denial of Service) on dispatch centers."
    },
    {
        id: 8,
        name: "Energy",
        icon: (
            <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
        ),
        details: "IEC 61850 Substations, DNP3 Protocol, AMI (Smart Meters). Impact: Regional blackout via load shedding manipulation."
    },
    {
        id: 9,
        name: "Financial Services",
        icon: (
            <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
        ),
        details: "SWIFT Gateways, FIX Protocol, High-Frequency Trading Engines. Risk: Integrity attacks on ledger data causing market panic."
    },
    {
        id: 10,
        name: "Food and Agriculture",
        icon: (
            <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
        ),
        details: "Industrial IoT Sensors, Automated Feeding Systems, Cold Chain Logistics. Threat: Spoilage of perishable goods via temperature hack."
    },
    {
        id: 11,
        name: "Government Facilities",
        icon: (
            <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M8 14v3m4-3v3m4-3v3M3 21h18M3 10h18M3 7l9-4 9 4M4 10h16v11H4V10z" />
            </svg>
        ),
        details: "FICAM/PIV Auth, SCIFs, Public Archives. Weakness: Legacy access control systems and insider threats."
    },
    {
        id: 12,
        name: "Healthcare",
        icon: (
            <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
            </svg>
        ),
        details: "HL7/DICOM, IoMT (Internet of Medical Things), MRI/CT Scanners. Risk: Ransomware locking patient records or device manipulation."
    },
    {
        id: 13,
        name: "Information Technology",
        icon: (
            <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v4a2 2 0 01-2 2M5 12a2 2 0 00-2 2v4a2 2 0 002 2h14a2 2 0 002-2v-4a2 2 0 00-2-2m-2-4h.01M17 16h.01" />
            </svg>
        ),
        details: "Active Directory, Cloud (AWS/Azure), SaaS, DNS. The backbone for all other sectors. Target: Supply chain injection."
    },
    {
        id: 14,
        name: "Nuclear Reactors",
        icon: (
            <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
        ),
        details: "NRC Regulations, Safety Systems, Fuel Rod Cooling. Strictly air-gapped. Attack Vector: Stuxnet-style USB bridging."
    },
    {
        id: 15,
        name: "Transportation",
        icon: (
            <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
        ),
        details: "Rail Signaling (PTC), Avionics (ARINC 429), Fleet Management. Impact: Collision or mass transit disruption."
    },
    {
        id: 16,
        name: "Water and Wastewater",
        icon: (
            <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
            </svg>
        ),
        details: "RTUs, HMI Software, Chemical Dosing Pumps. Threat: Altering chemical levels (e.g., Oldsmar Florida attack)."
    }
];

export default function SectorGrid() {
    return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {sectors.map((sector) => (
                <div key={sector.id} className="bg-surface/40 p-6 rounded-xl border border-white/5 hover:border-primary/40 transition-all group relative overflow-hidden">
                    <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity text-primary">
                        {sector.icon}
                    </div>
                    <div className="flex items-center gap-3 mb-4">
                        <div className="text-primary group-hover:scale-110 transition-transform duration-300">
                            {sector.icon}
                        </div>
                        <h4 className="font-bold text-white text-sm uppercase tracking-wide">{sector.name}</h4>
                    </div>
                    <p className="text-xs text-gray-400 leading-relaxed font-mono">
                        {sector.details}
                    </p>
                    <div className="mt-4 flex gap-2">
                        <span className="text-[10px] bg-black/40 px-2 py-1 rounded text-secondary border border-white/5">EQUIPMENT</span>
                        <span className="text-[10px] bg-black/40 px-2 py-1 rounded text-secondary border border-white/5">IMPACT</span>
                    </div>
                </div>
            ))}
        </div>
    );
}
