#!/usr/bin/env python3
"""Refresh cloud sync detail when player opens settings."""
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "index.html"
s = path.read_text()


def rep(old, new, label, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f"[{label}] expected {count}, got {n}\n{old[:220]}")
    s = s.replace(old, new, 1)


rep(
    "function refreshCloudSyncDisplay(){if(cloudSyncState==='syncing')return;",
    "function refreshCloudSyncOnSettingsOpen(){refreshCloudSyncNetworkStatus();updateCloudSyncDetail();}function refreshCloudSyncDisplay(){if(cloudSyncState==='syncing'){updateCloudSyncDetail();return;}",
    "settings open refresh + syncing detail",
)

rep(
    "function refreshCloudSyncNetworkStatus(){if(cloudSyncState==='syncing')return;",
    "function refreshCloudSyncNetworkStatus(){if(cloudSyncState==='syncing'){updateCloudSyncDetail();return;}",
    "network status syncing detail",
)

rep(
    "syncAccountProfileToUI();refreshCloudSyncNetworkStatus();clearCloudSyncFeedback();settingsOverlayEl.style.display='flex';",
    "syncAccountProfileToUI();refreshCloudSyncOnSettingsOpen();clearCloudSyncFeedback();settingsOverlayEl.style.display='flex';",
    "btn-settings handler",
)

path.write_text(s)
print("Patched cloud sync settings-open refresh")
