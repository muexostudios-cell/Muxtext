#!/usr/bin/env python3
"""Gun relay resilience: multi-peer fallback, probe/reconnect, cloud fetch retry."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
text = INDEX.read_text(encoding="utf-8")

OLD_peers = "GUN_PEERS_DEFAULT=['https://gun.o8.is/gun'];let gunPeersActive"
NEW_peers = "GUN_PEERS_DEFAULT=['https://gun.o8.is/gun','https://relay.peer.ooo/gun','https://gun.defucc.me/gun'];let gunPeersActive"
if OLD_peers not in text:
    raise SystemExit("peers block not found")
text = text.replace(OLD_peers, NEW_peers, 1)

OLD_probe_at = 'gunPeerWaiters=[];let accountMode'
NEW_probe_at = 'gunPeerWaiters=[],lastGunRelayProbeAt=0;let accountMode'
if OLD_probe_at not in text:
    raise SystemExit("probe_at block not found")
text = text.replace(OLD_probe_at, NEW_probe_at, 1)

OLD_refresh_to_relay = 'function refreshGunPeers(){try{const res=await fetch(\'https://raw.githubusercontent.com/wiki/amark/gun/volunteer.dht.md\',{cache:\'no-store\'});if(!res.ok)return gunPeersActive;const text=await res.text();gunPeersActive=mergeGunPeers([...GUN_PEERS_DEFAULT,...text.match(/https?:\\/\\/[^\\s\\])\'"<>]+\\/gun/g)||[]]);}catch(e){}return gunPeersActive;}function attachGunPeerListeners(gun){if(!gun||gun._muxPeerHook)return;gun._muxPeerHook=true;gun.on(\'hi\',()=>{markGunRelayConnected();});}function markGunRelayConnected(){if(gunPeerConnected)return;gunPeerConnected=true;gunPeerWaiters.splice(0).forEach(fn=>fn(true));if(typeof refreshCloudSyncDisplay===\'function\')refreshCloudSyncDisplay();}function waitForGunRelay(timeoutMs=8000){if(gunPeerConnected)return Promise.resolve(true);return new Promise(resolve=>{let done=false;const finish=ok=>{if(done)return;done=true;resolve(!!ok);};const timer=setTimeout(()=>finish(gunPeerConnected),timeoutMs);gunPeerWaiters.push(ok=>{clearTimeout(timer);finish(ok);});ensureGameGun(()=>{});});}async '
NEW_refresh_to_relay = 'function refreshGunPeers(){try{const res=await fetch(\'https://raw.githubusercontent.com/wiki/amark/gun/volunteer.dht.md\',{cache:\'no-store\'});if(!res.ok)return gunPeersActive;const text=await res.text();const next=mergeGunPeers([...GUN_PEERS_DEFAULT,...text.match(/https?:\\/\\/[^\\s\\])\'"<>]+\\/gun/g)||[]]);if(JSON.stringify(next)!==JSON.stringify(gunPeersActive)){gunPeersActive=next;if(gameGun)resetGameGun();}}catch(e){}return gunPeersActive;}function attachGunPeerListeners(gun){if(!gun||gun._muxPeerHook)return;gun._muxPeerHook=true;gun.on(\'hi\',()=>{markGunRelayConnected();});}function markGunRelayConnected(){if(gunPeerConnected)return;gunPeerConnected=true;gunPeerWaiters.splice(0).forEach(fn=>fn(true));if(typeof refreshCloudSyncDisplay===\'function\')refreshCloudSyncDisplay();}function waitForGunRelay(timeoutMs=8000){if(gunPeerConnected)return Promise.resolve(true);return new Promise(resolve=>{let done=false;const finish=ok=>{if(done)return;done=true;resolve(!!ok);};const timer=setTimeout(()=>finish(gunPeerConnected),timeoutMs);gunPeerWaiters.push(ok=>{clearTimeout(timer);finish(ok);});ensureGameGun(()=>{});});}function probeGunRelay(timeoutMs=6000){return new Promise(resolve=>{let done=false;const finish=ok=>{if(done)return;done=true;resolve(!!ok);};const timer=setTimeout(()=>finish(gunPeerConnected),timeoutMs);ensureGameGun(gun=>{try{const ping=String(Date.now());gun.get(CLOUD_ROOT).get(\'_relay_ping\').get(ping).put({t:Date.now()},ack=>{if(done)return;clearTimeout(timer);if(ack&&ack.err)finish(false);else{markGunRelayConnected();finish(true);}});}catch(e){if(!done){done=true;clearTimeout(timer);finish(false);}}});});}async '
if OLD_refresh_to_relay not in text:
    raise SystemExit("refresh_to_relay block not found")
text = text.replace(OLD_refresh_to_relay, NEW_refresh_to_relay, 1)

OLD_relay_ready = 'function ensureGunRelayReady(timeoutMs=8000){await refreshGunPeers();ensureGameGun(()=>{});return (await waitForGunRelay(timeoutMs))||gunPeerConnected;}'
NEW_relay_ready = 'function ensureGunRelayReady(timeoutMs=12000){await refreshGunPeers();ensureGameGun(()=>{});if(gunPeerConnected)return true;const w1=Math.floor(timeoutMs*0.4),w2=Math.floor(timeoutMs*0.35);if(await waitForGunRelay(w1))return true;if(await probeGunRelay(w1))return true;resetGameGun();await refreshGunPeers();ensureGameGun(()=>{});if(await waitForGunRelay(w2))return true;if(await probeGunRelay(w2))return true;return gunPeerConnected;}'
if OLD_relay_ready not in text:
    raise SystemExit("relay_ready block not found")
text = text.replace(OLD_relay_ready, NEW_relay_ready, 1)

OLD_cloud_ops = "function fetchCloudAccount(key,timeoutMs=9000){return new Promise(resolve=>{let done=false;const timer=setTimeout(()=>{if(!done){done=true;resolve(null);}},timeoutMs);ensureGameGun(gun=>{gun.get(CLOUD_ROOT).get('accounts').get(key).once(data=>{if(done)return;done=true;clearTimeout(timer);markGunRelayConnected();resolve(data&&data.passHash?data:null);});});});}function putCloudAccount(key,payload,timeoutMs=12000){return new Promise((resolve,reject)=>{let done=false;const timer=setTimeout(()=>{if(!done){done=true;reject(new Error('timeout'));}},timeoutMs);ensureGameGun(gun=>{try{gun.get(CLOUD_ROOT).get('accounts').get(key).put(payload,ack=>{if(done)return;done=true;clearTimeout(timer);if(ack&&ack.err)reject(ack.err);else{markGunRelayConnected();resolve(true);}});}catch(e){if(!done){done=true;clearTimeout(timer);reject(e);}}});});}"
NEW_cloud_ops = "function fetchCloudAccountOnce(key,timeoutMs){return new Promise(resolve=>{let done=false;const timer=setTimeout(()=>{if(!done){done=true;resolve(undefined);}},timeoutMs);ensureGameGun(gun=>{gun.get(CLOUD_ROOT).get('accounts').get(key).once(data=>{if(done)return;done=true;clearTimeout(timer);markGunRelayConnected();resolve(data&&data.passHash?data:null);});});});}async function fetchCloudAccount(key,timeoutMs=10000){for(let attempt=0;attempt<2;attempt++){const data=await fetchCloudAccountOnce(key,timeoutMs);if(data!==undefined)return data;if(attempt===0){resetGameGun();await refreshGunPeers();}}return null;}function putCloudAccountOnce(key,payload,timeoutMs){return new Promise((resolve,reject)=>{let done=false;const timer=setTimeout(()=>{if(!done){done=true;reject(new Error('timeout'));}},timeoutMs);ensureGameGun(gun=>{try{gun.get(CLOUD_ROOT).get('accounts').get(key).put(payload,ack=>{if(done)return;done=true;clearTimeout(timer);if(ack&&ack.err)reject(ack.err);else{markGunRelayConnected();resolve(true);}});}catch(e){if(!done){done=true;clearTimeout(timer);reject(e);}}});});}async function putCloudAccount(key,payload,timeoutMs=14000){for(let attempt=0;attempt<2;attempt++){try{await putCloudAccountOnce(key,payload,timeoutMs);return true;}catch(e){if(attempt===0){resetGameGun();await refreshGunPeers();}else throw e;}}return false;}"
if OLD_cloud_ops not in text:
    raise SystemExit("cloud_ops block not found")
text = text.replace(OLD_cloud_ops, NEW_cloud_ops, 1)

OLD_tick = "function tickCloudAutoSync(){if(cloudSyncInProgress||cloudUploadBusy)return;if(!hasActiveCloudSession()){stopCloudAutoSync();return;}if(typeof navigator!=='undefined'&&navigator.onLine===false)return;if(accountNeedsCloudPush()){forceCloudSyncFromLocal();return;}tickCloudIdleSync();}"
NEW_tick = "function tickCloudAutoSync(){if(cloudSyncInProgress||cloudUploadBusy)return;if(!hasActiveCloudSession()){stopCloudAutoSync();return;}if(typeof navigator!=='undefined'&&navigator.onLine===false)return;if(!gunPeerConnected&&Date.now()-lastGunRelayProbeAt>15000){lastGunRelayProbeAt=Date.now();ensureGunRelayReady(8000).then(ok=>{if(ok&&typeof restartCloudSyncRuntime==='function')restartCloudSyncRuntime();else if(typeof refreshCloudSyncDisplay==='function')refreshCloudSyncDisplay();});return;}if(accountNeedsCloudPush()){forceCloudSyncFromLocal();return;}tickCloudIdleSync();}"
if OLD_tick not in text:
    raise SystemExit("tick block not found")
text = text.replace(OLD_tick, NEW_tick, 1)

OLD_login = "}else if(!(await ensureGunRelayReady(10000))){showAccountError(t('cloudSyncRelayBlocked'));return;}const res=await loginAccount(username,password);"
NEW_login = "}else{const loginKey=normalizeAccountKey(username);const hasLocal=!!loadAccountStore().byKey[loginKey];const relayOk=await ensureGunRelayReady(12000);if(!relayOk&&!hasLocal){showAccountError(t('cloudSyncRelayBlocked'));return;}if(!relayOk)logInfo(t('cloudSyncRelayBlocked'));}const res=await loginAccount(username,password);"
if OLD_login not in text:
    raise SystemExit("login block not found")
text = text.replace(OLD_login, NEW_login, 1)

INDEX.write_text(text, encoding="utf-8")
print("Patched index.html (gun relay fix)")
