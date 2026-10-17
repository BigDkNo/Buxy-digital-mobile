# BUXY DIGITAL MOBILE — SYNTH 04 (SF Humanoid Upgrade)

## Stare: integrare vizuală pentru toate cele 5 pagini · Upgrade Sci-Fi / Humanoid AI

**Data:** 17 octombrie 2026. Aceasta este o implementare de cod, nu o recomandare generică. **Nu este publicată pe buxydigital.com, în Hatchable sau în Google Play.**

### Upgrade 17.10.2026 — Mai SF + Humanoid + Scanlines / Grid
- Paletă neon intensificată (cyan electric `#00ffd5`, violet `#9b6bff`, deep space background).
- Glow-uri și umbre holografice mai puternice pe carduri, filtre și butonul AI din dock.
- **Holographic grid** pe tot ecranul (mask radial) + grid dens pe carduri / panouri.
- **Scanlines** animate (overlay + mișcare verticală) pe toate paginile.
- Scan flash orizontal pe butonul AI din dock și pe bara Architect.
- Overline + copy: „SYNTHETIC VISION · HUMANOID AI”, „Humanoid AI Architect”.
- Animație pulse pe simbolul intro.
- Respectă `prefers-reduced-motion`.

### Ce este în acest folder

| Path | Rol |
|------|-----|
| `public/app/projects/index.html` | Pagina Projects (copy humanoid + structură) |
| `public/app/projects/synth04.css` | Stil Projects + grid/scanlines |
| `public/app/projects/synth04.js` | Filtre, modale DEMO |
| `public/app/synth04-global.css` | Temă comună Home / AI / Forum / Account |
| `public/app/synth04-global.js` | Icoane dock |
| `tools/apply_synth04.py` | Patcher safe (dry-run implicit) |
| `INTEGRATION.md` | Cum se aplică pe Hatchable |

### Cum se aplică (DEV)

1. Copie DEV a directorului `public/` din Hatchable.
2. `python tools/apply_synth04.py /cale/catre/public` (dry-run).
3. `python tools/apply_synth04.py /cale/catre/public --apply --backup /cale/backup`.
4. Test pe device. **Publică doar după acord explicit.**

Vezi [INTEGRATION.md](INTEGRATION.md) pentru detalii complete.
