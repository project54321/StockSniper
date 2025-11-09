📊 Stock Dashboard

A sleek, interactive dashboard to track stock prices, analyze key financial metrics, and stay updated on the latest news for any publicly traded company. Built with Streamlit, yfinance, Alpha Vantage, Plotly, and StockNews API, this dashboard provides investors, students, and finance enthusiasts with a modern and visually appealing interface for financial analysis.

Features
1. Stock Price Data

Pulls historical stock data using Yahoo Finance
.

Displays a line chart of closing prices over a selected date range.

Shows raw data in a scrollable table with row and column counts.

Automatically detects the Close price column for plotting.

2. Price Metrics

Calculates key metrics including:

Annual Return (%)

Volatility (Standard Deviation)

Risk-Adjusted Return (Sharpe ratio-like metric)

Metrics are presented with st.metric cards for easy readability.

Historical price data is available in an expandable table for detailed review.

3. Fundamental Financial Data

Pulls annual balance sheets, income statements, and cash flow statements using the Alpha Vantage API
.

Financial statements are neatly organized and displayed inside expanders for a clean, uncluttered layout.

Allows users to analyze company fundamentals at a glance.

4. News Feed

Fetches top 10 news articles about the selected company using StockNews API
.

Displays publish date, title, summary, and sentiment analysis (title & summary).

Each article is presented in a collapsible expander to reduce visual clutter.

5. Modern Layout

Inputs (ticker and date range) are displayed in a top bar with columns, not a sidebar, for a sleek interface.

Metrics, charts, tables, and news are responsive and visually distinct.

Footer with credit and GitHub link added for professional touch.

Demo

Installation
1. Clone the repository
git clone https://github.com/project54321/StockDashboard.git
cd StockDashboard

2. Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows

3. Install dependencies
pip install -r requirements.txt


requirements.txt example:

streamlit
yfinance
pandas
numpy
plotly
python-dotenv
alpha_vantage
stocknews

4. Add your API Key

Create a .env file in the project root:

API_KEY=YOUR_ALPHA_VANTAGE_API_KEY


Important: Keep .env in .gitignore to avoid committing your key.

Usage

Run the Streamlit app:

streamlit run app.py


Enter a ticker symbol (e.g., AAPL, MSFT).

Select start and end dates.

Navigate between the Pricing Data, Fundamental Data, and Top 10 News tabs.

Expand sections to view detailed data or news articles.

Environment Variables

API_KEY: Required for accessing Alpha Vantage data.

Loaded using python-dotenv
 for security.

Project Structure
StockDashboard/
│
├── app.py             # Main Streamlit application
├── requirements.txt   # Python dependencies
├── .env               # API keys (not committed)
├── README.md          # Project documentation
└── assets/            # Optional folder for screenshots, logos, etc.

Technologies Used

Python – Core programming language.

Streamlit – Interactive dashboard framework.

Plotly – Interactive charts and visualizations.

pandas / numpy – Data manipulation and calculations.

yfinance – Historical stock prices.

Alpha Vantage – Fundamental financial statements.

StockNews – Company news feed and sentiment analysis.

Contributing

Contributions are welcome! To contribute:

Fork the repository.

Create a new branch for your feature/bugfix.

Submit a pull request with a detailed description of your changes.

License

MIT License

Credits

Made by Arjun Averineni | GitHub
