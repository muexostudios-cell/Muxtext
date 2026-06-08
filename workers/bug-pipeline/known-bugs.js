/**
 * Known player-reported bug catalog — synced with GAME_VERSION_HISTORY fixes.
 * lifecycle: reported → clustered → probing → confirmed|client-only → fixed|monitoring
 */
export const KNOWN_BUGS = [
  {
    id: 'level-rollback',
    category: 'save',
    severity: 'high',
    fixedVersion: '2.14.3',
    keywords: ['等級', '回調', 'rollback', 'level', '降級', '經驗', 'xp', 'peak'],
    clientSignals: ['level_regression', 'peak_level_mismatch'],
    serverSignals: [],
    summary: { zh: '等級異常回調／雲端合併覆蓋較高進度', en: 'Level rollback after reload or cloud sync' },
  },
  {
    id: 'cloud-sync-fail',
    category: 'network',
    severity: 'high',
    fixedVersion: '2.17.1',
    keywords: ['雲端', '同步', 'cloud sync', 'cloud_upload', 'relay', 'gun relay', 'gun中繼', '連線', 'offline', 'timeout'],
    clientSignals: ['cloud_sync_offline', 'cloud_upload_fail', 'gun_relay_blocked'],
    serverSignals: ['gun_relay_unreachable'],
    summary: { zh: '雲端同步失敗或 Gun 中繼無法連線', en: 'Cloud sync or Gun relay connection failure' },
  },
  {
    id: 'chat-offline',
    category: 'server',
    severity: 'medium',
    fixedVersion: null,
    keywords: ['聊天', 'chat', '訊息', 'message', 'offline', 'crash'],
    clientSignals: ['chat_offline', 'chat_health_fail'],
    serverSignals: ['chat_worker_down'],
    summary: { zh: '聊天室無法連線或訊息載入失敗', en: 'Chat room unreachable or messages fail to load' },
  },
  {
    id: 'xp-bar-stale',
    category: 'client',
    severity: 'medium',
    fixedVersion: '2.6.6',
    keywords: ['經驗條', 'xp bar', 'xp', '經驗', '不更新', 'stale'],
    clientSignals: ['xp_bar_stale', 'xp_display_mismatch'],
    serverSignals: [],
    summary: { zh: '手動戰鬥後經驗條未即時更新', en: 'XP bar not updating after manual combat' },
  },
  {
    id: 'save-fail',
    category: 'save',
    severity: 'high',
    fixedVersion: null,
    keywords: ['存檔', 'save', 'storage', 'quota', 'lost', '消失'],
    clientSignals: ['save_write_fail', 'storage_quota'],
    serverSignals: [],
    summary: { zh: '本地存檔寫入失敗或容量不足', en: 'Local save write failure or storage quota' },
  },
  {
    id: 'payment-verify-fail',
    category: 'server',
    severity: 'medium',
    fixedVersion: null,
    keywords: ['付款', 'payment', 'stripe', '晶片', 'chip', 'verify', '充值'],
    clientSignals: ['payment_verify_fail'],
    serverSignals: ['stripe_verify_down'],
    summary: { zh: '晶片充值驗證失敗', en: 'Chip recharge verification failed' },
  },
  {
    id: 'dungeon-stuck',
    category: 'client',
    severity: 'medium',
    fixedVersion: null,
    keywords: ['卡住', 'stuck', '地城', 'dungeon', '戰鬥', 'combat', 'freeze', '凍結'],
    clientSignals: ['combat_queue_stuck', 'dungeon_state_invalid'],
    serverSignals: [],
    summary: { zh: '地城或戰鬥流程卡住無法繼續', en: 'Dungeon or combat flow stuck' },
  },
  {
    id: 'leaderboard-stale',
    category: 'network',
    severity: 'low',
    fixedVersion: '2.8.6',
    keywords: ['排行榜', 'leaderboard', 'rank', '等級', 'level'],
    clientSignals: ['leaderboard_level_mismatch'],
    serverSignals: [],
    summary: { zh: '排行榜等級與角色不符', en: 'Leaderboard level does not match character' },
  },
  {
    id: 'game-host-down',
    category: 'server',
    severity: 'critical',
    fixedVersion: null,
    keywords: ['無法載入', 'load', '404', 'blank', '白屏', 'host'],
    clientSignals: [],
    serverSignals: ['game_host_down'],
    summary: { zh: '遊戲主站無法載入', en: 'Game host unreachable' },
  },
];

export const LIFECYCLE_STAGES = [
  'reported',
  'clustered',
  'probing',
  'confirmed',
  'client-only',
  'fixed',
  'monitoring',
];

export function matchBugByText(text) {
  const lower = String(text || '').toLowerCase();
  const hits = [];
  for (const bug of KNOWN_BUGS) {
    const score = bug.keywords.reduce((n, kw) => (lower.includes(kw.toLowerCase()) ? n + 1 : n), 0);
    if (score > 0) hits.push({ bug, score });
  }
  hits.sort((a, b) => b.score - a.score);
  return hits[0]?.bug || null;
}

export function matchBugBySignals(signals = []) {
  const set = new Set(signals);
  const hits = KNOWN_BUGS.map((bug) => {
    const client = bug.clientSignals.filter((s) => set.has(s)).length;
    const server = bug.serverSignals.filter((s) => set.has(s)).length;
    return { bug, score: client * 2 + server * 3 };
  }).filter((h) => h.score > 0);
  hits.sort((a, b) => b.score - a.score);
  return hits[0]?.bug || null;
}
