# Cycle 1: The Semantic Web (RDF/OWL Ontology)

**Document ID**: CYCLE_01_SEMANTIC_WEB_ONTOLOGY
**Version**: 1.0 (Iteration)
**Date**: 2025-11-29
**Author**: AEON Research Division (Swarm Omega)
**Classification**: UNCLASSIFIED // ACADEMIC

---

## 1. The Ontology Definition (Turtle)

```turtle
@prefix ml: <http://aeon.ai/ontology/mckenney-lacan#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

# Classes
ml:Actor a owl:Class .
ml:Event a owl:Class .
ml:Register a owl:Class .
ml:Instrument a owl:Class .

# Registers
ml:Real a ml:Register .
ml:Symbolic a ml:Register .
ml:Imaginary a ml:Register .

# Properties
ml:hasSentiment a owl:DatatypeProperty ;
    rdfs:range xsd:float .

ml:hasEntropy a owl:DatatypeProperty ;
    rdfs:range xsd:float .

ml:inRegister a owl:ObjectProperty ;
    rdfs:domain ml:Event ;
    rdfs:range ml:Register .

# The Willy Loman Instance
ml:WillyLoman a ml:Actor ;
    ml:hasDISC "Dominance" .

# The Event (Beat 1)
ml:Beat_1 a ml:Event ;
    ml:hasActor ml:WillyLoman ;
    ml:hasTimestamp "00:00:00"^^xsd:time ;
    ml:inRegister ml:Real ;
    ml:hasSentiment -0.8 ;
    ml:hasText "I'm tired to the death." .

# Inference Rule (SWRL)
# If an Actor is in the Real without Symbolic support, they are in Crisis.
ml:Actor(?a) ^ ml:inRegister(?e, ml:Real) ^ not(ml:inRegister(?e, ml:Symbolic)) -> ml:hasStatus(?a, "Crisis") .
```

---

## 2. The Innovation

By mapping the Calculus to **RDF**, we allow the AEON Digital Twin to "Reason" about the psychological state of the network using standard Semantic Web reasoners (HermiT, Pellet). We can query the graph:
`SELECT ?actor WHERE { ?actor ml:hasStatus "Crisis" }`
