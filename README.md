# nerima-district-plans

プロトタイプ：練馬区地区計画データベース（PDF取得・抽出・境界ベクトル化・Web表示）

このリポジトリには、公式ページ（https://www.city.nerima.tokyo.jp/kusei/machi/chikukeikaku/chiku_ichiran.html）からPDFを取得し、テキストと計画図を抽出してWebアプリに表示するための初期スクリプトとテンプレートを格納します。

次の手順（ざっくり）
1. GitHub Actions またはローカルで scraper/get_pdf_links.py を実行して PDF をダウンロード
2. extractor/extract_metadata.py で PDF からテキストと図を抽出
3. vectorize/vectorize_from_image.py で計画図から輪郭を抽出して GeoJSON を作成（自動→手動補正ワークフロー）
4. frontend/README.md を参照してフロントエンドを起動（Next.js を想定）

成果物
- data/pdfs/ にダウンロードしたPDF
- data/json/ に抽出したメタデータJSON
- data/geojson/ に境界GeoJSON（暫定）

Issues / ToDo
- 全48件PDFの取得と抽出の実行（GitHub Actions で自動化済み）
- 画像→ベクターの精度確認と手動補正UIの実装（Leafletベース）
