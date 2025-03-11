# test_gemini.py
import google.generativeai as genai
from config import API_KEY, MODEL_ID

# Set your API key
genai.configure(api_key=API_KEY)

# Initialize the model
model = genai.GenerativeModel(MODEL_ID)

# Test prompt
prompt = "Hello, can you introduce yourself?"

# Generate response
response = model.generate_content(prompt)

print("Gemini API Response:\n", response.text)
