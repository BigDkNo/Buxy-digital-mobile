# SYNTH 04 · SF Humanoid Upgrade — Integration

This folder contains the **SYNTH 04 visual upgrade** (sci-fi + humanoid AI + holographic grid + scanlines) prepared for the Hatchable web app (`public/`).

## Important

`Buxy-digital-mobile` is a **Capacitor wrapper** that loads `https://buxydigital.com/app/` live.
The visual CSS/HTML changes must be applied to the **Hatchable / website** `public/` tree, not inside this Capacitor shell alone.

After Hatchable deploys the upgrade, the Android app will show it automatically (no new APK required for pure CSS/HTML).

## Files on this branch

| Path | Role |
|------|------|
| `public/app/projects/index.html` | Projects page (Humanoid AI copy) |
| `public/app/projects/synth04.css` | Projects styles + neon SF |
| `public/app/projects/synth04.js` | Filters, modals, brief DEMO |
| `public/app/synth04-sf-overlay.css` | **Grid holografic + scanlines** (all pages) |
| `public/app/synth04-global.js` | Dock icons |
| `tools/apply_synth04.py` | Safe patcher (dry-run by default) |

## Apply on Hatchable (DEV only)

```bash
# From repo root, with a DEV copy of Hatchable public/
python synth04/tools/apply_synth04.py /path/to/hatchable/public
python synth04/tools/apply_synth04.py /path/to/hatchable/public --apply --backup /path/to/backup
```

Or copy manually:

1. Copy `synth04/public/app/*` → Hatchable `public/app/`
2. Link `synth04-sf-overlay.css` after existing mobile CSS on all 5 app pages
3. Ensure Projects page uses `synth04.css` + `synth04.js`

## WebP assets

Place the three demo images under `public/app/projects/`:

- `synth04-laptop.webp`
- `synth04-phone.webp`
- `synth04-ribbon.webp`

(Available in the local release ZIP: `BUXY_DIGITAL_SYNTH04_SF_HUMANOID.zip`)

## Changelog (17 Oct 2026)

- Neon palette: `#00ffd5` / `#9b6bff`, deep space `#030508`
- Holographic grid (page + cards)
- Animated scanlines + AI dock scan flash
- Copy: SYNTHETIC VISION · HUMANOID AI, Humanoid AI Architect
- Respects `prefers-reduced-motion`

Do **not** publish to production until reviewed on device (iPhone + Android).
