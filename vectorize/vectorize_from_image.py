#!/usr/bin/env python3
"""
vectorize/vectorize_from_image.py

計画図（ラスタ画像）から輪郭を検出して簡易GeoJSONを作る試作スクリプト。
※ 生成されたジオメトリは地理参照されていません。実際の座標系に落とし込むにはジオリファレンス（制御点）や手動補正が必要です。
"""
import cv2
import json
from pathlib import Path
from shapely.geometry import Polygon, mapping

IMG_DIR = Path('data/images')
OUT_DIR = Path('data/geojson')
OUT_DIR.mkdir(parents=True, exist_ok=True)

def detect_contours(img_path: Path, min_area=1000):
    img = cv2.imread(str(img_path))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 二値化の閾値は画像により調整が必要
    _, th = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    polys = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < min_area:
            continue
        eps = 0.01 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, eps, True)
        coords = [(int(p[0][0]), int(p[0][1])) for p in approx]
        polys.append(coords)
    return polys

def main():
    for img in IMG_DIR.glob('*.png'):
        polys = detect_contours(img)
        features = []
        for i, coords in enumerate(polys):
            try:
                poly = Polygon(coords)
                if not poly.is_valid:
                    poly = poly.buffer(0)
                features.append({
                    'type': 'Feature',
                    'properties': {'source_image': str(img.name), 'index': i},
                    'geometry': mapping(poly)
                })
            except Exception as e:
                print(f"failed to create polygon for {img.name} idx={i}: {e}")
        fc = {'type': 'FeatureCollection', 'features': features}
        outp = OUT_DIR / f"{img.stem}.geojson"
        with open(outp, 'w', encoding='utf-8') as f:
            json.dump(fc, f, ensure_ascii=False, indent=2)
        print(f"vectorized {img.name} -> {outp} ({len(features)} features)")

if __name__ == '__main__':
    main()
