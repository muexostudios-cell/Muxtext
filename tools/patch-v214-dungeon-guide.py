#!/usr/bin/env python3
"""Apply v2.14.0 in-dungeon guide overlay with ! button beside daily curse."""
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "index.html"
s = path.read_text()


def rep(old, new, label, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f"[{label}] expected {count}, got {n}\n{old[:280]}")
    s = s.replace(old, new, 1)


# --- version ---
rep("GAME_VERSION='2.13.0'", "GAME_VERSION='2.14.0'", "ver")
rep(
    "GAME_VERSION_HISTORY=[{version:'2.13.0'",
    "GAME_VERSION_HISTORY=[{version:'2.14.0',date:'2026-06-08',summary:{zh:'v2.14 地城教學：今日詛咒旁！按鈕可查看設定與攻略。',en:'v2.14 dungeon guide: tap ! beside daily curse for settings and tips.'}},{version:'2.13.0'",
    "hist",
)

# --- CSS ---
rep(
    "#tutorial-overlay,#leaderboard-overlay{",
    "#tutorial-overlay,#leaderboard-overlay,#dungeon-guide-overlay{",
    "css overlay",
)
rep(
    "#version-history-panel,#version-update-box,#tutorial-panel,#leaderboard-panel{",
    "#version-history-panel,#version-update-box,#tutorial-panel,#leaderboard-panel,#dungeon-guide-panel{",
    "css panel",
)
rep(
    "#version-history-panel h3,#version-update-box h3,#tutorial-panel h3,#leaderboard-panel h3{",
    "#version-history-panel h3,#version-update-box h3,#tutorial-panel h3,#leaderboard-panel h3,#dungeon-guide-panel h3{",
    "css panel h3",
)
rep(
    "#version-history-list,#tutorial-content,#leaderboard-list{",
    "#version-history-list,#tutorial-content,#leaderboard-list,#dungeon-guide-content{",
    "css content scroll",
)
rep(
    "#btn-close-tutorial,#btn-close-leaderboard{",
    "#btn-close-tutorial,#btn-close-leaderboard,#btn-close-dungeon-guide{",
    "css close btn",
)
rep(
    ".tutorial-section p:last-child{margin-bottom:0}",
    ".tutorial-section p:last-child{margin-bottom:0}.dungeon-curse-row{display:flex;align-items:center;gap:.3rem;width:100%}.dungeon-curse-text{flex:1;color:var(--decay);font-size:.55rem;line-height:1.35}.btn-dungeon-guide{flex-shrink:0;width:1.35rem;height:1.35rem;padding:0;border:1px solid #555;border-radius:50%;background:#111;color:#ffcc00;font-family:inherit;font-size:.7rem;font-weight:700;line-height:1;cursor:pointer;-webkit-tap-highlight-color:transparent}.btn-dungeon-guide:active{border-color:#ffcc00;color:#fff;background:#222}#dungeon-curse-bar{padding:.35rem .5rem .2rem;border-bottom:1px solid #1a1a1a}#dungeon-run-header{display:flex;align-items:flex-start;gap:.25rem;width:100%;max-width:320px;margin:0 auto}#dungeon-run-header .dungeon-curse-row{flex:1}",
    "css curse row",
)
rep(
    "dungeon-run-banner{font-size:0.55rem;color:#aaa;padding:0.2rem 0.35rem 0.35rem;text-align:center;line-height:1.35;width:100%;display:none}",
    "dungeon-run-banner{font-size:0.55rem;color:#aaa;padding:0 0.35rem 0.35rem;text-align:center;line-height:1.35;flex:1;display:none}",
    "css banner",
)

# --- HTML ---
rep(
    '<div id="tutorial-overlay"><div id="tutorial-panel"><h3 id="tutorial-title">新手教學</h3><div id="tutorial-content"></div><button id="btn-close-tutorial">關閉</button></div></div>',
    '<div id="tutorial-overlay"><div id="tutorial-panel"><h3 id="tutorial-title">新手教學</h3><div id="tutorial-content"></div><button id="btn-close-tutorial">關閉</button></div></div><div id="dungeon-guide-overlay"><div id="dungeon-guide-panel"><h3 id="dungeon-guide-title">地城教學</h3><div id="dungeon-guide-content"></div><button id="btn-close-dungeon-guide">關閉</button></div></div>',
    "html guide overlay",
)
rep(
    '<div id="dungeon-adventure"><h3 id="dungeon-title">地城</h3><div id="dungeon-list"></div>',
    '<div id="dungeon-adventure"><h3 id="dungeon-title">地城</h3><div id="dungeon-curse-bar"></div><div id="dungeon-list"></div>',
    "html curse bar",
)
rep(
    '<div id="map-container"><div id="dungeon-run-banner"></div><div id="map"></div></div>',
    '<div id="map-container"><div id="dungeon-run-header"><div id="dungeon-run-banner"></div></div><div id="map"></div></div>',
    "html run header",
)

# --- i18n zh ---
rep(
    'dailyCursePreview:"今日詛咒地城: {0}",curseBleed:"裂血"',
    'dungeonGuideTitle:"地城教學",dungeonGuideBtn:"地城設定與攻略",dungeonGuideModTitle:"隨機詞綴一覽",dungeonGuideCurseTitle:"每日詛咒一覽",dungeonGuideLayoutTitle:"地圖布局",curseBleedDesc:"敵人攻擊+20% · 入場生命92% · 掉落+22%",curseAbyssDesc:"敵人生命+25% · 防禦+15% · 經驗+25%",curseHollowDesc:"閃避×72% · 金幣+30%",curseRuinDesc:"入場記憶崩壞+1.5% · 掉落+35%",curseWitherDesc:"敵人速度+20% · 入場生命90% · 金幣+22%",curseDreadDesc:"敵人攻擊+18% · 速度+12% · 經驗+22%",curseEclipseDesc:"敵人生命/攻擊/防禦強化 · 掉落+28%",layoutOpenDesc:"怪物與事件分散，路線選擇較自由",layoutDenseDesc:"牆壁較多、通道狹窄，容易被迫進戰",layoutHunterDesc:"精英怪出現率提高，風險與獎勵並存",layoutScatterDesc:"寶箱與聖壇較多，適合資源取向",dailyCursePreview:"今日詛咒地城: {0}",curseBleed:"裂血"',
    "i18n zh keys",
)

# --- i18n en ---
rep(
    'dailyCursePreview:"Today\'s cursed dungeon: {0}",curseBleed:"Bleed"',
    'dungeonGuideTitle:"Dungeon Guide",dungeonGuideBtn:"Dungeon settings & tips",dungeonGuideModTitle:"Random modifiers",dungeonGuideCurseTitle:"Daily curses",dungeonGuideLayoutTitle:"Map layouts",curseBleedDesc:"Enemy ATK +20% · Entry HP 92% · Drops +22%",curseAbyssDesc:"Enemy HP +25% · DEF +15% · XP +25%",curseHollowDesc:"Dodge ×72% · Gold +30%",curseRuinDesc:"Entry decay +1.5% · Drops +35%",curseWitherDesc:"Enemy SPD +20% · Entry HP 90% · Gold +22%",curseDreadDesc:"Enemy ATK +18% · SPD +12% · XP +22%",curseEclipseDesc:"Enemy HP/ATK/DEF buffed · Drops +28%",layoutOpenDesc:"Open paths; flexible routing",layoutDenseDesc:"Tight corridors; more forced fights",layoutHunterDesc:"Higher elite spawn rate",layoutScatterDesc:"More chests and shrines",dailyCursePreview:"Today\'s cursed dungeon: {0}",curseBleed:"Bleed"',
    "i18n en keys",
)

# --- guide sections (after TUTORIAL_SECTIONS closing) ---
GUIDE_SECTIONS = r"""const DUNGEON_GUIDE_SECTIONS=[{title:{zh:'一、進度與解鎖',en:'1. Progression & Unlocks'},paragraphs:{zh:['每段地城對應 3 個等級（如 Lv.1-3、Lv.4-6）。','須通關該段普通與困難頭目，才能解鎖下一段。','角色等級不可高於地城上限太多（約 ±5 級），否則無法進入。','地獄難度需消耗地獄門禁卡 #，獎勵最高但敵人極硬。'],en:['Each tier spans 3 levels (e.g. Lv.1-3, Lv.4-6).','Clear both Normal and Hard bosses to unlock the next tier.','Your level must be within ~5 of the tier cap or entry is blocked.','Hell costs a Hell Ticket #; best rewards but brutal enemies.']}},{title:{zh:'二、難度設定',en:'2. Difficulty Tiers'},paragraphs:{zh:['普通 x1.0：基準難度，適等級約一趟升 1 級。','困難 x1.8：敵人更硬，金幣與掉落更好。','地獄 x3.0：高防高閃避，建議暴擊/全傷害詞綴；通關記憶崩壞減免最多。','每趟通關擊敗王可獲額外經驗（約升級需求的 5–6%）。'],en:['Normal x1.0: baseline; ~1 level per clear at matching tier.','Hard x1.8: tougher foes, better gold and drops.','Hell x3.0: high DEF/dodge; crit/all-dmg builds help; best decay relief on clear.','Boss kill grants bonus XP (~5–6% of level requirement).']}},{title:{zh:'三、每趟隨機要素',en:'3. Per-Run Randomness'},paragraphs:{zh:['普通隨 1 個詞綴、困難 2 個、地獄 3 個，外加全服每日詛咒。','布局四選一：開闊 / 密集 / 獵殺 / 分散（見下方列表）。','地圖含怪物格、頭目格、寶箱、聖壇、陷阱與精英怪（約 12%）。','入場前在難度畫面可預覽今日詛咒；進場後地圖上方也會顯示。'],en:['Normal rolls 1 modifier, Hard 2, Hell 3, plus the global daily curse.','One of four layouts (listed below).','Map has mobs, boss, chests, shrines, traps, and ~12% elites.','Preview the daily curse before entry; it also shows above the map in-run.']}},{title:{zh:'四、記憶崩壞',en:'4. Memory Decay'},paragraphs:{zh:['死亡與部分事件會累積記憶崩壞，削弱角色屬性；100% 永久刪角。','通關可緩解：普通 -2%、困難 -5%、地獄 -8%；帶今日詛咒通關再 -2%。','詛咒「崩壞」會在入場額外 +1.5% 崩壞。','戰鬥中崩壞加成有上限；聖壇可小幅降低崩壞。'],en:['Death and some events raise Memory Decay, weakening stats; 100% deletes the character.','Clear relief: Normal -2%, Hard -5%, Hell -8%; daily curse clear adds -2%.','Ruin curse adds +1.5% decay on entry.','Combat decay bonus is capped; shrines can slightly reduce decay.']}},{title:{zh:'五、經驗與刷圖',en:'5. XP & Farming'},paragraphs:{zh:['適等級地城一趟約可升 1 級；刷低層經驗會被等級差懲罰。','同日同地城第 3 趟起：金幣 ×82%、經驗 ×90%（疲勞機制）。','困難/地獄有更高經驗倍率，但戰鬥風險同步上升。','優先挑戰與自身等級相符的段落，效率最高。'],en:['Matching tier gives ~1 level per run; overleveling low tiers penalizes XP.','3+ runs of the same dungeon per day: gold ×82%, XP ×90% (fatigue).','Hard/Hell have higher XP multipliers but much higher risk.','Farm tiers close to your level for best efficiency.']}},{title:{zh:'六、戰鬥攻略',en:'6. Combat Tips'},paragraphs:{zh:['7×7 地圖：點相鄰格移動；遇敵進入回合制戰鬥。','速度影響出手頻率；主手/副手輪流攻擊，注意攻擊冷卻。','敵人閃避隨樓層成長，暴擊與全傷害詞綴後期很重要。','擊敗王後可選離開或繼續探索；血量不足時果斷撤退。','自動喝藥可在設定中調整；地城內快捷按鈕會隱藏。'],en:['7×7 map: tap adjacent cells; combat is turn-based.','Speed affects turn rate; alternate main/off attacks; mind cooldowns.','Enemy dodge scales with floor; crit and all-dmg matter late game.','After the boss you may leave or keep exploring; retreat if low on HP.','Auto-herb in settings; quick buttons hide inside dungeons.']}}];"""

rep(
    "];function getTutorialField(obj){return obj[currentLang]||obj.zh;}",
    "];" + GUIDE_SECTIONS + "function getTutorialField(obj){return obj[currentLang]||obj.zh;}",
    "guide sections",
)

# --- guide functions (after renderTutorialContent) ---
rep(
    "function openTutorialOverlay(){renderTutorialContent();const ol=document.getElementById('tutorial-overlay');if(ol)ol.style.display='flex';}",
    "function openTutorialOverlay(){renderTutorialContent();const ol=document.getElementById('tutorial-overlay');if(ol)ol.style.display='flex';}function createDungeonGuideBtn(){const btn=document.createElement('button');btn.type='button';btn.className='btn-dungeon-guide';btn.textContent='!';btn.title=t('dungeonGuideBtn');btn.setAttribute('aria-label',t('dungeonGuideBtn'));btn.addEventListener('click',e=>{e.stopPropagation();openDungeonGuideOverlay();});return btn;}function buildDungeonCurseRow(text){const row=document.createElement('div');row.className='dungeon-curse-row';const span=document.createElement('span');span.className='dungeon-curse-text';span.textContent=text;row.appendChild(span);row.appendChild(createDungeonGuideBtn());return row;}function getCurseDescKey(labelKey){return labelKey+'Desc';}function renderDungeonGuideContent(){const list=document.getElementById('dungeon-guide-content');if(!list)return;list.innerHTML='';DUNGEON_GUIDE_SECTIONS.forEach(sec=>{const div=document.createElement('div');div.className='tutorial-section';const title=document.createElement('h4');title.textContent=getTutorialField(sec.title);div.appendChild(title);getTutorialField(sec.paragraphs).forEach(text=>{const p=document.createElement('p');p.textContent=text;div.appendChild(p);});list.appendChild(div);});const layoutDiv=document.createElement('div');layoutDiv.className='tutorial-section';const layoutTitle=document.createElement('h4');layoutTitle.textContent=t('dungeonGuideLayoutTitle');layoutDiv.appendChild(layoutTitle);DUNGEON_LAYOUTS.forEach(lay=>{const k='layout'+lay.charAt(0).toUpperCase()+lay.slice(1);const p=document.createElement('p');p.textContent=t(k)+' — '+t(k+'Desc');layoutDiv.appendChild(p);});list.appendChild(layoutDiv);const modDiv=document.createElement('div');modDiv.className='tutorial-section';const modTitle=document.createElement('h4');modTitle.textContent=t('dungeonGuideModTitle');modDiv.appendChild(modTitle);DUNGEON_MODIFIERS.forEach(mod=>{const p=document.createElement('p');p.textContent=t(mod.labelKey)+' — '+t(mod.descKey);modDiv.appendChild(p);});list.appendChild(modDiv);const curseDiv=document.createElement('div');curseDiv.className='tutorial-section';const curseTitle=document.createElement('h4');curseTitle.textContent=t('dungeonGuideCurseTitle');curseDiv.appendChild(curseTitle);const today=t('dailyCursePreview',getDailyCurseLabel());const todayP=document.createElement('p');todayP.style.color='var(--decay)';todayP.textContent='☠ '+today;curseDiv.appendChild(todayP);DAILY_CURSES.forEach(curse=>{const p=document.createElement('p');const dk=getCurseDescKey(curse.labelKey);p.textContent=t(curse.labelKey)+(t(dk)?' — '+t(dk):'');curseDiv.appendChild(p);});list.appendChild(curseDiv);}function openDungeonGuideOverlay(){renderDungeonGuideContent();const ol=document.getElementById('dungeon-guide-overlay');if(ol)ol.style.display='flex';}function closeDungeonGuideOverlay(){const ol=document.getElementById('dungeon-guide-overlay');if(ol)ol.style.display='none';}function renderDungeonCurseBar(){const bar=document.getElementById('dungeon-curse-bar');if(!bar)return;bar.innerHTML='';bar.appendChild(buildDungeonCurseRow(t('dailyCursePreview',getDailyCurseLabel())));}",
    "guide funcs",
)

# --- applyLanguage ---
rep(
    "const _bct=document.getElementById('btn-close-tutorial');if(_bct)_bct.textContent=t('btnClose');",
    "const _bct=document.getElementById('btn-close-tutorial');if(_bct)_bct.textContent=t('btnClose');const _dgt=document.getElementById('dungeon-guide-title');if(_dgt)_dgt.textContent=t('dungeonGuideTitle');const _bcdg=document.getElementById('btn-close-dungeon-guide');if(_bcdg)_bcdg.textContent=t('btnClose');",
    "apply lang",
)

# --- event listeners (setupTutorialUI) ---
rep(
    "function setupTutorialUI(){const btn=document.getElementById('btn-tutorial');if(btn)btn.addEventListener('click',openTutorialOverlay);const btnClose=document.getElementById('btn-close-tutorial');if(btnClose)btnClose.addEventListener('click',closeTutorialOverlay);const ol=document.getElementById('tutorial-overlay');if(ol)ol.addEventListener('click',e=>{if(e.target===ol)closeTutorialOverlay();});}",
    "function setupTutorialUI(){const btn=document.getElementById('btn-tutorial');if(btn)btn.addEventListener('click',openTutorialOverlay);const btnClose=document.getElementById('btn-close-tutorial');if(btnClose)btnClose.addEventListener('click',closeTutorialOverlay);const ol=document.getElementById('tutorial-overlay');if(ol)ol.addEventListener('click',e=>{if(e.target===ol)closeTutorialOverlay();});const dgClose=document.getElementById('btn-close-dungeon-guide');if(dgClose)dgClose.addEventListener('click',closeDungeonGuideOverlay);const dgOl=document.getElementById('dungeon-guide-overlay');if(dgOl)dgOl.addEventListener('click',e=>{if(e.target===dgOl)closeDungeonGuideOverlay();});}",
    "setup ui",
)

# --- lang switch re-render guide ---
rep(
    "if(document.getElementById('tutorial-overlay')?.style.display==='flex')renderTutorialContent();});document.getElementById('lang-en')",
    "if(document.getElementById('tutorial-overlay')?.style.display==='flex')renderTutorialContent();if(document.getElementById('dungeon-guide-overlay')?.style.display==='flex')renderDungeonGuideContent();});document.getElementById('lang-en')",
    "lang zh guide",
)
rep(
    "if(document.getElementById('tutorial-overlay')?.style.display==='flex')renderTutorialContent();});const ACCOUNTS_KEY=",
    "if(document.getElementById('tutorial-overlay')?.style.display==='flex')renderTutorialContent();if(document.getElementById('dungeon-guide-overlay')?.style.display==='flex')renderDungeonGuideContent();});const ACCOUNTS_KEY=",
    "lang en guide",
)

# --- renderDungeonAdventure ---
rep(
    "function renderDungeonAdventure(resetPage=true){dungeonList.innerHTML='';",
    "function renderDungeonAdventure(resetPage=true){renderDungeonCurseBar();dungeonList.innerHTML='';",
    "render curse bar",
)

# --- showDifficultySelection ---
rep(
    '<div style="color:var(--decay);font-size:0.55rem;margin-top:0.3rem;">${t(\'dailyCursePreview\',getDailyCurseLabel())}</div>`;diffList.innerHTML=\'\';',
    "`;diffInfo.appendChild(buildDungeonCurseRow(t('dailyCursePreview',getDailyCurseLabel())));diffList.innerHTML='';",
    "difficulty curse row",
)

# --- updateDungeonRunBanner ---
rep(
    "function updateDungeonRunBanner(){const el=document.getElementById('dungeon-run-banner');if(!el)return;if(!inDungeon||!currentDungeon){el.textContent='';el.style.display='none';return;}const layout=formatDungeonLayoutLabel(),mods=formatDungeonModifierList();el.textContent=mods?(layout+' · '+mods):layout;el.classList.toggle('cursed-run',hasActiveDailyCurse());el.style.display='block';}",
    "function updateDungeonRunBanner(){const header=document.getElementById('dungeon-run-header');const el=document.getElementById('dungeon-run-banner');if(!header||!el)return;if(!inDungeon||!currentDungeon){header.innerHTML='<div id=\"dungeon-run-banner\"></div>';return;}const curse=currentDungeon.modifiers&&currentDungeon.modifiers.find(m=>m.isCurse);const curseText=curse?t('dailyCurseTag',t(curse.labelKey)):t('dailyCursePreview',getDailyCurseLabel());const layout=formatDungeonLayoutLabel();const rest=currentDungeon.modifiers?currentDungeon.modifiers.filter(m=>!m.isCurse).map(m=>t(m.labelKey)).join(' · '):'';const detail=rest?(layout+' · '+rest):layout;header.innerHTML='';const curseRow=buildDungeonCurseRow(curseText);if(hasActiveDailyCurse())curseRow.classList.add('cursed-run');header.appendChild(curseRow);const banner=document.createElement('div');banner.id='dungeon-run-banner';banner.textContent=detail;banner.style.display=detail?'block':'none';header.appendChild(banner);}",
    "run banner",
)

path.write_text(s)
print("v2.14.0 dungeon guide patch OK")
