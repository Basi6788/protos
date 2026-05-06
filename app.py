from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import base64
import inspect
import time
from collections import deque
from google.protobuf.message import Message
from google.protobuf.json_format import MessageToDict, ParseDict

app = Flask(__name__)
CORS(app)

# ==========================================
# 🧠 1. DYNAMIC PROTOBUF LOADER
# ==========================================
PROTO_MAP = {}
try:
    # Tumhari image ke mutabiq sabhi files import kar rahe hain
    from ff_proto import account_show_pb2, core_pb2, count_likes_pb2, freefire_pb2, register_req_pb2, send_like_pb2
    
    modules = [account_show_pb2, core_pb2, count_likes_pb2, freefire_pb2, register_req_pb2, send_like_pb2]
    
    # Har module me check karo ke kon kon se protobuf Message classes hain
    for mod in modules:
        for name, obj in inspect.getmembers(mod):
            if inspect.isclass(obj) and issubclass(obj, Message):
                PROTO_MAP[name] = obj
    print(f"Loaded {len(PROTO_MAP)} Proto Messages Successfully!")
except Exception as e:
    print("Proto Loading Error:", str(e))

# ==========================================
# 📋 2. LOGGING SYSTEM (For Dashboard)
# ==========================================
api_logs = deque(maxlen=200) # Memory safe on Vercel

def add_log(action, msg_name, status, payload, response=""):
    log_entry = {
        "id": str(int(time.time() * 1000)),
        "time": time.strftime('%H:%M:%S'),
        "action": action,
        "msg_name": msg_name,
        "status": status,
        "payload": payload,
        "response": response
    }
    api_logs.appendleft(log_entry)

# ==========================================
# 🚀 3. API ENDPOINTS (Node.js yahan data bhejega)
# ==========================================
@app.route('/api/decode', methods=['POST'])
def decode_proto():
    """ Node.js se base64 binary lega aur usay JSON me decode karega """
    try:
        data = request.json
        msg_name = data.get('msg_name') # e.g. "LoginRes" or "MajorLogin"
        b64_data = data.get('data')     # Raw binary in base64

        if not msg_name or msg_name not in PROTO_MAP:
            add_log("DECODE_FAIL", msg_name or "UNKNOWN", 404, b64_data[:50], "Proto class not found in python files.")
            return jsonify({"error": f"Proto message '{msg_name}' not found in Python loaded classes."}), 404

        # Decode base64 back to binary
        raw_bytes = base64.b64decode(b64_data)
        
        # Parse using the specific class
        proto_obj = PROTO_MAP[msg_name]()
        proto_obj.ParseFromString(raw_bytes)
        
        # Convert to Dictionary (JSON)
        result_dict = MessageToDict(proto_obj, preserving_proto_field_name=True)
        
        add_log("DECODE_SUCCESS", msg_name, 200, f"Size: {len(raw_bytes)} bytes", result_dict)
        return jsonify({"success": True, "data": result_dict})

    except Exception as e:
        add_log("DECODE_ERROR", msg_name, 500, b64_data[:50] if b64_data else "", str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/api/logs/sync', methods=['GET'])
def get_logs():
    return jsonify(list(api_logs))

# ==========================================
# 👑 4. PYTHON API DASHBOARD
# ==========================================
@app.route('/', methods=['GET'])
def dashboard():
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>👑 Python Proto Decoder | API Logs</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
            body { background-color: #030008; color: #e2e8f0; font-family: 'JetBrains Mono', monospace; }
            .glass-panel { background: rgba(10, 10, 15, 0.8); backdrop-filter: blur(10px); border: 1px solid rgba(139, 92, 246, 0.3); }
        </style>
    </head>
    <body class="p-6 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-blue-900/20 via-[#030008] to-black min-h-screen">
        <div class="max-w-6xl mx-auto">
            <header class="flex justify-between items-center mb-6 border-b border-blue-500/20 pb-4">
                <div>
                    <h1 class="text-3xl font-black text-blue-400">🐍 PYTHON API CORE</h1>
                    <p class="text-xs text-gray-400 mt-1">Listening to Node.js Engine Requests...</p>
                </div>
                <div class="text-xs bg-blue-900/30 border border-blue-500/50 px-4 py-2 rounded text-blue-300 font-bold">
                    AVAILABLE PROTOS: """ + str(len(PROTO_MAP)) + """
                </div>
            </header>
            
            <div id="logs-container" class="space-y-4"></div>
        </div>

        <script>
            async function fetchLogs() {
                try {
                    const res = await fetch('/api/logs/sync');
                    const logs = await res.json();
                    
                    document.getElementById('logs-container').innerHTML = logs.map(l => {
                        let isError = l.status >= 400;
                        let statusColor = isError ? 'text-red-400' : 'text-green-400';
                        return `
                        <div class="glass-panel p-4 rounded-lg">
                            <div class="flex justify-between border-b border-white/5 pb-2 mb-2">
                                <span class="font-bold text-blue-300">[${l.time}] ${l.action} -> ${l.msg_name}</span>
                                <span class="${statusColor} font-black">${l.status}</span>
                            </div>
                            <div class="grid grid-cols-2 gap-2 text-[10px]">
                                <pre class="bg-black p-2 h-32 overflow-auto text-gray-400">Node Sent:\n${JSON.stringify(l.payload, null, 2)}</pre>
                                <pre class="bg-black p-2 h-32 overflow-auto ${isError ? 'text-red-300' : 'text-emerald-300'}">Python Replied:\n${JSON.stringify(l.response, null, 2)}</pre>
                            </div>
                        </div>`;
                    }).join('');
                } catch(e) {}
            }
            setInterval(fetchLogs, 2000);
            fetchLogs();
        </script>
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
