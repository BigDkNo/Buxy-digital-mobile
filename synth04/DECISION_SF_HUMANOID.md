# Decizie: direcția SF Humanoid — aprobată

**Data:** 17 octombrie 2026  
**Decident:** Proprietar BUXY  
**Execuție:** Grok  

## Decizie
Se adoptă **SYNTH 04 · SF Humanoid** ca direcție vizuală oficială pentru staging DEV (nu producție până la test pe device + aprobare explicită de publicare).

## Specificație vizuală
- Background deep space: `#030508`
- Mint electric: `#00ffd5`
- Violet: `#9b6bff`
- Cyan accent: `#00e8ff`
- Gold UI: `#e8c47a`
- Holographic grid (pagină + carduri)
- Scanlines animate + scan flash pe AI dock / Architect
- Copy: `SYNTHETIC VISION · HUMANOID AI`, `Humanoid AI Architect`
- Respectă `prefers-reduced-motion`

## Unde e implementat
- Branch GitHub: `feature/synth04-sf-humanoid` pe `BigDkNo/Buxy-digital-mobile`
- Pachet local: `BUXY_DIGITAL_SYNTH04_SF_HUMANOID.zip`
- Overlay: `synth04/public/app/synth04-sf-overlay.css`
- CSS full local: `synth04-global.css`, `projects/synth04.css`
- HTML Projects cu copy humanoid

## Ce NU s-a făcut (blocaje externe)
- Aplicare pe Hatchable `public/` — fără acces la mediul DEV Hatchable
- Publicare pe buxydigital.com / Google Play — interzisă fără aprobare
- Art final humanoid (WebP) — concept generat; asset-urile rămân ribbon/device abstract până la art final

## Următorii pași
1. Furnizare cale Hatchable DEV sau repo web → aplicare `apply_synth04.py`
2. Test iPhone + Android
3. Aprobare publicare de către proprietar
