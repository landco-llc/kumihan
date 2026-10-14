# KUMIHAN — Gemini preview downloads

開発者 / Developer: L&Co.LLC. `0.1.0-preview.1`。ホスト動作未検証 / Host behavior unverified.

[日本語の手順](../docs/installation.gemini.ja.md) · [English instructions](../docs/installation.gemini.md)

CLI extension と Apps スキルアップロードは別の経路です。4スキルの96ファイルは元の公開ソースと同一です。Apps ZIPは各スキル24ファイルを直下に配置し、既存GPT/Codex・Claude ZIPの上位フォルダ形式から包装のみ変更しました。CLI extension ZIPも manifest が直下です。

| Download | SHA256 |
| --- | --- |
| [kumihan-Gemini-CLI-extension-0.1.0-preview.1.zip](extensions/kumihan-Gemini-CLI-extension-0.1.0-preview.1.zip) | `a35afd7f6a62e3fb0f3f25d4aa66b1435ab167bd35e99cebde3ea4c256eefc70` |
| [kumihan-Gemini-Apps-skill-0.1.0-preview.1.zip](skills/kumihan-Gemini-Apps-skill-0.1.0-preview.1.zip) | `caaf6196a800708028b054c111d7c51ee5a199c21cb691325e418627b99c06a1` |
| [kumihan-documents-Gemini-Apps-skill-0.1.0-preview.1.zip](skills/kumihan-documents-Gemini-Apps-skill-0.1.0-preview.1.zip) | `d21484a6607adc330f3dfd30264e2ed44428285a8925f1478557b5d7eea2fe12` |
| [kumihan-review-Gemini-Apps-skill-0.1.0-preview.1.zip](skills/kumihan-review-Gemini-Apps-skill-0.1.0-preview.1.zip) | `101862ab9818b5dbf00facb72f12bd3ea1e6a1f125ed3be13d2c4410bcefbe57` |
| [kumihan-web-Gemini-Apps-skill-0.1.0-preview.1.zip](skills/kumihan-web-Gemini-Apps-skill-0.1.0-preview.1.zip) | `3c1af23ecbe5ebd36814e7de06f2f8e4364308c695b739a860eecfbbee6451da` |

[Member manifest](MANIFEST.json) · [Checksums](SHA256SUMS.txt)

Download this directory, then verify locally on macOS:

```sh
cd "downloads Gemini"
shasum -a 256 -c SHA256SUMS.txt
```

Preview packaging only; no stable release or end-to-end host verification is claimed. Git source and manual uploads have distinct update behavior; see the guides.
