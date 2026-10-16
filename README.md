# BUXY DIGITAL Mobile

A lightweight Capacitor Android wrapper around the BUXY DIGITAL web application at `https://buxydigital.com/app/`.

## Review branch changes

The Android build workflow now uses explicit, reviewable release version settings in `android-version.json`. A Python preparation script patches the temporary Android project and its signing configuration. The existing upload key is restored from GitHub Secrets; the workflow no longer writes signing passwords into a generated Gradle properties file or offers a workflow that creates an extra private key artifact.

The app still relies on the live website and therefore does **not** work offline. See [Android release and security checklist](docs/ANDROID-RELEASE-CHECKLIST.md) for limitations, planned tests, and next steps.

## Local checks

```sh
python3 -m unittest discover -s tests -v
npm install
npm run build
```

A package lockfile is intentionally deferred until npm dependencies can be resolved with a package registry; no synthetic lockfile is included. This review does not publish builds or change credentials.
