#!/usr/bin/env python3
"""Fix bugs and optimize from code audit."""
from pathlib import Path

html = Path("index.html").read_text()

replacements = [
    (
        "allowDevFallback:false,allowLiveTrustRedirect:true}",
        "allowDevFallback:false,allowLiveTrustRedirect:false}",
        "stripe trust redirect",
    ),
    (
        "combatRows.forEach(r=>{html+='<div class=\"chat-profile-stat-row\"><span>'+escapeChatHtml(r[0])+'</span><span>'+r[2]+'</span></div>';});",
        "combatRows.forEach(r=>{html+='<div class=\"chat-profile-stat-row\"><span>'+escapeChatHtml(r[0])+'</span><span>'+escapeChatHtml(String(r[1]??''))+'</span></div>';});",
        "combat stats index",
    ),
    (
        "if(btn)btn.style.display='none';ensureChatLazyInit();}else{if(panel.parentElement!==overlay)",
        "if(btn)btn.style.display='none';ensureChatLazyInit();initChat();}else{if(panel.parentElement!==overlay)",
        "desktop initChat",
    ),
    (
        "#chat-overlay #chat-input,#chat-overlay #chat-input-row{user-select:text;-webkit-user-select:text}",
        "#chat-overlay #chat-input,#chat-overlay #chat-input-row,#chat-embedded #chat-input,#chat-embedded #chat-input-row{user-select:text;-webkit-user-select:text}",
        "embedded chat user-select",
    ),
    (
        "function t(key,...args){let str=LANG[currentLang][key]||key;args.forEach((arg,i)=>{str=str.replace(`{${i}}`,arg);});return str;}",
        "function t(key,...args){let str=LANG[currentLang][key]||key;args.forEach((arg,i)=>{const safe=String(arg).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/\"/g,'&quot;');str=str.replace(`{${i}}`,safe);});return str;}",
        "t() escape args",
    ),
    (
        "if(eq.affixes.length===0){html+=`<span style=\"color:#555;\">${getBasicModDisplay()}</span>`;}else{eq.affixes.forEach(a=>{",
        "const _affixes=Array.isArray(eq.affixes)?eq.affixes:[];if(_affixes.length===0){html+=`<span style=\"color:#555;\">${getBasicModDisplay()}</span>`;}else{_affixes.forEach(a=>{",
        "affixes guard",
    ),
    (
        "function getChatMessageLevel(data){if(!data)return null;const lv=Number(data.level??data.profile?.lv??data.profile?.level);",
        "const CHAT_PROFILE_RARITIES=new Set(['common','rare','epic','legendary','hidden']);"
        "function sanitizeChatAvatarUrl(url){if(!url||typeof url!=='string')return '';const u=url.trim();if(!u.startsWith('data:image/')||u.length>12000)return '';return u;}"
        "function sanitizeChatEquipItem(eq){if(!eq||typeof eq!=='object')return null;const rarity=CHAT_PROFILE_RARITIES.has(eq.rarity)?eq.rarity:'common';"
        "const affixes=Array.isArray(eq.affixes)?eq.affixes.slice(0,8).map(a=>({stat:String(a?.stat||'').slice(0,24),value:Number(a?.value)||0})):[];"
        "return{name:String(eq.name||'').slice(0,40),rarity,type:String(eq.type||'').slice(0,16),level:Math.max(1,Math.min(99999,parseInt(eq.level,10)||1)),"
        "upgradeLv:Math.max(0,Math.min(99,parseInt(eq.upgradeLv,10)||0)),baseStat:String(eq.baseStat||'').slice(0,24),baseValue:Number(eq.baseValue)||0,affixes};}"
        "function sanitizeChatProfile(raw){if(!raw||typeof raw!=='object')return null;"
        "const p={n:String(raw.n||raw.name||'???').slice(0,32),lv:Math.max(1,Math.min(99999,parseInt(raw.lv??raw.level,10)||1)),"
        "g:Math.max(0,parseInt(raw.g??raw.gold,10)||0),c:Math.max(0,parseInt(raw.c??raw.chips,10)||0),"
        "cl:Math.max(1,parseInt(raw.cl??raw.craftLevel,10)||1),dl:Math.max(1,parseInt(raw.dl??raw.droneIdleLevel,10)||1),"
        "md:Math.max(0,Math.min(100,Number(raw.md??raw.memoryDecay)||0)),"
        "atk:Math.max(0,parseInt(raw.atk,10)||0),def:Math.max(0,parseInt(raw.def,10)||0),hp:Math.max(0,parseInt(raw.hp,10)||0),"
        "spd:Math.max(0,parseInt(raw.spd,10)||0),crit:Math.max(0,parseInt(raw.crit,10)||0),dodge:Math.max(0,parseInt(raw.dodge,10)||0),"
        "talents:{},equip:{},st:{}};const av=sanitizeChatAvatarUrl(raw.av||raw.avatar);if(av)p.av=av;"
        "if(raw.talents&&typeof raw.talents==='object'){for(const k of Object.keys(raw.talents).slice(0,12)){p.talents[k]=Math.max(0,parseInt(raw.talents[k],10)||0);}}"
        "if(raw.equip&&typeof raw.equip==='object'){for(const slot of Object.keys(raw.equip).slice(0,12)){const item=sanitizeChatEquipItem(raw.equip[slot]);if(item)p.equip[slot]=item;}}"
        "const st=raw.st||raw.stats||{};p.st={ca:parseInt(st.ca??st.createdAt,10)||0,pt:Math.max(0,parseInt(st.pt??st.totalPlaytime,10)||0),"
        "dc:Math.max(0,parseInt(st.dc??st.dungeonClears,10)||0),dk:Math.max(0,parseInt(st.dk??st.dungeonKills,10)||0)};return p;}"
        "function getChatMessageLevel(data){if(!data)return null;const lv=Number(data.level??data.profile?.lv??data.profile?.level);",
        "chat profile sanitize",
    ),
    (
        "content.innerHTML=profile?renderChatProfileHtml(profile):'<p class=\"chat-profile-empty\">'+escapeChatHtml(t('chatProfileUnavailable'))+'</p>';",
        "const safeProfile=profile?sanitizeChatProfile(profile):null;content.innerHTML=safeProfile?renderChatProfileHtml(safeProfile):'<p class=\"chat-profile-empty\">'+escapeChatHtml(t('chatProfileUnavailable'))+'</p>';",
        "showChatPlayerProfile sanitize",
    ),
    (
        "if(avatarDataUrl&&avatarDataUrl.length<30000)p.av=avatarDataUrl;return p;}",
        "return p;}",
        "drop avatar from chat snapshot",
    ),
    (
        "#chat-messages{flex:1;min-height:0;border-top:1px solid #111;border-bottom:1px solid #111}",
        "#chat-messages{flex:1;min-height:0;overflow-y:auto;padding:.5rem;border-top:1px solid #111;border-bottom:1px solid #111}",
        "merge chat-messages css 1",
    ),
    (
        "#chat-messages{flex:1;overflow-y:auto;padding:.5rem;min-height:0}",
        "",
        "merge chat-messages css 2",
    ),
    (
        "GAME_VERSION='2.5.5',GAME_VERSION_HISTORY=[{version:'2.5.5',date:'2025-06-07',summary:{zh:'聊天室顯示玩家等級；長按可檢視其他玩家個人頁面。',en:'Chat shows player level; long-press to view player profiles.'}},",
        "GAME_VERSION='2.5.6',GAME_VERSION_HISTORY=[{version:'2.5.6',date:'2025-06-07',summary:{zh:'修復聊天個人頁戰鬥屬性、安全性與桌面聊天連線等問題。',en:'Fix chat profile combat stats, security hardening, and desktop chat connect.'}},{version:'2.5.5',date:'2025-06-07',summary:{zh:'聊天室顯示玩家等級；長按可檢視其他玩家個人頁面。',en:'Chat shows player level; long-press to view player profiles.'}},",
        "version",
    ),
]

for old, new, label in replacements:
    if old not in html:
        raise SystemExit(f"Missing patch target: {label}")
    html = html.replace(old, new, 1)

Path("index.html").write_text(html)
print("Patched index.html")
