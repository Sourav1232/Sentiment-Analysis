import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = """You are a text sentiment analyser. Perform sentiment analysis on the provided text across 10 categories: 
Positive, Negative, Neutral, Sarcastic, Anger, Humor, Fear, Sadness, Joy, Political. 
Output the sentiment classification for each category without explanations on the scale of 1 to 10 showing the intensity
of the sentiment. Return your response as a python dictionary written in the form a string. Give only the bracket part.
The text on which the sentiment analysis is to be performed will be appended here: """

def generate_ai_content(input_text):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt+input_text)
    model.temperature = 0.01

    return response.text

def main():
    input_text = ""
    input_text = input("Please enter your input: ")
    response_str = generate_ai_content(input_text)
    response_dict = eval(response_str)

    print(type(response_dict))
    print(f"Sentiment:\n{response_dict}")

if __name__== '__main__' :
    main()
