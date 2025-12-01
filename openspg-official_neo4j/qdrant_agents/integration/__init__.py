#!/usr/bin/env python3
"""
Qdrant Agents - Integration Layer

Claude-Flow bridge for seamless Qdrant agent integration
"""

from .claude_flow_bridge import ClaudeFlowBridge, get_bridge

__all__ = [
    "ClaudeFlowBridge",
    "get_bridge"
]
