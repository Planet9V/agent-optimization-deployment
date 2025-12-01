# AEON Nexus: Implementation Codex

**Document ID**: AEON_NEXUS_IMPLEMENTATION_CODEX
**Parent Doc**: AEON_NEXUS_VISIONARY_PRD_v2
**Date**: 2025-11-29
**Author**: AEON Design Bureau (Swarm Iota)

---

## 1. Frontend Architecture (Next.js 15 + React 19)

We leverage **React Server Components (RSC)** to render the "Scholar Mode" text on the server, while streaming the "Conductor Mode" 3D assets via **Suspense**.

### 1.1 `app/layout.tsx` (The Root)
```tsx
import { View } from '@/components/canvas/View'
import { Preload } from '@react-three/drei'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="antialiased">
      <body className="bg-void text-hologram">
        {/* The DOM Layer (Scholar Mode) */}
        <div className="relative z-10 pointer-events-none">
          {children}
        </div>
        
        {/* The 3D Layer (Conductor Mode) */}
        <div className="fixed inset-0 z-0">
          <View className="h-full w-full">
            <Suspense fallback={null}>
               <PillarCosmology />
               <Preload all />
            </Suspense>
          </View>
        </div>
      </body>
    </html>
  )
}
```

### 1.2 `app/scholar/[slug]/page.tsx` (Server Component)
```tsx
import { getTheorem } from '@/lib/neo4j'

export default async function ScholarPage({ params }: { params: { slug: string } }) {
  const theorem = await getTheorem(params.slug)
  
  return (
    <main className="pointer-events-auto grid grid-cols-12 h-screen">
      {/* Left: 3D Viewport (Transparent) */}
      <div className="col-span-4" /> 
      
      {/* Center: The Text */}
      <article className="col-span-6 overflow-y-auto p-12 glass-panel">
        <h1 className="font-orbitron text-4xl mb-8">{theorem.title}</h1>
        <div className="font-inter text-lg leading-relaxed">
          {theorem.content}
        </div>
      </article>
      
      {/* Right: Zettelkasten */}
      <aside className="col-span-2 border-l border-glass p-4">
        <CitationGraph nodeId={theorem.id} />
      </aside>
    </main>
  )
}
```

---

## 2. The 3D Engine (React Three Fiber)

### 2.1 The Trauma Shader (`components/shaders/TraumaMaterial.tsx`)
We use `shaderMaterial` from Drei to create a reactive GLSL material.

```tsx
import { shaderMaterial } from '@react-three/drei'
import { extend } from '@react-three/fiber'
import * as THREE from 'three'

const TraumaMaterial = shaderMaterial(
  {
    uTime: 0,
    uTrauma: 0, // 0.0 to 1.0 (Riemann Curvature)
    uColor: new THREE.Color(0.0, 0.94, 1.0), // #00F0FF
  },
  // Vertex Shader
  `
    varying vec2 vUv;
    varying float vDisplacement;
    uniform float uTime;
    uniform float uTrauma;
    
    // Simplex Noise Function (omitted for brevity)
    
    void main() {
      vUv = uv;
      vec3 pos = position;
      
      // Trauma Displacement
      float noise = snoise(vec3(pos.x * 2.0, pos.y * 2.0, uTime * 0.5));
      float spike = noise * uTrauma * 0.5;
      
      pos += normal * spike;
      vDisplacement = spike;
      
      gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
    }
  `,
  // Fragment Shader
  `
    varying float vDisplacement;
    uniform vec3 uColor;
    uniform float uTrauma;
    
    void main() {
      // Color shifts to Red as Trauma increases
      vec3 finalColor = mix(uColor, vec3(1.0, 0.0, 0.3), uTrauma + vDisplacement);
      
      // Add "Glitch" scanlines
      float scanline = sin(gl_FragCoord.y * 0.1) * 0.1;
      
      gl_FragColor = vec4(finalColor + scanline, 0.8);
    }
  `
)

extend({ TraumaMaterial })
```

---

## 3. The Audio Engine (Tone.js)

### 3.1 The Conductor (`lib/audio/Conductor.ts`)
We use a Singleton pattern to manage the audio context.

```typescript
import * as Tone from 'tone'

class Conductor {
  private heartbeat: Tone.MembraneSynth
  private mischief: Tone.FMSynth
  private isPlaying: boolean = false

  constructor() {
    this.heartbeat = new Tone.MembraneSynth().toDestination()
    this.mischief = new Tone.FMSynth().toDestination()
    
    // The Trauma Bus
    const distortion = new Tone.Distortion(0.4).toDestination()
    this.mischief.connect(distortion)
  }

  public async start() {
    await Tone.start()
    Tone.Transport.start()
    this.isPlaying = true
  }

  public update(metrics: { H: number, M: number }) {
    // Heartbeat Rate driven by H(t)
    const bpm = 60 + (metrics.H * 60) // 60 to 120 BPM
    Tone.Transport.bpm.rampTo(bpm, 0.1)
    
    // Trigger Heartbeat
    if (Tone.Transport.seconds % (60/bpm) < 0.1) {
       this.heartbeat.triggerAttackRelease("C1", "8n")
    }
  }
}

export const conductor = new Conductor()
```

---

## 4. The Data Engine (Neo4j + OpenSPG)

We connect to the `openspg-neo4j` container.

### 4.1 The Connection (`lib/neo4j.ts`)
```typescript
import neo4j from 'neo4j-driver'

const driver = neo4j.driver(
  process.env.NEO4J_URI || 'bolt://localhost:7687',
  neo4j.auth.basic(
    process.env.NEO4J_USER || 'neo4j',
    process.env.NEO4J_PASSWORD || 'password'
  )
)

export async function getTheorem(slug: string) {
  const session = driver.session()
  try {
    const res = await session.run(
      `MATCH (t:Theorem {slug: $slug}) 
       OPTIONAL MATCH (t)-[:CITES]->(c:Theorem)
       RETURN t, collect(c) as citations`,
      { slug }
    )
    return res.records[0].toObject()
  } finally {
    await session.close()
  }
}
```

### 4.2 OpenSPG Integration (Knowledge Graph Construction)
To populate the graph from the Markdown corpus, we use the OpenSPG SDK (Python).

```python
# scripts/ingest_corpus.py
from openspg.client import Client
from openspg.schema import Schema, EntityType

client = Client(endpoint="http://openspg-server:8887")

# Define the Schema
theorem_type = EntityType(
    name="Theorem",
    properties={
        "title": "Text",
        "content": "Text",
        "slug": "Text"
    }
)

# Ingest Data
def ingest_file(filepath):
    with open(filepath) as f:
        content = f.read()
        # Parse Markdown (simplified)
        title = content.split('\n')[0].replace('# ', '')
        slug = filepath.split('/')[-1].replace('.md', '')
        
        client.upsert_vertex("Theorem", {
            "title": title,
            "content": content,
            "slug": slug
        })

# Run for all 65 volumes
```
