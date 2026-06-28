#!/usr/bin/env python3
"""
test_algorithm.py - Validiere dass der Algorithmus echte NotSpots vorschlägt
"""

import json
import re
from math import radians, cos, sin, asin, sqrt

def haversine_km(lat1, lon1, lat2, lon2):
    """Calculate distance between two points in km"""
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return 6371 * c

# Load COMMUNES
with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()
    pattern = r"const COMMUNES = (\[.*?\]);"
    match = re.search(pattern, content, re.DOTALL)
    communes_str = match.group(1)
    communes = json.loads(communes_str)

# Constants
HOT_CANTONS = ["ZH", "LU", "BS", "GE", "BE"]
HOT_NAMES = ["zürich", "luzern", "bern", "genf", "interlaken", "zermatt", "basel", "lugano", "lausanne", "davos", "grindelwald", "st. moritz"]
MAX_DIST = {"auto": 180, "öv": 120, "velo": 35, "zu_fuss": 8}

def get_weight(c, session_counts=None, persona_name="entdecker"):
    """Replicate getWeight() logic"""
    if session_counts is None:
        session_counts = {}

    w = 1.0
    pop = c.get("pop", 1000)
    name = c.get("name", "").lower()

    # Population boost
    if pop < 200:
        w *= 5
    elif pop < 500:
        w *= 4
    elif pop < 1000:
        w *= 3
    elif pop < 3000:
        w *= 2
    elif pop < 5000:
        w *= 1.5
    elif pop < 10000:
        w *= 1.2
    elif pop > 100000:
        w *= 0.1
    elif pop > 50000:
        w *= 0.2
    elif pop > 20000:
        w *= 0.5

    # Canton boost
    if c.get("canton") in HOT_CANTONS:
        w *= 0.5
    else:
        w *= 1.3

    # Session count penalty (avoid repeats)
    canton = c.get("canton")
    w *= 1 / (1 + (session_counts.get(canton, 0) * 0.5))

    # Hot name penalty
    if any(n in name for n in HOT_NAMES):
        w *= 0.2

    return max(0.001, w)

def get_dist_score(c, user_lat, user_lng, transport_modes):
    """Replicate getDistScore() logic"""
    dist = haversine_km(user_lat, user_lng, c.get("lat"), c.get("lng"))
    max_dist = max([MAX_DIST.get(t, 150) for t in transport_modes])
    ratio = min(1, dist / max_dist)
    return max(0.6, 1.0 - (ratio * 0.4))

def test_scenario(user_lat, user_lng, transport_modes, env_filters=None):
    """Test: User at location with filters → what gets recommended?"""
    if env_filters is None:
        env_filters = []

    print("=" * 80)
    print(f"🧪 TEST SCENARIO")
    print(f"   User Location: {user_lat}, {user_lng}")
    print(f"   Transport: {transport_modes}")
    print(f"   Filters: {env_filters}")
    print("=" * 80)
    print()

    # Filter pool (hard cutoff: distance + categories)
    pool = []
    for c in communes:
        # Distance filter
        dist = haversine_km(user_lat, user_lng, c.get("lat"), c.get("lng"))
        max_dist = max([MAX_DIST.get(t, 150) for t in transport_modes])
        if dist > max_dist:
            continue

        # Category filter
        cats = c.get("cats", [])
        if env_filters and not any(f in cats for f in env_filters):
            continue

        pool.append(c)

    print(f"✓ Pool nach Filtering: {len(pool)} Gemeinden")
    print()

    # Score each commune
    scored = []
    for c in pool:
        w = get_weight(c)
        d = get_dist_score(c, user_lat, user_lng, transport_modes)
        final_score = w * (d ** 1.5)  # pow(distScore, 1.5)

        scored.append({
            "name": c.get("name"),
            "canton": c.get("canton"),
            "pop": c.get("pop"),
            "dist_km": round(haversine_km(user_lat, user_lng, c.get("lat"), c.get("lng")), 1),
            "weight": round(w, 3),
            "dist_score": round(d, 3),
            "final_score": round(final_score, 3),
            "cats": c.get("cats", [])
        })

    # Sort by final score
    scored.sort(key=lambda x: x["final_score"], reverse=True)

    print("🏆 TOP 10 Recommendations (nach Algorithmus):")
    print()
    for i, c in enumerate(scored[:10], 1):
        is_small = "✅ SMALL" if c["pop"] < 5000 else "⚠️  LARGE"
        is_hotspot = "⚠️  HOTSPOT" if c["canton"] in HOT_CANTONS else "✓ NotSpot"
        print(f"{i:2d}. {c['name']:30s} | Pop:{c['pop']:6d} | {is_small:10s} | {is_hotspot:10s}")
        print(f"    Canton: {c['canton']:3s} | Dist: {c['dist_km']:5.1f}km | Score: {c['final_score']:8.3f} (w={c['weight']:.3f}, d={c['dist_score']:.3f})")
        print(f"    Cats: {', '.join(c['cats'][:4])}")
        print()

    # Validation
    print("=" * 80)
    print("✓ VALIDATION CHECK:")
    top3_pop = [c["pop"] for c in scored[:3]]
    top3_canton = [c["canton"] for c in scored[:3]]
    top3_small = sum(1 for p in top3_pop if p < 5000)
    top3_notspot = sum(1 for can in top3_canton if can not in HOT_CANTONS)

    print(f"  Top 3: {top3_small}/3 sind Klein-Gemeinden (<5k) ✓" if top3_small >= 2 else f"  Top 3: {top3_small}/3 Klein-Gemeinden ⚠️ PROBLEM!")
    print(f"  Top 3: {top3_notspot}/3 sind echte NotSpots ✓" if top3_notspot >= 2 else f"  Top 3: {top3_notspot}/3 echte NotSpots ⚠️ PROBLEM!")
    print()

# === TEST CASES ===
print("\n\n")
print("╔" + "=" * 78 + "╗")
print("║" + " NotSpot Algorithm Validation Test Suite ".center(78) + "║")
print("╚" + "=" * 78 + "╝")
print("\n")

# Test 1: Zürich User, Auto only
print("TEST 1: User in Zürich, Filter: 'Auto' (180km Radius)")
test_scenario(47.3769, 8.5417, ["auto"])

# Test 2: Zürich User, Auto + Wandern
print("\n\nTEST 2: User in Zürich, Filter: 'Auto' + 'Wandern'")
test_scenario(47.3769, 8.5417, ["auto"], ["wandern"])

# Test 3: Zürich User, zu Fuss (8km)
print("\n\nTEST 3: User in Zürich, Filter: 'zu Fuss' (8km Radius)")
test_scenario(47.3769, 8.5417, ["zu_fuss"])

# Test 4: Bern User, Auto
print("\n\nTEST 4: User in Bern, Filter: 'Auto'")
test_scenario(46.9481, 7.4474, ["auto"])

print("\n\n" + "=" * 80)
print("✅ TESTS COMPLETE")
print("=" * 80)
