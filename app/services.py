import google.generativeai as genai  #Importing the Gemini API client
import os  #environment variable management
from dotenv import load_dotenv   #loading environment variables from .env file
load_dotenv()  
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))  #Configure the Gemini API client with the API key from environment variables


# this function is for the generate the market report for sector and market data using model.
async def generate_market_report(sector: str, market_data: str):
    # this block is for getting market report for sector and market data using model.
    try:
        model_name = 'gemini-flash-latest'
        model = genai.GenerativeModel(model_name)
        clean_sector = sector.strip().title()
        prompt = (
            f"Analyze the following market data for the {sector} sector in India. "
            f"Provide a structured markdown report: {market_data}"
        )
        response = model.generate_content(prompt)
        if response and response.text:
            return response.text
        return "AI Analysis failed to give detailed report."
    # this block for if the model fails, and want to see the error and also which models are available to our API key.
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Available models for your key:")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name}")
        raise e