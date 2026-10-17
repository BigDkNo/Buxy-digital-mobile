# BUXY DIGITAL — SYNTH Live: verificări înainte de Google Play

Stadiu: staging https://buxydigital.com/app/synth/ și draft PR #3; păstrăm Android appId com.buxydigital.app.

## Verificări realizate la 17 octombrie 2026
- Validator Hatchable: 0 erori. Au rămas patru avertismente vechi despre API-uri publice.
- Home, Projects, AI, Account: ecrane afișate în browser mobil; imagini și navigare încărcate.
- Forum: endpoint public /api/forum/feed răspunde cu categorii și discuții autentice.
- Acces anonim: /api/client/requests, /api/client/ai-architect și /api/forum/topic-create returnează 401.
- GET cereri cu utilizator de test: 200 și listă goală, fără date ale altor clienți.
- AI cu utilizator de test: 200; brief nou generat în română, fără creare de proiect.
- Cereri, subiecte și răspunsuri invalide: 400; nu s-a modificat niciun conținut persistent.
- În browser, AI și Account afișează solicitarea de autentificare când vizitatorul nu este conectat.
- AI → cerere: brief-ul este precompletat în formular; test end-to-end cu cont autentic real încă necesar.
- APK debug pe ramura feature/synth-live-2026-10-17 construit în GitHub Actions cu identitatea Android existentă, fără semnătură Play.

## Dovezi suplimentare din testarea pe telefon — 17 octombrie 2026
- Utilizator autentificat a confirmat vizual că o cerere BUXY SYNTH Website a fost înregistrată; ecranul a afișat „Cerere trimisă!”, iar numărul cererilor din Account a crescut de la 2 la 3.
- Confirmare vizuală: noua cerere apare în lista Account cu status nou. Nu s-au stocat aici date personale, e-mailuri sau identificatori ai clienților.
- Remediere SYNTH Live v11: statusul new nu mai este numărat drept „în analiză”; contorul indică cererile noi / în așteptare, iar etichetele din listă sunt afișate în română.
- Încă de verificat: dacă butonul „Vezi contul” navighează corect după trimiterea cererii și fluxul real complet AI → formular → cerere.

## Teste manuale necesare înainte de promovarea la versiunea unică
1. Cont: login, logout, recuperare parolă, revenire după login și expirarea sesiunii.
2. AI: generare brief cu cont real, schimbare idee/categorie, rezultat vechi ascuns, erori și fallback.
3. AI → proiect: formular precompletat, verificare date, trimitere controlată de un tester și confirmare în Account/admin.
4. Projects: filtre, cerere Website și App, validări și protecție fără autentificare.
5. Forum: filtre, discuții, răspunsuri, like, topic nou, moderație, erori fără internet.
6. UX Android: back, tastatură, safe areas, scroll, dock, text mărit și accesibilitate.
7. Stabilitate: cold start fără internet, reconectare, test pe Android 12–16.
8. Google Play: verificare Data Safety, politica de confidențialitate, ștergere cont, rapoarte de crash.
9. Release: verificați cel mai mare versionCode deja folosit și utilizați numai cheia de upload existentă.

## Cerința Google Play
Emailul Google Play Support din 17 octombrie 2026 solicită încă 14 zile de testare închisă cu testeri reali.
Testerii trebuie să folosească efectiv aplicația, să transmită feedback și să testeze eventualele remedieri.
Nu confundați mai multe conturi administrate de aceeași persoană cu participarea unor testeri independenți.

Nu faceți merge în main și nu publicați în Google Play până când testele reale sunt trecute.

Staging: https://buxydigital.com/app/synth/
PR: https://github.com/BigDkNo/Buxy-digital-mobile/pull/3
APK debug build: https://github.com/BigDkNo/Buxy-digital-mobile/actions/runs/39038318575

## SYNTH Live v16–v17 — verificări de moderare și AI, 17 octombrie 2026
- Forum: 31 discuții publice și 10 categorii încărcate din API; vizitatorii nu pot publica fără cont.
- Forum v16: butoane separate pentru raportarea subiectului, autorului și răspunsului, precum și blocarea autorilor și gestionarea persoanelor blocate. Raportările folosesc sistemul admin existent. Testul vizual mobil a confirmat apariția controalelor, deschiderea/anularea raportării și blocarea listei private pentru vizitatorii anonimi.
- API /api/forum/user-blocks: anonymous GET/POST 401; user GET 200; acțiune invalidă 400; țintă lipsă 400; țintă inexistentă 404. Blocarea unui autor real și deblocarea lui într-un cont autentic sunt încă NETESTATE.
- AI v17: buton „Semnalează un rezultat AI nepotrivit”, formular cu motiv explicit; endpoint /api/client/ai-report cu sesiune obligatorie, salvare pentru moderare și notificare către administrator. GET anonim nu este permis; POST anonim 401 și POST cu date invalide 400. Nu s-au creat sesizări reale în cadrul acestor teste.
- Politici de date: tabelele forum_user_blocks și ai_content_reports au acces pe rânduri (read/write = own). Verificarea Hatchable a raportat 0 erori; avertismentele rămase sunt pentru 4 API-uri publice existente.
- Fișiere: testerul a confirmat vizual încărcare JPG, afișare în lista proiectului și deschidere în browser pe adresa temporară de stocare.
- Proiecte: testerul a confirmat creare cerere Website și salvarea unui brief AI, comentarii persistente și derularea corectă în fereastra detaliilor.

## Blocaje reale înainte de cererea Google Play
1. Politica Google Play pentru User Generated Content cere acceptarea Termenilor/Regulilor comunității înainte de publicare, moderare continuă, raportare și blocare accesibile. **Termenii/Regulile comunității și acceptarea lor explicită rămân de verificat/implementat în toate fluxurile de publicare.** Nu considerați conformitatea UGC finalizată doar pentru că există butoane.
2. Raportările de conținut și utilizatori trebuie să primească analiză și intervenție în timp util. Verificați procedura de moderare și răspuns, inclusiv AI.
3. Testați cu un cont real: blocare/deblocare autor, raportare de test controlată, raportare AI, moderarea și notificarea, apoi curățarea conținutului de test.
4. Google Play solicită API 36 pentru actualizări începând din 31 august 2026; fișierul de proiect android-version.json declară targetSdk 36 și compileSdk 36. **Nu a fost verificat în Play Console codul ultimei versiuni:** versionCode 2 din GitHub poate necesita creștere înainte de semnarea AAB.
5. Păstrați identificatorul existent com.buxydigital.app, aplicația originală și cheia de semnare; generarea unui AAB release semnat se face după testele pe telefon și validarea datelor Play Console.
6. Pentru testarea închisă, Play Console solicită cel puțin 12 testeri înscriși timp de minimum 14 zile încontinuu pentru conturile personale noi. Obțineți feedback real și documentați corecțiile. Nu înlocuiți testeri independenți cu 12 conturi utilizate doar de aceeași persoană.
7. Verificați politica de confidențialitate și Data Safety pentru fișierele de proiect, moderarea Forumului, AI și raportările utilizatorilor.

Surse oficiale: https://support.google.com/googleplay/android-developer/answer/9876937 ; https://support.google.com/googleplay/android-developer/answer/13985936 ; https://support.google.com/googleplay/android-developer/answer/14151465 ; https://support.google.com/googleplay/android-developer/answer/11926878

