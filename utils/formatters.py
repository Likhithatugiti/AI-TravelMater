"""
Formatting Utilities
Converts raw data into display-ready HTML / Markdown strings.
"""

from typing import Dict, Any


def format_flight_card(flight: Dict[str, Any]) -> str:
    """
    Render a single flight result as an HTML card string.

    Args:
        flight: normalised flight dict from extract_cheapest_flights().

    Returns:
        HTML string.
    """
    logo_html = (
        f'<img src="{flight["airline_logo"]}" style="height:28px; margin-right:8px;" />'
        if flight.get("airline_logo")
        else ""
    )
    stops_color = "#2ecc71" if flight["stops"] == 0 else "#e67e22"

    return f"""
    <div class="flight-card">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.5rem;">
            <div>
                {logo_html}
                <strong style="font-size:1.1rem;">{flight['airline']}</strong>
                <span style="background:{stops_color}; color:white; padding:2px 8px;
                             border-radius:12px; font-size:0.75rem; margin-left:8px;">
                    {flight['stop_label']}
                </span>
            </div>
            <span class="price-badge">{flight['price_display']}</span>
        </div>
        <div style="display:flex; gap:2rem; margin-top:0.8rem; flex-wrap:wrap; color:#444;">
            <div>
                <div style="font-size:0.75rem; color:#888;">DEPARTURE</div>
                <div><strong>{flight['departure_time']}</strong></div>
                <div style="font-size:0.85rem;">{flight['departure_airport']}</div>
            </div>
            <div style="font-size:1.5rem; color:#0f3460; align-self:center;">→</div>
            <div>
                <div style="font-size:0.75rem; color:#888;">ARRIVAL</div>
                <div><strong>{flight['arrival_time']}</strong></div>
                <div style="font-size:0.85rem;">{flight['arrival_airport']}</div>
            </div>
            <div style="margin-left:auto; text-align:right;">
                <div style="font-size:0.75rem; color:#888;">DURATION</div>
                <div><strong>{flight['duration']}</strong></div>
            </div>
        </div>
        <div style="margin-top:0.8rem;">
            <a href="{flight['booking_url']}" target="_blank"
               style="background:#0f3460; color:white; padding:0.4rem 1.2rem;
                      border-radius:6px; text-decoration:none; font-size:0.9rem;">
                Book Now ↗
            </a>
        </div>
    </div>
    """


def format_itinerary_html(itinerary_md: str) -> str:
    """
    Wrap a markdown itinerary string in a styled HTML container.

    Args:
        itinerary_md: raw markdown text from the Planner Agent.

    Returns:
        HTML string.
    """
    return f"""
    <div style="background:white; border-radius:12px; padding:1.5rem;
                box-shadow:0 4px 15px rgba(0,0,0,0.08); line-height:1.8;">
        {itinerary_md}
    </div>
    """


def budget_table_html(budget_breakdown: Dict[str, float]) -> str:
    """
    Render a simple budget breakdown table.

    Args:
        budget_breakdown: dict mapping category names to USD amounts.

    Returns:
        HTML table string.
    """
    rows = ""
    total = sum(budget_breakdown.values())
    for category, amount in budget_breakdown.items():
        pct = (amount / total * 100) if total else 0
        rows += f"""
        <tr>
            <td style="padding:0.5rem 1rem;">{category}</td>
            <td style="padding:0.5rem 1rem; text-align:right;">${amount:,.0f}</td>
            <td style="padding:0.5rem 1rem;">
                <div style="background:#e0e7ff; border-radius:4px; height:12px; width:100%;">
                    <div style="background:#0f3460; height:12px; border-radius:4px;
                                width:{pct:.0f}%;"></div>
                </div>
            </td>
        </tr>
        """
    rows += f"""
    <tr style="font-weight:700; border-top:2px solid #0f3460;">
        <td style="padding:0.5rem 1rem;">Total</td>
        <td style="padding:0.5rem 1rem; text-align:right;">${total:,.0f}</td>
        <td></td>
    </tr>
    """
    return f"""
    <table style="width:100%; border-collapse:collapse; font-size:0.95rem;">
        <thead>
            <tr style="background:#0f3460; color:white;">
                <th style="padding:0.6rem 1rem; text-align:left;">Category</th>
                <th style="padding:0.6rem 1rem; text-align:right;">Amount (USD)</th>
                <th style="padding:0.6rem 1rem; text-align:left;">Share</th>
            </tr>
        </thead>
        <tbody>{rows}</tbody>
    </table>
    """
