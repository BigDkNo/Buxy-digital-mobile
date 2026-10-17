# SYNTH 04 · SF Humanoid Upgrade — Integration

This folder contains the **SYNTH 04 visual upgrade** (sci-fi + humanoid AI + holographic grid + scanlines) prepared for the Hatchable web app (`public/`).

## Important

`Buxy-digital-mobile` is a **Capacitor wrapper** that loads `https://buxydigital.com/app/` live.
The visual CSS/HTML changes must be applied to the **Hatchable / website** `public/` tree, not inside this Capacitor shell alone.

After Hatchable deploys the upgrade, the Android app will show it automatically (no new APK required for pure CSS/HTML).

## Files

| Path | Role |
|------|------|
| `public/app/projects/index.html` | Projects page (Humanoid AI copy + structure) |
| `public/app/projects/synth04.css` | Projects-only styles + grid/scanlines |
| `public/app/projects/synth04.js` | Projects interactivity (filters, modals DEMO) |
| `public/app/synth04-global.css` | Shared theme for Home / AI / Forum / Account |
| `public/app/synth04-global.js` | Dock icons / active state |
| `tools/apply_synth04.py` | Safe patcher (dry-run by default) |

## WebP assets

Copy the three original demo images into Hatchable:

- `public/app/projects/synth04-laptop.webp`
- `public/app/projects/synth04-phone.webp`
- `public/app/projects/synth04-ribbon.webp`

(Humanoid concept images were generated as design reference; replace these WebPs when final art is ready.)

## Apply on Hatchable (DEV only)

```bash
# 1. Copy a DEV snapshot of Hatchable public/
python tools/apply_synth04.py /path/to/hatchable/public          # dry-run
python tools/apply_synth04.py /path/to/hatchable/public --apply --backup /path/to/backup
```

Do **not** publish to production until reviewed on device (iPhone + Android).

## Changelog (17 Oct 2026)

- Neon palette: `#00ffd5` / `#9b6bff`, deep space `#030508`
- Holographic grid (page + cards)
- Animated scanlines + AI dock scan flash
- Copy: SYNTHETIC VISION · HUMANOID AI, Humanoid AI Architect
- Respects `prefers-reduced-motion`
