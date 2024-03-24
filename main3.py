import os
from dotenv import load_dotenv
import google.generativeai as genai
import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

# Load Google API key from environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# HTML form for user input
html_form = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sentiment Analysis</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
            animation: fadeIn 1s ease-in-out;
        }
        .container {
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            animation: slideIn 1s ease-in-out;
        }
        h1 {
            text-align: center;
            color: #333;
            animation: fadeInUp 1s ease-in-out;
        }
        form {
            text-align: center;
            animation: fadeInUp 1s ease-in-out;
        }
        label {
            font-size: 18px;
            color: #555;
            animation: fadeInUp 1s ease-in-out;
        }
        textarea {
            width: 100%;
            padding: 10px;
            margin-top: 5px;
            margin-bottom: 15px;
            border: 1px solid #ccc;
            border-radius: 5px;
            resize: vertical;
            animation: fadeInUp 1s ease-in-out;
        }
        button {
            padding: 10px 20px;
            background-color: #4caf50;
            color: #fff;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s ease;
            animation: fadeInUp 1s ease-in-out;
        }
        button:hover {
            background-color: #45a049;
        }

        @keyframes fadeIn {
            0% {
                opacity: 0;
            }
            100% {
                opacity: 1;
            }
        }

        @keyframes fadeInUp {
            0% {
                opacity: 0;
                transform: translateY(20px);
            }
            100% {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes slideIn {
            0% {
                opacity: 0;
                transform: translateY(-20px);
            }
            100% {
                opacity: 1;
                transform: translateY(0);
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Larsen and Toubro's Sentiment Analysis</h1>
        <form action="/get_sentiment" method="post">
            <label for="text">Enter text:</label><br>
            <textarea id="text" name="text" rows="4" cols="50" placeholder="Enter your text here..."></textarea><br>
            <button type="submit">Submit</button>
        </form>
    </div>
</body>
</html>

"""

# Function to generate AI content
def generate_ai_content(input_text):
    prompt = """You are a text sentiment analyzer. Perform sentiment analysis on the provided text across 10 categories: 
    Positive, Negative, Neutral, Sarcastic, Anger, Humor, Fear, Sadness, Joy, Political. 
    Output the sentiment classification for each category without explanations on the scale of 1 to 10 showing the intensity
    of the sentiment. Return your response as a python dictionary written in the form a string. Give only the bracket part.
    The text on which the sentiment analysis is to be performed will be appended here: """
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + input_text)
    model.temperature = 0.01
    return response.text

# Route for rendering HTML form
@app.get("/", response_class=HTMLResponse)
async def home():
    return html_form

# Route for handling form submission and getting sentiment analysis
@app.post("/get_sentiment")
async def get_sentiment(request: Request, text: str = Form(...)):
    input_text = text
    response_str = generate_ai_content(input_text)
    response_dict = eval(response_str)

    # Create HTML response with sliders for each emotion category
    html_response = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sentiment Analysis Result</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f2f2f2;
                margin: 0;
                padding: 20px;
            }}

            .container {{
                max-width: 600px;
                margin: 0 auto;
                background-color: #fff;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                padding: 20px;
                animation: fadeIn 1s ease-in-out;
            }}

            @keyframes fadeIn {{
                0% {{
                    opacity: 0;
                }}
                100% {{
                    opacity: 1;
                }}
            }}

            h2 {{
                color: #333;
                margin-bottom: 20px;
            }}

            p {{
                margin-bottom: 10px;
                color: #555;
            }}

            p.input-text {{
                font-style: italic;
            }}

            p.result-text {{
                font-weight: bold;
                font-size: 18px;
                color: #007bff; /* Blue color */
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Sentiment Analysis Result:</h2>
            <p class="input-text">Input Text: {input_text}</p>
    """.format(input_text=input_text)
    
    for emotion, value in response_dict.items():
        html_response += """
            <label for="{0}">{0}</label>
            <input type="range" id="{0}" name="{0}" min="0" max="10" value="{1}" disabled>
            <br>
        """.format(emotion, value)
    
    html_response += """
        </div>
    </body>
    </html>
    """

    return HTMLResponse(content=html_response)


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
