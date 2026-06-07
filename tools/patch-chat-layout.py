#!/usr/bin/env python3
"""Fix chat overlay enter/exit display on mobile and desktop."""
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "index.html"
s = path.read_text(encoding="utf-8")

# --- CSS: desktop chat in panel-sidebar, not always-on in game-main ---
old_css = (
    "#chat-embedded{display:none;flex-direction:column;flex:1;min-height:0;background:#000;border-top:1px solid #1a1a1a}"
    "#game.desktop-layout #chat-embedded{display:flex}"
    "#game.desktop-layout #chat-embedded #chat-panel{display:flex;flex-direction:column;flex:1;min-height:0;width:100%;height:100%;max-width:none;border:none;box-shadow:none}"
    "#game.desktop-layout #chat-embedded #chat-messages{flex:1;min-height:0;overflow-y:auto;padding:.5rem;border-top:1px solid #111;border-bottom:1px solid #111}"
    "#game.desktop-layout #chat-embedded #chat-input-row{margin-top:auto;flex-shrink:0}"
    "#game.desktop-layout #btn-close-chat{display:none!important}"
    "#game.desktop-layout #btn-chat{display:none!important}"
    "#btn-chat{display:none}"
    "#game:not(.desktop-layout) #tab-bar #btn-chat.tab-btn-chat{display:flex}"
)
new_css = (
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
)
if old_css not in s:
    raise SystemExit("CSS block not found")
s = s.replace(old_css, new_css, 1)

# --- JS: state + helpers ---
old_state = "let currentTab='log';const GAME_BASE_W"
new_state = "let currentTab='log',chatOverlayOpen=false,chatTabBeforeOpen='log';const GAME_BASE_W"
if old_state not in s:
    raise SystemExit("currentTab state not found")
s = s.replace(old_state, new_state, 1)

old_title = "const map={equip:'tabEquip',inventory:'tabInventory',craft:'tabCraft',profile:'tabProfile'};el.textContent=t(map[currentTab]||'tabEquip');}"
new_title = "const map={equip:'tabEquip',inventory:'tabInventory',craft:'tabCraft',profile:'tabProfile',chat:'chatTitle'};el.textContent=t(map[currentTab]||'tabEquip');}"
if old_title not in s:
    raise SystemExit("updatePanelSidebarTitle map not found")
s = s.replace(old_title, new_title, 1)

old_update_chat = (
    "function updateChatLayout(){const panel=document.getElementById('chat-panel');const overlay=document.getElementById('chat-overlay');"
    "const embedded=document.getElementById('chat-embedded');const btn=document.getElementById('btn-chat');const tabEquip=document.getElementById('tab-equip');"
    "const closeBtn=document.getElementById('btn-close-chat');if(!panel||!overlay||!embedded)return;if(isDesktopLayout()){"
    "if(panel.parentElement!==embedded)embedded.appendChild(panel);embedded.style.display='flex';overlay.style.display='none';"
    "if(closeBtn)closeBtn.style.display='none';if(btn)btn.style.display='none';ensureChatLazyInit();initChat();}else{"
    "if(panel.parentElement!==overlay)overlay.appendChild(panel);embedded.style.display='none';if(closeBtn)closeBtn.style.display='block';"
    "if(btn){btn.style.display='flex';btn.className='tab-btn tab-btn-chat';}}}"
)
new_update_chat = (
    "function resetChatPanelLayout(panel){if(!panel)return;panel.style.width='';panel.style.height='';panel.style.maxWidth='';"
    "panel.style.maxHeight='';panel.style.border='';panel.style.boxShadow='';panel.style.display='';}"
    "function updateChatLayout(){const panel=document.getElementById('chat-panel');const overlay=document.getElementById('chat-overlay');"
    "const embedded=document.getElementById('chat-embedded');const btn=document.getElementById('btn-chat');const closeBtn=document.getElementById('btn-close-chat');"
    "const panelSidebar=document.getElementById('panel-sidebar');if(!panel||!overlay||!embedded)return;if(isDesktopLayout()){"
    "overlay.style.display='none';document.body.style.overflow='';chatOverlayOpen=false;"
    "if(panelSidebar&&embedded.parentElement!==panelSidebar)panelSidebar.appendChild(embedded);"
    "if(panel.parentElement!==embedded)embedded.appendChild(panel);resetChatPanelLayout(panel);"
    "if(closeBtn)closeBtn.style.display='none';if(btn){btn.style.display='';btn.className='tab-btn tab-btn-chat'+(currentTab==='chat'?' active':'');}"
    "const showChat=currentTab==='chat';embedded.classList.toggle('show',showChat);embedded.style.display=showChat?'flex':'none';"
    "if(showChat){ensureChatLazyInit();initChat();}}else{if(panel.parentElement!==overlay)overlay.appendChild(panel);resetChatPanelLayout(panel);"
    "embedded.style.display='none';embedded.classList.remove('show');if(closeBtn)closeBtn.style.display='block';"
    "if(btn){btn.style.display='flex';btn.className='tab-btn tab-btn-chat'+(chatOverlayOpen?' active':'');}"
    "if(!chatOverlayOpen)overlay.style.display='none';}}"
)
if old_update_chat not in s:
    raise SystemExit("updateChatLayout not found")
s = s.replace(old_update_chat, new_update_chat, 1)

old_open = (
    "function openChatOverlay(e){if(e){e.preventDefault();e.stopPropagation();}if(isDesktopLayout())return;"
    "const panel=document.getElementById('chat-panel');const ol=document.getElementById('chat-overlay');if(!panel||!ol)return;"
    "updateChatLayout();if(panel.parentElement!==ol)ol.appendChild(panel);ol.style.display='flex';document.body.style.overflow='hidden';"
    "initChat();setTimeout(()=>document.getElementById('chat-input')?.focus(),150);}"
    "function closeChatOverlay(){const ol=document.getElementById('chat-overlay');if(ol)ol.style.display='none';document.body.style.overflow='';}"
)
new_open = (
    "function handleChatTabClick(e){if(e){e.preventDefault();e.stopPropagation();}if(isDesktopLayout())switchTab('chat');else openChatOverlay(e);}"
    "function openChatOverlay(e){if(e){e.preventDefault();e.stopPropagation();}if(isDesktopLayout()){switchTab('chat');return;}"
    "const panel=document.getElementById('chat-panel');const ol=document.getElementById('chat-overlay');if(!panel||!ol)return;"
    "if(!chatOverlayOpen){chatTabBeforeOpen=currentTab;chatOverlayOpen=true;}"
    "updateChatLayout();if(panel.parentElement!==ol)ol.appendChild(panel);ol.style.display='flex';document.body.style.overflow='hidden';"
    "const chatBtn=document.getElementById('btn-chat');if(chatBtn){chatBtn.classList.add('active');document.querySelectorAll('.tab-btn[data-tab]').forEach(b=>b.classList.remove('active'));}"
    "equipPanel.classList.remove('show');inventoryPanel.classList.remove('show');craftPanel.classList.remove('show');"
    "craftIdlePanel.classList.remove('show');profilePanel.classList.remove('show');setLogVisible(false);initChat();"
    "setTimeout(()=>document.getElementById('chat-input')?.focus(),150);}"
    "function closeChatOverlay(restoreTab){if(restoreTab===undefined)restoreTab=true;const ol=document.getElementById('chat-overlay');"
    "if(ol)ol.style.display='none';document.body.style.overflow='';if(!chatOverlayOpen)return;chatOverlayOpen=false;"
    "const chatBtn=document.getElementById('btn-chat');if(chatBtn)chatBtn.classList.remove('active');"
    "if(restoreTab)switchTab(chatTabBeforeOpen||'log',true);else updateChatLayout();}"
)
if old_open not in s:
    raise SystemExit("openChatOverlay not found")
s = s.replace(old_open, new_open, 1)

old_layout_desktop = (
    "}else if(currentTab==='log'||currentTab==='craftIdle'||!['equip','inventory','craft','profile'].includes(currentTab))switchTab('equip');"
)
new_layout_desktop = (
    "}else if(chatOverlayOpen){chatOverlayOpen=false;currentTab='chat';}else if(currentTab==='log'||currentTab==='craftIdle'||"
    "!['equip','inventory','craft','profile','chat'].includes(currentTab))switchTab('equip');"
)
if old_layout_desktop not in s:
    raise SystemExit("updateLayoutMode desktop branch not found")
s = s.replace(old_layout_desktop, new_layout_desktop, 1)

old_layout_mobile = (
    "setLogVisible(currentTab==='log');if(['equip','inventory','craft','profile'].includes(currentTab))switchTab(currentTab);"
)
new_layout_mobile = (
    "if(chatOverlayOpen)closeChatOverlay(false);if(currentTab==='chat')currentTab='equip';"
    "setLogVisible(currentTab==='log');if(['equip','inventory','craft','profile'].includes(currentTab))switchTab(currentTab);"
)
if old_layout_mobile not in s:
    raise SystemExit("updateLayoutMode mobile branch not found")
s = s.replace(old_layout_mobile, new_layout_mobile, 1)

old_switch = (
    "function switchTab(tab){if(isDesktopLayout()&&tab==='log'&&!droneDungeonActive)tab='equip';"
    "if(droneDungeonActive&&!DRONE_DUNGEON_ALLOWED_TABS.includes(tab))return;currentTab=tab;"
    "document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));const tabBtn=document.querySelector(`[data-tab=\"${tab}\"]`);"
    "if(tabBtn)tabBtn.classList.add('active');equipPanel.classList.remove('show');inventoryPanel.classList.remove('show');"
    "craftPanel.classList.remove('show');craftIdlePanel.classList.remove('show');profilePanel.classList.remove('show');setLogVisible(tab==='log');"
    "if(tab==='equip'){equipPanel.classList.add('show');renderEquipPanel();}else if(tab==='inventory'){inventoryPanel.classList.add('show');"
    "renderInventoryPanel();}else if(tab==='craft'){craftPanel.classList.add('show');renderCraftPanel();}else if(tab==='profile'){"
    "profilePanel.classList.add('show');renderProfilePanel();}updatePanelSidebarTitle();}"
)
new_switch = (
    "function switchTab(tab,skipCloseChat){if(!skipCloseChat&&!isDesktopLayout()&&chatOverlayOpen&&tab!=='chat')closeChatOverlay(false);"
    "if(isDesktopLayout()&&tab==='log'&&!droneDungeonActive)tab='equip';"
    "if(droneDungeonActive&&!DRONE_DUNGEON_ALLOWED_TABS.includes(tab)&&tab!=='chat')return;currentTab=tab;"
    "document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));const tabBtn=document.querySelector(`[data-tab=\"${tab}\"]`);"
    "const chatBtn=document.getElementById('btn-chat');if(tab==='chat'){if(chatBtn)chatBtn.classList.add('active');}else if(tabBtn)tabBtn.classList.add('active');"
    "equipPanel.classList.remove('show');inventoryPanel.classList.remove('show');craftPanel.classList.remove('show');"
    "craftIdlePanel.classList.remove('show');profilePanel.classList.remove('show');const embedded=document.getElementById('chat-embedded');"
    "if(embedded){embedded.classList.remove('show');if(!isDesktopLayout()||tab!=='chat')embedded.style.display='none';}"
    "setLogVisible(tab==='log');if(tab==='equip'){equipPanel.classList.add('show');renderEquipPanel();}else if(tab==='inventory'){"
    "inventoryPanel.classList.add('show');renderInventoryPanel();}else if(tab==='craft'){craftPanel.classList.add('show');renderCraftPanel();}"
    "else if(tab==='profile'){profilePanel.classList.add('show');renderProfilePanel();}else if(tab==='chat'&&isDesktopLayout()){"
    "setLogVisible(false);if(embedded){embedded.classList.add('show');embedded.style.display='flex';}ensureChatLazyInit();initChat();}"
    "updatePanelSidebarTitle();updateChatLayout();}"
)
if old_switch not in s:
    raise SystemExit("switchTab not found")
s = s.replace(old_switch, new_switch, 1)

old_listener = "document.getElementById('btn-chat').addEventListener('click',openChatOverlay);"
new_listener = "document.getElementById('btn-chat').addEventListener('click',handleChatTabClick);"
if old_listener not in s:
    raise SystemExit("btn-chat listener not found")
s = s.replace(old_listener, new_listener, 1)

# --- version bump ---
old_ver = "GAME_VERSION='2.5.8',GAME_VERSION_HISTORY=[{version:'2.5.8',date:'2025-06-07',summary:{zh:'預設介面與文字放大；文字大小上限調至 2.00x。',en:'Larger default UI/text scale; text size slider max 2.00x.'}},"
new_ver = (
    "GAME_VERSION='2.5.9',GAME_VERSION_HISTORY=[{version:'2.5.9',date:'2025-06-07',summary:{zh:'修復聊天室進入／關閉顯示異常；桌面版改為側欄分頁、手機版覆蓋層狀態同步。',"
    "en:'Fix chat open/close layout; desktop sidebar tab and mobile overlay state sync.'}},{version:'2.5.8',date:'2025-06-07',summary:{zh:'預設介面與文字放大；文字大小上限調至 2.00x。',en:'Larger default UI/text scale; text size slider max 2.00x.'}},"
)
if old_ver not in s:
    raise SystemExit("GAME_VERSION not found")
s = s.replace(old_ver, new_ver, 1)

path.write_text(s, encoding="utf-8")
print("Patched index.html -> v2.5.9 chat layout fix")
