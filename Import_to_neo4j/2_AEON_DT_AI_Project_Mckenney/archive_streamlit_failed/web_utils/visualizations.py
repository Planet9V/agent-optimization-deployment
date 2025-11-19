"""
Visualization Utilities for AEON Web Interface
Provides chart generation functions using Plotly
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import List, Dict, Any


def create_sector_pie_chart(sector_data: List[Dict[str, Any]]) -> go.Figure:
    """
    Create pie chart for sector distribution

    Args:
        sector_data: List of dicts with 'sector' and 'count' keys

    Returns:
        Plotly figure
    """
    if not sector_data:
        # Return empty figure
        fig = go.Figure()
        fig.update_layout(title="No sector data available")
        return fig

    df = pd.DataFrame(sector_data)
    fig = px.pie(
        df,
        values='count',
        names='sector',
        title='Documents by Sector',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig


def create_entity_type_bar_chart(entity_data: List[Dict[str, Any]]) -> go.Figure:
    """
    Create bar chart for entity type distribution

    Args:
        entity_data: List of dicts with 'type'/'label' and 'count' keys

    Returns:
        Plotly figure
    """
    if not entity_data:
        fig = go.Figure()
        fig.update_layout(title="No entity data available")
        return fig

    df = pd.DataFrame(entity_data)

    # Handle both 'type' and 'label' column names
    label_col = 'type' if 'type' in df.columns else 'label'

    # Sort by count descending
    df = df.sort_values('count', ascending=False)

    fig = px.bar(
        df,
        x=label_col,
        y='count',
        title='Entity Type Distribution',
        labels={label_col: 'Entity Type', 'count': 'Count'},
        color='count',
        color_continuous_scale='Viridis'
    )
    fig.update_layout(
        xaxis_tickangle=-45,
        showlegend=False
    )
    return fig


def create_processing_stats_chart(stats: Dict[str, int]) -> go.Figure:
    """
    Create horizontal bar chart for processing pipeline stats

    Args:
        stats: Dictionary with processing stage counts

    Returns:
        Plotly figure
    """
    stages = [
        ('Discovered', stats.get('files_discovered', 0)),
        ('Converted', stats.get('files_converted', 0)),
        ('Classified', stats.get('files_classified', 0)),
        ('NER Processed', stats.get('files_ner_processed', 0)),
        ('Ingested', stats.get('files_ingested', 0))
    ]

    labels = [s[0] for s in stages]
    values = [s[1] for s in stages]

    fig = go.Figure(go.Bar(
        x=values,
        y=labels,
        orientation='h',
        marker=dict(
            color=values,
            colorscale='Blues',
            showscale=False
        ),
        text=values,
        textposition='outside'
    ))

    fig.update_layout(
        title='Processing Pipeline Status',
        xaxis_title='Document Count',
        yaxis_title='Processing Stage',
        height=300
    )

    return fig


def create_timeline_chart(documents: List[Dict[str, Any]]) -> go.Figure:
    """
    Create timeline chart of document processing

    Args:
        documents: List of documents with processed_date

    Returns:
        Plotly figure
    """
    if not documents:
        fig = go.Figure()
        fig.update_layout(title="No timeline data available")
        return fig

    df = pd.DataFrame(documents)

    # Convert processed_date to datetime
    df['processed_date'] = pd.to_datetime(df['processed_date'])

    # Group by date
    daily_counts = df.groupby(df['processed_date'].dt.date).size().reset_index(name='count')
    daily_counts.columns = ['date', 'count']

    fig = px.line(
        daily_counts,
        x='date',
        y='count',
        title='Document Processing Timeline',
        labels={'date': 'Date', 'count': 'Documents Processed'},
        markers=True
    )

    fig.update_traces(line_color='#1f77b4', line_width=2)
    fig.update_layout(hovermode='x unified')

    return fig


def create_entity_network_graph(
    entities: List[Dict[str, Any]],
    max_nodes: int = 30
) -> go.Figure:
    """
    Create simple network graph of entity co-occurrences

    Args:
        entities: List of entity dictionaries
        max_nodes: Maximum number of nodes to display

    Returns:
        Plotly figure
    """
    # This is a simplified version - would need actual co-occurrence data
    # For now, create a simple node graph

    if not entities:
        fig = go.Figure()
        fig.update_layout(title="No entity data available")
        return fig

    # Limit to top entities
    entities = entities[:max_nodes]

    # Create node positions (circular layout)
    import math
    n = len(entities)
    angles = [2 * math.pi * i / n for i in range(n)]
    x_nodes = [math.cos(a) for a in angles]
    y_nodes = [math.sin(a) for a in angles]

    # Create node trace
    node_trace = go.Scatter(
        x=x_nodes,
        y=y_nodes,
        mode='markers+text',
        marker=dict(
            size=20,
            color='lightblue',
            line=dict(width=2, color='darkblue')
        ),
        text=[e.get('text', e.get('label', 'Unknown'))[:20] for e in entities],
        textposition="top center",
        hoverinfo='text',
        hovertext=[f"{e.get('text', 'Unknown')}<br>Type: {e.get('label', 'Unknown')}<br>Docs: {e.get('document_count', 0)}"
                   for e in entities]
    )

    fig = go.Figure(data=[node_trace])

    fig.update_layout(
        title='Entity Network (Top Entities)',
        showlegend=False,
        hovermode='closest',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=500
    )

    return fig


def create_metrics_card(title: str, value: Any, delta: Any = None) -> Dict[str, Any]:
    """
    Create data for a metric card display

    Args:
        title: Metric title
        value: Main metric value
        delta: Change/delta value (optional)

    Returns:
        Dictionary with metric data
    """
    return {
        "title": title,
        "value": value,
        "delta": delta
    }


def format_number(value: int) -> str:
    """Format large numbers with K/M suffixes"""
    if value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    elif value >= 1_000:
        return f"{value / 1_000:.1f}K"
    else:
        return str(value)
