import http.server
import socketserver
from socketserver import ThreadingMixIn
import os
import socket
import urllib.parse
import io
import sys
from datetime import datetime

# Check for terminal unicode support (especially for Windows)
def get_emoji(emoji_name, fallback=""):
    try:
        if sys.platform == "win32":
            if "TERM" in os.environ or os.environ.get("WT_SESSION"):
                return emoji_name
            return fallback
        return emoji_name
    except Exception:
        return fallback

# Emojis
ICO_ROCKET = get_emoji("\N{ROCKET}")
ICO_PIN = get_emoji("\N{ROUND PUSHPIN}")
ICO_LINK = get_emoji("\N{LINK SYMBOL}")
ICO_STOP = get_emoji("\N{OCTAGONAL SIGN}")
ICO_CROSS = get_emoji("\N{CROSS MARK}")
ICO_GLOBE = get_emoji("\N{EARTH GLOBE EUROPE-AFRICA}")

# Tab auto-complete if available
try:
    import readline
    if 'libedit' in readline.__doc__:
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.parse_and_bind("tab: complete")
    HAS_READLINE = True
except ImportError:
    HAS_READLINE = False

PORT = 8000

# Logger
class SlimLogger(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        timestamp = datetime.now().strftime("%H:%M:%S")
        client_ip = self.client_address[0]
        try:
            request_line = str(args[0])
            parts = request_line.split()
            if len(parts) > 1:
                url_obj = urllib.parse.urlparse(parts[1])
                raw_path = urllib.parse.unquote(url_obj.path)
                if any(raw_path.lower().endswith(ext) for ext in ['.ico', '.map']):
                    return
                is_preview = "preview=1" in url_obj.query
                local_item_path = os.path.abspath(os.path.join(os.getcwd(), raw_path.lstrip('/')))
                if raw_path == "/" or raw_path == "/index.html":
                    print(f"[{timestamp}] {client_ip} reached Home (Root)")
                elif os.path.isfile(local_item_path):
                    if not is_preview:
                        print(f"[{timestamp}] {client_ip} ACCESS to file: {raw_path}")
                elif os.path.isdir(local_item_path):
                    print(f"[{timestamp}] {client_ip} opened directory: {raw_path}")
        except Exception:
            pass

    def list_directory(self, path):
        try:
            items = os.listdir(path)
        except OSError:
            self.send_error(404, "No permission")
            return None
        
        items.sort(key=lambda a: a.lower())
        displaypath = urllib.parse.unquote(self.path)
        timestamp = datetime.now().strftime("%H:%M:%S")
        client_ip = self.client_address[0]

        img_exts = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
        photos = [i for i in items if any(i.lower().endswith(ext) for ext in img_exts)]
        
        if len(photos) > 5:
            print(f"[{timestamp}] {client_ip} loaded preview for {len(photos)} photos")
        elif len(photos) > 0:
            for p in photos:
                print(f"[{timestamp}] {client_ip} loading preview for: {p}")

        r = []
        r.append('<!DOCTYPE html><html><head><meta charset="utf-8">')
        r.append('<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">')
        r.append('<style>')
        r.append('body { font-family: sans-serif; background: #121212; color: #eee; padding: 20px; margin: 0; padding-bottom: 120px; }')
        r.append('h2 { padding: 10px; margin-top: 0; border-bottom: 1px solid #333; font-size: 1.2rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }')
        r.append('.grid { display: grid; gap: 12px; transition: 0.2s; padding: 10px; }')
        for i in range(1, 6): r.append(f'.cols-{i} {{ grid-template-columns: repeat({i}, 1fr); }}')
        r.append('.item { position: relative; background: #1e1e1e; border-radius: 12px; border: 1px solid #333; text-decoration: none; color: inherit; width: 100%; aspect-ratio: 1 / 1; display: flex; flex-direction: column; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }')
        r.append('.item:hover { border-color: #007bff; transform: translateY(-2px); transition: 0.2s; }')
        r.append('.content { position: absolute; top: 0; left: 0; right: 0; bottom: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 15%; }')
        r.append('img { width: 100%; height: 100%; object-fit: cover; position: absolute; top: 0; left: 0; }')
        r.append('svg { width: 100%; height: 100%; max-width: 60px; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.5)); }')
        r.append('.file-name { position: absolute; bottom: 0; left: 0; right: 0; background: rgba(0,0,0,0.75); font-size: 10px; padding: 6px 4px; text-align: center; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; z-index: 2; }')
        r.append('.footer { position: fixed; bottom: 0; left: 0; width: 100%; height: 85px; background: rgba(26, 26, 26, 0.95); backdrop-filter: blur(10px); border-top: 1px solid #333; display: flex; justify-content: center; align-items: center; gap: 50px; z-index: 9999; }')
        r.append('.zoom-btn { background: #2a2a2a; color: white; border: 1px solid #444; width: 60px; height: 60px; border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 22px; transition: 0.1s; }')
        r.append('.zoom-btn:active { background: #444; transform: scale(0.9); }')
        r.append('</style></head><body>')
        
        r.append(f'<h2>{displaypath}</h2>')
        r.append('<div id="mainGrid" class="grid">')

        icon_folder = '<svg viewBox="0 0 24 24" fill="#f39c12"><path d="M10 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z"/></svg>'
        icon_up = '<svg viewBox="0 0 24 24" fill="#95a5a6"><path d="M5 20h14v-2H5v2zm0-10l1.41 1.41L11 6.83V16h2V6.83l4.59 4.58L19 10l-7-7-7 7z"/></svg>'
        icon_file = '<svg viewBox="0 0 24 24" fill="#ecf0f1"><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg>'
        icon_code = '<svg viewBox="0 0 24 24" fill="#3498db"><path d="M9.4 16.6L4.8 12l4.6-4.6L8 6l-6 6 6 6 1.4-1.4zm5.2 0l4.6-4.6-4.6-4.6L16 6l6 6-6 6-1.4-1.4z"/></svg>'

        if displaypath != "/":
            r.append(f'<a class="item" href=".."><div class="content">{icon_up}</div><div class="file-name">..</div></a>')

        for name in items:
            fullname = os.path.join(path, name)
            quoted_name = urllib.parse.quote(name)
            if os.path.isdir(fullname):
                r.append(f'<a class="item" href="{quoted_name}/"><div class="content">{icon_folder}</div><div class="file-name">{name}/</div></a>')
            else:
                ext = os.path.splitext(name)[1].lower()
                if ext in img_exts:
                    r.append(f'<a class="item" href="{quoted_name}"><img src="{quoted_name}?preview=1"><div class="file-name">{name}</div></a>')
                elif ext in ['.py', '.js', '.html', '.css', '.md', '.json', '.c', '.cpp']:
                    r.append(f'<a class="item" href="{quoted_name}"><div class="content">{icon_code}</div><div class="file-name">{name}</div></a>')
                else:
                    r.append(f'<a class="item" href="{quoted_name}"><div class="content">{icon_file}</div><div class="file-name">{name}</div></a>')
        
        r.append('</div><div class="footer">')
        r.append('<button class="zoom-btn" onclick="zoom(1)">\N{LEFT-POINTING MAGNIFYING GLASS}&minus;</button>')
        r.append('<button class="zoom-btn" onclick="zoom(-1)">\N{LEFT-POINTING MAGNIFYING GLASS}&plus;</button>')
        r.append('</div><script>')
        r.append('let currentCols = parseInt(localStorage.getItem("galleryCols")) || 2;')
        r.append('const grid = document.getElementById("mainGrid");')
        r.append('grid.className = "grid cols-" + currentCols;')
        r.append('function zoom(dir) {')
        r.append('  currentCols = Math.max(1, Math.min(5, currentCols + dir));')
        r.append('  grid.className = "grid cols-" + currentCols;')
        r.append('  localStorage.setItem("galleryCols", currentCols);')
        r.append('}</script></body></html>')
        
        encoded = '\n'.join(r).encode('utf-8')
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        return io.BytesIO(encoded)

# Multi-threaded server to allow simultaneous access from multiple devices
class SilentServer(ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True  # Terminate threads when main program exits
    def handle_error(self, request, client_address): 
        pass

# Get local ip
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80)); ip = s.getsockname()[0]
    except Exception: ip = "127.0.0.1"
    finally: s.close()
    return ip

# cwd and ls -alh outputs
def list_files_terminal():
    print(f"\n{ICO_PIN} Current Path: {os.getcwd()}\n" + "-" * 50)
    try: os.system('ls -alh' if os.name != 'nt' else 'dir')
    except:
        for item in sorted(os.listdir('.')): print(item)
    print("-" * 50)

# user inputs
def navigate_and_select():
    while True:
        list_files_terminal()
        print("\nCOMMANDS:")
        print("  cd <path>    -> Change directory")
        print("  run / host   -> Start hosting THIS folder")
        print("  exit         -> Close program")

        try: user_input = input("\nShell> ").strip()
        except EOFError: return None
        if user_input.lower() in ["run", "host", ""]: return os.getcwd()
        if user_input.lower() == "exit": return None
        if user_input.startswith("cd "): target = user_input[3:].strip()
        else: target = user_input
        target = os.path.expanduser(target.replace("\\ ", " ").replace("'", "").replace('"', ''))
        if os.path.isdir(target): os.chdir(target)
        else: print(f"{ICO_CROSS} Error: '{target}' not found.")

# run server
def run_server():
    target_dir = navigate_and_select()
    if not target_dir: return
    ip = get_local_ip()
    try:
        with SilentServer(("", PORT), SlimLogger) as httpd:
            header = f"\n{ICO_ROCKET} SERVER ACTIVE!"
            path_info = f"{ICO_PIN} Directory: {target_dir}"
            url_info = f"{ICO_LINK} URL: http://{ip}:{PORT}"
            stop_info = f"{ICO_STOP} Press CTRL+C to stop"
            print("\n" + "="*50 + f"{header}\n{path_info}\n{url_info}\n{stop_info}\n" + "="*50 + f"\n{ICO_GLOBE} LOGS:\n" + "-" * 50)
            httpd.serve_forever()
    except KeyboardInterrupt:
        print(f"\n\n{ICO_STOP} Hosting stopped. Returning to navigation..."); run_server()

if __name__ == "__main__":
    run_server()