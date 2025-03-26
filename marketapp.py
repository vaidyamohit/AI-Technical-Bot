from stock_utility_handler import StockAPI, StockAnalyzer
from ai_insights_handler import AIInsights

import streamlit as st
import os
import tempfile
from docx import Document
from docx.shared import Inches

# Initialize session state variables
if 'page' not in st.session_state:
    st.session_state.page = "page1"
    st.session_state.ticker = "RELIANCE"
    st.session_state.market = "BSE"
    st.session_state.image_path = ""
    st.session_state.ai_insights = ""
    st.session_state.internal_results_available = False


# Page 1: Input Page
def page1():
    st.title('📈 Stock AI Agent')

    # Sidebar: Detailed About Section
    st.sidebar.header("ℹ️ About This AI-Powered Stock Analysis Bot")
    st.sidebar.write("""
    ### 📌 Overview  
    This AI-powered stock analysis bot helps **investors, traders, and finance enthusiasts** make **data-driven** decisions.  
    It provides **detailed stock analysis, AI-generated insights, and visualized stock trends**.

    ### 🎯 Who Can Benefit?  
    - **Retail Investors** 📈 - Understand stock trends before investing.  
    - **Day Traders** 💹 - Get insights on short-term movements.  
    - **Financial Analysts** 📊 - Leverage AI for deeper stock analysis.  
    - **Students & Researchers** 🎓 - Learn about market trends and stock behavior.  

    ### 🔍 What This Bot Offers?  
    ✅ **Stock Price Trends:** Analyze stock price movements over time.  
    ✅ **AI-Powered Insights:** Uses AI to suggest if a stock is worth investing in.  
    ✅ **Moving Averages (7-Day & 20-Day):** Identify bullish and bearish trends.  
    ✅ **Trading Volume Analysis:** Understand buying and selling pressure.  
    ✅ **Market Comparisons:** Supports multiple stock markets like **BSE & NASDAQ**.  
    ✅ **Downloadable Reports:** Get a `.docx` file with full analysis and chart.  

    ### ⚡ How It Works?  
    1️⃣ **Enter the stock ticker symbol (e.g., RELIANCE, AAPL, MSFT).**  
    2️⃣ **Select the market (BSE or NASDAQ).**  
    3️⃣ **Click ‘Submit’ to generate insights.**  
    4️⃣ **View stock chart & AI insights.**  
    5️⃣ **Download the full analysis as a `.docx` file.**  

    🚀 **Powered by AI & Machine Learning for Smarter Investing!**

    ---
    © **Copyright 2024 - Mohit Vaidya & Nakul Arora, FORE School of Management**
    """)

    # Input Section
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.ticker = st.text_input("🏷️ Enter Stock Ticker Symbol", value=st.session_state.ticker, key="ticker_input")
    with col2:
        st.session_state.market = st.selectbox("🌍 Select Market", ["BSE", "NASDAQ"], index=["BSE", "NASDAQ"].index(st.session_state.market), key="market_input")

    st.markdown("---")

    # Submit Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button('🚀 Submit'):
            st.session_state.page = "page2"
            st.session_state.internal_results_available = False
            st.rerun()


# Page 2: Analysis Page
def page2():
    st.title(f"📈 Analysis for {st.session_state.ticker} ({st.session_state.market})")

    stock = st.session_state.ticker
    market = st.session_state.market

    if not st.session_state.internal_results_available:
        with st.spinner('🔍 Analyzing... Please wait...'):
            temp_dir = tempfile.gettempdir()
            image_path = os.path.join(temp_dir, f"{market}_{stock}.png")
            st.session_state.image_path = image_path

            try:
                stock_api_obj = StockAPI("1UJ6ACYM0P4MHORZ")
                stock_analyzer_obj = StockAnalyzer()
                ai_insights_obj = AIInsights("AIzaSyAVi1v80vt41mTjZED6BaMs5-74HKFkSk0")

                market_data = stock_api_obj.get_stock_info(stock, market)
                df = stock_analyzer_obj.json_to_dataframe(market_data, stock, market)
                stock_analyzer_obj.plot_stock_data(df, stock, market, image_path)

                response = ai_insights_obj.get_ai_insights(image_path, stock, market)
                st.session_state.ai_insights = "\n".join([part.text for candidate in response.candidates for part in candidate.content.parts])

                st.session_state.internal_results_available = True

            except Exception as e:
                st.error(f"❌ An error occurred: {e}")
                return

    # Display Analysis
    if st.session_state.internal_results_available:
        st.subheader("📊 Chart Analysis")
        
        # Using columns for better layout
        col1, col2 = st.columns([3, 2])
        with col1:
            st.image(st.session_state.image_path, caption=f"{stock} Chart", use_column_width=True)
        with col2:
            st.subheader("💡 AI Insights")
            st.write(st.session_state.ai_insights)

        # 🆕 Create a Word Document
        doc_path = os.path.join(tempfile.gettempdir(), f"{stock}_{market}_analysis.docx")
        doc = Document()
        doc.add_heading(f"Stock Analysis for {stock} ({market})", level=1)

        # Add AI Insights
        doc.add_heading("AI Insights:", level=2)
        doc.add_paragraph(st.session_state.ai_insights)

        # Add Stock Chart
        doc.add_heading("Stock Performance Chart:", level=2)
        doc.add_picture(st.session_state.image_path, width=Inches(5))

        # Save Document
        doc.save(doc_path)

        # 🆕 Streamlit Download Button for `.docx`
        with open(doc_path, "rb") as file:
            st.download_button(
                label="📥 Download Full Analysis (Docx)",
                data=file,
                file_name=f"{stock}_{market}_analysis.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

        st.markdown("---")

        # Back button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔙 Back to Home"):
                st.session_state.page = "page1"
                st.session_state.internal_results_available = False
                st.rerun()


# Route between pages
if st.session_state.page == "page1":
    page1()
elif st.session_state.page == "page2":
    page2()
