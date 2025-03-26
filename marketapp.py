import streamlit as st
import os
import tempfile

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
        
        col1, col2 = st.columns([3, 2])
        with col1:
            st.image(st.session_state.image_path, caption=f"{stock} Chart", use_column_width=True)
        with col2:
            st.subheader("💡 AI Insights")
            st.write(st.session_state.ai_insights)

        # Create a downloadable text file
        analysis_text = f"Stock Analysis for {stock} ({market})\n\n" + st.session_state.ai_insights
        analysis_path = os.path.join(tempfile.gettempdir(), f"{stock}_{market}_analysis.txt")
        with open(analysis_path, "w") as file:
            file.write(analysis_text)

        # Streamlit Download Button
        with open(analysis_path, "rb") as file:
            st.download_button(
                label="📥 Download Analysis",
                data=file,
                file_name=f"{stock}_{market}_analysis.txt",
                mime="text/plain"
            )

        st.markdown("---")

        # Back button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔙 Back to Home"):
                st.session_state.page = "page1"
                st.session_state.internal_results_available = False
                st.rerun()
