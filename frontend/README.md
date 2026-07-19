# frontend

フロントエンドは Next.js と Leaflet を想定しています。ここでは最小限の手順とファイル構成案を記載します。

開発 (ローカル)
- cd frontend
- npm install
- npm run dev

必要な機能（実装予定）:
- / : 一覧・検索ページ
- /map : Leaflet 地図、GeoJSON を読み込んでポリゴン表示
- /item/[id] : 詳細ページ、PDF埋込（PDF.js）

備考
- 本リポジトリではまず API をシミュレートするスタブデータ（data/json）でフロントを動かし、次に実データを Actions のアーティファクトから取り込むワークフローを実装します。
