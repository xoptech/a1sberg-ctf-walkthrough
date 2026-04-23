from flask import Flask, request, render_template_string

app = Flask(__name__)

# Load flag from file
try:
    with open("flag.txt", "r") as f:
        FLAG = f.read().strip()
except FileNotFoundError:
    FLAG = "picoCTF{fake_flag_for_testing}"

# The "Forbidden" list - this makes the exploit a challenge!
BLOCKED = [
    "flag", "config", "self", "class", "mro", 
    "subclasses", "import", "os", "system", 
    "eval", "exec"
]

@app.route("/")
def index():
    # We can still use a hardcoded string here for the main page
    template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Echo Chamber | Terminal</title>
        <link rel="stylesheet" href="/static/style.css">
        <script src="/static/script.js" defer></script>
    </head>
    <body>
        <div class="scanline"></div>
        <div class="container">
            <h1>ECHO CHAMBER v1.0.4</h1>
            <p class="typing">The chamber repeats what you say... but some words are forbidden.</p>
            <form action="/echo" method="get">
                <div class="input-wrapper">
                    <span class="prompt">guest@echo:~$</span>
                    <input type="text" name="message" autocomplete="off" autofocus required>
                </div>
                <button type="submit" class="glitch-btn">TRANSMIT</button>
            </form>
        </div>
    </body>
    </html>
    """
    return render_template_string(template)

@app.route("/echo")
def echo():
    msg = request.args.get("message", "")

    # The Filter: It still checks for blocked words
    for word in BLOCKED:
        if word in msg.lower():
            return "ACCESS DENIED: Restricted Keyword Detected.", 403

    # VULNERABLE LINE: The f-string injects 'msg' directly into the template
    # This allows SSTI (Server-Side Template Injection)
    template = f"""
    <!DOCTYPE html>
    <html>
    <head><link rel="stylesheet" href="/static/style.css"></head>
    <body>
        <div class="scanline"></div>
        <div class="container">
            <h1>TRANSMISSION RECEIVED</h1>
            <div class="output-box">
                <p>> {msg}</p>
            </div>
            <a href="/" class="back-link">_RETURN_TO_ROOT</a>
        </div>
    </body>
    </html>
    """
    
    return render_template_string(template)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4690)