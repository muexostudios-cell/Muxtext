#!/usr/bin/env python3
"""Fix chat layout when global text size setting changes."""
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "index.html"
s = path.read_text(encoding="utf-8")

# --- root vars ---
old_root = "--chat-panel-h:75dvh;--chat-offset-top:0px;"
new_root = "--chat-panel-h:75dvh;--chat-offset-top:0px;--chat-text-scale:1;"
if old_root not in s:
    raise SystemExit("root chat vars not found")
s = s.replace(old_root, new_root, 1)

# --- overlay positioning: use visible viewport box, not inset+translate ---
old_overlay = (
    "#chat-overlay{display:none;position:fixed;inset:0;z-index:102;background:rgba(0,0,0,.92);"
    "justify-content:center;align-items:center;box-sizing:border-box;"
    "padding:max(.5rem,env(safe-area-inset-top,0px)) max(.5rem,env(safe-area-inset-right,0px)) "
    "max(.5rem,env(safe-area-inset-bottom,0px)) max(.5rem,env(safe-area-inset-left,0px));"
    "transform:translateY(var(--chat-offset-top,0px))}"
)
new_overlay = (
    "#chat-overlay{display:none;position:fixed;left:0;right:0;top:var(--chat-offset-top,0px);"
    "height:var(--chat-vh,100dvh);width:100%;z-index:102;background:rgba(0,0,0,.92);"
    "justify-content:center;align-items:center;box-sizing:border-box;"
    "padding:max(.5rem,env(safe-area-inset-top,0px)) max(.5rem,env(safe-area-inset-right,0px)) "
    "max(.5rem,env(safe-area-inset-bottom,0px)) max(.5rem,env(safe-area-inset-left,0px))}"
)
if old_overlay not in s:
    raise SystemExit("chat-overlay css not found")
s = s.replace(old_overlay, new_overlay, 1)

old_panel_h = "height:min(var(--chat-panel-h,75dvh),520px);max-height:calc(var(--chat-vh,100dvh) - 1rem)"
new_panel_h = "height:min(var(--chat-panel-h,75dvh),calc(var(--chat-vh,100dvh) - 1rem));max-height:calc(var(--chat-vh,100dvh) - 1rem)"
if old_panel_h not in s:
    raise SystemExit("chat panel height css not found")
s = s.replace(old_panel_h, new_panel_h, 1)

# --- chat typography: em relative to isolated chat root (not html rem) ---
old_chat_root = "#chat-overlay #chat-input,#chat-overlay #chat-input-row,#chat-embedded #chat-input,#chat-embedded #chat-input-row{user-select:text;-webkit-user-select:text}"
new_chat_root = (
    "#chat-overlay,#chat-embedded{font-size:calc(12px * var(--chat-text-scale,1))}"
    "#chat-overlay #chat-panel,#chat-embedded #chat-panel{overflow:hidden}"
    "#chat-overlay #chat-input-row,#chat-embedded #chat-input-row{align-items:stretch;min-width:0}"
    "#chat-input{min-width:0}"
    "#chat-send{flex-shrink:0;max-width:42%}"
    "#chat-overlay #chat-input,#chat-overlay #chat-input-row,#chat-embedded #chat-input,#chat-embedded #chat-input-row{user-select:text;-webkit-user-select:text}"
)
if old_chat_root not in s:
    raise SystemExit("chat input user-select css not found")
s = s.replace(old_chat_root, new_chat_root, 1)

# rem -> em inside chat (relative to #chat-overlay / #chat-embedded font-size)
rem_em = [
    ("#chat-overlay #chat-panel{width:min(95vw,var(--chat-vw,100vw),400px);max-width:400px;height:min(var(--chat-panel-h,75dvh),calc(var(--chat-vh,100dvh) - 1rem));max-height:calc(var(--chat-vh,100dvh) - 1rem);border:1px solid #fff;box-shadow:none;background:#000;display:flex;flex-direction:column;min-height:0;color:var(--text);font-size:.6rem}", "font-size:.6em"),
    ("#chat-panel{display:flex;flex-direction:column;min-height:0;color:var(--text);font-size:.6rem;background:#000}", "font-size:.6em"),
    ("#chat-title{flex-shrink:0;color:#fff;font-size:.75rem;padding:.5rem;border-bottom:1px solid #333;text-align:center;margin:0}", "font-size:.75em"),
    ("#chat-status{flex-shrink:0;font-size:.5rem;color:#666;text-align:center;padding:.25rem;border-bottom:1px solid #111}", "font-size:.5em"),
    ("#chat-messages:empty::before{content:attr(data-empty);display:block;color:#555;text-align:center;padding:1rem;font-size:.55rem}", "font-size:.55em"),
    (".chat-time{color:#555;font-size:.45rem;margin-left:auto}", "font-size:.45em"),
    (".chat-level{color:#aaa;font-size:.48rem;flex-shrink:0}", "font-size:.48em"),
    ("#chat-input{flex:1;background:#111;border:1px solid #666;color:#fff;font-family:inherit;font-size:.6rem;padding:.4rem;outline:0}", "font-size:.6em"),
    ("#chat-send{background:0 0;border:1px solid #fff;color:#fff;font-family:inherit;font-size:.55rem;padding:.4rem .6rem;cursor:pointer;white-space:nowrap}", "font-size:.55em"),
    ("#btn-close-chat{display:none;flex-shrink:0;width:calc(100% - 1rem);margin:.3rem auto .5rem;padding:.35rem;background:0 0;border:1px solid #333;color:#666;font-family:inherit;font-size:.55rem;cursor:pointer}", "font-size:.55em"),
]
for old, new in rem_em:
    if old not in s:
        raise SystemExit(f"chat css block missing: {old[:60]}...")
    s = s.replace(old, old.replace(old.split("font-size:")[1].split(";")[0] + ";", new + ";"), 1)

# --- JS: metrics + settings ---
old_metrics = (
    "function syncChatViewportMetrics(){const vp=getLayoutViewport();const root=document.documentElement;const pad=16;"
    "const panelH=Math.max(220,Math.min(vp.height-pad,520));root.style.setProperty('--chat-vw',vp.width+'px');"
    "root.style.setProperty('--chat-vh',vp.height+'px');root.style.setProperty('--chat-panel-h',panelH+'px');"
    "root.style.setProperty('--chat-offset-top',vp.offsetTop+'px');}"
)
new_metrics = (
    "function syncChatViewportMetrics(){const vp=getLayoutViewport();const root=document.documentElement;const pad=16;"
    "const ts=Math.max(TEXT_SIZE_MIN,Math.min(TEXT_SIZE_MAX,settings.textSize||TEXT_SIZE_DEFAULT));"
    "const chrome=Math.round(150*ts);const maxCap=Math.round(Math.min(vp.height-pad,520*ts));"
    "const panelH=Math.max(Math.round(200*ts),Math.min(maxCap,vp.height-pad));"
    "root.style.setProperty('--chat-text-scale',String(ts));root.style.setProperty('--chat-vw',vp.width+'px');"
    "root.style.setProperty('--chat-vh',vp.height+'px');root.style.setProperty('--chat-panel-h',panelH+'px');"
    "root.style.setProperty('--chat-offset-top',Math.max(0,vp.offsetTop)+'px');}"
)
if old_metrics not in s:
    raise SystemExit("syncChatViewportMetrics not found")
s = s.replace(old_metrics, new_metrics, 1)

old_apply = "function applySettings(){document.documentElement.style.fontSize=(12*settings.textSize)+'px';fitGameToViewport();scheduleChatMetrics();}"
new_apply = (
    "function applySettings(){const ts=Math.max(TEXT_SIZE_MIN,Math.min(TEXT_SIZE_MAX,settings.textSize||TEXT_SIZE_DEFAULT));"
    "document.documentElement.style.fontSize=(12*ts)+'px';document.documentElement.style.setProperty('--chat-text-scale',String(ts));"
    "fitGameToViewport();scheduleChatMetrics();if(chatOverlayOpen||currentTab==='chat')requestAnimationFrame(scrollChatToLatest);}"
)
if old_apply not in s:
    raise SystemExit("applySettings not found")
s = s.replace(old_apply, new_apply, 1)

# --- version ---
old_ver = (
    "GAME_VERSION='2.6.1',GAME_VERSION_HISTORY=[{version:'2.6.1',date:'2025-06-07',summary:{zh:'介面縮放預設與上限改為 1.00x。',en:'UI scale default and max set to 1.00x.'}},"
)
new_ver = (
    "GAME_VERSION='2.6.2',GAME_VERSION_HISTORY=[{version:'2.6.2',date:'2025-06-07',summary:{zh:'修復調整文字大小後聊天室版面異常；面板高度隨設定同步。',en:'Fix chat layout after text size changes; panel height syncs with setting.'}},{version:'2.6.1',date:'2025-06-07',summary:{zh:'介面縮放預設與上限改為 1.00x。',en:'UI scale default and max set to 1.00x.'}},"
)
if old_ver not in s:
    raise SystemExit("GAME_VERSION not found")
s = s.replace(old_ver, new_ver, 1)

path.write_text(s, encoding="utf-8")
print("Patched index.html -> v2.6.2 chat text-size layout fix")
