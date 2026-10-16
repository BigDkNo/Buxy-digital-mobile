"""Configure the ephemeral Capacitor Android project without handling secrets.

Gradle signing passwords are provided at build time via ORG_GRADLE_PROJECT_*
environment variables. No passwords or private keys are stored by this script.
"""

import json
import re
from pathlib import Path


class AndroidConfigurationError(ValueError):
    pass


def substitute_once(source: str, pattern: str, replacement, label: str) -> str:
    updated, count = re.subn(pattern, replacement, source, count=1, flags=re.MULTILINE)
    if count != 1:
        raise AndroidConfigurationError(f"Expected Android configuration field: {label}")
    return updated


def configure(root: Path) -> None:
    version = json.loads((root / 'android-version.json').read_text(encoding='utf-8'))
    code = version.get('versionCode')
    name = version.get('versionName')
    sdk = version.get('compileSdk')
    target = version.get('targetSdk')
    if type(code) is not int or code < 1:
        raise AndroidConfigurationError('versionCode must be a positive integer')
    if not isinstance(name, str) or not re.fullmatch(r'[0-9]+(?:\.[0-9]+){1,3}', name):
        raise AndroidConfigurationError('versionName must be a numeric dotted version')
    if type(sdk) is not int or type(target) is not int or sdk < 35 or target < 35 or target > sdk:
        raise AndroidConfigurationError('Invalid Android SDK versions')

    variables_path = root / 'android' / 'variables.gradle'
    app_path = root / 'android' / 'app' / 'build.gradle'
    variables = variables_path.read_text(encoding='utf-8')
    app = app_path.read_text(encoding='utf-8')

    variables = substitute_once(variables, r'^(\s*compileSdkVersion\s*=\s*)\d+',
                                lambda match: f'{match.group(1)}{sdk}', 'compileSdkVersion')
    variables = substitute_once(variables, r'^(\s*targetSdkVersion\s*=\s*)\d+',
                                lambda match: f'{match.group(1)}{target}', 'targetSdkVersion')
    app = substitute_once(app, r'^(\s*versionCode\s+)\d+',
                          lambda match: f'{match.group(1)}{code}', 'versionCode')
    app = substitute_once(app, r'^(\s*versionName\s+)["\'][^"\']+["\']',
                          lambda match: f'{match.group(1)}"{name}"', 'versionName')

    if app.count('android {') != 1 or app.count('buildTypes {') != 1:
        raise AndroidConfigurationError('Generated Gradle layout changed; manual review required')
    signing = """android {
    signingConfigs {
        release {
            storeFile file('buxy-upload-key.jks')
            storePassword project.findProperty('BUXY_STORE_PASSWORD')
            keyAlias project.findProperty('BUXY_KEY_ALIAS')
            keyPassword project.findProperty('BUXY_KEY_PASSWORD')
        }
    }
"""
    app = app.replace('android {', signing, 1)
    before, after = app.split('buildTypes {', 1)
    if after.count('release {') != 1:
        raise AndroidConfigurationError('Expected one release buildType in Gradle')
    after = after.replace('release {', 'release {\n            signingConfig signingConfigs.release', 1)
    app = before + 'buildTypes {' + after

    # Write both files only after all validation succeeds.
    variables_path.write_text(variables, encoding='utf-8')
    app_path.write_text(app, encoding='utf-8')
    print(f'Android build configured for versionCode={code}, versionName={name}, targetSdk={target}')


if __name__ == '__main__':
    configure(Path(__file__).resolve().parents[1])
