import React, { useRef, useMemo, useState } from 'react'
import { useFrame } from '@react-three/fiber'
import { useSpring, animated } from '@react-spring/three'
import * as THREE from 'three'
import { TraumaMaterial } from '@/components/shaders/TraumaMaterial'

interface QuantumNodeProps {
    id: string
    position: [number, number, number]
    relevance: number // 0.0 to 1.0 (from GNN)
    entropy: number   // 0.0 to 1.0 (Global State)
    label: string
    onClick: (id: string) => void
}

export function QuantumNode({ id, position, relevance, entropy, label, onClick }: QuantumNodeProps) {
    const meshRef = useRef<THREE.Mesh>(null)
    const [hovered, setHovered] = useState(false)

    // 1. The Mathematics of Collapse
    // P(Render) = 1 / (1 + e^(-k * (Relevance - Entropy)))
    // If Entropy is high, only highly relevant nodes survive.
    const probability = useMemo(() => {
        const k = 10 // Steepness
        const threshold = entropy
        return 1 / (1 + Math.exp(-k * (relevance - threshold)))
    }, [relevance, entropy])

    // 2. The Physics of Existence (Spring Animation)
    // If probability > 0.5, we "exist" (scale = 1). Otherwise, we are in superposition (scale = 0).
    const { scale, color } = useSpring({
        scale: probability > 0.5 ? (hovered ? 1.2 : 1.0) : 0.0,
        color: hovered ? '#00F0FF' : '#2A2A2A',
        config: { mass: 1, tension: 170, friction: 26 } // Spring-Mass-Damper
    })

    // 3. The Observer Effect
    // Hovering increases local relevance (handled by parent state usually, but simulated here)

    useFrame((state) => {
        if (!meshRef.current) return
        // Subtle "Breathing" animation based on Relevance
        meshRef.current.rotation.y += 0.01 * relevance
    })

    return (
        <animated.mesh
            ref={meshRef}
            position={position}
            scale={scale}
            onClick={() => onClick(id)}
            onPointerOver={() => setHovered(true)}
            onPointerOut={() => setHovered(false)}
        >
            {/* The Geometry: A Dodecahedron (Platonic Solid) */}
            <dodecahedronGeometry args={[1, 0]} />

            {/* The Material: Custom Shader */}
            <traumaMaterial
                uTime={0}
                uTrauma={entropy} // High entropy = More distortion
                uColor={new THREE.Color(color.get())}
                transparent
                opacity={probability} // Dissolve effect
            />

            {/* The Label (Only visible if collapsed) */}
            {probability > 0.8 && (
                <Html distanceFactor={10}>
                    <div className="font-orbitron text-xs text-hologram bg-black/50 p-1 rounded backdrop-blur-md">
                        {label}
                        <span className="text-[8px] block text-gray-400">P={probability.toFixed(2)}</span>
                    </div>
                </Html>
            )}
        </animated.mesh>
    )
}
