#!/usr/bin/env python3
"""Keep mobile tab-bar pinned below chat and other panels."""
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "index.html"
s = path.read_text(encoding="utf-8")

import re

m = re.search(
    r'(<div id="tab-bar">.*?</div>)(<div id="action-bar">.*?</div>)(<div id="chat-embedded"></div>)',
    s,
    re.DOTALL,
)
if not m:
    raise SystemExit("game-main footer block not found")
tab_bar, action_bar, chat_embedded = m.group(1), m.group(2), m.group(3)
s = s[: m.start()] + chat_embedded + action_bar + tab_bar + s[m.end() :]

old_css = "#tab-bar{display:flex;border-bottom:1px solid #1a1a1a;flex-shrink:0;align-items:stretch;width:100%}"
new_css = (
    "#tab-bar{display:flex;border-bottom:1px solid #1a1a1a;flex-shrink:0;align-items:stretch;width:100%}"
    "#game-main:not(.combat-layout) #tab-bar{border-bottom:none;border-top:1px solid #1a1a1a;margin-top:auto}"
    "#game-main:not(.combat-layout) #chat-embedded.show{flex:1;min-height:0}"
)
if old_css not in s:
    raise SystemExit("tab-bar css not found")
s = s.replace(old_css, new_css, 1)

old_update = (
    "function updateChatLayout(){const panel=document.getElementById('chat-panel');const embedded=document.getElementById('chat-embedded');"
    "const btn=document.getElementById('btn-chat');const panelSidebar=document.getElementById('panel-sidebar');const gameMain=document.getElementById('game-main');"
    "const tabBar=document.getElementById('tab-bar');if(!panel||!embedded)return;document.body.style.overflow='';if(isDesktopLayout()){"
    "if(panelSidebar&&embedded.parentElement!==panelSidebar)panelSidebar.appendChild(embedded);}else if(gameMain&&tabBar&&embedded.parentElement!==gameMain)"
    "tabBar.insertAdjacentElement('beforebegin',embedded);if(panel.parentElement!==embedded)embedded.appendChild(panel);resetChatPanelLayout(panel);"
    "const showChat=currentTab==='chat';if(btn){btn.style.display='';btn.className='tab-btn tab-btn-chat'+(showChat?' active':'');}"
    "embedded.classList.toggle('show',showChat);embedded.style.display=showChat?'flex':'none';if(showChat){ensureChatLazyInit();initChat();"
    "scheduleChatMetrics();scrollChatToLatest();}else scheduleChatMetrics();}"
)
new_update = (
    "function ensureMobileShellOrder(){const gameMain=document.getElementById('game-main');const embedded=document.getElementById('chat-embedded');"
    "const actionBar=document.getElementById('action-bar');const tabBar=document.getElementById('tab-bar');if(!gameMain||!tabBar||isDesktopLayout())return;"
    "if(embedded&&embedded.parentElement!==gameMain)gameMain.appendChild(embedded);if(actionBar&&actionBar.parentElement!==gameMain)gameMain.appendChild(actionBar);"
    "gameMain.appendChild(tabBar);if(actionBar)gameMain.insertBefore(actionBar,tabBar);if(embedded)gameMain.insertBefore(embedded,actionBar||tabBar);}"
    "function updateChatLayout(){const panel=document.getElementById('chat-panel');const embedded=document.getElementById('chat-embedded');"
    "const btn=document.getElementById('btn-chat');const panelSidebar=document.getElementById('panel-sidebar');if(!panel||!embedded)return;"
    "document.body.style.overflow='';if(isDesktopLayout()){if(panelSidebar&&embedded.parentElement!==panelSidebar)panelSidebar.appendChild(embedded);}"
    "else ensureMobileShellOrder();if(panel.parentElement!==embedded)embedded.appendChild(panel);resetChatPanelLayout(panel);const showChat=currentTab==='chat';"
    "if(btn){btn.style.display='';btn.className='tab-btn tab-btn-chat'+(showChat?' active':'');}embedded.classList.toggle('show',showChat);"
    "embedded.style.display=showChat?'flex':'none';if(showChat){ensureChatLazyInit();initChat();scheduleChatMetrics();scrollChatToLatest();}else scheduleChatMetrics();}"
)
if old_update not in s:
    raise SystemExit("updateChatLayout not found")
s = s.replace(old_update, new_update, 1)

old_ver = "GAME_VERSION='2.24.46'"
new_ver = "GAME_VERSION='2.24.47'"
if old_ver not in s:
    raise SystemExit("GAME_VERSION not found")
s = s.replace(old_ver, new_ver, 1)

path.write_text(s, encoding="utf-8")
print("Patched index.html -> v2.24.47 chat tab-bar bottom fix")
