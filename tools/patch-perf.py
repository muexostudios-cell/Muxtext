#!/usr/bin/env python3
"""Performance optimizations for multi-player / concurrent usage."""
from pathlib import Path

path = Path('/workspace/index.html')
c = path.read_text(encoding='utf-8')

replacements = [
    # Slower local save debounce
    (
        'saveTimeout=setTimeout(()=>{saveGame();saveTimeout=null;},500);',
        'saveTimeout=setTimeout(()=>{saveGame();saveTimeout=null;},1000);',
    ),
    # Slower cloud upload debounce (reduce Gun relay load)
    (
        'cloudUploadTimeout=setTimeout(()=>{uploadCurrentAccountToCloud();cloudUploadTimeout=null;},2000);',
        'cloudUploadTimeout=setTimeout(()=>{uploadCurrentAccountToCloud();cloudUploadTimeout=null;},30000);',
    ),
    # Status bar should not trigger save every tick
    (
        "}else{droneStatus.style.display='none';}throttleSave();}function setAtkBtnStyle(active)",
        "}else{droneStatus.style.display='none';}}function setAtkBtnStyle(active)",
    ),
    # AES key session cache
    (
        'async function deriveAesKey(password,saltB64){const salt=Uint8Array.from(atob(saltB64),c=>c.charCodeAt(0));',
        "let cachedAesKey=null,cachedAesSalt='';async function deriveAesKey(password,saltB64){if(cachedAesKey&&cachedAesSalt===saltB64)return cachedAesKey;const salt=Uint8Array.from(atob(saltB64),c=>c.charCodeAt(0));",
    ),
    (
        "return crypto.subtle.deriveKey({name:'PBKDF2',salt,iterations:100000,hash:'SHA-256'},km,{name:'AES-GCM',length:256},false,['encrypt','decrypt']);}async function encryptString",
        "const key=await crypto.subtle.deriveKey({name:'PBKDF2',salt,iterations:100000,hash:'SHA-256'},km,{name:'AES-GCM',length:256},false,['encrypt','decrypt']);cachedAesKey=key;cachedAesSalt=saltB64;return key;}async function encryptString",
    ),
    # Clear crypto cache on logout
    (
        'function clearSessionAccountSecret(){sessionAccountSecret=null;try{sessionStorage.removeItem(SESSION_SECRET_KEY);}catch(e){}}',
        "function clearSessionAccountSecret(){sessionAccountSecret=null;try{sessionStorage.removeItem(SESSION_SECRET_KEY);}catch(e){}cachedAesKey=null;cachedAesSalt='';}",
    ),
    # Chat lazy init + batching vars (before escapeChatHtml)
    (
        "const seenChatIds=new Set();let chatGun=null,chatRoom=null,chatReady=false,chatStatusMode='loading';function escapeChatHtml",
        "const seenChatIds=new Set();let chatGun=null,chatRoom=null,chatReady=false,chatStatusMode='loading',chatLazyBound=false,chatFlushPending=false,chatBatchQueue=[],lastChatSendAt=0;const CHAT_SEND_COOLDOWN_MS=1500,CHAT_HISTORY_MS=172800000,SEEN_CHAT_MAX=400;function ensureChatLazyInit(){if(chatReady||chatLazyBound)return;chatLazyBound=true;const input=document.getElementById('chat-input');const bind=()=>initChat();if(input)input.addEventListener('focus',bind,{once:true});const btn=document.getElementById('btn-chat');if(btn)btn.addEventListener('click',bind,{once:true});const embedded=document.getElementById('chat-embedded');if(embedded)embedded.addEventListener('mousedown',bind,{once:true});}function queueChatMessage(data){chatBatchQueue.push(data);if(!chatFlushPending){chatFlushPending=true;requestAnimationFrame(()=>{chatFlushPending=false;const batch=chatBatchQueue.splice(0,chatBatchQueue.length);for(const item of batch)appendChatMessage(item);});}}function trimSeenChatIds(){if(seenChatIds.size<=SEEN_CHAT_MAX)return;const keep=[...seenChatIds].slice(-300);seenChatIds.clear();keep.forEach(id=>seenChatIds.add(id));}function escapeChatHtml",
    ),
    # Desktop: lazy chat instead of immediate init
    (
        "if(btn)btn.style.display='none';initChat();}else{if(panel.parentElement!==overlay)",
        "if(btn)btn.style.display='none';ensureChatLazyInit();}else{if(panel.parentElement!==overlay)",
    ),
    # Game load: defer Gun connection until user interacts with chat
    (
        'startPlaytimeCounter();initChat();',
        'startPlaytimeCounter();ensureChatLazyInit();',
        True,
    ),
    # initChat: batch incoming, skip stale history
    (
        "chatRoom.map().on((data,id)=>{if(!data||!data.text||!id)return;if(seenChatIds.has(id))return;seenChatIds.add(id);appendChatMessage(data);});",
        "chatRoom.map().on((data,id)=>{if(!data||!data.text||!id)return;if(seenChatIds.has(id))return;if(data.time&&data.time<Date.now()-CHAT_HISTORY_MS)return;seenChatIds.add(id);trimSeenChatIds();queueChatMessage(data);});",
    ),
    # sendChatMessage rate limit
    (
        "function sendChatMessage(){const input=document.getElementById('chat-input');if(!input)return;const text=input.value.trim();if(!text)return;",
        "function sendChatMessage(){const input=document.getElementById('chat-input');if(!input)return;const text=input.value.trim();if(!text)return;if(Date.now()-lastChatSendAt<CHAT_SEND_COOLDOWN_MS)return;lastChatSendAt=Date.now();",
    ),
    # Incremental map render
    (
        "function renderMap(){if(!currentDungeon)return;mapEl.innerHTML='';for(let r=0;r<7;r++){for(let c=0;c<7;c++){const cell=mapData[r][c];const char=getCellChar(cell,r,c);const cls=getCellClasses(cell,r,c);const div=document.createElement('div');div.className=`cell ${cls}`;div.textContent=char;div.dataset.r=r;div.dataset.c=c;mapEl.appendChild(div);}}}",
        "let mapCellEls=null;function invalidateMapCells(){mapCellEls=null;if(mapEl)mapEl.innerHTML='';}function renderMap(){if(!currentDungeon)return;if(!mapCellEls){mapEl.innerHTML='';mapCellEls=[];for(let r=0;r<7;r++){mapCellEls[r]=[];for(let c=0;c<7;c++){const div=document.createElement('div');div.dataset.r=r;div.dataset.c=c;mapEl.appendChild(div);mapCellEls[r][c]=div;}}}for(let r=0;r<7;r++){for(let c=0;c<7;c++){const cell=mapData[r][c];const div=mapCellEls[r][c];div.className=`cell ${getCellClasses(cell,r,c)}`;div.textContent=getCellChar(cell,r,c);}}}",
    ),
    # Invalidate map cache on restart
    (
        'function restartGame(){clearAllTimers();clearDroneTimers();clearAccountSave();',
        'function restartGame(){invalidateMapCells();clearAllTimers();clearDroneTimers();clearAccountSave();',
    ),
    # Playtime: pause when tab hidden
    (
        'function startPlaytimeCounter(){if(playtimeInterval)clearInterval(playtimeInterval);playtimeInterval=setInterval(()=>{if(!player.stats)player.stats={createdAt:Date.now(),totalPlaytime:0,dungeonClears:0,dungeonKills:0,droneKills:0};player.stats.totalPlaytime=(player.stats.totalPlaytime||0)+1;},1000);}',
        "function startPlaytimeCounter(){if(playtimeInterval)clearInterval(playtimeInterval);if(document.hidden)return;playtimeInterval=setInterval(()=>{if(document.hidden)return;if(!player.stats)player.stats={createdAt:Date.now(),totalPlaytime:0,dungeonClears:0,dungeonKills:0,droneKills:0};player.stats.totalPlaytime=(player.stats.totalPlaytime||0)+1;},1000);}if(!window.__tdPlaytimeVisBound){window.__tdPlaytimeVisBound=true;document.addEventListener('visibilitychange',()=>{if(document.hidden){if(playtimeInterval){clearInterval(playtimeInterval);playtimeInterval=null;}}else if(!playtimeInterval)startPlaytimeCounter();});}",
    ),
    # Version bump
    (
        "GAME_VERSION='2.2.2',GAME_VERSION_HISTORY=[{version:'2.2.2'",
        "GAME_VERSION='2.3',GAME_VERSION_HISTORY=[{version:'2.3',date:'2025-06-07',summary:{zh:'效能優化：減少存檔/雲端同步頻率、聊天批次處理、地圖增量渲染，改善多玩家同時在線體驗。',en:'Performance: save/cloud debounce, chat batching, incremental map render.'}},{version:'2.2.2'",
    ),
]

applied = 0
for item in replacements:
    replace_all = False
    if len(item) == 3:
        old, new, replace_all = item
    else:
        old, new = item
    if old not in c:
        raise SystemExit(f'MISSING patch: {old[:60]}...')
    count = c.count(old) if replace_all else 1
    c = c.replace(old, new, count if replace_all else 1)
    applied += count if replace_all else 1

path.write_text(c, encoding='utf-8')
print(f'Applied {applied} performance patches')
