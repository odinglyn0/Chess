from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import threading
from typing import Any, Mapping, Optional
import webbrowser

from .config import AppConfig
from .controller import GantryController
from .errors import GantryError, ValidationError
from .service import GantryService


HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Chess Gantry Controller</title>
<style>
:root{color-scheme:dark;--bg:#0b0e14;--card:#151a24;--card2:#1d2431;--line:#30394a;--text:#eef3ff;--muted:#9eabc2;--accent:#67e8b5;--danger:#ff6b7a;--warn:#f4c66d;font-family:Inter,system-ui,sans-serif}
*{box-sizing:border-box}body{margin:0;background:radial-gradient(circle at top left,#16213b,transparent 32rem),var(--bg);color:var(--text)}main{width:min(1120px,calc(100% - 30px));margin:auto;padding:34px 0 60px}header{display:flex;justify-content:space-between;gap:20px;align-items:flex-start;margin-bottom:22px}h1{margin:0;font-size:clamp(2rem,5vw,3.2rem);letter-spacing:-.045em}h2{font-size:1.05rem;margin:0 0 16px}p{color:var(--muted);line-height:1.55}.subtitle{max-width:720px;margin:8px 0 0}.pill{border:1px solid var(--line);background:var(--card);border-radius:999px;padding:9px 12px;white-space:nowrap;color:var(--muted)}.pill.good{color:var(--accent)}.pill.bad{color:var(--danger)}.grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}.card{border:1px solid var(--line);border-radius:17px;padding:20px;background:rgba(21,26,36,.96);box-shadow:0 20px 55px rgba(0,0,0,.18)}.wide{grid-column:1/-1}.fields{display:grid;grid-template-columns:1fr 1fr;gap:11px}.three{grid-template-columns:1fr 1fr 1fr}label{display:block;font-size:.8rem;color:var(--muted);margin-bottom:6px}input,select,textarea{width:100%;border:1px solid var(--line);border-radius:10px;background:var(--card2);color:var(--text);padding:11px 12px;font:inherit;outline:none}textarea{min-height:190px;resize:vertical;font:13px/1.5 ui-monospace,monospace}input:focus,select:focus,textarea:focus{border-color:var(--accent);box-shadow:0 0 0 3px rgba(103,232,181,.12)}.actions{display:flex;flex-wrap:wrap;gap:9px;margin-top:14px}button{border:1px solid var(--line);border-radius:10px;background:var(--card2);color:var(--text);padding:10px 14px;font-weight:700;cursor:pointer}button:hover:not(:disabled){border-color:#64718f;transform:translateY(-1px)}button:disabled{opacity:.38;cursor:not-allowed}.primary{background:var(--accent);border-color:var(--accent);color:#07130f}.danger{background:#421b24;border-color:#7d3040;color:#ffdce2}.metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:9px}.metric{border:1px solid var(--line);background:var(--card2);border-radius:11px;padding:12px}.metric span{display:block;color:var(--muted);font-size:.74rem;margin-bottom:4px}.metric strong{font-size:1.05rem}.notice{border-left:3px solid var(--warn);background:#292318;color:#f2dba9;padding:10px 12px;margin-top:14px;font-size:.84rem;line-height:1.45}.safe{border-left-color:var(--accent);background:#162a24;color:#c9f7e4}pre{margin:0;min-height:130px;max-height:310px;overflow:auto;border:1px solid var(--line);border-radius:11px;background:#080b10;padding:12px;color:#bcc7dc;white-space:pre-wrap;font:12px/1.55 ui-monospace,monospace}.split{display:grid;grid-template-columns:1fr 1fr;gap:12px}.small{font-size:.8rem;color:var(--muted)}.check{display:flex;gap:8px;align-items:center;margin-top:12px;color:var(--muted);font-size:.85rem}.check input{width:auto}.locked{color:var(--danger)}
@media(max-width:780px){header{display:block}.pill{display:inline-block;margin-top:14px}.grid,.split{grid-template-columns:1fr}.wide{grid-column:auto}.three{grid-template-columns:1fr}.metrics{grid-template-columns:1fr 1fr}}
</style>
</head>
<body><main>
<header><div><h1>Chess Gantry Controller</h1><p class="subtitle">One local interface for serial diagnostics, coupled outer X/Y motion, independent inner Z motion, and validated chess move JSON.</p></div><div id="pill" class="pill">Starting…</div></header>
<section class="grid">
<div class="card"><h2>1. Serial connection</h2><div class="fields"><div><label for="port">USB port</label><select id="port"><option value="">Auto-detect</option></select></div><div><label for="baud">Baud</label><select id="baud"><option value="">Auto / config</option><option>115200</option><option>250000</option></select></div></div><div class="actions"><button id="connect" class="primary">Connect</button><button id="refresh">Refresh ports</button><button id="disconnect">Disconnect</button></div><p id="firmware" class="small">No controller identified.</p></div>
<div class="card"><h2>2. Machine state</h2><div class="metrics"><div class="metric"><span>Inner Z</span><strong id="xread">—</strong></div><div class="metric"><span>Outer position</span><strong id="yread">—</strong></div><div class="metric"><span>Initialized</span><strong id="homed">No</strong></div><div class="metric"><span>Board rev.</span><strong id="revision">—</strong></div></div><div class="actions"><button id="endstops">Check endstops</button><button id="home" class="primary">Home XYZ gantry</button><button id="stop" class="danger">Emergency stop</button></div><div class="notice">Physical X/Y align independently on their endstops. The inner motor is plugged into E but firmware maps it as logical Z and homes it against the Z switch.</div></div>
<div class="card wide"><h2>3. Manual coordinate test</h2><div class="fields three"><div><label for="xmm">X (mm)</label><input id="xmm" type="number" step="0.1" value="10"></div><div><label for="ymm">Y (mm)</label><input id="ymm" type="number" step="0.1" value="10"></div><div><label for="feed">Feed (mm/min)</label><input id="feed" type="number" step="10" value="600"></div></div><div class="actions"><button id="move" class="primary">Move to coordinate</button></div><p id="limits" class="small">Workspace loading…</p></div>
<div class="card wide"><h2>4. Chess move JSON</h2><div class="split"><div><label for="movejson">Incoming move</label><textarea id="movejson">{
  "event_id": "web-test-001",
  "position": "white_pawn_e",
  "px": 4,
  "py": 1,
  "nx": 4,
  "ny": 3
}</textarea><div class="actions"><button id="plan" class="primary">Plan only</button><button id="execute">Execute move</button></div><label class="check"><input id="confirm" type="checkbox"> I checked the workspace and understand this can move hardware.</label><p id="lockState" class="small locked"></p></div><div><label>Plan / generated G-code</label><pre id="planout">No plan yet.</pre></div></div></div>
<div class="card"><h2>Board state</h2><div class="actions"><button id="boardRefresh">Refresh state</button></div><pre id="boardout">Loading…</pre></div>
<div class="card"><h2>Activity</h2><pre id="log">Page ready.</pre></div>
</section></main>
<script>
const $=id=>document.getElementById(id);let state={},busy=false;
function log(msg){const e=$('log');e.textContent+=`\n[${new Date().toLocaleTimeString()}] ${msg}`;e.scrollTop=e.scrollHeight}
async function api(path,options={}){const r=await fetch(path,{headers:{'Content-Type':'application/json'},...options});const d=await r.json();if(!r.ok||d.ok===false)throw new Error(d.error||`HTTP ${r.status}`);return d}
function render(s){state=s||{};const c=!!s.connected;$('pill').className=`pill ${c?'good':(s.last_error?'bad':'')}`;$('pill').textContent=c?`${s.port} · ${s.baudrate}`:'Disconnected';$('firmware').textContent=s.firmware||s.last_error||'No controller identified.';$('xread').textContent=s.position_mm?.x==null?'—':`${s.position_mm.x.toFixed(2)} mm`;$('yread').textContent=s.position_mm?.y==null?'—':`${s.position_mm.y.toFixed(2)} mm`;$('homed').textContent=s.homed?'Yes':'No';$('revision').textContent=s.board_revision??'—';const w=s.workspace_mm||{};$('limits').textContent=`Allowed workspace: X ${w.min_x??'?'}–${w.max_x??'?'} mm, Y ${w.min_y??'?'}–${w.max_y??'?'} mm. Manual feed limit: ${s.max_manual_feed_mm_min??'?'} mm/min.`;$('lockState').textContent=s.calibrated?'Hardware execution is unlocked by config.':'Chess execution is locked: safety.calibrated is false.';$('connect').disabled=busy||c;$('disconnect').disabled=busy||!c;$('refresh').disabled=busy;$('endstops').disabled=busy||!c;$('home').disabled=busy||!c;$('move').disabled=busy||!c||!s.homed;$('execute').disabled=busy||!c||!s.calibrated;$('plan').disabled=busy;$('stop').disabled=!c}
async function status(){try{render((await api('/api/status')).status)}catch(e){log(`Status error: ${e.message}`)}}
async function ports(){try{const selected=$('port').value;const d=await api('/api/ports');$('port').innerHTML='<option value="">Auto-detect</option>';for(const p of d.ports){const o=document.createElement('option');o.value=p.device;o.textContent=`${p.device} — ${p.description}${p.likely_printer?' ★':''}`;$('port').appendChild(o)}if([...$('port').options].some(o=>o.value===selected))$('port').value=selected;log(`Found ${d.ports.length} serial port(s).`)}catch(e){log(`Port scan: ${e.message}`)}}
async function action(label,fn){if(busy)return;busy=true;render(state);log(label);try{const d=await fn();if(d.status)render(d.status);return d}catch(e){log(`ERROR: ${e.message}`);await status()}finally{busy=false;render(state)}}
$('connect').onclick=()=>action('Connecting and verifying Marlin with M115…',async()=>{const d=await api('/api/connect',{method:'POST',body:JSON.stringify({port:$('port').value||null,baudrate:$('baud').value?Number($('baud').value):null})});log(`Connected to ${d.status.port}.`);return d});
$('disconnect').onclick=()=>action('Disconnecting…',()=>api('/api/disconnect',{method:'POST',body:'{}'}));$('refresh').onclick=ports;
$('endstops').onclick=()=>action('Checking endstops…',async()=>{const d=await api('/api/endstops',{method:'POST',body:'{}'});log(d.lines.join('\n'));return d});
$('home').onclick=()=>{if(confirm('Is the complete gantry physically at a safe, squared zero position?'))action('Setting current X/Y/E coordinates to zero without movement…',()=>api('/api/home',{method:'POST',body:JSON.stringify({confirm_motion:true})}))};
$('move').onclick=()=>{if(confirm('Move the gantry to this absolute X/Y coordinate?'))action('Sending manual coordinate move…',()=>api('/api/move',{method:'POST',body:JSON.stringify({x_mm:Number($('xmm').value),y_mm:Number($('ymm').value),feed_mm_min:Number($('feed').value),confirm_motion:true})}))};
function moveObject(){let obj;try{obj=JSON.parse($('movejson').value)}catch(e){throw new Error(`Move JSON: ${e.message}`)}return obj}
$('plan').onclick=()=>action('Planning without moving hardware…',async()=>{const d=await api('/api/plan',{method:'POST',body:JSON.stringify({move:moveObject()})});$('planout').textContent=JSON.stringify(d.summary,null,2)+'\n\n'+d.gcode;log('Plan generated; board state was not changed.');return d});
$('execute').onclick=()=>{if(!$('confirm').checked){log('Execution blocked: check the motion confirmation box.');return}if(!confirm('Execute this generated chess move now?'))return;action('Executing validated chess move…',async()=>{const d=await api('/api/execute',{method:'POST',body:JSON.stringify({move:moveObject(),confirm_motion:true})});$('planout').textContent=JSON.stringify(d.summary,null,2)+'\n\n'+d.gcode;await board();log('Move completed and board state committed.');return d})};
$('stop').onclick=()=>{if(confirm('Send M112 emergency stop? The controller will require reset/power-cycle and re-homing.'))action('EMERGENCY STOP…',()=>api('/api/stop',{method:'POST',body:'{}'}))};
async function board(){try{$('boardout').textContent=JSON.stringify((await api('/api/board')).board_state,null,2)}catch(e){$('boardout').textContent=`ERROR: ${e.message}`}}$('boardRefresh').onclick=board;
(async()=>{await ports();await status();await board();setInterval(()=>{if(!busy)status()},1800)})();
</script></body></html>"""


class RequestHandler(BaseHTTPRequestHandler):
    controller: GantryController

    def log_message(self, fmt: str, *args: Any) -> None:
        print(f"[web] {self.address_string()} - {fmt % args}")

    def _send_json(self, payload: Mapping[str, Any], status: int = 200) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self) -> dict[str, Any]:
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError as exc:
            raise ValidationError("invalid request length") from exc
        if length > 262_144:
            raise ValidationError("request is too large")
        if length == 0:
            return {}
        try:
            value = json.loads(self.rfile.read(length))
        except json.JSONDecodeError as exc:
            raise ValidationError("request body must be valid JSON") from exc
        if not isinstance(value, dict):
            raise ValidationError("request body must be a JSON object")
        return value

    @staticmethod
    def _move_payload(payload: Mapping[str, Any]) -> Mapping[str, Any]:
        value = payload.get("move", payload)
        if not isinstance(value, Mapping):
            raise ValidationError("move must be a JSON object")
        return value

    def do_GET(self) -> None:
        if self.path == "/" or self.path.startswith("/?"):
            body = HTML.encode("utf-8")
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(body)
            return
        if self.path == "/api/status":
            self._send_json({"ok": True, "status": self.controller.status()})
            return
        if self.path == "/api/ports":
            self._send_json(
                {
                    "ok": True,
                    "ports": [
                        item.as_dict() for item in self.controller.available_ports()
                    ],
                }
            )
            return
        if self.path == "/api/board":
            self._send_json({"ok": True, "board_state": self.controller.board_state()})
            return
        if self.path == "/api/pending":
            self._send_json(
                {"ok": True, "pending": self.controller.pending_transaction()}
            )
            return
        self._send_json({"ok": False, "error": "not found"}, HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:
        try:
            payload = self._read_json()
            if self.path == "/api/connect":
                port = payload.get("port")
                baudrate = payload.get("baudrate")
                if port is not None and not isinstance(port, str):
                    raise ValidationError("port must be a string or null")
                if baudrate is not None:
                    if isinstance(baudrate, bool):
                        raise ValidationError("baudrate must be an integer or null")
                    try:
                        baudrate = int(baudrate)
                    except (TypeError, ValueError) as exc:
                        raise ValidationError(
                            "baudrate must be an integer or null"
                        ) from exc
                status = self.controller.connect(port=port or None, baudrate=baudrate)
                self._send_json({"ok": True, "status": status})
                return
            if self.path == "/api/disconnect":
                self._send_json({"ok": True, "status": self.controller.disconnect()})
                return
            if self.path == "/api/endstops":
                lines = self.controller.check_endstops()
                self._send_json(
                    {
                        "ok": True,
                        "lines": list(lines),
                        "status": self.controller.status(),
                    }
                )
                return
            if self.path == "/api/home":
                if payload.get("confirm_motion") is not True:
                    raise ValidationError(
                        "homing requires explicit motion confirmation"
                    )
                self._send_json({"ok": True, "status": self.controller.home_xy()})
                return
            if self.path == "/api/move":
                if payload.get("confirm_motion") is not True:
                    raise ValidationError(
                        "manual movement requires explicit motion confirmation"
                    )
                try:
                    x_mm = float(payload["x_mm"])
                    y_mm = float(payload["y_mm"])
                    feed = float(payload["feed_mm_min"])
                except KeyError as exc:
                    raise ValidationError(f"missing field: {exc.args[0]}") from exc
                except (TypeError, ValueError) as exc:
                    raise ValidationError(
                        "coordinates and feed rate must be numbers"
                    ) from exc
                status = self.controller.move_to_mm(
                    x_mm=x_mm, y_mm=y_mm, feed_mm_min=feed
                )
                self._send_json({"ok": True, "status": status})
                return
            if self.path == "/api/plan":
                plan = self.controller.plan_move(self._move_payload(payload))
                self._send_json(
                    {
                        "ok": True,
                        "summary": plan.summary(),
                        "gcode": plan.program.text(),
                        "status": self.controller.status(),
                    }
                )
                return
            if self.path == "/api/execute":
                plan = self.controller.execute_move(
                    self._move_payload(payload),
                    confirm_motion=payload.get("confirm_motion") is True,
                )
                self._send_json(
                    {
                        "ok": True,
                        "summary": plan.summary(),
                        "gcode": plan.program.text(),
                        "status": self.controller.status(),
                    }
                )
                return
            if self.path == "/api/stop":
                self._send_json(
                    {"ok": True, "status": self.controller.emergency_stop()}
                )
                return
            self._send_json({"ok": False, "error": "not found"}, HTTPStatus.NOT_FOUND)
        except GantryError as exc:
            self._send_json(
                {"ok": False, "error": str(exc), "status": self.controller.status()},
                HTTPStatus.CONFLICT,
            )
        except Exception as exc:
            self._send_json(
                {"ok": False, "error": f"unexpected server error: {exc}"},
                HTTPStatus.INTERNAL_SERVER_ERROR,
            )


class GantryHTTPServer(ThreadingHTTPServer):
    daemon_threads = True


def run_web_server(
    *,
    config: AppConfig,
    state_path: str,
    journal_path: str,
    audit_path: str,
    host: str = "127.0.0.1",
    port: int = 8000,
    open_browser: bool = True,
    demo: bool = False,
    allow_network: bool = False,
) -> None:
    if not 1 <= port <= 65_535:
        raise ValidationError("web port must be between 1 and 65535")
    if host not in {"127.0.0.1", "localhost", "::1"} and not allow_network:
        raise ValidationError(
            "refusing a network-visible bind without --allow-network; use 127.0.0.1 for local control"
        )

    service = GantryService(config, state_path, journal_path, audit_path)
    controller = GantryController(config, service, demo=demo)
    RequestHandler.controller = controller
    server = GantryHTTPServer((host, port), RequestHandler)
    display_host = "127.0.0.1" if host in {"0.0.0.0", "::"} else host
    url = f"http://{display_host}:{port}"
    print(f"Chess Gantry Controller running at {url}")
    print("Press Control-C to stop it.")

    if open_browser:
        threading.Timer(0.4, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping web controller…")
    finally:
        controller.disconnect()
        server.server_close()
