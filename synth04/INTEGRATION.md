# SYNTH 04 · SF Humanoid — Integration (APROBAT DEV)

**Direcție oficială (17.10.2026):** SF Humanoid — aprobată de proprietar.
Vezi `DECISION_SF_HUMANOID.md`.

## Specificație
- Background `#030508` · mint `#00ffd5` · violet `#9b6bff` · cyan `#00e8ff`
- Grid holografic + scanlines animate
- Copy: `SYNTHETIC VISION · HUMANOID AI`, `Humanoid AI Architect`

## Important
`Buxy-digital-mobile` = Capacitor wrapper → `https://buxydigital.com/app/` live.
CSS/HTML se aplică pe **Hatchable `public/`**. După deploy Hatchable, Android vede tema automat.

## Fișiere
| Path | Rol |
|------|-----|
| `DECISION_SF_HUMANOID.md` | Decizia oficială |
| `public/app/synth04-sf-overlay.css` | Grid + scanlines |
| `public/app/projects/synth04.css` | Projects SF |
| `public/app/projects/synth04.js` | Filtre / modale DEMO |
| `public/app/projects/index.html` | Copy humanoid |
| `public/app/synth04-global.js` | Dock |
| `tools/apply_synth04.py` | Patcher dry-run implicit |

## Aplicare Hatchable DEV
```bash
python synth04/tools/apply_synth04.py /path/to/hatchable/public
python synth04/tools/apply_synth04.py /path/to/hatchable/public --apply --backup /path/to/backup
```

Nu publica pe producție fără test pe device + acord explicit.
