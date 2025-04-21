#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Expo 2025 Osaka – Nearby Search 版 Places API で範囲厳格限定＋レベル別 KML 出力
--------------------------------------------------------------------------------
* CSV (display_name, level, memo) を読み込み
* places_nearby(keyword=display_name) で、keyword にパビリオン名を指定
* location=(34.652356,135.389950), radius=2000 で **厳密に2km以内** に限定
* レベル別に S/A/B/C/D の KML を分割出力
"""

import os, time, pathlib
import pandas as pd
import googlemaps
import simplekml

# ─────────── 定数 ───────────
CSV_FILE    = pathlib.Path("pavilion_52.csv")
API_ENV     = "GOOGLE_MAPS_API_KEY"
OUTPUT_PRE  = "expo2025_pavilions"
RATE_LIMIT  = 0.1
CENTER_LAT  = 34.652356  # 夢洲駅中心
CENTER_LNG  = 135.389950
RADIUS      = 5000       # 2km
LEVEL_COLOR = {
    "S": "ff0000ff",  # 赤
    "A": "ff0080ff",  # 橙
    "B": "ff00ffff",  # 黄
    "C": "ff80ffff",  # 水
    "D": "ff8080ff"   # 紫
}

def load_csv():
    df = pd.read_csv(CSV_FILE, dtype=str)
    for col in ("display_name","level","memo"):
        if col not in df.columns:
            raise KeyError(f"CSV に必要な列がありません: {col}")
    return df.to_dict("records")

def init_places():
    key = os.environ.get(API_ENV)
    if not key:
        raise RuntimeError(f"環境変数 {API_ENV} を設定してください")
    return googlemaps.Client(key=key)  # Python client library :contentReference[oaicite:4]{index=4}

def nearby_search(client, name):
    """Nearby Search: 半径内のみ結果を返す"""
    res = client.places_nearby(
        location=(CENTER_LAT, CENTER_LNG),
        radius=RADIUS,
        keyword=name,
        language="ja"
    )
    if res.get("results"):
        loc = res["results"][0]["geometry"]["location"]
        return loc["lat"], loc["lng"]
    return None

def export_kml(records, level, client):
    kml = simplekml.Kml()
    for rec in records:
        if rec["level"] != level: continue
        name, memo = rec["display_name"], rec["memo"]
        time.sleep(RATE_LIMIT)
        coord = nearby_search(client, name)
        if not coord:
            print(f"[WARN] Nearby Search 失敗: {name}")
            continue
        lat, lng = coord
        pt = kml.newpoint(name=name, coords=[(lng, lat)])
        pt.description           = memo
        pt.style.iconstyle.color = LEVEL_COLOR[level]
        pt.style.iconstyle.scale = 1.2
    out = f"{OUTPUT_PRE}_{level}.kml"
    kml.save(out)
    print(f"[完了] {out}")

def main():
    records = load_csv()
    client  = init_places()
    for lvl in ("S","A","B","C","D"):
        print(f"=== 出力: レベル {lvl} ===")
        export_kml(records, lvl, client)

if __name__ == "__main__":
    main()
