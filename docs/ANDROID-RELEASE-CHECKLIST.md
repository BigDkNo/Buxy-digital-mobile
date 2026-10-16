# BUXY DIGITAL Android release and security checklist

## Existing upload key: preserve it

- Google Play manages the **app signing key**. GitHub Actions uses the separate **upload key** to sign the Android App Bundle (AAB) submitted to Google Play.
- The registered upload certificate SHA-256 is:
  `05:10:39:B3:53:F4:DD:B9:83:84:A1:D9:3F:47:51:44:9E:9A:8F:46:A4:BB:3C:B1:0A:75:CB:C9:0B:9B:9A:7A`.
- Before uploading an AAB, compare this with the public certificate embedded in the signed bundle using `keytool -printcert -jarfile app-release.aab` (or `jarsigner -verify -certs -verbose app-release.aab`).
- Never upload a `.jks`, private key, keystore password, signing password, or raw GitHub Secret to a public artifact or repository. Do not email or paste those values into chat.
- The legacy key-generation workflow is disabled in this review branch; **do not request an upload-key reset** without checking ownership, a secure backup, and the existing Google Play enrollment.

## Versioning, builds and releases

- `android-version.json` is the release configuration. The starting values (`versionCode: 2`, `versionName: 1.0.1`) **match the prior workflow**, not necessarily the latest version published on Google Play.
- **Before the next Play Console upload**, check the maximum `versionCode` across all existing Play tracks. Any new AAB must have a higher `versionCode` than versions already uploaded. Increase the version in a separately reviewed change.
- GitHub Actions compiles using the existing signing key from managed secrets. Passwords are supplied at Gradle run time through `ORG_GRADLE_PROJECT_*` environment variables, and are never written to `gradle.properties`.
- The workflow uploads only the signed `app-release.aab`, not the keystore. The keystore only exists on the ephemeral GitHub-hosted runner.
- Dependency installation still uses `npm install`. For reproducible builds, create a genuine `package-lock.json` with a package registry available, review it, commit it, and **then** change CI to `npm ci`. This branch deliberately does not fabricate a lockfile.
- Test the Android Gradle configuration script locally: `python3 -m unittest discover -s tests -v`.

## App behavior and offline testing

The Capacitor configuration uses `server.url: https://buxydigital.com/app/`, which causes the Android WebView to load a remote website. The bundled `index.html` is only a basic loading placeholder and **does not provide a functional offline fallback**. Do not remove `server.url` without a product decision: doing so changes how users interact with the app.

Before approving a production release, manually test on a physical Android device:

1. Start on reliable Wi-Fi: verify login, navigation, buttons, and links.
2. Enable Airplane Mode before cold starting the app: observe the error/blank screen and whether the user has a clear recovery action.
3. Start online, disconnect mid-session, reconnect: ensure state and navigation recover appropriately.
4. Simulate website unavailability / HTTP 5xx: verify a visible error and retry path.
5. Verify that login credentials and private user data are not exposed in WebView logs or URL query strings.
6. Verify back button, accessibility, loading behavior, and Android 15/16 rendering.

**Proposed next phase (not implemented here):** choose between a native offline error/retry screen, locally bundled UI, or a dedicated offline-first application. That is an architectural change and needs separate acceptance tests.

## Review guardrails

This branch is for review only. Do not merge it, launch a new workflow, release to a test/production Play track, rotate keys, or change GitHub Secrets without explicit approval.
