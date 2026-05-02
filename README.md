# ✈️ AI TravelMate

> **An Intelligent Agent for Smart Travel Planning and Assistance**  
> Published in *Global Journal of Engineering Innovations & Interdisciplinary Research* (GJEIIR), 2026;6(2):0142

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-red?logo=streamlit)](https://streamlit.io)
[![Gemini](https://img.shields.io/badge/Google%20Gemini-AI-orange?logo=google)](https://aistudio.google.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 📖 Overview

AI TravelMate solves the biggest pain point in trip planning: having to juggle dozens of tabs across flights, hotels, restaurants, and activity sites. It combines:

- **Google Gemini AI** – Three specialised agents (Researcher, Planner, Hotel & Restaurant Finder) to generate personalised, context-aware travel plans.
- **SerpAPI / Google Flights** – Live flight search with pricing, departure/arrival times, and booking links.
- **Streamlit** – A clean, interactive web UI that works on any device.

Users enter their origin, destination, dates, budget, and activity preferences — and receive a complete, day-by-day itinerary in seconds.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                  User Interface Layer                │
│              (Streamlit – app.py)                   │
└───────────────────────┬─────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────┐
│               Orchestration Layer                    │
│         (Input validation, workflow control)         │
└──────┬───────────────────────────────────┬──────────┘
       │                                   │
┌──────▼──────┐  ┌──────────────┐  ┌──────▼─────────────┐
│  Researcher │  │    Planner   │  │ Hotel & Restaurant  │
│    Agent    │  │    Agent     │  │    Finder Agent     │
│ (Gemini AI) │  │ (Gemini AI)  │  │    (Gemini AI)      │
└──────┬──────┘  └──────┬───────┘  └──────┬─────────────┘
       │                │                  │
┌──────▼────────────────▼──────────────────▼─────────────┐
│                External API & Data Layer                │
│         SerpAPI (Google Flights) + Gemini API           │
└─────────────────────────────┬───────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────┐
│              Processing Layer / Data Extraction          │
│     flight_utils.py · formatters.py · currency_utils.py │
└─────────────────────────────┬───────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────┐
│                       Output Layer                      │
│   Flights · Hotels & Restaurants · Day-wise Itinerary   │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ai-travelmate.git
cd ai-travelmate
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API keys

```bash
cp .env.example .env
```

Edit `.env` and fill in your keys:

| Variable | Where to get it |
|---|---|
| `GEMINI_API_KEY` | [Google AI Studio](https://aistudio.google.com/app/apikey) |
| `SERPAPI_KEY` | [SerpAPI Dashboard](https://serpapi.com/manage-api-key) |

> **Note:** `SERPAPI_KEY` is optional. If absent, the app uses mock flight data so you can still demo the full UI.

### 5. Run the app

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 📁 Project Structure

```
ai-travelmate/
├── app.py                        # Main Streamlit application
│
├── agents/
│   ├── __init__.py
│   ├── researcher_agent.py       # Destination research via Gemini
│   ├── planner_agent.py          # Day-wise itinerary generation
│   └── hotel_restaurant_agent.py # Hotel & restaurant recommendations
│
├── utils/
│   ├── __init__.py
│   ├── flight_utils.py           # SerpAPI flight fetching & filtering
│   ├── formatters.py             # HTML/Markdown formatting helpers
│   ├── currency_utils.py         # Currency reference data
│   └── prompts.py                # All Gemini prompt templates
│
├── components/
│   ├── __init__.py
│   └── ui_components.py          # Streamlit UI rendering functions
│
├── tests/
│   ├── __init__.py
│   ├── test_flight_utils.py      # Unit tests for flight utilities
│   └── test_formatters.py        # Unit tests for formatters
│
├── .streamlit/
│   └── config.toml               # Streamlit theme configuration
│
├── .env.example                  # API key template
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🤖 AI Agents

### Researcher Agent
Gathers destination insights — top attractions, cultural tips, local transport, safety advice, and recommended experiences tailored to the traveller's theme and activities.

### Planner Agent
Creates a detailed day-by-day schedule covering morning/afternoon/evening activities, transport between venues, dining suggestions, and an overall budget breakdown.

### Hotel & Restaurant Finder Agent
Recommends 5 hotels (across budget tiers) and 6 restaurants with cuisine type, price range, signature dishes, and why each suits the traveller's profile.

---

## 🛠️ Technologies

| Technology | Role |
|---|---|
| **Python 3.10+** | Core language |
| **Streamlit** | Interactive web UI |
| **Google Gemini 1.5 Flash** | AI agent reasoning & content generation |
| **SerpAPI** | Real-time Google Flights data |
| **Pandas** | Data preprocessing |
| **Requests** | HTTP API calls |
| **python-dotenv** | Secure API key management |
| **pytest** | Unit testing |

---

## 🧪 Running Tests

```bash
pytest tests/ -v
```

With coverage:

```bash
pytest tests/ --cov=. --cov-report=html
```

---

## 🛣️ Roadmap

- [ ] Voice input support
- [ ] Multi-language interface (Hindi, Spanish, French, etc.)
- [ ] Automated booking deep-links (flights & hotels)
- [ ] Visa & travel insurance recommendations
- [ ] AR/VR destination previews
- [ ] Real-time weather integration
- [ ] Offline mode with cached popular destinations

---

## 📄 License

This project is licensed under the **MIT License** – see [LICENSE](LICENSE) for details.

---

## 📚 Citation

If you use this work in academic research, please cite:

```bibtex
@article{enuguru2026aitravelmate,
  title   = {AI TRAVELMATE - An Intelligent Agent for Smart Travel Planning and Assistance},
  author  = {Enuguru, Hanuman Sai Gupta and Garaka, Sneha Latha and Pratti, Gayatri
             and Teki, Vijayaratnam and Tanimki, Prabhu Das and Satti, Bhanu Prakash Reddy},
  journal = {Global Journal of Engineering Innovations \& Interdisciplinary Research},
  volume  = {6},
  number  = {2},
  pages   = {0142},
  year    = {2026}
}
```

---

## 🙏 Acknowledgements

Developed at **Sri Vasavi Engineering College**, Department of Computer Science Engineering, Tadepalligudem, Andhra Pradesh, India.
