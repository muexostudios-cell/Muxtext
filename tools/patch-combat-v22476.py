#!/usr/bin/env python3
"""Apply v2.24.76 combat UI fix patches to index.html."""
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "index.html"
html = path.read_text(encoding="utf-8")

replacements = [
    ('content="2.24.75"', 'content="2.24.76"'),
    (
        "#battle-screen{display:none;flex-direction:column;padding:.5rem;border-bottom:1px solid #1a1a1a;flex-shrink:0;min-height:0;max-height:58dvh;overflow-y:auto}",
        "#battle-screen{display:none;flex-direction:column;padding:.5rem;border-bottom:1px solid #1a1a1a;flex-shrink:0;min-height:0;max-height:44dvh;overflow-y:auto}",
    ),
    (
        "#game-main.combat-layout #battle-screen{order:2;flex-shrink:0}",
        "#game-main.combat-layout #battle-screen{order:2;flex-shrink:0;min-height:0}#game.desktop-layout #game-main.combat-layout #battle-screen.active{max-height:50dvh}",
    ),
    (
        "#game-main.combat-layout #log-panel.log-visible{order:3;flex:1;min-height:0;display:flex!important;flex-direction:column;border-bottom:1px solid #1a1a1a}",
        "#game-main.combat-layout #log-panel.log-visible{order:4;flex:1;min-height:0;max-height:26dvh;display:flex!important;flex-direction:column;border-bottom:1px solid #1a1a1a}",
    ),
    (
        "#game-main.combat-layout #combat-dock{order:4}",
        "#game-main.combat-layout #combat-dock{order:3;flex-shrink:0;z-index:2;background:#000}",
    ),
    (
        "#game-main.combat-layout #tab-bar{order:5;border-top:1px solid #1a1a1a}",
        "#game-main.combat-layout #tab-bar{order:5;flex-shrink:0;border-top:1px solid #1a1a1a}",
    ),
    (
        "#game-main.combat-layout #action-bar{order:6;border-top:1px solid #1a1a1a}",
        "#game-main.combat-layout #action-bar{order:6;flex-shrink:0;border-top:1px solid #1a1a1a}",
    ),
    (
        "function getMonsterCombatPortraitSize(enemy,cardEl){const card=cardEl||document.getElementById('enemy-card')||document.getElementById('player-card');let cardW=card?card.clientWidth:0;if(cardW<=0&&card)cardW=card.getBoundingClientRect().width|0;if(cardW<=0){const battle=document.getElementById('battle-screen');if(battle&&battle.clientWidth>0)cardW=Math.floor(battle.clientWidth/2);}if(cardW<=0)cardW=180;const innerW=Math.max(56,Math.min(96,Math.floor(cardW*0.48)));if(!enemy)return innerW;if(enemy.isBoss)return Math.min(104,Math.floor(innerW*1.1));if(enemy.elite)return Math.floor(innerW*0.98);return Math.floor(innerW*0.92);}",
        "function getMonsterCombatPortraitSize(enemy,cardEl){const card=cardEl||document.getElementById('enemy-card')||document.getElementById('player-card');let cardW=card?card.clientWidth:0;if(cardW<=0&&card)cardW=card.getBoundingClientRect().width|0;if(cardW<=0){const battle=document.getElementById('battle-screen');if(battle&&battle.clientWidth>0)cardW=Math.floor((battle.clientWidth-16)/2);}if(cardW<=0)cardW=typeof isDesktopLayout==='function'&&isDesktopLayout()?170:150;const innerW=Math.max(52,Math.min(80,Math.floor(cardW*0.44)));if(!enemy)return innerW;if(enemy.isBoss)return Math.min(88,Math.floor(innerW*1.08));if(enemy.elite)return Math.floor(innerW*0.96);return Math.floor(innerW*0.92);}",
    ),
    (
        "function getPlayerCombatPortraitHtml(size){const px=size||getMonsterCombatPortraitSize(currentEnemy);const rarity=getPlayerPortraitSparkRarity();return pixelIconImgHtml(getPlayerCombatPortraitUrl(),px,' pixel-player',rarity||'');}",
        "function getPlayerCombatPortraitHtml(size){const px=size||getMonsterCombatPortraitSize(currentEnemy,document.getElementById('player-card'));const rarity=getPlayerPortraitSparkRarity();const inner=pixelIconImgHtml(getPlayerCombatPortraitUrl(),px,' pixel-player',rarity||'');if(inner.includes('pixel-icon-wrap'))return inner;return '<span class=\"pixel-icon-wrap combat-portrait-wrap\" style=\"width:'+px+'px;height:'+px+'px\">'+inner+'</span>';}",
    ),
    (
        "function updateCombatLayout(){const main=document.getElementById('game-main');if(!main)return;const on=!!(inCombat&&currentEnemy);main.classList.toggle('combat-layout',on);if(on)setLogVisible(true);updateLogOverlayBounds();updateHomeViewState();}",
        "function updateCombatLayout(){const main=document.getElementById('game-main');if(!main)return;const on=!!(inCombat&&currentEnemy);main.classList.toggle('combat-layout',on);if(on)setLogVisible(true);updateLogOverlayBounds();updateHomeViewState();if(on)requestAnimationFrame(()=>{updateBattleUI({full:true});updateButtons();});}",
    ),
    (
        "const portraitPx=getMonsterCombatPortraitSize(currentEnemy,enemyCard);syncCombatPortraitStage('player-portrait',portraitPx);syncCombatPortraitStage('enemy-portrait',portraitPx);const playerPortrait=document.getElementById('player-portrait');if(playerPortrait)playerPortrait.innerHTML=getPlayerCombatPortraitHtml(portraitPx);const enemyPortrait=document.getElementById('enemy-portrait');if(enemyPortrait)enemyPortrait.innerHTML=getMonsterPixelIconHtml(currentEnemy,portraitPx);",
        "const playerCard=document.getElementById('player-card');const playerPx=getMonsterCombatPortraitSize(currentEnemy,playerCard||enemyCard);const enemyPx=getMonsterCombatPortraitSize(currentEnemy,enemyCard);syncCombatPortraitStage('player-portrait',playerPx);syncCombatPortraitStage('enemy-portrait',enemyPx);const playerPortrait=document.getElementById('player-portrait');if(playerPortrait)playerPortrait.innerHTML=getPlayerCombatPortraitHtml(playerPx);const enemyPortrait=document.getElementById('enemy-portrait');if(enemyPortrait)enemyPortrait.innerHTML=getMonsterPixelIconHtml(currentEnemy,enemyPx);",
    ),
    ("GAME_VERSION='2.24.75'", "GAME_VERSION='2.24.76'"),
    (
        "GAME_VERSION_HISTORY=[{version:'2.24.75',date:'2026-06-09',summary:{zh:'v2.24.75 修復戰鬥介面異常與武器攻擊按鈕消失（桌面 combat-layout、肖像尺寸）。',en:'v2.24.75 fix combat UI glitches and missing weapon attack buttons.'}},",
        "GAME_VERSION_HISTORY=[{version:'2.24.76',date:'2026-06-09',summary:{zh:'v2.24.76 戰鬥佈局：攻擊列置於日誌上方、限制戰鬥區高度、修正肖像尺寸。',en:'v2.24.76 combat layout: attack bar above log, battle height cap, portrait fix.'}},{version:'2.24.75',date:'2026-06-09',summary:{zh:'v2.24.75 修復戰鬥介面異常與武器攻擊按鈕消失（桌面 combat-layout、肖像尺寸）。',en:'v2.24.75 fix combat UI glitches and missing weapon attack buttons.'}},",
    ),
    (
        "logBalanceV22475:'[修復 v2.24.75] 戰鬥介面異常與武器攻擊按鈕消失：桌面啟用 combat-layout、限制肖像尺寸。',",
        "logBalanceV22476:'[修復 v2.24.76] 戰鬥佈局：攻擊列置於日誌上方、限制戰鬥區高度、修正雙側肖像尺寸。',logBalanceV22475:'[修復 v2.24.75] 戰鬥介面異常與武器攻擊按鈕消失：桌面啟用 combat-layout、限制肖像尺寸。',",
    ),
    (
        'logBalanceV22475:"[Fix v2.24.75] Combat UI glitches and missing weapon attack buttons."',
        'logBalanceV22476:"[Fix v2.24.76] Combat layout: attack bar above log, battle height cap, portrait sizing fix.",logBalanceV22475:"[Fix v2.24.75] Combat UI glitches and missing weapon attack buttons."',
    ),
]

for old, new in replacements:
    if old not in html:
        raise SystemExit(f"Missing patch anchor:\n{old[:120]}...")
    html = html.replace(old, new, 1)

path.write_text(html, encoding="utf-8")
print("Patched index.html for v2.24.76")
