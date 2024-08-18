from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import openai

app = FastAPI()

# Set up OpenAI API key
openai.api_key = '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'

templates = Jinja2Templates(directory="templates")

# Function to generate chatbot response
def generate_response(prompt: str) -> str:
    # Define the system message to guide the AI's behavior
    system_message = (
        "You are an AI teacher who uses Socratic questioning, visual learning techniques, "
        "and gamification to help students learn. Engage students with probing questions that "
        "encourage critical thinking, suggest visual aids or diagrams when appropriate, and incorporate "
        "elements of fun and challenge into the learning process."
    )
    
    # Define the messages structure for the API call
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt}
    ]
    
    # Generate the response using GPT-4
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0.7,  # Controls creativity; higher values make output more creative.
        max_tokens=300,  # The max number of tokens the model can use in the response.
        top_p=0.9,  # Top-p sampling for diversity.
        frequency_penalty=0,  # Discourages repetition.
        presence_penalty=0.6  # Encourages introducing new topics or concepts.
    )
    
    # Return the content of the response
    return response['choices'][0]['message']['content']

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/get_response", response_class=JSONResponse)
async def post_get_response(user_input: str = Form(...)):
    bot_response = generate_response(user_input)
    return {"response": bot_response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
