#!/usr/bin/env python3
"""Optimize chat layout with viewport-aware sizing and fix display conflicts."""
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "index.html"
s = path.read_text(encoding="utf-8")

# --- :root CSS vars for chat viewport metrics ---
old_root = ":root{--bg:#000;--surface:#000;--border:#1a1a1a;--text:#fff;"
new_root = (
    ":root{--bg:#000;--surface:#000;--border:#1a1a1a;--text:#fff;"
    "--chat-vw:100vw;--chat-vh:100dvh;--chat-panel-h:75dvh;--chat-offset-top:0px;"
)
if old_root not in s:
    raise SystemExit(":root block not found")
s = s.replace(old_root, new_root, 1)

# --- Consolidated chat CSS (fix flex scroll, safe-area, overlay sizing) ---
old_css = (
    "#chat-embedded{display:none;flex-direction:column;flex:1;min-height:0;background:#000}"
    "#game.desktop-layout #panel-sidebar #chat-embedded{display:none;flex:1;min-height:0;border:none}"
    "#game.desktop-layout #panel-sidebar #chat-embedded.show{display:flex}"
    "#game.desktop-layout #panel-sidebar #chat-embedded #chat-panel{display:flex;flex-direction:column;flex:1;min-height:0;width:100%;height:100%;max-width:none;border:none;box-shadow:none}"
    "#game.desktop-layout #panel-sidebar #chat-embedded #chat-title,#game.desktop-layout #panel-sidebar #chat-embedded #btn-close-chat{display:none}"
    "#game.desktop-layout #panel-sidebar #chat-embedded #chat-messages{flex:1;min-height:0;overflow-y:auto;padding:.5rem;border-top:1px solid #111;border-bottom:1px solid #111}"
    "#game.desktop-layout #panel-sidebar #chat-embedded #chat-input-row{margin-top:auto;flex-shrink:0}"
    "#game.desktop-layout #btn-close-chat{display:none!important}"
    "#btn-chat{display:none}"
    "#tab-bar #btn-chat.tab-btn-chat{display:flex}"
    "#btn-chat.tab-btn-chat.active{color:#fff;border-bottom-color:#fff}"
    "#tab-bar #btn-chat.tab-btn-chat{color:#fff;border:none;border-bottom:1px solid transparent;background:0 0;cursor:pointer;-webkit-tap-highlight-color:transparent}"
    "#chat-overlay #chat-input,#chat-overlay #chat-input-row,#chat-embedded #chat-input,#chat-embedded #chat-input-row{user-select:text;-webkit-user-select:text}"
    "#chat-overlay #chat-panel{height:min(75dvh,520px);max-height:calc(100dvh - 2rem)}"
    "#chat-overlay{display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,.92);z-index:102;justify-content:center;align-items:center}"
    "#chat-panel{background:#000;border:1px solid #fff;width:95%;max-width:400px;height:min(70vh,520px);display:flex;flex-direction:column;color:var(--text);font-size:.6rem;box-shadow:none}"
    "#chat-title{color:#fff;font-size:.75rem;padding:.5rem;border-bottom:1px solid #333;text-align:center;margin:0}"
    "#chat-status{font-size:.5rem;color:#666;text-align:center;padding:.25rem;border-bottom:1px solid #111}"
    "#chat-messages:empty::before{content:attr(data-empty);display:block;color:#555;text-align:center;padding:1rem;font-size:.55rem}"
)
new_css = (
    "#chat-embedded{display:none;flex-direction:column;flex:1;min-height:0;background:#000}"
    "#game.desktop-layout #panel-sidebar #chat-embedded{display:none;flex:1;min-height:0;border:none}"
    "#game.desktop-layout #panel-sidebar #chat-embedded.show{display:flex}"
    "#game.desktop-layout #panel-sidebar #chat-embedded #chat-panel{display:flex;flex-direction:column;flex:1;min-height:0;width:100%;height:100%;max-width:none;border:none;box-shadow:none}"
    "#game.desktop-layout #panel-sidebar #chat-embedded #chat-title,#game.desktop-layout #panel-sidebar #chat-embedded #btn-close-chat{display:none}"
    "#game.desktop-layout #panel-sidebar #chat-embedded #chat-messages{flex:1;min-height:0;overflow-y:auto;-webkit-overflow-scrolling:touch;padding:.5rem;border-top:1px solid #111;border-bottom:1px solid #111}"
    "#game.desktop-layout #panel-sidebar #chat-embedded #chat-input-row{margin-top:auto;flex-shrink:0}"
    "#btn-chat{display:none}"
    "#tab-bar #btn-chat.tab-btn-chat{display:flex}"
    "#game.desktop-layout #tab-bar #btn-chat.tab-btn-chat{display:flex}"
    "#btn-chat.tab-btn-chat.active{color:#fff;border-bottom-color:#fff}"
    "#tab-bar #btn-chat.tab-btn-chat{color:#fff;border:none;border-bottom:1px solid transparent;background:0 0;cursor:pointer;-webkit-tap-highlight-color:transparent}"
    "#chat-overlay #chat-input,#chat-overlay #chat-input-row,#chat-embedded #chat-input,#chat-embedded #chat-input-row{user-select:text;-webkit-user-select:text}"
    "#chat-overlay{display:none;position:fixed;inset:0;z-index:102;background:rgba(0,0,0,.92);justify-content:center;align-items:center;box-sizing:border-box;padding:max(.5rem,env(safe-area-inset-top,0px)) max(.5rem,env(safe-area-inset-right,0px)) max(.5rem,env(safe-area-inset-bottom,0px)) max(.5rem,env(safe-area-inset-left,0px));transform:translateY(var(--chat-offset-top,0px))}"
    "#chat-overlay.open{display:flex}"
    "#chat-overlay #chat-panel{width:min(95vw,var(--chat-vw,100vw),400px);max-width:400px;height:min(var(--chat-panel-h,75dvh),520px);max-height:calc(var(--chat-vh,100dvh) - 1rem);border:1px solid #fff;box-shadow:none;background:#000;display:flex;flex-direction:column;min-height:0;color:var(--text);font-size:.6rem}"
    "#chat-panel{display:flex;flex-direction:column;min-height:0;color:var(--text);font-size:.6rem;background:#000}"
    "#chat-title{flex-shrink:0;color:#fff;font-size:.75rem;padding:.5rem;border-bottom:1px solid #333;text-align:center;margin:0}"
    "#chat-status{flex-shrink:0;font-size:.5rem;color:#666;text-align:center;padding:.25rem;border-bottom:1px solid #111}"
    "#chat-messages{flex:1;min-height:0;overflow-y:auto;-webkit-overflow-scrolling:touch;padding:.5rem}"
    "#chat-messages:empty::before{content:attr(data-empty);display:block;color:#555;text-align:center;padding:1rem;font-size:.55rem}"
)
if old_css not in s:
    raise SystemExit("chat CSS block not found")
s = s.replace(old_css, new_css, 1)

old_close_btn = (
    "#btn-close-chat{display:block;width:calc(100% - 1rem);margin:.3rem auto .5rem;padding:.35rem;background:0 0;border:1px solid #333;color:#666;font-family:inherit;font-size:.55rem;cursor:pointer}"
)
new_close_btn = (
    "#btn-close-chat{display:none;flex-shrink:0;width:calc(100% - 1rem);margin:.3rem auto .5rem;padding:.35rem;background:0 0;border:1px solid #333;color:#666;font-family:inherit;font-size:.55rem;cursor:pointer}"
    "#chat-overlay #btn-close-chat{display:block}"
    "#game.desktop-layout #btn-close-chat,#chat-embedded #btn-close-chat{display:none!important}"
)
if old_close_btn not in s:
    raise SystemExit("btn-close-chat CSS not found")
s = s.replace(old_close_btn, new_close_btn, 1)

# --- Viewport helpers ---
old_desktop = "function isDesktopLayout(){return window.innerWidth>=DESKTOP_MIN_W&&window.innerHeight>=500;}"
new_desktop = (
    "function getLayoutViewport(){const vv=window.visualViewport;return{width:Math.round(vv?.width||window.innerWidth),"
    "height:Math.round(vv?.height||window.innerHeight),offsetTop:Math.round(vv?.offsetTop||0),offsetLeft:Math.round(vv?.offsetLeft||0)};}"
    "function isDesktopLayout(){const vp=getLayoutViewport();return vp.width>=DESKTOP_MIN_W&&vp.height>=500;}"
    "let chatMetricsRaf=0;"
    "function syncChatViewportMetrics(){const vp=getLayoutViewport();const root=document.documentElement;const pad=16;"
    "const panelH=Math.max(220,Math.min(vp.height-pad,520));root.style.setProperty('--chat-vw',vp.width+'px');"
    "root.style.setProperty('--chat-vh',vp.height+'px');root.style.setProperty('--chat-panel-h',panelH+'px');"
    "root.style.setProperty('--chat-offset-top',vp.offsetTop+'px');}"
    "function scheduleChatMetrics(){if(chatMetricsRaf)return;chatMetricsRaf=requestAnimationFrame(()=>{chatMetricsRaf=0;syncChatViewportMetrics();});}"
    "function scrollChatToLatest(){const el=document.getElementById('chat-messages');if(!el)return;requestAnimationFrame(()=>{el.scrollTop=el.scrollHeight;});}"
)
if old_desktop not in s:
    raise SystemExit("isDesktopLayout not found")
s = s.replace(old_desktop, new_desktop, 1)

# --- updateChatLayout: overlay class + metrics ---
old_update = (
    "if(!chatOverlayOpen)overlay.style.display='none';}}"
)
new_update = (
    "if(chatOverlayOpen){overlay.style.display='flex';overlay.classList.add('open');}else{overlay.style.display='none';overlay.classList.remove('open');}"
    "scheduleChatMetrics();}}"
)
if old_update not in s:
    raise SystemExit("updateChatLayout mobile tail not found")
s = s.replace(old_update, new_update, 1)

old_update_desktop_tail = "if(showChat){ensureChatLazyInit();initChat();}}else{"
new_update_desktop_tail = "if(showChat){ensureChatLazyInit();initChat();}scheduleChatMetrics();}else{"
if old_update_desktop_tail not in s:
    raise SystemExit("updateChatLayout desktop tail not found")
s = s.replace(old_update_desktop_tail, new_update_desktop_tail, 1)

old_update_desktop_overlay = "if(isDesktopLayout()){overlay.style.display='none';document.body.style.overflow='';chatOverlayOpen=false;"
new_update_desktop_overlay = (
    "if(isDesktopLayout()){overlay.style.display='none';overlay.classList.remove('open');document.body.style.overflow='';chatOverlayOpen=false;"
)
if old_update_desktop_overlay not in s:
    raise SystemExit("updateChatLayout desktop overlay reset not found")
s = s.replace(old_update_desktop_overlay, new_update_desktop_overlay, 1)

# --- open/close overlay ---
old_open_display = (
    "updateChatLayout();if(panel.parentElement!==ol)ol.appendChild(panel);ol.style.display='flex';document.body.style.overflow='hidden';"
)
new_open_display = (
    "updateChatLayout();if(panel.parentElement!==ol)ol.appendChild(panel);ol.style.display='flex';ol.classList.add('open');document.body.style.overflow='hidden';"
    "scheduleChatMetrics();scrollChatToLatest();"
)
if old_open_display not in s:
    raise SystemExit("openChatOverlay display not found")
s = s.replace(old_open_display, new_open_display, 1)

old_close = "if(ol)ol.style.display='none';document.body.style.overflow='';"
new_close = "if(ol){ol.style.display='none';ol.classList.remove('open');}document.body.style.overflow='';"
if old_close not in s:
    raise SystemExit("closeChatOverlay hide not found")
s = s.replace(old_close, new_close, 1)

# --- applySettings + resize listeners ---
old_apply = "function applySettings(){document.documentElement.style.fontSize=(12*settings.textSize)+'px';fitGameToViewport();}"
new_apply = "function applySettings(){document.documentElement.style.fontSize=(12*settings.textSize)+'px';fitGameToViewport();scheduleChatMetrics();}"
if old_apply not in s:
    raise SystemExit("applySettings not found")
s = s.replace(old_apply, new_apply, 1)

old_vv = "if(window.visualViewport){window.visualViewport.addEventListener('resize',updateLayoutMode);}"
new_vv = (
    "if(window.visualViewport){window.visualViewport.addEventListener('resize',updateLayoutMode);"
    "window.visualViewport.addEventListener('scroll',scheduleChatMetrics);}"
)
if old_vv not in s:
    raise SystemExit("visualViewport listener not found")
s = s.replace(old_vv, new_vv, 1)

old_init = "loadSettings();applySettings();loadLanguage();"
new_init = "loadSettings();applySettings();scheduleChatMetrics();loadLanguage();"
if old_init not in s:
    raise SystemExit("settings init not found")
s = s.replace(old_init, new_init, 1)

# --- chat input focus for mobile keyboard ---
old_listener = "document.getElementById('btn-close-chat').addEventListener('click',closeChatOverlay);"
new_listener = (
    "document.getElementById('btn-close-chat').addEventListener('click',closeChatOverlay);"
    "const chatInputEl=document.getElementById('chat-input');if(chatInputEl){chatInputEl.addEventListener('focus',()=>{"
    "scheduleChatMetrics();setTimeout(()=>{try{chatInputEl.scrollIntoView({block:'nearest',behavior:'smooth'});}catch(_){}},280);});}"
)
if old_listener not in s:
    raise SystemExit("btn-close-chat listener not found")
s = s.replace(old_listener, new_listener, 1)

# --- version bump ---
old_ver = (
    "GAME_VERSION='2.5.9',GAME_VERSION_HISTORY=[{version:'2.5.9',date:'2025-06-07',summary:{zh:'修復聊天室進入／關閉顯示異常；桌面版改為側欄分頁、手機版覆蓋層狀態同步。',"
    "en:'Fix chat open/close layout; desktop sidebar tab and mobile overlay state sync.'}},"
)
new_ver = (
    "GAME_VERSION='2.6.0',GAME_VERSION_HISTORY=[{version:'2.6.0',date:'2025-06-07',summary:{zh:'聊天室依螢幕尺寸自動調整；修復訊息區滾動、安全區與虛擬鍵盤遮擋。',"
    "en:'Chat auto-sizes to viewport; fix message scroll, safe-area, and keyboard overlap.'}},{version:'2.5.9',date:'2025-06-07',summary:{zh:'修復聊天室進入／關閉顯示異常；桌面版改為側欄分頁、手機版覆蓋層狀態同步。',"
    "en:'Fix chat open/close layout; desktop sidebar tab and mobile overlay state sync.'}},"
)
if old_ver not in s:
    raise SystemExit("GAME_VERSION not found")
s = s.replace(old_ver, new_ver, 1)

path.write_text(s, encoding="utf-8")
print("Patched index.html -> v2.6.0 chat viewport layout")
