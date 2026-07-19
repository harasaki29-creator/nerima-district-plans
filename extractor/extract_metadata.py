#!/usr/bin/env python3
"""
extractor/extract_metadata.py

PyMuPDF を使って PDF のテキストとページ画像を抽出し、簡易メタデータ(JSON)を出力します。
出力先: data/json/, data/images/
"""
import json
import fitz  # PyMuPDF
from pathlib import Path

PDF_DIR = Path("data/pdfs")
OUT_JSON_DIR = Path("data/json")
OUT_IMG_DIR = Path("data/images")
OUT_JSON_DIR.mkdir(parents=True, exist_ok=True)
OUT_IMG_DIR.mkdir(parents=True, exist_ok=True)

def extract_pdf(path: Path):
    doc = fitz.open(str(path))
    meta = {
        "filename": path.name,
        "n_pages": doc.page_count,
        "pages": []
    }
    for i, page in enumerate(doc):
        text = page.get_text("text")
        pix = page.get_pixmap(dpi=200)
        img_name = f"{path.stem}_p{i+1}.png"
        img_path = OUT_IMG_DIR / img_name
        pix.save(str(img_path))
        meta["pages"].append({
            "page": i+1,
            "text": text,
            "image": str(img_path)
        })
    out_json = OUT_JSON_DIR / f"{path.stem}.json"
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    print(f"extracted: {path.name} -> {out_json}")

def main():
    for pdf in PDF_DIR.glob('*.pdf'):
        try:
            extract_pdf(pdf)
        except Exception as e:
            print(f"failed to extract {pdf}: {e}")

if __name__ == '__main__':
    main()
