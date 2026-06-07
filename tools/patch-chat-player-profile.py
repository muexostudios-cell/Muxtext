#!/usr/bin/env python3
"""Patch index.html: chat level display + long-press player profile."""
from pathlib import Path

html = Path("index.html").read_text()

OLD_APPEND = (
    "function appendChatMessage(data){if(!data||!data.text)return;const el=document.getElementById('chat-messages');"
    "if(!el)return;const div=document.createElement('div');div.className='chat-msg';const time=data.time?"
    "new Date(data.time).toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'}):'';"
    "div.innerHTML='<span class=\"chat-user\">'+escapeChatHtml(data.user||'???')+'</span><span class=\"chat-time\">'+time+'</span><br>'+escapeChatHtml(data.text);"
    "el.appendChild(div);while(el.children.length>100)el.removeChild(el.firstChild);el.scrollTop=el.scrollHeight;}"
)

NEW_APPEND = (
    "function getChatMessageLevel(data){if(!data)return null;const lv=Number(data.level??data.profile?.lv??data.profile?.level);"
    "return Number.isFinite(lv)&&lv>=1?Math.floor(lv):null;}"
    "function buildChatProfileSnapshot(){clampCraftStationLevel();clampDroneIdleLevel();initTalentPoints();const stats=player.stats||{};"
    "const equip={};for(const slotDef of EQUIP_SLOTS){const eq=player.equipment[slotDef.slot];if(!eq)continue;"
    "equip[slotDef.slot]={name:eq.name,rarity:eq.rarity,type:eq.type,level:eq.level,upgradeLv:eq.upgradeLv||0,baseStat:eq.baseStat,baseValue:eq.baseValue,affixes:eq.affixes.map(a=>({stat:a.stat,value:a.value}))};}"
    "const talents={};TALENT_STATS.forEach(s=>{talents[s.key]=player.talents[s.key]||0;});"
    "const p={n:playerCustomName,lv:player.level,g:player.gold,c:player.overloadChips||0,cl:player.craftLevel,dl:player.droneIdleLevel||1,"
    "md:Math.round(player.memoryDecay*10)/10,atk:getMainAtk(),def:player.def,hp:player.maxHp,spd:player.spd,crit:Math.floor(player.critChance*100),"
    "dodge:Math.floor(player.dodge*100),talents,equip,st:{ca:stats.createdAt||0,pt:stats.totalPlaytime||0,dc:stats.dungeonClears||0,dk:stats.dungeonKills||0}};"
    "if(avatarDataUrl&&avatarDataUrl.length<30000)p.av=avatarDataUrl;return p;}"
    "function renderChatProfileHtml(p){const name=escapeChatHtml(p.n||p.name||'???');const lv=p.lv??p.level??'?';const gold=p.g??p.gold??0;"
    "const chips=p.c??p.chips??0;const craftLv=p.cl??p.craftLevel??1;const droneIdleLv=p.dl??p.droneIdleLevel??1;const decay=p.md??p.memoryDecay??0;"
    "const avatar=p.av||p.avatar||'';let html='<div class=\"chat-profile-header\">';"
    "if(avatar){html+='<div class=\"chat-profile-avatar\"><img src=\"'+escapeChatHtml(avatar)+'\" alt=\"\"></div>';}"
    "else{html+='<div class=\"chat-profile-avatar chat-profile-avatar-empty\">[ ]</div>';}"
    "html+='<div class=\"chat-profile-info\"><div class=\"chat-profile-name\">'+name+'</div>';"
    "html+='<div class=\"chat-profile-stat\">'+escapeChatHtml(t('lvLabel'))+' '+lv+'</div>';"
    "html+='<div class=\"chat-profile-stat\">'+escapeChatHtml(t('goldLabel'))+' '+gold+'</div>';"
    "html+='<div class=\"chat-profile-stat chip-text\">'+escapeChatHtml(t('chipLabel'))+' '+chips+'</div>';"
    "html+='<div class=\"chat-profile-stat\">'+escapeChatHtml(t('profileCraftLabel'))+' '+craftLv+'</div>';"
    "html+='<div class=\"chat-profile-stat\">'+escapeChatHtml(t('profileDroneIdleLabel'))+' '+droneIdleLv+'</div>';"
    "html+='<div class=\"chat-profile-stat\">'+escapeChatHtml(t('profileDecayLabel'))+' '+decay+'% / 100%</div></div></div>';"
    "const zh=currentLang==='zh';const combatRows=[[zh?'攻擊':'ATK',p.atk],[zh?'防禦':'DEF',p.def],[zh?'生命':'HP',p.hp],[zh?'速度':'SPD',p.spd],"
    "['CRIT',(p.crit??0)+'%'],['DODGE',(p.dodge??0)+'%']];"
    "html+='<div class=\"chat-profile-section\"><h4>'+escapeChatHtml(t('combatStatsTitle'))+'</h4><div class=\"chat-profile-stats\">';"
    "combatRows.forEach(r=>{html+='<div class=\"chat-profile-stat-row\"><span>'+escapeChatHtml(r[0])+'</span><span>'+r[1]+'</span></div>';});"
    "html+='</div></div><div class=\"chat-profile-section\"><h4>'+escapeChatHtml(t('talentStatsTitle'))+'</h4><div class=\"chat-profile-stats\">';"
    "const talents=p.talents||{};TALENT_STATS.forEach(s=>{const pts=talents[s.key]||0;const pct=(pts*s.perPoint).toFixed(2);"
    "html+='<div class=\"chat-profile-stat-row\"><span>'+escapeChatHtml(getTalentStatLabel(s))+'</span><span>+'+pct+'%</span></div>';});"
    "html+='</div></div><div class=\"chat-profile-section\"><h4>'+escapeChatHtml(t('equipmentTitle'))+'</h4>';"
    "const equip=p.equip||{};let hasEquip=false;for(const slotDef of EQUIP_SLOTS){const eq=equip[slotDef.slot];if(!eq)continue;hasEquip=true;"
    "html+='<div class=\"chat-profile-equip-slot rarity-'+eq.rarity+'\"><div class=\"chat-profile-equip-slot-label\">'+escapeChatHtml(getEquipSlotLabel(slotDef.slot))+'</div>'+getEquipDetailHtml(eq,true)+'</div>';}"
    "if(!hasEquip)html+='<div class=\"chat-profile-empty\">--</div>';html+='</div>';"
    "const st=p.st||p.stats||{};const createdAt=st.ca??st.createdAt;html+='<div class=\"chat-profile-section\"><h4>'+escapeChatHtml(t('statsTitle'))+'</h4><div class=\"chat-profile-stats\">';"
    "if(createdAt)html+='<div class=\"chat-profile-stat-row\"><span>'+escapeChatHtml(t('statCreated'))+'</span><span>'+new Date(createdAt).toLocaleDateString(currentLang==='zh'?'zh-HK':'en-US')+'</span></div>';"
    "html+='<div class=\"chat-profile-stat-row\"><span>'+escapeChatHtml(t('statPlaytime'))+'</span><span>'+formatPlaytime(st.pt??st.totalPlaytime??0)+'</span></div>';"
    "html+='<div class=\"chat-profile-stat-row\"><span>'+escapeChatHtml(t('statDungeonClears'))+'</span><span>'+formatNumber(st.dc??st.dungeonClears??0)+'</span></div>';"
    "html+='<div class=\"chat-profile-stat-row\"><span>'+escapeChatHtml(t('statDungeonKills'))+'</span><span>'+formatNumber(st.dk??st.dungeonKills??0)+'</span></div></div></div>';return html;}"
    "function showChatPlayerProfile(data){const overlay=document.getElementById('player-profile-overlay');const content=document.getElementById('player-profile-content');"
    "if(!overlay||!content)return;const profile=data?.profile;const title=document.getElementById('player-profile-title');"
    "if(title)title.textContent=t('chatProfileTitle');"
    "content.innerHTML=profile?renderChatProfileHtml(profile):'<p class=\"chat-profile-empty\">'+escapeChatHtml(t('chatProfileUnavailable'))+'</p>';"
    "overlay.style.display='flex';}"
    "function closeChatPlayerProfile(){const overlay=document.getElementById('player-profile-overlay');if(overlay)overlay.style.display='none';}"
    "function bindChatProfileLongPress(el,data){let isLongPress=false,moved=false;const startPos={x:0,y:0};let timer=null;"
    "el.addEventListener('pointerdown',e=>{e.preventDefault();isLongPress=false;moved=false;startPos.x=e.clientX;startPos.y=e.clientY;"
    "timer=setTimeout(()=>{isLongPress=true;showChatPlayerProfile(data);},500);});"
    "el.addEventListener('pointermove',e=>{const dx=e.clientX-startPos.x,dy=e.clientY-startPos.y;if(Math.abs(dx)>10||Math.abs(dy)>10){moved=true;clearTimeout(timer);}});"
    "el.addEventListener('pointerup',()=>clearTimeout(timer));el.addEventListener('pointerleave',()=>clearTimeout(timer));el.addEventListener('pointercancel',()=>clearTimeout(timer));}"
    "function appendChatMessage(data){if(!data||!data.text)return;const el=document.getElementById('chat-messages');if(!el)return;"
    "const div=document.createElement('div');div.className='chat-msg';const head=document.createElement('div');head.className='chat-msg-head';"
    "const lvl=getChatMessageLevel(data);if(lvl!=null){const lvlSpan=document.createElement('span');lvlSpan.className='chat-level';lvlSpan.textContent='Lv.'+lvl;head.appendChild(lvlSpan);}"
    "const userWrap=document.createElement('span');userWrap.className='chat-user-wrap';const userSpan=document.createElement('span');userSpan.className='chat-user';"
    "userSpan.textContent=data.user||'???';userWrap.appendChild(userSpan);head.appendChild(userWrap);"
    "const timeSpan=document.createElement('span');timeSpan.className='chat-time';timeSpan.textContent=data.time?new Date(data.time).toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'}):'';"
    "head.appendChild(timeSpan);div.appendChild(head);const textDiv=document.createElement('div');textDiv.className='chat-text';textDiv.textContent=data.text;div.appendChild(textDiv);"
    "bindChatProfileLongPress(userWrap,data);el.appendChild(div);while(el.children.length>100)el.removeChild(el.firstChild);el.scrollTop=el.scrollHeight;}"
)

OLD_SEND = (
    "function sendChatMessage(){const input=document.getElementById('chat-input');if(!input)return;const text=input.value.trim();if(!text)return;"
    "if(Date.now()-lastChatSendAt<CHAT_SEND_COOLDOWN_MS)return;lastChatSendAt=Date.now();const base=getChatEndpoint();const user=playerCustomName||'PLAYER';"
    "if(!base||!chatReady){appendChatMessage({user,text,time:Date.now()});input.value='';updateChatStatus('offline');return;}"
    "fetch(base+'/messages',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({user,text})}).then(r=>r.json()).then(data=>{if(data&&data.message)ingestChatMessages([data.message]);input.value='';}).catch(()=>{appendChatMessage({user,text,time:Date.now()});input.value='';updateChatStatus('offline');});}"
)

NEW_SEND = (
    "function sendChatMessage(){const input=document.getElementById('chat-input');if(!input)return;const text=input.value.trim();if(!text)return;"
    "if(Date.now()-lastChatSendAt<CHAT_SEND_COOLDOWN_MS)return;lastChatSendAt=Date.now();const base=getChatEndpoint();const user=playerCustomName||'PLAYER';"
    "const level=player.level||1;const profile=buildChatProfileSnapshot();const localMsg={user,text,time:Date.now(),level,profile};"
    "if(!base||!chatReady){appendChatMessage(localMsg);input.value='';updateChatStatus('offline');return;}"
    "fetch(base+'/messages',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({user,text,level,profile})}).then(r=>r.json()).then(data=>{if(data&&data.message)ingestChatMessages([data.message]);input.value='';}).catch(()=>{appendChatMessage(localMsg);input.value='';updateChatStatus('offline');});}"
)

replacements = [
    (OLD_APPEND, NEW_APPEND, "appendChatMessage"),
    (OLD_SEND, NEW_SEND, "sendChatMessage"),
    (
        '.chat-time{color:#555;font-size:.45rem;margin-left:.3rem}',
        '.chat-time{color:#555;font-size:.45rem;margin-left:auto}.chat-msg-head{display:flex;align-items:baseline;gap:.25rem;flex-wrap:wrap;margin-bottom:.15rem}.chat-level{color:#aaa;font-size:.48rem;flex-shrink:0}.chat-user-wrap{cursor:pointer;touch-action:manipulation}.chat-user-wrap:active .chat-user{color:var(--chip)}.chat-text{word-break:break-word}',
        "chat CSS",
    ),
    (
        '#talent-overlay,#levelup-overlay,#drone-dungeon-overlay,#drone-result-overlay,#permanent-death-overlay,#recycle-overlay,#filter-overlay{display:none;',
        '#player-profile-overlay,#talent-overlay,#levelup-overlay,#drone-dungeon-overlay,#drone-result-overlay,#permanent-death-overlay,#recycle-overlay,#filter-overlay{display:none;',
        "overlay group",
    ),
    (
        '#talent-box,#levelup-box,#drone-dungeon-box,#drone-result-box{background:#000;border:1px solid #fff;padding:1rem;width:90%;max-width:360px;color:var(--text);font-size:.6rem;text-align:left;max-height:85vh;overflow-y:auto}',
        '#player-profile-box,#talent-box,#levelup-box,#drone-dungeon-box,#drone-result-box{background:#000;border:1px solid #fff;padding:1rem;width:90%;max-width:360px;color:var(--text);font-size:.6rem;text-align:left;max-height:85vh;overflow-y:auto}',
        "overlay box group",
    ),
    (
        '<div id="chat-overlay"><div id="chat-panel">',
        '<div id="player-profile-overlay"><div id="player-profile-box"><h3 id="player-profile-title">玩家資訊</h3><div id="player-profile-content"></div><button type="button" class="btn-close" id="btn-close-player-profile">關閉</button></div></div><div id="chat-overlay"><div id="chat-panel">',
        "profile overlay HTML",
    ),
    (
        'chatStatusOffline:"離線 · 僅本地顯示"',
        'chatStatusOffline:"離線 · 僅本地顯示",chatProfileTitle:"玩家資訊",chatProfileUnavailable:"無法查看此玩家的個人資料（舊版訊息或資料未附帶）"',
        "zh LANG",
    ),
    (
        'chatStatusOffline:"Offline · local only"',
        'chatStatusOffline:"Offline · local only",chatProfileTitle:"Player Info",chatProfileUnavailable:"Profile unavailable (legacy message or missing data)"',
        "en LANG",
    ),
    (
        "GAME_VERSION='2.5.4',GAME_VERSION_HISTORY=[{version:'2.5.4',date:'2025-06-07',summary:{zh:'無人機掛機上限跟隨玩家等級；修復語言按鈕與狀態欄平均排版。',en:'Drone idle cap follows player level; fix language buttons and even status bar layout.'}},",
        "GAME_VERSION='2.5.5',GAME_VERSION_HISTORY=[{version:'2.5.5',date:'2025-06-07',summary:{zh:'聊天室顯示玩家等級；長按可檢視其他玩家個人頁面。',en:'Chat shows player level; long-press to view player profiles.'}},{version:'2.5.4',date:'2025-06-07',summary:{zh:'無人機掛機上限跟隨玩家等級；修復語言按鈕與狀態欄平均排版。',en:'Drone idle cap follows player level; fix language buttons and even status bar layout.'}},",
        "version",
    ),
    (
        "document.getElementById('btn-close-chat').addEventListener('click',closeChatOverlay);",
        "document.getElementById('btn-close-chat').addEventListener('click',closeChatOverlay);document.getElementById('btn-close-player-profile').addEventListener('click',closeChatPlayerProfile);document.getElementById('player-profile-overlay').addEventListener('click',e=>{if(e.target===document.getElementById('player-profile-overlay'))closeChatPlayerProfile();});",
        "event listeners",
    ),
]

extra_css = (
    "#player-profile-overlay{position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,.92);z-index:110;justify-content:center;align-items:center;backdrop-filter:blur(2px)}"
    "#player-profile-box{width:92%;max-width:380px;font-size:.55rem}#player-profile-box h3{color:#fff;font-size:.75rem;text-align:center;margin-bottom:.5rem;border-bottom:1px solid #333;padding-bottom:.3rem}"
    "#btn-close-player-profile{width:100%;margin-top:.6rem;padding:.4rem;background:0 0;border:1px solid #fff;color:#fff;font-family:inherit;font-size:.55rem;cursor:pointer}"
    ".chat-profile-header{display:flex;gap:.5rem;margin-bottom:.5rem;padding-bottom:.4rem;border-bottom:1px solid #1a1a1a}"
    ".chat-profile-avatar{width:2.4rem;height:2.4rem;border:1px solid #333;display:flex;align-items:center;justify-content:center;flex-shrink:0;overflow:hidden}"
    ".chat-profile-avatar img{width:100%;height:100%;object-fit:cover}.chat-profile-avatar-empty{color:#555;font-size:.45rem}"
    ".chat-profile-name{color:#fff;font-size:.65rem;margin-bottom:.2rem}.chat-profile-stat{font-size:.5rem;color:#aaa;line-height:1.5}"
    ".chat-profile-section{margin-bottom:.45rem}.chat-profile-section h4{color:#fff;font-size:.55rem;margin-bottom:.25rem;border-bottom:1px solid #1a1a1a;padding-bottom:.15rem}"
    ".chat-profile-stats{font-size:.5rem;color:#aaa}.chat-profile-stat-row{display:flex;justify-content:space-between;gap:.5rem;padding:.08rem 0}"
    ".chat-profile-equip-slot{margin-bottom:.35rem;padding:.25rem;border:1px solid #1a1a1a}.chat-profile-equip-slot-label{color:#666;font-size:.48rem;margin-bottom:.15rem}"
    ".chat-profile-empty{color:#555;text-align:center;padding:.5rem;font-size:.5rem}"
)

if extra_css not in html:
    html = html.replace("</style>", extra_css + "</style>", 1)

for old, new, label in replacements:
    if old not in html:
        raise SystemExit(f"Missing patch target: {label}")
    html = html.replace(old, new, 1)

Path("index.html").write_text(html)
print("Patched index.html")
