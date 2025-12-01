"""
Tailwind UI Components Library
Modern, reusable UI components with Tailwind v4 styling for Streamlit
"""

import streamlit.components.v1 as components
from typing import List, Dict, Any, Optional

def tailwind_html(html_content: str, height: Optional[int] = None) -> Any:
    """
    Render HTML with Tailwind v4 CDN styling

    Args:
        html_content: HTML content to render
        height: Optional fixed height for component

    Returns:
        Streamlit component with Tailwind styling
    """
    wrapped_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
        <style type="text/tailwindcss">
            @theme {{
                --color-primary: #1f77b4;
                --color-primary-dark: #1557a0;
                --color-success: #28a745;
                --color-warning: #ffc107;
                --color-danger: #dc3545;
                --color-info: #17a2b8;
                --font-sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            }}

            body {{
                margin: 0;
                padding: 0;
                font-family: var(--font-sans);
            }}

            .animate-fadeIn {{
                animation: fadeIn 0.3s ease-in;
            }}

            @keyframes fadeIn {{
                from {{ opacity: 0; transform: translateY(10px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}

            .hover-lift {{
                transition: transform 0.2s ease, box-shadow 0.2s ease;
            }}

            .hover-lift:hover {{
                transform: translateY(-2px);
                box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    return components.html(wrapped_html, height=height, scrolling=True)


def status_card(
    title: str,
    value: str,
    status: str = "success",
    icon: str = "✅",
    subtitle: Optional[str] = None
) -> Any:
    """
    Modern status card with Tailwind styling

    Args:
        title: Card title
        value: Main value to display
        status: Status type (success, warning, error, info)
        icon: Emoji icon
        subtitle: Optional subtitle text

    Returns:
        Tailwind-styled status card component
    """
    colors = {
        "success": {
            "bg": "bg-green-50",
            "border": "border-green-500",
            "text": "text-green-900",
            "value": "text-green-700"
        },
        "warning": {
            "bg": "bg-yellow-50",
            "border": "border-yellow-500",
            "text": "text-yellow-900",
            "value": "text-yellow-700"
        },
        "error": {
            "bg": "bg-red-50",
            "border": "border-red-500",
            "text": "text-red-900",
            "value": "text-red-700"
        },
        "info": {
            "bg": "bg-blue-50",
            "border": "border-blue-500",
            "text": "text-blue-900",
            "value": "text-blue-700"
        }
    }

    color_scheme = colors.get(status, colors["info"])
    subtitle_html = f'<p class="text-xs {color_scheme["text"]} opacity-75 mt-1">{subtitle}</p>' if subtitle else ''

    html = f"""
    <div class="p-6 rounded-lg border-l-4 {color_scheme['bg']} {color_scheme['border']} shadow-sm hover-lift animate-fadeIn">
        <div class="flex items-center gap-3">
            <span class="text-4xl">{icon}</span>
            <div class="flex-1">
                <h3 class="text-sm font-medium uppercase tracking-wider {color_scheme['text']} opacity-75">{title}</h3>
                <p class="text-3xl font-bold {color_scheme['value']} mt-1">{value}</p>
                {subtitle_html}
            </div>
        </div>
    </div>
    """
    return tailwind_html(html, height=140)


def metric_grid(metrics: List[Dict[str, Any]]) -> Any:
    """
    Responsive metric grid with Tailwind

    Args:
        metrics: List of metric dicts with keys: label, value, delta (optional), icon (optional)

    Example:
        metrics = [
            {"label": "Documents", "value": "115", "delta": "+12", "icon": "📚"},
            {"label": "Entities", "value": "12,256", "delta": "+340", "icon": "🏷️"}
        ]

    Returns:
        Tailwind-styled metric grid component
    """
    metric_cards = "".join([
        f"""
        <div class="bg-white p-6 rounded-lg shadow-md border border-gray-200 hover-lift animate-fadeIn">
            <div class="flex items-center justify-between mb-3">
                <div class="text-sm text-gray-600 font-medium">{m['label']}</div>
                {f'<span class="text-2xl">{m.get("icon", "")}</span>' if m.get('icon') else ''}
            </div>
            <div class="text-3xl font-bold text-gray-900">{m['value']}</div>
            {f'<div class="text-sm text-green-600 font-medium mt-2">↑ {m["delta"]}</div>' if m.get('delta') else ''}
        </div>
        """
        for m in metrics
    ])

    html = f"""
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 p-4">
        {metric_cards}
    </div>
    """
    return tailwind_html(html, height=180)


def data_table(data: List[Dict], columns: List[str], max_rows: int = 10) -> Any:
    """
    Beautiful responsive table with Tailwind

    Args:
        data: List of dicts representing table rows
        columns: List of column keys to display
        max_rows: Maximum number of rows to show

    Returns:
        Tailwind-styled data table component
    """
    rows = "".join([
        f"""
        <tr class="hover:bg-gray-50 transition-colors">
            {''.join([f'<td class="px-6 py-4 text-sm text-gray-900 whitespace-nowrap">{row.get(col, "")}</td>' for col in columns])}
        </tr>
        """
        for row in data[:max_rows]
    ])

    html = f"""
    <div class="overflow-x-auto rounded-lg border border-gray-200 shadow-sm animate-fadeIn">
        <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
                <tr>
                    {''.join([f'<th class="px-6 py-3 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">{col}</th>' for col in columns])}
                </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
                {rows}
            </tbody>
        </table>
    </div>
    """
    return tailwind_html(html, height=min(400, (len(data[:max_rows]) + 1) * 50 + 100))


def alert_box(message: str, alert_type: str = "info", title: Optional[str] = None, dismissible: bool = False) -> Any:
    """
    Alert/notification box with Tailwind styling

    Args:
        message: Alert message
        alert_type: Type (success, warning, error, info)
        title: Optional title
        dismissible: Show close button

    Returns:
        Tailwind-styled alert box
    """
    icons = {
        "success": "✅",
        "warning": "⚠️",
        "error": "❌",
        "info": "ℹ️"
    }

    colors = {
        "success": "bg-green-50 border-green-200 text-green-800",
        "warning": "bg-yellow-50 border-yellow-200 text-yellow-800",
        "error": "bg-red-50 border-red-200 text-red-800",
        "info": "bg-blue-50 border-blue-200 text-blue-800"
    }

    color = colors.get(alert_type, colors["info"])
    icon = icons.get(alert_type, "ℹ️")

    title_html = f'<h4 class="font-bold mb-1">{title}</h4>' if title else ''
    dismiss_html = '<button class="ml-auto text-lg opacity-50 hover:opacity-100">&times;</button>' if dismissible else ''

    html = f"""
    <div class="{color} border rounded-lg p-4 mb-4 flex items-start gap-3 animate-fadeIn">
        <span class="text-2xl flex-shrink-0">{icon}</span>
        <div class="flex-1">
            {title_html}
            <p class="text-sm">{message}</p>
        </div>
        {dismiss_html}
    </div>
    """
    return tailwind_html(html, height=120)


def progress_bar(value: int, max_value: int = 100, label: str = "", show_percentage: bool = True) -> Any:
    """
    Modern progress bar with Tailwind

    Args:
        value: Current progress value
        max_value: Maximum value (default 100)
        label: Progress label
        show_percentage: Show percentage text

    Returns:
        Tailwind-styled progress bar
    """
    percentage = min(100, (value / max_value) * 100)

    percentage_text = f'<span class="text-sm font-medium text-gray-700">{percentage:.1f}%</span>' if show_percentage else ''

    # Color based on percentage
    if percentage >= 80:
        color = "bg-green-500"
    elif percentage >= 50:
        color = "bg-blue-500"
    elif percentage >= 25:
        color = "bg-yellow-500"
    else:
        color = "bg-red-500"

    html = f"""
    <div class="w-full animate-fadeIn">
        <div class="flex justify-between items-center mb-2">
            <span class="text-sm font-medium text-gray-700">{label}</span>
            {percentage_text}
        </div>
        <div class="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
            <div class="{color} h-3 rounded-full transition-all duration-500 ease-out" style="width: {percentage}%"></div>
        </div>
    </div>
    """
    return tailwind_html(html, height=80)


def badge(text: str, variant: str = "default", size: str = "md") -> Any:
    """
    Small badge/tag component

    Args:
        text: Badge text
        variant: Color variant (default, success, warning, error, info)
        size: Size (sm, md, lg)

    Returns:
        Tailwind-styled badge
    """
    variants = {
        "default": "bg-gray-100 text-gray-800",
        "success": "bg-green-100 text-green-800",
        "warning": "bg-yellow-100 text-yellow-800",
        "error": "bg-red-100 text-red-800",
        "info": "bg-blue-100 text-blue-800"
    }

    sizes = {
        "sm": "text-xs px-2 py-1",
        "md": "text-sm px-3 py-1",
        "lg": "text-base px-4 py-2"
    }

    variant_class = variants.get(variant, variants["default"])
    size_class = sizes.get(size, sizes["md"])

    html = f"""
    <span class="inline-flex items-center {variant_class} {size_class} font-medium rounded-full">
        {text}
    </span>
    """
    return tailwind_html(html, height=50)


def stat_card_minimal(label: str, value: str, trend: Optional[str] = None, icon: Optional[str] = None) -> Any:
    """
    Minimal statistics card

    Args:
        label: Stat label
        value: Stat value
        trend: Optional trend indicator (e.g., "+12%")
        icon: Optional emoji icon

    Returns:
        Minimal Tailwind-styled stat card
    """
    icon_html = f'<div class="text-3xl mb-2">{icon}</div>' if icon else ''
    trend_html = ''
    if trend:
        trend_color = "text-green-600" if trend.startswith("+") else "text-red-600"
        trend_html = f'<div class="{trend_color} text-sm font-medium">{trend}</div>'

    html = f"""
    <div class="bg-white p-6 rounded-lg border-2 border-gray-100 hover:border-blue-300 transition-colors hover-lift animate-fadeIn">
        {icon_html}
        <div class="text-sm text-gray-600 font-medium mb-1">{label}</div>
        <div class="text-2xl font-bold text-gray-900">{value}</div>
        {trend_html}
    </div>
    """
    return tailwind_html(html, height=160)


def button_group(buttons: List[Dict[str, str]]) -> Any:
    """
    Group of action buttons

    Args:
        buttons: List of button dicts with keys: label, variant (primary, secondary, danger)

    Example:
        buttons = [
            {"label": "Save", "variant": "primary"},
            {"label": "Cancel", "variant": "secondary"}
        ]

    Returns:
        Tailwind-styled button group
    """
    button_variants = {
        "primary": "bg-blue-600 hover:bg-blue-700 text-white",
        "secondary": "bg-gray-200 hover:bg-gray-300 text-gray-800",
        "danger": "bg-red-600 hover:bg-red-700 text-white",
        "success": "bg-green-600 hover:bg-green-700 text-white"
    }

    button_html = "".join([
        f"""
        <button class="{button_variants.get(btn.get('variant', 'secondary'))} px-6 py-2 rounded-lg font-medium transition-colors shadow-sm hover:shadow-md">
            {btn['label']}
        </button>
        """
        for btn in buttons
    ])

    html = f"""
    <div class="flex gap-3 flex-wrap">
        {button_html}
    </div>
    """
    return tailwind_html(html, height=80)


def info_panel(title: str, content: str, icon: str = "ℹ️") -> Any:
    """
    Information panel with icon

    Args:
        title: Panel title
        content: Panel content (HTML allowed)
        icon: Emoji icon

    Returns:
        Tailwind-styled info panel
    """
    html = f"""
    <div class="bg-gradient-to-r from-blue-50 to-indigo-50 border-l-4 border-blue-500 rounded-lg p-6 shadow-sm animate-fadeIn">
        <div class="flex items-start gap-4">
            <div class="text-4xl flex-shrink-0">{icon}</div>
            <div>
                <h3 class="text-lg font-bold text-gray-900 mb-2">{title}</h3>
                <div class="text-sm text-gray-700 leading-relaxed">{content}</div>
            </div>
        </div>
    </div>
    """
    return tailwind_html(html, height=180)


# Utility function for injecting Tailwind CDN into Streamlit pages
def inject_tailwind_cdn() -> str:
    """
    Returns HTML script tag for Tailwind v4 CDN
    Use with st.markdown(inject_tailwind_cdn(), unsafe_allow_html=True)

    Returns:
        HTML script tag for Tailwind CDN
    """
    return """
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    <style type="text/tailwindcss">
        @theme {
            --color-primary: #1f77b4;
            --color-primary-dark: #1557a0;
            --color-success: #28a745;
            --color-warning: #ffc107;
            --color-danger: #dc3545;
            --color-info: #17a2b8;
        }

        .hover-lift {
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        .hover-lift:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        }

        .animate-fadeIn {
            animation: fadeIn 0.3s ease-in;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
    """
