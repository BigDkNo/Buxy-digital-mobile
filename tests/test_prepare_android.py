import json
import tempfile
import unittest
from pathlib import Path

from scripts.prepare_android import AndroidConfigurationError, configure


class AndroidBuildPreparationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'android' / 'app').mkdir(parents=True)
        (self.root / 'android-version.json').write_text(json.dumps({
            'versionCode': 2, 'versionName': '1.0.1', 'compileSdk': 36, 'targetSdk': 36
        }), encoding='utf-8')
        (self.root / 'android' / 'variables.gradle').write_text(
            'ext {\n compileSdkVersion = 35\n targetSdkVersion = 35\n}\n', encoding='utf-8')
        (self.root / 'android' / 'app' / 'build.gradle').write_text(
            'android {\n defaultConfig {\n versionCode 1\n versionName "1.0"\n }\n'
            ' buildTypes {\n  release {\n   minifyEnabled false\n  }\n }\n}\n', encoding='utf-8')

    def test_configure_preserves_release_version_and_keeps_secrets_out(self):
        configure(self.root)
        app = (self.root / 'android' / 'app' / 'build.gradle').read_text()
        variables = (self.root / 'android' / 'variables.gradle').read_text()
        self.assertIn('versionCode 2', app)
        self.assertIn('versionName "1.0.1"', app)
        self.assertIn('signingConfig signingConfigs.release', app)
        self.assertIn("project.findProperty('BUXY_KEY_PASSWORD')", app)
        self.assertNotIn('password123', app)
        self.assertIn('compileSdkVersion = 36', variables)
        self.assertIn('targetSdkVersion = 36', variables)

    def test_unexpected_template_stops_before_writing(self):
        gradle = self.root / 'android' / 'app' / 'build.gradle'
        original = gradle.read_text().replace('buildTypes {', 'differentBlock {')
        gradle.write_text(original)
        with self.assertRaises(AndroidConfigurationError):
            configure(self.root)
        self.assertEqual(gradle.read_text(), original)
        self.assertIn('compileSdkVersion = 35', (self.root / 'android' / 'variables.gradle').read_text())

    def test_invalid_version_rejected(self):
        (self.root / 'android-version.json').write_text(json.dumps({
            'versionCode': 0, 'versionName': '1.0.1', 'compileSdk': 36, 'targetSdk': 36
        }))
        with self.assertRaises(AndroidConfigurationError):
            configure(self.root)


if __name__ == '__main__':
    unittest.main()
