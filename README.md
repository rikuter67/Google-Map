Expo2025 Pavilion KML Generator
================================

1. 入力ファイル：pavilion_52.csv
   └ display_name, level, memo を定義

     |
     v

2. スクリプト：expo2025.py
   • CSV 読込
   • Google Maps Places API による範囲検索
   • レベル別に KML ファイル出力 (S～D)
   • エラーハンドリング／ログ出力

     |
     v

3. 出力
   • expo2025_pavilions_S.kml … レベル S
   • expo2025_pavilions_A.kml … レベル A
   • …  
   • expo2025_pavilions_D.kml … レベル D
   • expo2025_pavilions_full.csv … 全パビリオン詳細

----------------------------------
Setup & Best Practices
----------------------------------
• API キー管理  
  – GOOGLE_MAPS_API_KEY を環境変数に設定  
  – リファラー/IP 制限を忘れずに  
  – .gitignore でキーをコミット除外  

• 利用ライブラリ  
  – googlemaps, simplekml, pandas  

• クォータ管理  
  – 定期的に使用量を確認  
  – 無駄なリクエストは避ける  

• CSV 保守  
  – 公式名称を使用して Google Maps で正確に検索可能に  
  – memo は500文字以内で要点を簡潔に  

• マップ連携例  
  – KML を Google My Maps／Google Earth にインポート  
  – GitHub Pages に iframe 埋め込み  

