# 📊 Scalable AI-Driven BI Dashboard
**A High-Performance Analytics System Bridging Business Logic and Python Engineering**

## 🎯 The "Why" Behind the Project
After graduating with a **B.E. in Computer Science in 2020**, I spent 6 years gaining deep operational experience across the **Telecom, Service, and Private Enterprise** sectors. 

Throughout these roles, I identified a recurring challenge: **Data Overload.** Businesses struggle to turn thousands of rows of manual records into actionable decisions. I built this dashboard to solve that problem—combining my "boots-on-the-ground" business experience with professional-grade Python development.

## 🚀 Key Features
* **Enterprise-Scale Processing:** Engineered to handle **10,000+ SKUs** without performance lag using specialized data caching.
* **AI-Powered Stocking Logic:** A custom-built weighted scoring engine that identifies "Best Value" and "Top Performer" products based on sales-to-price ratios.
* **Dynamic Visualizations:** Interactive Plotly scatter plots and trend analysis for deep-dive market exploration.
* **Global Search Architecture:** A robust search implementation that allows users to query the entire database instantly.

## 🛠️ Technical Problem Solving
To move beyond "student-level" code, I implemented several professional optimizations:

1.  **Memory Management:** Utilized `st.cache_data` to ensure the 10,000+ row dataset is loaded into memory only once, significantly reducing server load.
2.  **Modular Logic:** Separated the "UI" from the "Business Logic." The KPI calculations (`analysis.py`) and AI scoring (`recommendation.py`) are kept in a separate `utils/` directory for professional maintainability.
3.  **Visual Throttling:** Implemented user-controlled data sampling to ensure the browser remains responsive even when handling massive datasets.

## 🧰 Tech Stack
* **Language:** Python 3.x
* **Library (Data):** Pandas (Vectorized operations for speed)
* **Library (UI):** Streamlit (Web Interface)
* **Library (Viz):** Plotly Express (Interactive charts)
* **Deployment:** Streamlit Community Cloud / GitHub

## 📁 Project Structure
```text
├── app.py                # Main User Interface & Dashboard Layout
├── utils/                # Professional Modular Logic Folder
│   ├── analysis.py       # KPI & Data Processing Engine
│   └── recommendation.py # AI Scoring & Stocking Logic
├── requirements.txt      # Dependency Management
└── data/                 # Sample Enterprise Dataset (10k+ rows)