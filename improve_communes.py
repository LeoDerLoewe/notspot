#!/usr/bin/env python3
"""
improve_communes.py - Verbessere kategorisierung der existierenden 615 Gemeinden
+ Merge mit zusätzlichen Schweizer Gemeinden-Grunddaten
"""

import json
import re

def improve_commune(c):
    """Verbessere eine Gemeinde basierend auf vorhandenen Daten"""
    name = c.get("name", "").lower()
    canton = c.get("canton", "")
    pop = c.get("pop", 0)
    elev = c.get("elev", 400)
    cats = set(c.get("cats", []))

    # 1. Höhen-basierte Kategorisierung
    if elev > 1300:
        cats.update(["berge", "wandern"])
    elif elev > 900:
        cats.add("wandern")

    # 2. Canton-basierte Heuristiken
    alpine_cantons = ["GR", "VS", "UR", "BE", "GL"]
    if canton in alpine_cantons and "berge" not in cats:
        cats.add("berge")

    lake_cantons = {"ZH": ["zürich"], "TI": ["lugano", "locarno"], "VD": ["lausanne", "montreux"]}
    if canton in lake_cantons:
        for city_hint in lake_cantons[canton]:
            if city_hint in name:
                cats.add("see")

    # 3. Namen-Pattern Matching
    name_patterns = {
        "wald": ["wald", "wil"],
        "see": ["see", "lac", "zee", "felden"],
        "kultur": ["stadt", "burg", "schloss", "kloster", "museum"],
        "thermalbad": ["bad", "bain", "thermal"],
        "berg": ["berg", "alp", "horn", "spitz"],
    }

    for cat, patterns in name_patterns.items():
        if any(p in name for p in patterns) and cat not in cats:
            cats.add(cat)

    # 4. Population-basiert
    if pop > 20000:
        cats.add("stadt")
    if pop < 500:
        cats.add("land")

    # 5. Sicherstelle Transport ist da
    if canton in ["ZH", "AG", "BL", "BS"]:  # Städtische Kantone
        cats.update(["auto", "öv"])
    else:
        cats.add("auto")

    # 6. Naturkategorien fallback
    if not any(cat in cats for cat in ["berge", "see", "wald"]):
        if elev > 600:
            cats.add("wald")

    # Cleanup: Nur echte Kategorien
    valid_cats = {
        "see", "berge", "wald", "fluss", "land", "stadt",
        "wandern", "schwimmen", "klettern", "wintersport",
        "velo", "kultur", "thermalbad", "kloster", "burg",
        "hunde", "weinberg", "auto", "öv", "zu_fuss"
    }
    cats = list(cats & valid_cats)

    return {**c, "cats": sorted(cats)}


def load_communes_from_html(filepath):
    """Extrahiere COMMUNES aus index.html"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Find const COMMUNES = [ ... ];
    pattern = r"const COMMUNES = \[(.*?)\];"
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        print("❌ Could not find COMMUNES in index.html")
        return None, None

    communes_str = match.group(1)
    communes = json.loads("[" + communes_str + "]")
    return communes, (match.start(), match.end())


def save_communes_to_html(filepath, communes, old_pos):
    """Schreibe verbesserte COMMUNES zurück"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Generiere neuen JSON
    new_communes_str = "const COMMUNES = [" + json.dumps(communes, ensure_ascii=False, separators=(",", ":")) + "];"

    # Ersetze alten Block
    start, end = old_pos
    new_content = content[:start - len("const COMMUNES = ")] + new_communes_str + content[end:]

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"✓ Wrote {len(communes)} communes back to index.html")


def main():
    print("=" * 70)
    print("NotSpot: Improve existing 615 communes categorization")
    print("=" * 70)
    print()

    # Load
    communes, pos = load_communes_from_html("index.html")
    if communes is None:
        return

    print(f"✓ Loaded {len(communes)} communes")
    print()

    # Improve each
    improved = [improve_commune(c) for c in communes]

    print("✓ Improved categorization for all communes:")
    print()

    # Stats
    cat_freq = {}
    for c in improved:
        for cat in c.get("cats", []):
            cat_freq[cat] = cat_freq.get(cat, 0) + 1

    print("Category distribution:")
    for cat in sorted(cat_freq, key=lambda x: cat_freq[x], reverse=True):
        count = cat_freq[cat]
        pct = 100 * count / len(improved)
        print(f"  {cat:15s} {count:4d} communes ({pct:5.1f}%)")

    print()

    # Save
    save_communes_to_html("index.html", improved, pos)

    print()
    print("=" * 70)
    print("✅ Done! Improved COMMUNES saved to index.html")
    print()
    print("Next steps:")
    print("  1. Test in browser: http://localhost:8888")
    print("  2. Run enrich_communes.py for full 2190 communes (30min)")
    print("  3. Deploy!")


if __name__ == "__main__":
    main()
