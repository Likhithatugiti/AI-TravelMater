"""
Currency Utilities
Provides basic currency reference information per destination IATA code.
For a production app, connect to a live exchange-rate API such as
Open Exchange Rates (https://openexchangerates.org/).
"""

# Static reference table – extend or replace with a live API call
CURRENCY_MAP = {
    # Asia
    "BKK": {"country": "Thailand", "currency": "Thai Baht (THB)", "approx_usd": "1 USD ≈ 35 THB"},
    "SIN": {"country": "Singapore", "currency": "Singapore Dollar (SGD)", "approx_usd": "1 USD ≈ 1.35 SGD"},
    "KUL": {"country": "Malaysia", "currency": "Malaysian Ringgit (MYR)", "approx_usd": "1 USD ≈ 4.7 MYR"},
    "HKG": {"country": "Hong Kong", "currency": "Hong Kong Dollar (HKD)", "approx_usd": "1 USD ≈ 7.8 HKD"},
    "NRT": {"country": "Japan", "currency": "Japanese Yen (JPY)", "approx_usd": "1 USD ≈ 150 JPY"},
    "ICN": {"country": "South Korea", "currency": "South Korean Won (KRW)", "approx_usd": "1 USD ≈ 1320 KRW"},
    "PEK": {"country": "China", "currency": "Chinese Yuan (CNY)", "approx_usd": "1 USD ≈ 7.2 CNY"},
    # South Asia
    "DEL": {"country": "India", "currency": "Indian Rupee (INR)", "approx_usd": "1 USD ≈ 83 INR"},
    "BOM": {"country": "India", "currency": "Indian Rupee (INR)", "approx_usd": "1 USD ≈ 83 INR"},
    "CMB": {"country": "Sri Lanka", "currency": "Sri Lankan Rupee (LKR)", "approx_usd": "1 USD ≈ 310 LKR"},
    # Middle East
    "DXB": {"country": "UAE", "currency": "UAE Dirham (AED)", "approx_usd": "1 USD ≈ 3.67 AED"},
    "DOH": {"country": "Qatar", "currency": "Qatari Riyal (QAR)", "approx_usd": "1 USD ≈ 3.64 QAR"},
    # Europe
    "LHR": {"country": "United Kingdom", "currency": "British Pound (GBP)", "approx_usd": "1 USD ≈ 0.79 GBP"},
    "CDG": {"country": "France", "currency": "Euro (EUR)", "approx_usd": "1 USD ≈ 0.92 EUR"},
    "FCO": {"country": "Italy", "currency": "Euro (EUR)", "approx_usd": "1 USD ≈ 0.92 EUR"},
    "MAD": {"country": "Spain", "currency": "Euro (EUR)", "approx_usd": "1 USD ≈ 0.92 EUR"},
    # Americas
    "JFK": {"country": "USA", "currency": "US Dollar (USD)", "approx_usd": "Base currency"},
    "LAX": {"country": "USA", "currency": "US Dollar (USD)", "approx_usd": "Base currency"},
    "GRU": {"country": "Brazil", "currency": "Brazilian Real (BRL)", "approx_usd": "1 USD ≈ 5.0 BRL"},
    "MEX": {"country": "Mexico", "currency": "Mexican Peso (MXN)", "approx_usd": "1 USD ≈ 17 MXN"},
}


def get_currency_info(destination_iata: str) -> str:
    """
    Return an HTML snippet showing currency exchange info for a destination.

    Args:
        destination_iata: 3-letter IATA airport/city code.

    Returns:
        HTML string with currency information.
    """
    info = CURRENCY_MAP.get(destination_iata.upper())
    if not info:
        return (
            "<p>Currency information not available for this destination. "
            "Please check <a href='https://xe.com' target='_blank'>XE.com</a> "
            "for live rates.</p>"
        )

    return f"""
    <table style="width:100%; border-collapse:collapse;">
        <tr>
            <td style="padding:0.5rem; font-weight:600; color:#555;">Country</td>
            <td style="padding:0.5rem;">{info['country']}</td>
        </tr>
        <tr style="background:#f8f9ff;">
            <td style="padding:0.5rem; font-weight:600; color:#555;">Local Currency</td>
            <td style="padding:0.5rem;">{info['currency']}</td>
        </tr>
        <tr>
            <td style="padding:0.5rem; font-weight:600; color:#555;">Approx. Exchange Rate</td>
            <td style="padding:0.5rem; color:#0f3460; font-weight:700;">{info['approx_usd']}</td>
        </tr>
        <tr style="background:#f8f9ff;">
            <td style="padding:0.5rem; font-weight:600; color:#555;">Live Rates</td>
            <td style="padding:0.5rem;">
                <a href="https://xe.com/currencyconverter/" target="_blank"
                   style="color:#0f3460;">Check live rates on XE.com ↗</a>
            </td>
        </tr>
    </table>
    <p style="font-size:0.8rem; color:#888; margin-top:0.5rem;">
        * Rates are approximate and for reference only. Verify before travel.
    </p>
    """
