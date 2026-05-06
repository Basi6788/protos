from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import base64
import time
from collections import deque
from google.protobuf.json_format import MessageToDict

app = Flask(__name__)
CORS(app)

# ==========================================
# 🧠 1. DYNAMIC PROTOBUF LOADER (FIXED & BULLETPROOF)
# ==========================================
PROTO_MAP = {}
try:
    from ff_proto import account_show_pb2, core_pb2, count_likes_pb2, freefire_pb2, register_req_pb2, send_like_pb2
    
    modules = [account_show_pb2, core_pb2, count_likes_pb2, freefire_pb2, register_req_pb2, send_like_pb2]
    
    for mod in modules:
        # Protobuf ki files me messages ko unke internal DESCRIPTOR se nikalna zyada safe hai
        if hasattr(mod, 'DESCRIPTOR'):
            for msg_name in mod.DESCRIPTOR.message_types_by_name.keys():
                if hasattr(mod, msg_name):
                    PROTO_MAP[msg_name] = getattr(mod, msg_name)
                    
    print(f"Loaded {len(PROTO_MAP)} Proto Messages Successfully!")
except Exception as e:
    print("Proto Loading Error:", str(e))

# ==========================================
# 📋 2. LOGGING SYSTEM
# ==========================================
api_logs = deque(maxlen=200)

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
# 🚀 3. API ENDPOINTS 
# ==========================================
@app.route('/api/decode', methods=['POST'])
def decode_proto():
    try:
        data = request.json
        msg_name = data.get('msg_name') 
        b64_data = data.get('data')     

        if not msg_name or msg_name not in PROTO_MAP:
            add_log("DECODE_FAIL", msg_name or "UNKNOWN", 404, b64_data[:50] if b64_data else "None", "Proto message class not found.")
            return jsonify({"error": f"Proto message '{msg_name}' not found."}), 404

        raw_bytes = base64.b64decode(b64_data)
        
        proto_obj = PROTO_MAP[msg_name]()
        proto_obj.ParseFromString(raw_bytes)
        
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
# 👑 4. PYTHON API DASHBOARD (AURORA GLOW THEME + MOBILE FIX)
# ==========================================
@app.route('/', methods=['GET'])
def dashboard():
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>👑 PYTHON CORE | KING NEXUS</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
            body { background-color: #030008; color: #e2e8f0; font-family: 'JetBrains Mono', monospace; }
            h1 { font-family: 'Orbitron', sans-serif; }
            ::-webkit-scrollbar { width: 4px; height: 4px; }
            ::-webkit-scrollbar-track { background: #000; }
            ::-webkit-scrollbar-thumb { background: #8b5cf6; border-radius: 10px; }
            /* AURORA GLOW & SHADOWS */
            .aurora-glow { box-shadow: 0 0 20px rgba(139, 92, 246, 0.4), inset 0 0 10px rgba(139, 92, 246, 0.2); border: 1px solid rgba(139, 92, 246, 0.5); }
            .glass-panel { background: rgba(10, 10, 15, 0.85); backdrop-filter: blur(12px); border: 1px solid rgba(139, 92, 246, 0.2); transition: all 0.3s ease; }
            .glass-panel:hover { box-shadow: 0 0 15px rgba(139, 92, 246, 0.3); border-color: rgba(139, 92, 246, 0.6); }
            pre { white-space: pre-wrap; word-wrap: break-word; font-size: 9px; line-height: 1.4; }
        </style>
    </head>
    <body class="p-3 sm:p-6 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-purple-900/20 via-[#030008] to-black min-h-screen">
        <div class="max-w-7xl mx-auto">
            <header class="flex flex-col sm:flex-row justify-between items-center mb-6 border-b border-purple-500/20 pb-4 gap-4">
                <div class="flex items-center gap-3 w-full sm:w-auto justify-center sm:justify-start">
                    <div class="p-2 bg-purple-900/30 rounded-full aurora-glow flex-shrink-0">
                        <span class="text-xl">👑</span>
                    </div>
                    <div>
                        <h1 class="text-2xl sm:text-3xl font-black text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-blue-500 tracking-widest uppercase">PYTHON_CORE</h1>
                        <p class="text-[10px] text-purple-400/70 mt-1 uppercase tracking-[0.2em] text-center sm:text-left">King Nexus Decode Engine</p>
                    </div>
                </div>
                <div class="text-[10px] sm:text-xs bg-purple-900/30 border border-purple-500/50 px-4 py-2 rounded-full text-purple-300 font-black tracking-widest aurora-glow whitespace-nowrap">
                    PROTOS ONLINE: <span id="proto-count" class="text-white">""" + str(len(PROTO_MAP)) + """</span>
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
                        let statusColor = isError ? 'text-red-400 bg-red-900/30 border-red-500/50' : 'text-emerald-400 bg-emerald-900/30 border-emerald-500/50';
                        return \`
                        <div class="glass-panel p-3 sm:p-4 rounded-xl">
                            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center border-b border-white/5 pb-3 mb-3 gap-2">
                                <div class="flex items-center gap-2 flex-wrap">
                                    <span class="text-purple-300 font-bold text-xs bg-purple-900/30 px-2 py-1 rounded border border-purple-500/30">\${l.action}</span>
                                    <span class="font-black text-white text-[11px] sm:text-xs tracking-wider">\${l.msg_name}</span>
                                    <span class="text-gray-500 text-[9px]">\${l.time}</span>
                                </div>
                                <span class="\${statusColor} border text-[10px] font-black px-3 py-1 rounded-full shadow-sm">\${l.status}</span>
                            </div>
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                                <div class="relative pt-2">
                                    <div class="absolute -top-1 left-2 bg-[#0a0a0a] text-gray-400 text-[8px] font-black px-2 py-0.5 rounded-full border border-gray-700">NODE SENT</div>
                                    <pre class="bg-[#050508] p-3 rounded-lg h-32 overflow-auto text-purple-300/80 border border-white/5 custom-scroll">\${JSON.stringify(l.payload, null, 2)}</pre>
                                </div>
                                <div class="relative pt-2">
                                    <div class="absolute -top-1 left-2 bg-[#0a0a0a] text-gray-400 text-[8px] font-black px-2 py-0.5 rounded-full border border-gray-700">PYTHON DECODED</div>
                                    <pre class="bg-[#050508] p-3 rounded-lg h-32 overflow-auto \${isError ? 'text-red-300/80' : 'text-emerald-300/80'} border border-white/5 custom-scroll">\${JSON.stringify(l.response, null, 2)}</pre>
                                </div>
                            </div>
                        </div>\`;
                    }).join('');
                } catch(e) {}
            }
            setInterval(fetchLogs, 1500);
            fetchLogs();
        </script>
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
