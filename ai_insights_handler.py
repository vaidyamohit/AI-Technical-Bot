import google.generativeai as genai
import PIL.Image

class AIInsights:
    def __init__(self, api_key):
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name="gemini-2.0-flash")

    def get_ai_insights(self, image_path, stock, market):
        image = PIL.Image.open(image_path)
        prompt = f"""
        This is a stock performance image of '{stock}' for the last 100 days on market: '{market}'.
        It includes closing prices, moving averages (7-day, 20-day, 100-day, 200-day), and Fibonacci retracement levels.
        
        Based on trading volume, moving averages, and Fibonacci levels:
        - **Buy Range:** At what price is it ideal to enter a position?
        - **Exit Range:** At what price should an investor consider selling?
        
        Please provide analysis and recommendations.
        """
        response = self.model.generate_content([prompt, image])
        return response
