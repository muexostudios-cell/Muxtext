#!/usr/bin/env python3
"""Remove multiplayer chat message search; rename connected status label."""
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "index.html"
s = path.read_text(encoding="utf-8")

old_html = (
    '<h3 id="chat-title">多人聊天室</h3><div id="chat-toolbar">'
    '<button type="button" id="btn-chat-search">搜尋</button></div>'
    '<div id="chat-search-panel"><input type="text" id="chat-search-input" maxlength="80" '
    'placeholder="搜尋聊天紀錄..." autocomplete="off"><div id="chat-search-results"></div>'
    '<button type="button" id="btn-close-chat-search">關閉搜尋</button></div>'
    '<div id="chat-status">'
)
new_html = '<h3 id="chat-title">多人聊天室</h3><div id="chat-status">'
if old_html not in s:
    raise SystemExit("chat panel html not found")
s = s.replace(old_html, new_html, 1)

old_css = (
    "#chat-toolbar{display:flex;gap:.35rem;padding:.35rem .5rem;border-bottom:1px solid #111;flex-shrink:0}"
    "#btn-chat-search{flex:1;background:0 0;border:1px solid #444;color:#fff;font-family:inherit;font-size:.55rem;padding:.3rem .45rem;cursor:pointer}"
    "#chat-search-panel{display:none;flex-direction:column;gap:.35rem;padding:.4rem .5rem;border-bottom:1px solid #111;flex-shrink:0;max-height:40%;min-height:0}"
    "#chat-search-panel.open{display:flex}"
    "#chat-search-input{width:100%;background:#111;border:1px solid #333;color:#fff;font-family:inherit;font-size:.55rem;padding:.35rem .45rem}"
    "#chat-search-results{flex:1;min-height:0;overflow-y:auto;-webkit-overflow-scrolling:touch;border:1px solid #222;background:#050505}"
    ".chat-search-hit{padding:.4rem .45rem;border-bottom:1px solid #111;cursor:pointer;touch-action:manipulation}"
    ".chat-search-hit:active{background:#111}"
    ".chat-search-hit-meta{font-size:.5rem;color:#888;margin-bottom:.15rem}"
    ".chat-search-hit-text{font-size:.55rem;color:#ddd;line-height:1.35;word-break:break-word}"
    ".chat-msg.chat-msg-highlight{outline:1px solid #fff;outline-offset:-1px;background:#0a0a0a}"
    "#btn-close-chat-search{background:0 0;border:1px solid #333;color:#666;font-family:inherit;font-size:.5rem;padding:.3rem;cursor:pointer}"
)
if old_css not in s:
    raise SystemExit("chat search css not found")
s = s.replace(old_css, "", 1)

old_lang_zh = (
    "chatSearchBtn:'搜尋',chatSearchPlaceholder:'搜尋聊天紀錄...',chatSearchClose:'關閉搜尋',"
    "chatSearchEmpty:'找不到符合的訊息',chatSearchHint:'點擊結果跳轉；長按聊天訊息可帶入搜尋',"
)
if old_lang_zh not in s:
    raise SystemExit("zh chatSearch lang not found")
s = s.replace(old_lang_zh, "", 1)

old_lang_en = (
    'chatSearchBtn:"SEARCH",chatSearchPlaceholder:"Search chat history...",chatSearchClose:"CLOSE SEARCH",'
    'chatSearchEmpty:"No matching messages",chatSearchHint:"Tap result to jump; long-press a message to search",'
)
if old_lang_en not in s:
    raise SystemExit("en chatSearch lang not found")
s = s.replace(old_lang_en, "", 1)

s = s.replace(
    'chatStatusOnline:"已連線 · 夜之城公共頻道"',
    'chatStatusOnline:"已連線至公共頻道"',
    1,
)
s = s.replace(
    'chatStatusOnline:"Online · Night City public channel"',
    'chatStatusOnline:"Connected to public channel"',
    1,
)

old_apply = (
    "const chatSearchBtn=document.getElementById('btn-chat-search');"
    "if(chatSearchBtn)chatSearchBtn.textContent=t('chatSearchBtn');"
    "const chatSearchInput=document.getElementById('chat-search-input');"
    "if(chatSearchInput)chatSearchInput.placeholder=t('chatSearchPlaceholder');"
    "const chatSearchCloseBtn=document.getElementById('btn-close-chat-search');"
    "if(chatSearchCloseBtn)chatSearchCloseBtn.textContent=t('chatSearchClose');"
)
if old_apply not in s:
    raise SystemExit("applyLanguage chatSearch not found")
s = s.replace(old_apply, "", 1)

s = s.replace("chatArchiveDirty=false,chatSearchOpen=false;", "chatArchiveDirty=false;", 1)

js_start = s.find("function jumpToChatMessage(")
js_end = s.find("function pct(", js_start)
if js_start < 0 or js_end < 0:
    raise SystemExit("chat search js block markers not found")
s = s[:js_start] + s[js_end:]

s = s.replace("bindChatMessageSearchLongPress(div,data);", "", 1)
s = s.replace("setupChatSearchUI();", "", 1)

old_ver = "GAME_VERSION='2.24.47'"
new_ver = "GAME_VERSION='2.24.48'"
if old_ver not in s:
    raise SystemExit("GAME_VERSION not found")
s = s.replace(old_ver, new_ver, 1)

path.write_text(s, encoding="utf-8")
print("Patched index.html -> v2.24.48 remove chat search")
