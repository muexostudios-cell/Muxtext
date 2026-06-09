#!/usr/bin/env python3
"""Patch index.html with expanded monsters and improved combat pixel art."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
content = (ROOT / 'index.html').read_text()
sprite_code = (ROOT / 'tools' / 'combat-sprite-draw.js').read_text().strip()

# --- MONSTER_POOL / BOSS_POOL ---
OLD_POOL = (
    'const MONSTER_POOL=[{hp:52,atk:14,def:5,spd:4,dodge:3,gold:10,xp:5},'
    '{hp:34,atk:20,def:2,spd:9,dodge:14,gold:12,xp:6},'
    '{hp:88,atk:8,def:10,spd:3,dodge:1,gold:8,xp:4},'
    '{hp:60,atk:16,def:4,spd:7,dodge:9,gold:14,xp:7},'
    '{hp:110,atk:24,def:12,spd:2,dodge:0,gold:20,xp:10},'
    '{hp:72,atk:18,def:7,spd:5,dodge:5,gold:18,xp:9}];'
    'const BOSS_POOL=[{hp:200,atk:32,def:10,spd:4,dodge:2,gold:50,xp:25},'
    '{hp:300,atk:42,def:14,spd:5,dodge:3,gold:80,xp:40},'
    '{hp:400,atk:52,def:18,spd:3,dodge:1,gold:120,xp:60}];'
)
NEW_POOL = (
    'const MONSTER_POOL=[{hp:52,atk:14,def:5,spd:4,dodge:3,gold:10,xp:5},'
    '{hp:34,atk:20,def:2,spd:9,dodge:14,gold:12,xp:6},'
    '{hp:88,atk:8,def:10,spd:3,dodge:1,gold:8,xp:4},'
    '{hp:60,atk:16,def:4,spd:7,dodge:9,gold:14,xp:7},'
    '{hp:110,atk:24,def:12,spd:2,dodge:0,gold:20,xp:10},'
    '{hp:72,atk:18,def:7,spd:5,dodge:5,gold:18,xp:9},'
    '{hp:48,atk:22,def:3,spd:8,dodge:6,gold:16,xp:8},'
    '{hp:95,atk:10,def:6,spd:4,dodge:2,gold:11,xp:5},'
    '{hp:40,atk:17,def:2,spd:11,dodge:12,gold:13,xp:7},'
    '{hp:65,atk:19,def:5,spd:6,dodge:4,gold:22,xp:11},'
    '{hp:80,atk:21,def:8,spd:5,dodge:7,gold:19,xp:9},'
    '{hp:58,atk:15,def:4,spd:6,dodge:8,gold:15,xp:8}];'
    'const BOSS_POOL=[{hp:200,atk:32,def:10,spd:4,dodge:2,gold:50,xp:25},'
    '{hp:300,atk:42,def:14,spd:5,dodge:3,gold:80,xp:40},'
    '{hp:400,atk:52,def:18,spd:3,dodge:1,gold:120,xp:60},'
    '{hp:350,atk:48,def:12,spd:4,dodge:2,gold:100,xp:50},'
    '{hp:280,atk:38,def:16,spd:6,dodge:4,gold:90,xp:45}];'
)
if OLD_POOL not in content:
    raise SystemExit('MONSTER_POOL anchor not found')
content = content.replace(OLD_POOL, NEW_POOL)

# --- Names zh ---
content = content.replace(
    'enemyNames:["廢鐵機械人","數據幽魂","變異老鼠","電磁蛇","守衛炮台","深淵魔眼"],bossNames:["地城守護者","深淵領主","機械巨龍"]',
    'enemyNames:["廢鐵機械人","數據幽魂","變異老鼠","電磁蛇","守衛炮台","深淵魔眼","賽博蠍王","酸液史萊姆","暗影蝙蝠","焰翼幼龍","幽靈騎士","腐化藤蔓"],bossNames:["地城守護者","深淵領主","機械飛龍","深淵九頭蛇","墮落熾天使"]',
)
content = content.replace(
    'enemyNames:["SCRAP_BOT","DATA_GHOST","MUTANT_RAT","VOLT_SNAKE","TURRET","VOID_EYE"],bossNames:["GUARDIAN","VOID_LORD","MECH_DRAGON"]',
    'enemyNames:["SCRAP_BOT","DATA_GHOST","MUTANT_RAT","VOLT_SNAKE","TURRET","VOID_EYE","CYBER_SCORP","ACID_SLIME","SHADOW_BAT","FLAME_WYRM","SPECTER_KNIGHT","BLIGHT_VINE"],bossNames:["GUARDIAN","VOID_LORD","MECH_WYRM","ABYSS_HYDRA","FALLEN_SERAPH"]',
)

# --- Combat upscale helpers (after PIXEL_ICON_SIZE) ---
anchor = 'const PIXEL_ICON_SIZE=16;let _pixelIconCache=new Map();'
insert = (
    'const PIXEL_ICON_SIZE=16;const COMBAT_PORTRAIT_SCALE=2;'
    'function gridToCombatDataUrl(grid){const S=PIXEL_ICON_SIZE,O=S*COMBAT_PORTRAIT_SCALE,c=document.createElement(\'canvas\');'
    'c.width=O;c.height=O;const ctx=c.getContext(\'2d\');ctx.imageSmoothingEnabled=false;'
    'const t=document.createElement(\'canvas\');t.width=S;t.height=S;const tc=t.getContext(\'2d\');'
    'const img=tc.createImageData(S,S);img.data.set(grid);tc.putImageData(img,0,0);ctx.drawImage(t,0,0,O,O);return c.toDataURL(\'image/png\');}'
    'function getCachedCombatIcon(key,drawFn){if(_pixelIconCache.has(key))return _pixelIconCache.get(key);'
    'const grid=makePixelGrid();drawFn(grid);if(_pixelIconCache.size>=_PIXEL_ICON_CACHE_MAX)_pixelIconCache.clear();'
    'const url=gridToCombatDataUrl(grid);_pixelIconCache.set(key,url);return url;}'
    'let _pixelIconCache=new Map();'
)
if anchor not in content:
    raise SystemExit('PIXEL_ICON_SIZE anchor not found')
content = content.replace(anchor, insert)

# --- Replace sprite drawing block ---
start = content.find('function drawCyberMobShape(')
end = content.find('function drawPlayerCombatPixels(')
if start < 0 or end < 0:
    raise SystemExit('sprite function block not found')

# Extract only drawing functions from sprite file (skip duplicate COMBAT helpers)
sprite_funcs = sprite_code
for skip in ['const COMBAT_PORTRAIT_SCALE=2;', 'function gridToCombatDataUrl', 'function getCachedCombatIcon']:
    idx = sprite_funcs.find(skip)
    if idx >= 0:
        # remove until next function or end
        nxt = sprite_funcs.find('function ', idx + 10)
        if skip.startswith('const'):
            nxt = sprite_funcs.find('function ', idx)
        sprite_funcs = sprite_funcs[:idx] + (sprite_funcs[nxt:] if nxt > 0 else '')

content = content[:start] + sprite_funcs + content[end:]

# --- getMonsterVisualKey cache bump ---
content = content.replace(
    "if(!enemy)return'mob|0|v3';const pi=enemy.poolIndex!=null?enemy.poolIndex:0;if(enemy.isBoss)return'boss|'+pi+'|v3';return'mob|'+pi+'|'+(enemy.elite?'e':'n')+'|v3';",
    "if(!enemy)return'mob|0|v5';const pi=enemy.poolIndex!=null?enemy.poolIndex:0;if(enemy.isBoss)return'boss|'+pi+'|v5';return'mob|'+pi+'|'+(enemy.elite?'e':'n')+'|v5';",
)

# --- Use combat cache for portraits ---
content = content.replace(
    'function getMonsterPixelIconUrl(enemy){return getCachedPixelIcon(getMonsterVisualKey(enemy),g=>drawMonsterPixels(g,enemy));}',
    'function getMonsterPixelIconUrl(enemy){return getCachedCombatIcon(getMonsterVisualKey(enemy),g=>drawMonsterPixels(g,enemy));}',
)
content = content.replace(
    'function getPlayerCombatPortraitUrl(){return getCachedPixelIcon(getPlayerCombatVisualKey(),drawPlayerCombatPixels);}',
    'function getPlayerCombatPortraitUrl(){return getCachedCombatIcon(getPlayerCombatVisualKey(),drawPlayerCombatPixels);}',
)
content = content.replace(
    "return'player|v1|empty';let k='player|v1|';",
    "return'player|v2|empty';let k='player|v2|';",
)

# --- Boss variant modulo 5 + CSS ---
content = content.replace(
    "bossVariant%3):''",
    "bossVariant%5):''",
)
content = content.replace(
    '.pixel-icon-wrap.rarity-boss.boss-variant-2 .boss-particle{background:#ffcc44;box-shadow:0 0 5px #ffaa00,0 0 10px rgba(255,170,0,.4)}',
    '.pixel-icon-wrap.rarity-boss.boss-variant-2 .boss-particle{background:#ffcc44;box-shadow:0 0 5px #ffaa00,0 0 10px rgba(255,170,0,.4)}'
    '.pixel-icon-wrap.rarity-boss.boss-variant-3 .boss-particle{background:#ff6644;box-shadow:0 0 5px #ff4422,0 0 10px rgba(255,68,34,.45)}'
    '.pixel-icon-wrap.rarity-boss.boss-variant-4 .boss-particle{background:#88ddff;box-shadow:0 0 5px #44ccff,0 0 10px rgba(68,204,255,.4)}',
)

# --- Larger combat portrait display ---
content = content.replace(
    'if(enemy.isBoss)return innerW;if(enemy.elite)return Math.floor(innerW*0.96);return Math.floor(innerW*0.92);',
    'if(enemy.isBoss)return innerW;if(enemy.elite)return Math.floor(innerW*0.98);return Math.floor(innerW*0.95);',
)

# --- Version bump ---
ver_m = re.search(r"GAME_VERSION='([0-9.]+)'", content)
if not ver_m:
    raise SystemExit('GAME_VERSION not found')
parts = ver_m.group(1).split('.')
parts[-1] = str(int(parts[-1]) + 1)
new_ver = '.'.join(parts)

content = re.sub(r'content="[0-9.]+"(?=[^>]*><title>)', f'content="{new_ver}"', content, count=1)
content = content.replace(f"GAME_VERSION='{ver_m.group(1)}'", f"GAME_VERSION='{new_ver}'")
content = re.sub(
    r"GAME_VERSION_HISTORY=\[\{version:'[0-9.]+'",
    f"GAME_VERSION_HISTORY=[{{version:'{new_ver}',date:'2026-06-09',summary:{{zh:'v{new_ver} 擴充 12 種怪物與 5 種頭目，重繪飛龍等精美像素戰鬥肖像（2× 解析度）。',en:'v{new_ver} 12 mob + 5 boss types, refined pixel portraits incl. dragons (2× res).'}}}},{{version:'{ver_m.group(1)}'",
    content,
    count=1,
)

# Changelog keys - derive from version
vkey = 'V' + new_ver.replace('.', '')
old_vkey = 'V' + ver_m.group(1).replace('.', '')
content = content.replace(
    f"logBalance{old_vkey}:",
    f"logBalance{vkey}:'[功能 v{new_ver}] 擴充 12 種地下城怪物與 5 種頭目；重繪飛龍等像素肖像並提升戰鬥解析度。',logBalance{old_vkey}:",
    1,
)
# EN changelog - find first logBalance in en section after logBalanceV22415 pattern
en_pat = f'logBalance{old_vkey}:"'
if en_pat in content:
    content = content.replace(
        en_pat,
        f'logBalance{vkey}:"[Feature v{new_ver}] 12 dungeon mobs + 5 bosses; refined dragon pixel portraits at 2× combat resolution.",{en_pat}',
        1,
    )

(ROOT / 'index.html').write_text(content)
(ROOT / 'version.json').write_text(
    '{\n  "version": "' + new_ver + '",\n  "updated": "2026-06-09"\n}\n'
)
print(f'Patched to v{new_ver}')
