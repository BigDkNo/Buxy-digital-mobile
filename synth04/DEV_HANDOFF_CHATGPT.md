# BUXY DIGITAL — SYNTH 04: predare DEV ChatGPT ↔ Grok

**Stadiu:** codul de integrare este pe ramura de dezvoltare; **NU a fost aplicat pe Hatchable sau Google Play**.

## Ce am verificat

- Site-ul mobil BUXY DIGITAL rulează HTML/CSS/JS din Hatchable `public/app/`, încărcat de Android prin Capacitor.
- Proiectul GitHub `BigDkNo/Buxy-digital-mobile` este în principal wrapper Android; **nu conține sursa integrală Hatchable**.
- Branch-ul Grok `feature/synth04-sf-humanoid` conține overlay-ul Sci-Fi, dar are o versiune scurtată a `projects/index.html` și a `synth04.css`.
- Din pachetul Grok lipsesc 3 WebP și `synth04-global.css`, deci `tools/apply_synth04.py` nu poate rula integral.
- Arhiva completă creată anterior conține pagina Projects reală, CSS/JS complet, `synth04-global.css`, `synth04-global.js`, cele 3 imagini originale WebP.
- S-a încercat `fork_project` pentru o clonă DEV în Hatchable. Copierea a fost blocată de configurația proiectului sursă: regulile `hatchable.toml` referă tabele fără migrații de creare. **Nu am intervenit în proiectul original pentru a rezolva forțat această problemă.**

## Soluția GitHub — fără prod

Noul script `synth04/tools/apply_synth04_complete_dev.py` importă conținutul **din arhiva completă revizuită**, cu SHA256 verificat:

`BUXY_DIGITAL_SYNTH04_5_PAGINI_DEV_COMPLET.zip`

SHA256 al arhivei:
`bac708d9f2f4e4b6a342157c3e7dfbdb3e56f054aab8dd2196092102b2aa9810`

Această arhivă trebuie furnizată de proprietar din artefactele proiectului ChatGPT. Nu folosiți starter-ul React întreg drept aplicație live.

```bash
# Creați o copie locală DEV a surselor Hatchable care include:
# public/app/index.html, projects/, ai/, forum/, account/,
# app.js, ai.js, forum.js, account.js, mobile.css, sections.css, sw.js

cd /path/to/your/dev-checkout
touch .buxy-synth04-dev

# Verificare fără modificări:
python /path/to/android-repo/synth04/tools/apply_synth04_complete_dev.py \
  ./public --package /path/to/BUXY_DIGITAL_SYNTH04_5_PAGINI_DEV_COMPLET.zip

# Doar DUPĂ verificare; backup obligatoriu, într-un director inexistent:
python /path/to/android-repo/synth04/tools/apply_synth04_complete_dev.py \
  ./public --package /path/to/BUXY_DIGITAL_SYNTH04_5_PAGINI_DEV_COMPLET.zip \
  --apply --backup /path/to/new-empty-backup-path
```

**Rezultatul rămâne LOCAL.** Nu execută niciun deploy, nu atinge API-uri externe și nu accesează datele clienților.

## Ce integrează

1. Projects: HTML/CSS/JS **complete** și carduri cu imaginile originale laptop/telefon/ribbon.
2. Home, AI, Forum și Account: include tema comună fără să elimine logica/rutele existente.
3. SF Humanoid: overlay-ul Grok cu grid și scanlines, opțional, cu `prefers-reduced-motion`.
4. Service worker: pre-cache static pentru noile resurse, fără API-uri ori date private.
5. Navigația permanentă `/app/`, `/app/projects/`, `/app/ai/`, `/app/forum/`, `/app/account/`.

## Ce trebuie rezolvat înainte de integrare reală

1. Obținerea unei copii complete a sursei web Hatchable în spațiul DEV (fără a umbla în site-ul activ).
2. Verificarea diferențelor de la această ramură și executarea dry-run pe acea copie.
3. Test mobil real al autentificării, AI real, Forum, Account, navigării și offline.
4. Corectarea imaginilor/contrastului doar pe DEV; apoi aprobare explicită de publicare.

**Nu faceți merge în main, nu aplicați peste producție și nu lansați build Play.**
