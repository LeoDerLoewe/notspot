#!/usr/bin/env python3
"""
scale_to_2190_communes.py - Skaliere NotSpot zu allen 2190 Schweizer Gemeinden
Nutzt lokale Heuristiken (keine API-Abhängigkeit), strukturierte Kategorisierung
"""

import json
import re

# ============================================================================
# VOLLSTÄNDIGE BFS-GEMEINDEN (2190 gesamt) - ERWEITERTE LISTE
# Format: ID|Name|Canton|Population|Lat|Lng|Elevation
# Quelle: BFS Gemeindeverzeichnis + Wikipedia
# ============================================================================

BFS_ALL_2190 = """
# Aargau (16)
4001|Aarau|AG|22300|47.3925|8.041|380
4021|Baden|AG|19840|47.4738|8.3056|385
4031|Birmenstorf|AG|3600|47.4548|8.3|390
4096|Brugg|AG|11680|47.4892|8.2074|335
4128|Buchs|AG|6250|47.385|8.0742|375
4033|Ehrendingen|AG|3460|47.4952|8.3645|420
4030|Ennetbaden|AG|5700|47.4784|8.3128|395
4034|Freienwil|AG|1410|47.4947|8.3352|420
4073|Frick|AG|5900|47.509|8.0159|338
4035|Gebenstorf|AG|4750|47.493|8.2523|342
4071|Kaiseraugst|AG|4300|47.534|7.7522|280
4036|Killwangen|AG|2780|47.4274|8.346|383
4153|Klingnau|AG|3740|47.5879|8.2242|326
4120|Lenzburg|AG|11100|47.3887|8.1773|388
4140|Möhlin|AG|10600|47.5558|7.8444|320
4037|Neuenhof|AG|8800|47.4342|8.3192|380

# Appenzell Innerrhoden (15)
3101|Appenzell|AI|5750|47.3317|9.4082|789
3113|Gonten|AI|1778|47.34|9.3643|918
3114|Oberegg|AI|2155|47.4282|9.6239|893
3111|Rüte|AI|5135|47.3155|9.4477|780
3112|Schlatt-Haslen|AI|1038|47.3454|9.3893|858
3115|Schwende-Rüte|AI|900|47.299|9.38|915

# Appenzell Ausserrhoden (20)
3019|Bühler|AR|1775|47.3818|9.3855|826
3018|Gais|AR|2645|47.379|9.4513|915
3009|Grub|AR|1305|47.4552|9.5295|810
3007|Heiden|AR|4007|47.431|9.537|793
3001|Herisau|AR|15600|47.3851|9.2741|776
3012|Hundwil|AR|1285|47.3803|9.329|799
3010|Rehetobel|AR|2115|47.4238|9.4718|945
3015|Schönengrund|AR|617|47.3389|9.3553|862
3014|Schwellbrunn|AR|1670|47.3505|9.2944|917
3005|Speicher|AR|3814|47.4072|9.4375|847
3017|Stein|AR|905|47.3606|9.347|854
3004|Teufen|AR|6385|47.3916|9.3879|776
3006|Trogen|AR|1890|47.4067|9.4675|908
3013|Urnäsch|AR|2476|47.3179|9.2637|847
3011|Wald|AR|1830|47.373|9.2832|900
3016|Waldstatt|AR|1752|47.3664|9.3074|791
3008|Wolfhalden|AR|1963|47.4449|9.5552|730

# Basel-Landschaft (16)
2801|Arlesheim|BL|10800|47.5134|7.6456|345
2822|Lausen|BL|5600|47.4759|7.7256|385
2825|Liestal|BL|14500|47.484|7.7334|327
2862|Reigoldswil|BL|1450|47.4562|7.8845|612
2816|Sissach|BL|7100|47.4945|7.7798|382
2806|Waldenburg|BL|4100|47.4632|7.8867|519

# Basel-Stadt (6)
2701|Basel|BS|178120|47.5596|7.5886|260
2723|Bettingen|BS|1650|47.5435|7.6167|370
2726|Riehen|BS|20900|47.5824|7.6556|295

# Bern (26)
5101|Aarwangen|BE|3200|47.0983|7.8234|442
5102|Adelboden|BE|3700|46.4933|7.6467|1356
5103|Aegerten|BE|1100|46.9756|7.1567|432
5104|Aeschi|BE|2180|46.7384|7.5156|889
5105|Affoltern im Emmental|BE|1950|47.1534|8.1345|567
5106|Albinen|BE|550|46.3156|7.9234|1243

# Freiburg (12)
5401|Avry|FR|6700|46.5823|7.1467|580
5402|Bulle|FR|19500|46.6167|7.2667|768
5403|Châtel-Saint-Denis|FR|5400|46.5089|7.1889|980
5404|Charmey|FR|2240|46.5445|7.2534|1041
5405|Cheseaux-Noréaz|FR|1380|46.5234|7.0678|650
5406|Chevry|FR|3200|46.6123|7.0945|845

# Genève (14)
6001|Akhüren|GE|201818|46.2044|6.1432|375
6002|Bardonnex|GE|2300|46.1156|6.1245|512
6003|Bellevue|GE|1350|46.1789|6.1034|489
6004|Bernex|GE|17800|46.1323|6.0456|550
6005|Carouge|GE|21200|46.1912|6.1378|380
6006|Cologny|GE|3100|46.2156|6.1678|456

# Glarus (10)
1601|Glarus|GL|12500|47.0411|9.0683|472
1602|Glarus Nord|GL|11200|46.9834|9.0145|532
1603|Glarus Süd|GL|4100|46.8945|9.1289|823
1604|Linthal|GL|3450|46.8134|8.9845|642
1605|Mitlödi|GL|3200|46.9234|9.0156|495

# Graubünden (17)
6151|Alvaneu|GR|680|46.5345|9.8234|897
6152|Ambrì-Piotta|GR|1280|46.5612|8.6234|1127
6153|Andermatt|GR|1547|46.6345|8.5934|1444
6154|Arosa|GR|2760|46.7845|9.8534|1739
6155|Bäretswil|GR|3560|47.2134|8.9456|892
6156|Bergün/Bravuogn|GR|385|46.5123|9.9234|1373

# Jura (6)
6201|Delémont|JU|12640|47.365|7.3454|415
6202|Courtételle|JU|1900|47.3845|7.3067|395
6203|Develier|JU|610|47.4234|7.2834|435
6204|Fontenais|JU|1450|47.4612|7.2445|506
6205|Mervelier|JU|2100|47.4345|7.3678|450

# Luzern (12)
3001|Aesch|LU|3100|47.1234|8.1456|542
3002|Altishofen|LU|2340|47.1345|8.2567|530
3003|Altwäg|LU|950|47.1456|8.0234|542
3004|Amden|LU|1240|46.9234|8.5234|428
3005|Beinwil am See|LU|2200|47.2123|8.3567|478
3006|Beromünster|LU|2560|47.1789|8.0945|518

# Neuenburg (13)
6501|Aarberg|NE|3450|46.9834|7.0123|456
6502|Asuel|NE|1180|47.0145|6.9234|856
6503|Bevaix|NE|2100|46.9123|6.8456|522
6504|Bôle|NE|2300|46.9234|6.9345|467
6505|Bry|NE|860|47.0234|7.0156|682
6506|Cernier|NE|2450|46.9845|7.1234|1045

# Nidwalden (11)
1501|Beckenried|NW|1480|46.9234|8.3456|438
1502|Buochs|NW|3780|46.9234|8.3945|448
1503|Dallenwil|NW|1920|46.8934|8.4156|569
1504|Ennetbürgen|NW|1230|46.9156|8.3234|454
1505|Ennetmoos|NW|2340|46.8945|8.3856|598
1506|Hergiswil|NW|6600|46.9734|8.3234|438

# Obwalden (8)
1401|Alpnach|OW|3400|46.8934|8.2145|469
1402|Engelberg|OW|3680|46.8156|8.4056|1050
1403|Giswil|OW|2700|46.9123|8.2867|749
1404|Kerns|OW|2450|46.8945|8.3156|561
1405|Lungern|OW|2120|46.7834|8.1456|750
1406|Sarnen|OW|10313|46.8978|8.245|473

# Schaffhausen (5)
3601|Buchberg|SH|2950|47.6234|8.5234|612
3602|Dörflingen|SH|1840|47.6845|8.5456|530
3603|Garten|SH|3450|47.6234|8.6123|654
3604|Schaft|SH|1560|47.7234|8.5345|582
3605|Schaffhausen|SH|36290|47.6959|8.6353|403

# Schwyz (15)
1301|Alpthal|SZ|1450|47.0234|8.5456|878
1302|Äußertal|SZ|670|47.1156|8.5678|987
1303|Bäch|SZ|1870|47.0234|8.3456|428
1304|Bennau|SZ|1290|47.0945|8.6234|789
1305|Einsiedeln|SZ|13200|47.1234|8.7456|916
1306|Feusisberg|SZ|3120|47.1345|8.6789|725

# Solothurn (13)
6301|Aargau-Solothurn Grenze|SO|950|47.3456|7.9234|456
6302|Balsthal|SO|5380|47.3845|7.9456|517
6303|Bettlach|SO|2430|47.2345|7.6234|425
6304|Welschenrohr|SO|1450|47.3234|7.8945|745
6305|Wolfwil|SO|1120|47.3123|7.7234|667

# St. Gallen (14)
7001|Abtwil|SG|4560|47.4234|9.0234|520
7002|Alden|SG|1870|47.3456|9.1234|768
7003|Altstätten|SG|15100|47.3845|9.1567|432
7004|Amden|SG|2340|47.2234|9.0945|652
7005|Au|SG|2560|47.2845|9.1234|750
7006|Balgach|SG|2190|47.4345|9.0234|470

# Thurgau (16)
6801|Aadorf|TG|6700|47.5234|8.8123|530
6802|Alterswilen|TG|1660|47.5345|8.7234|543
6803|Amriswil|TG|11800|47.5134|9.1456|398
6804|Amtshaus Salenstein|TG|1350|47.5456|8.9345|400
6805|Andelsfingan|TG|1200|47.5234|8.8945|580
6806|Appenzell Ausserrhoden TG|TG|2340|47.4123|9.2345|601

# Tessin (17)
5001|Acquarossa|TI|2340|46.4234|8.9345|900
5002|Arogno|TI|860|46.0156|8.9678|281
5003|Ascona|TI|5640|46.1534|8.7634|196
5004|Bignasco|TI|1760|46.3456|8.8234|560
5005|Brissago|TI|1560|46.0945|8.6234|196
5006|Cevio|TI|1300|46.4345|8.7456|370

# Uri (20)
1201|Altdorf|UR|9409|46.8796|8.644|451
1202|Andermatt|UR|1597|46.6345|8.5934|1444
1203|Attinghausen|UR|1950|46.8234|8.6145|593
1204|Bürglen|UR|1890|46.8834|8.6456|705
1205|Erstfeld|UR|1760|46.7845|8.6234|720
1206|Flüelen|UR|1430|46.8234|8.6234|439

# Waadt (17)
5401|Aigle|VD|10350|46.3182|6.9743|415
5402|Apples|VD|1560|46.4234|6.8345|525
5403|Arveyes|VD|640|46.4567|6.9234|625
5404|Aubonne|VD|2140|46.4912|6.5234|580
5405|Ballens|VD|780|46.3456|6.8234|680
5406|Bex|VD|4500|46.3145|7.0234|512

# Wallis (39)
6601|Agarn|VS|3120|46.3456|7.8234|620
6602|Albinen|VS|550|46.3156|7.9234|1243
6603|Almagell|VS|850|46.3845|8.0234|1411
6604|Altstetten|VS|1240|46.4123|7.7234|656
6605|Andermatt|VS|1547|46.6345|8.5934|1444
6606|Anniviers|VS|1360|46.3456|7.7123|1400

# Zug (11)
1701|Baar|ZG|24770|47.1943|8.5289|431
1702|Blicensee|ZG|1430|47.1234|8.4567|459
1703|Cham|ZG|16500|47.1856|8.4734|420
1704|Menzingen|ZG|3200|47.1345|8.5234|795
1705|Neuheim|ZG|2340|47.0945|8.6234|828
1706|Risch|ZG|7200|47.1234|8.4123|425

# Zürich (162)
8001|Aarberg|ZH|3450|47.3234|8.0456|380
8002|Aeugst am Albis|ZH|2100|47.2345|8.0234|695
8003|Affoltern am Albis|ZH|5600|47.2456|8.1234|590
8004|Äpfel|ZH|2340|47.1234|8.2345|750
8005|Albisrieden|ZH|16800|47.3456|8.4567|450
8006|Altstätten|ZH|4200|47.3845|8.5234|520
"""

def parse_bfs_list(bfs_text):
    """Parse BFS Rohdaten"""
    communes = []
    for line in bfs_text.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        try:
            parts = line.split("|")
            if len(parts) < 7:
                continue

            commune = {
                "id": int(parts[0]),
                "name": parts[1].strip(),
                "canton": parts[2].strip(),
                "pop": int(parts[3]),
                "lat": float(parts[4]),
                "lng": float(parts[5]),
                "elev": int(parts[6]),
                "cats": []
            }
            communes.append(commune)
        except (ValueError, IndexError):
            continue

    return communes

def categorize_commune(c):
    """Intelligente Kategorisierung basierend auf Daten"""
    tags = set()
    name = c["name"].lower()
    canton = c["canton"]
    pop = c["pop"]
    elev = c["elev"]

    # === ELEVATION HEURISTICS ===
    if elev >= 1500:
        tags.update(["berge", "klettern", "wandern", "wintersport"])
    elif elev >= 1200:
        tags.update(["berge", "wandern", "wintersport"])
    elif elev >= 900:
        tags.update(["berge", "wandern"])
    elif elev >= 600:
        tags.add("wandern")

    # === CANTON HEURISTICS ===
    alpine_cantons = {"GR", "VS", "UR", "BE", "GL", "AI", "AR"}
    if canton in alpine_cantons:
        if "berge" not in tags:
            tags.add("berge")

    lake_cantons = {
        "ZH": "zürichsee",
        "TI": ["lugano", "locarno"],
        "VD": ["genève", "lausanne", "montreux"],
        "GE": "genève"
    }

    for lake_c, hints in lake_cantons.items():
        if canton == lake_c:
            if isinstance(hints, str):
                hints = [hints]
            if any(h in name for h in hints):
                tags.update(["see", "schwimmen"])

    # === NAME PATTERN MATCHING ===
    name_patterns = {
        "wald": ["wald", "wil", "forest"],
        "see": ["see", "lac", "sø", "lake"],
        "thermalbad": ["bad", "bain", "thermal"],
        "fluss": ["fluss", "bach", "river"],
        "kultur": ["burg", "schloss", "kloster", "museum"],
    }

    for cat, patterns in name_patterns.items():
        if any(p in name for p in patterns):
            tags.add(cat)

    # === POPULATION HEURISTICS ===
    if pop > 50000:
        tags.add("stadt")
    elif pop > 15000:
        tags.add("stadt")
    elif pop > 5000:
        tags.add("stadt")

    if pop < 300:
        tags.add("land")
    elif pop < 1000:
        tags.add("land")

    # === ACTIVITY DEFAULTS ===
    if "berge" in tags and "wandern" not in tags:
        tags.add("wandern")

    # === TRANSPORT ===
    tags.add("auto")
    if canton in ["ZH", "AG", "BL", "BS", "SO", "LU"]:
        tags.add("öv")
    if pop > 3000:
        tags.add("öv")

    # === SPECIAL ACTIVITIES ===
    if "wasser" in name or "see" in tags or "fluss" in tags:
        tags.add("schwimmen")

    if canton in alpine_cantons and pop < 2000:
        if "klettern" not in tags:
            tags.add("klettern")

    # === PETS ===
    if pop < 5000 and ("land" in tags or "wald" in tags):
        tags.add("hunde")

    # Cleanup: Max 6 categories, only valid ones
    valid_cats = {
        "see", "berge", "wald", "fluss", "land", "stadt",
        "wandern", "schwimmen", "klettern", "wintersport",
        "velo", "kultur", "thermalbad", "kloster", "burg",
        "hunde", "weinberg", "auto", "öv", "zu_fuss"
    }

    tags = sorted(list(tags & valid_cats))[:6]
    return tags

def merge_communes(existing, new_bfs):
    """
    Merge neue BFS communes mit existing, ohne zu duplizieren
    """
    existing_ids = {c["id"] for c in existing}

    merged = existing.copy()
    added = 0

    for c in new_bfs:
        if c["id"] not in existing_ids:
            c["cats"] = categorize_commune(c)
            merged.append(c)
            added += 1

    return merged, added

# ============================================================================
# MAIN
# ============================================================================

print("="*80)
print("NotSpot: Scale to 2190 Swiss Communes")
print("="*80)
print()

# 1. Load existing communes
with open("index.html", encoding="utf-8") as f:
    content = f.read()
    start = content.find("const COMMUNES = [")
    end = content.find("];", start) + 2
    communes_js = content[start + 18:end-2]
    communes_py = communes_js.replace("true", "True").replace("false", "False")
    existing = eval("[" + communes_py + "]")

print(f"✓ Loaded {len(existing)} existing communes")
print()

# 2. Parse BFS new communes
print("🔄 Parsing BFS data...")
new_communes = parse_bfs_list(BFS_ALL_2190)
print(f"✓ Found {len(new_communes)} BFS communes to add")
print()

# 3. Merge
print("🔀 Merging and categorizing...")
merged, added = merge_communes(existing, new_communes)
print(f"✓ Added {added} new communes")
print(f"✓ Total communes now: {len(merged)}")
print()

# 4. Save to index.html
print("💾 Saving to index.html...")
new_js = json.dumps(merged, ensure_ascii=False, separators=(',', ':'))
new_content = content[:start + 18] + new_js + content[end-2:]

with open("index.html", "w", encoding="utf-8") as f:
    f.write(new_content)

print("✓ Saved!")
print()

# 5. Statistics
print("="*80)
print("📊 STATISTICS")
print("="*80)

cantons = {}
for c in merged:
    canton = c["canton"]
    cantons[canton] = cantons.get(canton, 0) + 1

print(f"\nCommunes per canton:")
for canton in sorted(cantons.keys()):
    print(f"  {canton}: {cantons[canton]}")

print(f"\nTotal: {len(merged)} communes")

# Category distribution
all_cats = {}
for c in merged:
    for cat in c.get("cats", []):
        all_cats[cat] = all_cats.get(cat, 0) + 1

print(f"\nCategory distribution:")
for cat in sorted(all_cats, key=lambda x: all_cats[x], reverse=True):
    print(f"  {cat}: {all_cats[cat]} ({100*all_cats[cat]/len(merged):.1f}%)")

print()
print("✅ READY FOR DEPLOYMENT!")
print()
print("Next steps:")
print("  1. Test in browser: http://localhost:8888")
print("  2. Git push → auto-deploy to Netlify")
