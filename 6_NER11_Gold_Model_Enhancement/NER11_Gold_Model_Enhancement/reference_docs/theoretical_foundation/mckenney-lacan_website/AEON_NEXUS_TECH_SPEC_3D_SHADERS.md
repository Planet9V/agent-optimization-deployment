# AEON Nexus: Technical Specification - 3D Shaders & Geometry

**Document ID**: AEON_NEXUS_TECH_SPEC_3D_SHADERS
**Parent Doc**: AEON_NEXUS_PRD_EXHAUSTIVE
**Date**: 2025-11-29
**Author**: AEON Design Bureau (Swarm Iota)

---

## 1. The Trauma Shader (Vertex Displacement)

This shader visualizes the **Riemann Curvature ($R$)** of the system.
When the system is stressed, the smooth manifold becomes jagged and spiked.

### 1.1 GLSL Vertex Shader
```glsl
uniform float uTime;
uniform float uTrauma; // Mapped from CSV Column 'S' (Curvature)
uniform float uHeartbeat; // Mapped from CSV Column 'D' (Heartbeat)

varying vec2 vUv;
varying float vDisplacement;

// Simplex Noise Function (External Lib)
#include <simplex_noise>

void main() {
    vUv = uv;
    vec3 pos = position;

    // 1. Base Undulation (Breathing)
    float breath = sin(uTime * 0.5) * 0.1;
    
    // 2. Trauma Spikes
    // If uTrauma is high, the noise frequency and amplitude increase
    float noiseFreq = 2.0 + (uTrauma * 10.0);
    float noiseAmp = 0.1 + (uTrauma * 2.0);
    float noise = snoise(pos * noiseFreq + uTime);
    
    // 3. Heartbeat Pulse
    // A sudden expansion triggered by the heartbeat signal
    float pulse = smoothstep(0.8, 1.0, sin(uHeartbeat * 3.14)) * 0.2;

    // Apply Displacement along Normal
    float displacement = breath + (noise * noiseAmp) + pulse;
    pos += normal * displacement;

    vDisplacement = displacement;
    gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
}
```

---

## 2. The Holographic Shader (Fragment)

This shader creates the "Glassmorphic" look of the Digital Twin.

### 2.1 GLSL Fragment Shader
```glsl
uniform vec3 uColorBase;
uniform vec3 uColorTrauma;
uniform float uTrauma;

varying float vDisplacement;

void main() {
    // 1. Fresnel Effect (Glowing Edges)
    vec3 viewDir = normalize(cameraPosition - vWorldPosition);
    float fresnel = dot(viewDir, vNormal);
    fresnel = pow(1.0 - abs(fresnel), 3.0);

    // 2. Color Mixing
    // Mix between Safe Blue and Trauma Red based on displacement
    vec3 color = mix(uColorBase, uColorTrauma, vDisplacement * uTrauma);

    // 3. Holographic Scanline
    float scanline = sin(gl_FragCoord.y * 0.1 + uTime * 5.0) * 0.1;
    
    // 4. Alpha (Transparency)
    float alpha = 0.6 + fresnel + scanline;

    gl_FragColor = vec4(color + fresnel, alpha);
}
```

---

## 3. The Manifold Geometry (12D Projection)

We cannot render 12 dimensions directly. We use a **Calabi-Yau Projection**.

### 3.1 React Three Fiber Component
```tsx
function PsychometricManifold({ data }) {
  const mesh = useRef();
  
  useFrame((state) => {
    // Update Uniforms from Data Stream
    mesh.current.material.uniforms.uTrauma.value = data.current.curvature;
    mesh.current.material.uniforms.uHeartbeat.value = data.current.heartbeat;
  });

  return (
    <mesh ref={mesh}>
      {/* A complex TorusKnot represents the topological complexity */}
      <torusKnotGeometry args={[10, 3, 100, 16]} /> 
      <shaderMaterial 
        vertexShader={TraumaVertexShader}
        fragmentShader={HolographicFragmentShader}
        transparent={true}
        side={THREE.DoubleSide}
      />
    </mesh>
  );
}
```
