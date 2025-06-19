from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from agents import Runner
from my_agents.teachers import professor

app = FastAPI()

def render_html(user: str = "", bot: str = "", message: str = ""):
    chat_bubbles = ""
    if user and bot:
        chat_bubbles = f"""
            <div class='bubble user'><strong>You:</strong><br>{user}</div>
            <div class='bubble bot'><strong>Professor:</strong><br>{bot}</div>
        """

    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>🧠 Professor Chat</title>
      <style>
  * {{
    box-sizing: border-box;
  }}
  body {{
    margin: 0;
    padding: 0;
    background: linear-gradient(145deg, #dde6f0, #ffffff);
    font-family: 'Segoe UI', sans-serif;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
  }}
  .chat-box {{
    background: #ffffff;
    width: 95%;
    max-width: 500px;
    padding: 1.5rem;
    border-radius: 15px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    display: flex;
    flex-direction: column;
    max-height: 90vh;
    overflow-y: auto;
  }}
  h2 {{
    text-align: center;
    color: #4f46e5;
    margin-bottom: 1rem;
  }}
  .bubble {{
    padding: 1rem;
    border-radius: 10px;
    margin: 8px 0;
    max-width: 100%;
    overflow-wrap: break-word;
    word-wrap: break-word;
  }}
  .user {{
    background-color: #4f46e5;
    color: white;
    text-align: right;
  }}
  .bot {{
    background-color: #f1f5ff;
    color: #333;
    text-align: left;
  }}
  form {{
    display: flex;
    gap: 0.5rem;
    margin-top: auto;
    flex-wrap: wrap;
  }}
  input[type="text"] {{
    flex: 1;
    padding: 0.75rem;
    border-radius: 8px;
    border: 1px solid #ccc;
    font-size: 1rem;
    min-width: 0;
  }}
  button {{
    background-color: #4f46e5;
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    font-size: 1rem;
    cursor: pointer;
  }}
  .footer {{
    text-align: center;
    font-size: 0.8rem;
    margin-top: 1rem;
    color: #888;
  }}

  @media screen and (max-width: 600px) {{
    .chat-box {{
      padding: 1rem;
      border-radius: 10px;
    }}
    h2 {{
      font-size: 1.2rem;
    }}
    input[type="text"], button {{
      font-size: 0.9rem;
      padding: 0.5rem;
    }}
  }}
</style>

    </head>
    <body>
      <div class="chat-box">
        <h2>🧠 Talk to Professor</h2>

        {chat_bubbles}

        <form method="post">
          <input type="text" name="message" placeholder="Type your message..."  required>
          <button type="submit">Send</button>
        </form>

        <div class="footer">Created by Nizam ul din</div>
      </div>
    </body>
    </html>
    """
    return html_template

@app.get("/", response_class=HTMLResponse)
async def chat_form():
    return render_html()

@app.post("/", response_class=HTMLResponse)
async def chat_response(message: str = Form(...)):
    result = await Runner.run(professor, message)
    return render_html(user=message, bot=result.final_output, message=message)
