import google.generativeai as genai
import PIL.Image
import io

class AIInsights:
    def __init__(self, api_key):
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name="gemini-2.0-flash")

    def get_technical_insights(self, image_path, stock, market):
        with PIL.Image.open(image_path) as image:
            prompt = (
                f"This is an image of the stock performance of '{stock}' over the last 100 days on the '{market}' market. "
                "Based on the volume traded, closing prices, and 7- and 20-day moving averages, please provide an analysis and "
                "recommendation on whether this stock should be purchased."
            )
            response = self.model.generate_content([prompt, image])
            return response.text

    def get_fundamental_insights(self, financial_ratios, stock):
        prompt = (
            f"Here are the key financial ratios for '{stock}':\n"
            f"ROIC: {financial_ratios.get('ROIC (%)', 'N/A')}%\n"
            f"ROA: {financial_ratios.get('ROA (%)', 'N/A')}%\n"
            f"Debt-to-Equity: {financial_ratios.get('Debt-to-Equity', 'N/A')}\n"
            f"Current Ratio: {financial_ratios.get('Current Ratio', 'N/A')}\n"
            f"EBIT Margin: {financial_ratios.get('EBIT Margin (%)', 'N/A')}%\n"
            f"Operating Cash Flow to Debt: {financial_ratios.get('Operating Cash Flow to Debt', 'N/A')}\n\n"
            "Based on these financial ratios, please analyze the company's financial health and provide an investment recommendation."
        )
        response = self.model.generate_content(prompt)
        return response.text
