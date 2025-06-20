from fastapi import FastAPI, Form, Request, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from my_agents.teachers import professor
from agents.agents import Runner
import uuid

app = FastAPI()

chat_sessions = {}

def render_html(chat_bubbles: str = ""):
    return f"""
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: var(--bg, #f4f4f4);
                color: var(--text, black);
                padding: 0;
                margin: 0;
                transition: background 0.3s, color 0.3s;
            }}
            .header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 15px;
                background-color: #343a40;
                color: white;
            }}
            .header img {{
                width: 40px;
                height: 40px;
                border-radius: 50%;
                margin-right: 10px;
            }}
            .header h1 {{
                font-size: 20px;
                margin: 0;
                display: flex;
                align-items: center;
            }}
            .toggle-btn {{
                background: #007bff;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 8px;
                cursor: pointer;
                font-size: 14px;
            }}
            .container {{
                max-width: 600px;
                margin: auto;
                background: var(--container, white);
                padding: 15px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
                margin-top: 20px;
            }}
            .bubble {{
                padding: 10px 15px;
                border-radius: 15px;
                margin: 10px 0;
                line-height: 1.4;
                word-wrap: break-word;
            }}
            .user {{
                background-color: #d1e7dd;
            }}
            .bot {{
                background-color: #e2e3e5;
            }}
            form {{
                display: flex;
                flex-direction: column;
                gap: 10px;
                margin-top: 15px;
            }}
            input[type="text"] {{
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 8px;
                font-size: 16px;
            }}
            input[type="submit"],
            .clear-btn {{
                background-color: #007bff;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                cursor: pointer;
            }}
            .clear-btn {{
                background-color: #dc3545;
            }}
            input[type="submit"]:hover {{
                background-color: #0056b3;
            }}
            .clear-btn:hover {{
                background-color: #b02a37;
            }}
            @media screen and (max-width: 600px) {{
                .container {{
                    margin: 5px;
                    padding: 10px;
                }}
                input[type="text"],
                input[type="submit"],
                .clear-btn {{
                    font-size: 15px;
                    padding: 8px;
                }}
                .header h1 {{
                    font-size: 16px;
                }}
                .header img {{
                    width: 30px;
                    height: 30px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1><img src="https://cdn-icons-png.flaticon.com/512/4712/4712104.png"> Professor Chatbot</h1>
            <button onclick="toggleDark()" class="toggle-btn">🌙 Theme</button>
        </div>

        <div class="container" id="chat-container">
            {chat_bubbles}
            <form method="post">
                <input type="text" name="message" placeholder="Type your message..." required autofocus>
                <input type="submit" value="Send">
            </form>
            <form method="post" action="/clear">
                <button class="clear-btn" type="submit">🗑️ Clear Chat</button>
            </form>
        </div>

        <script>
            window.onload = function() {{
                window.scrollTo(0, document.body.scrollHeight);
                const inputField = document.querySelector('input[name="message"]');
                if (inputField) {{
                    inputField.value = "";
                    inputField.focus();
                }}

                // Apply dark theme if saved
                if (localStorage.getItem("dark") === "true") {{
                    document.documentElement.style.setProperty('--bg', '#121212');
                    document.documentElement.style.setProperty('--text', 'white');
                    document.documentElement.style.setProperty('--container', '#1e1e1e');
                }}
            }};

            function toggleDark() {{
                const dark = localStorage.getItem("dark") === "true";
                localStorage.setItem("dark", !dark);
                location.reload();
            }}
        </script>
    </body>
    </html>
    """

@app.get("/", response_class=HTMLResponse)
async def home(session_id: str = Cookie(default=None)):
    if not session_id:
        session_id = str(uuid.uuid4())
        response = RedirectResponse(url="/")
        response.set_cookie(key="session_id", value=session_id)
        return response

    user_history = chat_sessions.get(session_id, [])
    chat_bubbles = "".join(f"<div class='bubble {speaker.lower()}'><strong>{speaker}:</strong><br>{msg}</div>" for speaker, msg in user_history)

    return render_html(chat_bubbles=chat_bubbles)

@app.post("/", response_class=HTMLResponse)
async def chat(request: Request, message: str = Form(...), session_id: str = Cookie(default=None)):
    if not session_id:
        session_id = str(uuid.uuid4())
        response = RedirectResponse(url="/")
        response.set_cookie(key="session_id", value=session_id)
        return response

    result = await Runner.run(professor, message)
    chat_sessions.setdefault(session_id, []).extend([
        ("You", message),
        ("Professor", result)
    ])

    chat_bubbles = "".join(f"<div class='bubble {speaker.lower()}'><strong>{speaker}:</strong><br>{msg}</div>" for speaker, msg in chat_sessions[session_id])
    return render_html(chat_bubbles=chat_bubbles)

@app.post("/clear", response_class=HTMLResponse)
async def clear_chat(session_id: str = Cookie(default=None)):
    if session_id in chat_sessions:
        chat_sessions[session_id] = []
    return RedirectResponse(url="/", status_code=303)
