from flask import Flask, Response, render_template_string
import subprocess
import os

app = Flask (name)
process = None

@app.route('/')
def home():
    return '''
        <h2>App Controller</h2>
        <a href="/run">▶️ Start app.py</a><br>
        <a href="/stop">⛔ Stop app.py</a><br>
        <a href="/logs">📜 View Live Logs</a>
    '''

@app.route('/run')
def run_script():
    global process
    if process is None or process.poll() is not None:
        with open("log.txt", "w") as f:
            process = subprocess.Popen(
                ["python3", "FOxTcpBot.py"],
                stdout=f,
                stderr=subprocess.STDOUT
            )
        return "✅ FOxTcpBot started in background"
    else:
        return "⚠️ FOxTcpBot is already running"

@app.route('/stop')
def stop_script():
    global process
    if process and process.poll() is None:
        process.terminate()
        return "🛑 FOxTcpBot has been stopped"
    else:
        return "⚠️ FOxTcpBot is not running"

@app.route('/logs')
def stream_logs():
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Live Logs</title>
        <meta http-equiv="refresh" content="1">
        <style>
            body {
                background-color: #111;
                color: #0f0;
                font-family: monospace;
                padding: 10px;
            }
            pre {
                white-space: pre-wrap;
                word-wrap: break-word;
                border: 1px solid #444;
                padding: 10px;
                background: #000;
                max-height: 80vh;
                overflow-y: scroll;
            }
            button {
                background: #0f0;
                border: none;
                padding: 8px 16px;
                font-weight: bold;
                color: #000;
                cursor: pointer;
                border-radius: 5px;
                margin-bottom: 10px;
            }
        </style>
        <script>
            function copyLogs() {
                const text = document.getElementById('logBox').innerText;
                navigator.clipboard.writeText(text).then(() => {
                    alert("✅ Logs copied to clipboard!");
                });
            }
        </script>
    </head>
    <body>
        <h3>📜 Live Logs</h3>
        <button onclick="copyLogs()">📋 Copy Logs</button>
        <pre id="logBox">{{ logs }}</pre>
    </body>
    </html>
    '''
    logs = ""
    if os.path.exists("log.txt"):
        with open("log.txt", "r") as f:
            logs = f.read()[-5000:]  # Show last 5000 characters
    return render_template_string(html, logs=logs)

if name == 'main':
    app.run(debug=True)
