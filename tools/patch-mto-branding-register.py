#!/usr/bin/env python3
"""MTO branding, player name label, register name confirmation."""
from pathlib import Path

path = Path('/workspace/index.html')
c = path.read_text(encoding='utf-8')

replacements = [
    # HTML defaults
    (
        '<p id="loading-text">夜之城加載中…</p>',
        "<p id=\"loading-text\">MTO 'MUX TEXT ONLINE' 加載中…</p>",
    ),
    (
        '<h3 id="account-title">夜之城帳號</h3>',
        "<h3 id=\"account-title\">MTO 'MUX TEXT ONLINE' 帳號</h3>",
    ),
    (
        '<label id="label-account-display">遊戲代號</label>',
        '<label id="label-account-display">玩家名字</label>',
    ),
    # LANG zh
    (
        'accountTitle:"夜之城帳號"',
        "accountTitle:\"MTO 'MUX TEXT ONLINE' 帳號\"",
    ),
    (
        'loadingText:"夜之城加載中…"',
        "loadingText:\"MTO 'MUX TEXT ONLINE' 加載中…\"",
    ),
    (
        'labelAccountDisplay:"遊戲代號"',
        'labelAccountDisplay:"玩家名字",registerNameConfirm:"玩家可享有一次免費改名次數。<br>如日後想進行改名，須在遊戲中購買改名卡進行改名。<br><br>玩家名字：<b>{0}</b><br><br>是否確認當前名字並開始遊戲？",registerConfirmStart:"確認開始",registerThinkAgain:"再想想"',
    ),
    # LANG en
    (
        'accountTitle:"Night City Account"',
        "accountTitle:\"MTO 'MUX TEXT ONLINE' Account\"",
    ),
    (
        'loadingText:"Night City loading..."',
        "loadingText:\"MTO 'MUX TEXT ONLINE' loading...\"",
    ),
    (
        'labelAccountDisplay:"CODENAME"',
        'labelAccountDisplay:"Player Name",registerNameConfirm:"You get one free rename.<br>To change your name later, purchase a rename card in-game.<br><br>Player name: <b>{0}</b><br><br>Confirm this name and start?",registerConfirmStart:"CONFIRM START",registerThinkAgain:"THINK AGAIN"',
    ),
    # showConfirm with custom labels
    (
        'let pendingConfirmCallback=null,pendingDroneCallback=null;function showConfirm(msg,callback){confirmMsg.innerHTML=msg;pendingConfirmCallback=callback;pendingDroneCallback=null;confirmYes.style.display=\'block\';confirmNo.style.display=\'block\';confirmDrone.style.display=\'none\';confirmOverlay.style.display=\'flex\';}',
        "let pendingConfirmCallback=null,pendingDroneCallback=null;function resetConfirmButtons(){confirmYes.textContent=t('confirmYes');confirmNo.textContent=t('confirmNo');}function showConfirm(msg,callback,btnLabels){confirmMsg.innerHTML=msg;pendingConfirmCallback=callback;pendingDroneCallback=null;confirmYes.style.display='block';confirmNo.style.display='block';confirmDrone.style.display='none';if(btnLabels){if(btnLabels.yes)confirmYes.textContent=btnLabels.yes;if(btnLabels.no)confirmNo.textContent=btnLabels.no;}else{resetConfirmButtons();}confirmOverlay.style.display='flex';}",
    ),
    (
        "confirmYes.addEventListener('click',()=>{confirmOverlay.style.display='none';if(pendingConfirmCallback)pendingConfirmCallback();pendingConfirmCallback=null;pendingDroneCallback=null;});confirmNo.addEventListener('click',()=>{confirmOverlay.style.display='none';pendingConfirmCallback=null;pendingDroneCallback=null;});",
        "confirmYes.addEventListener('click',()=>{confirmOverlay.style.display='none';if(pendingConfirmCallback)pendingConfirmCallback();pendingConfirmCallback=null;pendingDroneCallback=null;resetConfirmButtons();});confirmNo.addEventListener('click',()=>{confirmOverlay.style.display='none';pendingConfirmCallback=null;pendingDroneCallback=null;resetConfirmButtons();});",
    ),
    (
        "confirmOverlay.addEventListener('click',e=>{if(e.target===confirmOverlay){confirmOverlay.style.display='none';pendingConfirmCallback=null;pendingDroneCallback=null;",
        "confirmOverlay.addEventListener('click',e=>{if(e.target===confirmOverlay){confirmOverlay.style.display='none';pendingConfirmCallback=null;pendingDroneCallback=null;resetConfirmButtons();",
    ),
    # handleAccountSubmit register confirmation
    (
        "async function handleAccountSubmit(){if(accountSubmitting)return;clearAccountError();const username=document.getElementById('account-username').value.trim();const password=document.getElementById('account-password').value;const confirmPw=document.getElementById('account-password-confirm').value;const displayName=document.getElementById('account-display-input').value.trim();if(!username||!password||(accountMode==='register'&&(!displayName||!confirmPw))){showAccountError(t('accountErrorEmpty'));return;}setAccountSubmitting(true);try{if(!(await ensureGunRelayReady(10000))){showAccountError(t('cloudSyncRelayBlocked'));return;}if(accountMode==='register'){if(password!==confirmPw){showAccountError(t('accountErrorPasswordMatch'));return;}const res=await registerAccount(username,password,displayName);if(!res.ok){showAccountError(t(res.msg));return;}beginGameAfterAccount(false);return;}const res=await loginAccount(username,password);if(!res.ok){showAccountError(t(res.msg));return;}beginGameAfterAccount(!!res.pulled);}finally{setAccountSubmitting(false);}}",
        "async function proceedWithRegistration(username,password,displayName){setAccountSubmitting(true);try{if(!(await ensureGunRelayReady(10000))){showAccountError(t('cloudSyncRelayBlocked'));return;}const res=await registerAccount(username,password,displayName);if(!res.ok){showAccountError(t(res.msg));return;}beginGameAfterAccount(false);}finally{setAccountSubmitting(false);}}async function handleAccountSubmit(){if(accountSubmitting)return;clearAccountError();const username=document.getElementById('account-username').value.trim();const password=document.getElementById('account-password').value;const confirmPw=document.getElementById('account-password-confirm').value;const displayName=document.getElementById('account-display-input').value.trim();if(!username||!password||(accountMode==='register'&&(!displayName||!confirmPw))){showAccountError(t('accountErrorEmpty'));return;}if(accountMode==='register'){if(password!==confirmPw){showAccountError(t('accountErrorPasswordMatch'));return;}const codename=displayName.trim().substring(0,12);showConfirm(t('registerNameConfirm',codename),()=>{proceedWithRegistration(username,password,codename);},{yes:t('registerConfirmStart'),no:t('registerThinkAgain')});return;}setAccountSubmitting(true);try{if(!(await ensureGunRelayReady(10000))){showAccountError(t('cloudSyncRelayBlocked'));return;}const res=await loginAccount(username,password);if(!res.ok){showAccountError(t(res.msg));return;}beginGameAfterAccount(!!res.pulled);}finally{setAccountSubmitting(false);}}",
    ),
    # applyLanguage loading text
    (
        "function applyLanguage(){\ndocument.getElementById('settings-title').textContent=t('settingsTitle');",
        "function applyLanguage(){\nconst _lt=document.getElementById('loading-text');if(_lt)_lt.textContent=t('loadingText');document.getElementById('settings-title').textContent=t('settingsTitle');",
    ),
    # Version
    (
        "GAME_VERSION='2.5.1'",
        "GAME_VERSION='2.5.2'",
    ),
    (
        "GAME_VERSION_HISTORY=[{version:'2.5.1'",
        "GAME_VERSION_HISTORY=[{version:'2.5.2',date:'2025-06-07',summary:{zh:'MTO 品牌更新：載入與帳號標題；註冊玩家名字確認流程。',en:'MTO branding update; register player name confirmation flow.'}},{version:'2.5.1'",
    ),
]

for i, (old, new) in enumerate(replacements):
    if old not in c:
        raise SystemExit(f'MISSING patch {i}: {old[:120]}...')
    c = c.replace(old, new, 1)

for pat in ['registerNameConfirm', "MTO 'MUX TEXT ONLINE'", 'proceedWithRegistration', 'registerConfirmStart']:
    if pat not in c:
        raise SystemExit(f'MISSING after patch: {pat}')

path.write_text(c, encoding='utf-8')
print('Applied MTO branding + register confirm patches')
