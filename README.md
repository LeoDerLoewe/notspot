# NotSpot – Anti-Hotspot Discovery App

> **Hotspot war gestern. NotSpot ist heute.**

NotSpot is a Swiss anti-tourism discovery app that redirects traveler flows away from overcrowded hotspots (Zürich, Interlaken, Luzern) to authentic, undiscovered small communes across Switzerland.

## 🎯 Vision

- **Redistribute Tourism**: Push visitors to small communes (< 5k inhabitants)
- **Relieve Hotspots**: Reduce traffic and congestion in popular destinations  
- **Discover Real Switzerland**: 615+ authentic communities across all 26 cantons
- **Support Sustainable Tourism**: Enable tourism to flow where it's needed

## 🚀 Quick Start

### Access the App
- **Live**: https://notspot.ch
- **Local**: `python3 -m http.server 8888` → http://localhost:8888

### How It Works
1. **Press the Button**: "Spin" to get a random Swiss commune
2. **Set Filters**: 
   - Transport mode (Auto, ÖV, Velo, Zu Fuss)
   - Environment (Berge, See, Wald, Land)
   - Activities (Wandern, Schwimmen, Klettern, etc.)
3. **Get Recommendations**: Algorithm suggests nearby NotSpots, never hotspots
4. **Explore**: Get Google Maps directions, view POIs, rate your discovery

## 📊 Algorithm (Anti-Hotspot)

### How It Selects Communes

**Population-based boost:**
- `pop < 500` → 4x weight boost (prime NotSpot!)
- `pop < 1,000` → 3x boost
- `pop > 100,000` → 0.1x penalty (avoid cities)

**Canton-based adjustment:**
- Hotspot cantons (ZH, LU, BS, GE, BE) → 0.5x penalty
- Other cantons → 1.3x boost

**Distance scoring (linear curve):**
- Closer locations preferred, but not penalized at max distance
- Formula: `max(0.6, 1.0 - (ratio * 0.4))`
- Result: Realistic travel times, genuine locality

**Persona-based soft boosts:**
- 6 personas (Entdecker, Naturmensch, Kulturliebhaber, etc.)
- Each has category preferences for dynamic recommendations

### Example: Zürich User
**Filter:** Auto mode (180km), Schwimmen + Wandern
**Result (Top 3):**
1. **Bauen (UR, 139 inhabitants)** – See + Schwimmen + Berge – 53km away
2. **Vorderthal (SZ, 434 inhabitants)** – Wald + Wandern – 44km away  
3. **Sisikon (UR, 459 inhabitants)** – Wandern + Berge – 50km away

*(Not Luzern, not Interlaken, not Zugersee-suburbs – real NotSpots)*

## 🏗️ Architecture

```
index.html                 ← Single-file vanilla JS app (~2100 lines)
├─ HTML/CSS/JS inline      ← Progressive enhancement, no build step
├─ COMMUNES array           ← 615 Swiss communes (JSON)
├─ Anti-hotspot algorithm   ← getWeight(), getDistScore(), filterPool()
├─ OSM/Leaflet maps         ← POI discovery via Overpass API
└─ PostHog analytics        ← GDPR consent, anonymized tracking

communes.json              ← Backup of commune data
netlify.toml               ← Cache headers, redirects (CH domains)
test_algorithm.py          ← Validation suite (personas, edge cases)
scale_to_2190_communes.py  ← Semi-automation for full dataset expansion
```

## 📈 Data & Scaling

### Current Status (MVP)
- **615 communes** (all major + small communities)
- **Tested personas**: Kindergruppe, Familie, Entdecker, Naturmensch
- **Algorithms validated**: Distance, popularity, canton biases

### Roadmap to 2190 Communes
1. **Download BFS dataset**: https://www.bfs.admin.ch/bfs/de/home/dienstleistungen/gis/geodaten.html
2. **Run scale_to_2190_communes.py**: Auto-categorization via heuristics
3. **Deploy**: No breaking changes, seamless scaling

## 🔧 Development

### Make Changes
```bash
# Edit index.html directly (single-file app)
vim index.html

# No build step needed – refresh browser
```

### Test Algorithm
```bash
python3 test_algorithm.py

# Output: Validates recommendations for different personas
# Ensures small communes rank highest
```

### Local Server
```bash
python3 -m http.server 8888
# Open http://localhost:8888
```

### Backup Before Major Changes
```bash
cp index.html index.html.backup-$(date +%Y%m%d)
```

## 🌐 Deployment

### To Netlify
```bash
# Option 1: Git + GitHub (auto-deploy on push)
git push origin main

# Option 2: Netlify CLI
netlify deploy --prod --dir .

# Option 3: Manual (drag & drop index.html to app.netlify.com)
```

**Custom domains:**
- notspot.ch (primary)
- notspot.de, notspot.at (redirects)

## 📊 Analytics & Impact

### PostHog Tracking
- `spin_started`: User initiates discovery
- `spin_result_shown`: Recommendation delivered + metadata (population, distance, persona)
- `poi_viewed`: POI exploration
- `location_set`: GPS vs. manual location choice

### Proof of Impact (Roadmap)
- Photo uploads from visitors
- "Was dort"-badge system
- Public impact dashboard: "X visitors to [commune] this month"
- Heatmaps showing tourism redistribution

## 🔒 Security & Privacy

- **GDPR Compliant**: Consent banner, analytics opt-out
- **No server-side storage**: Location stored locally only
- **RLS on data**: Commune data publicly available (no auth needed)
- **Photo bucket** (future): Will require signed URLs before production multi-tenant

## 📚 Key Files & Functions

| File | Key Functions | Purpose |
|------|---------------|---------|
| `index.html` | `getWeight()` | Popularity-based filtering |
| `index.html` | `getDistScore()` | Distance preference curve |
| `index.html` | `filterPool()` | Category + distance filtering |
| `index.html` | `weightedPick()` | Stochastic selection with weighting |
| `index.html` | `generateStory()` | Personalized recommendation narratives |
| `test_algorithm.py` | `score_commune()` | Test harness for algorithm validation |
| `scale_to_2190_communes.py` | `categorize_commune()` | Heuristic-based auto-tagging |

## 🎨 Design System

**Colors:**
- `--coral: #FF5B47` – Primary CTA (NotSpot brand)
- `--mint: #A8E6CF` – Success, RLS active
- `--night: #1A1B3A` – Text, dark backgrounds
- `--cream-bg: #FFF8F0` – Page background

**Typography:**
- Display: Playfair Display (brand, italic)
- Body: Space Grotesk
- Mono: JetBrains Mono

**Spacing:** Mobile-first, 480px viewport, safe-area-insets for notch devices

## 🤝 Contributing

NotSpot is actively maintained. To contribute:

1. **Test the algorithm** with local changes
2. **Document changes** in commit messages (see history)
3. **No build step** – vanilla JS only
4. **Backup before major edits**

## 📝 Roadmap

### Phase 1 (MVP – Now)
- ✅ Anti-hotspot algorithm
- ✅ 615 Swiss communes
- ✅ Persona system
- ✅ OSM/POI integration
- → **Deploy to production**

### Phase 2 (This Week)
- [ ] Scale to 2190 communes
- [ ] Photo upload + gallery
- [ ] "Was dort"-badge system
- [ ] Public impact dashboard

### Phase 3 (Future)
- [ ] Real-time traffic integration (TomTom API)
- [ ] ML: Correlate NotSpot clicks → traffic reduction
- [ ] Multi-language support (FR, IT, EN)
- [ ] Offline mode improvements
- [ ] Community tagging/feedback

## 📞 Contact

**Maintainer:** Leo  
**Email:** info@notspot.ch  
**Website:** https://notspot.ch  
**Instagram:** @notspot.ch

---

**Hotspot war gestern. NotSpot ist heute.** 🌲✨
