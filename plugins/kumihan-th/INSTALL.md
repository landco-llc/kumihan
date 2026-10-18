# การติดตั้ง / Installation / 導入

ไฟล์ซอร์สสำหรับตรวจสอบยังไม่เผยแพร่ ลิงก์ [Thai v0.1.1 release](https://github.com/landco-llc/kumihan/releases/tag/kumihan-th-v0.1.1) เมื่อเผยแพร่แล้ว ตรวจ SHA256SUMS.txt และ MANIFEST.json ก่อนแตกไฟล์ ใช้ ZIP ของ Skill เดียวหรือปลั๊กอินรวมตามรูปแบบที่โฮสต์รองรับ

## ChatGPT / Codex

ChatGPT: ใช้การนำเข้า Skill หรือปลั๊กอินเฉพาะเมื่อบัญชีและอินเทอร์เฟซปัจจุบันรองรับเท่านั้น การแนบ ZIP ในแชตไม่ได้ติดตั้งปลั๊กอิน และไม่ยืนยันการขึ้นรายการสาธารณะ

Codex: Full plugin ZIP contains portable plugin.json and .codex-plugin/plugin.json plus four local skills. Use the host's supported local plugin import workflow. When only local Skills are supported, extract a standalone ZIP into the configured skills directory, preserving its named root folder. Reload/discover skills, invoke its exact name and check that its local references resolve. Native plugin discovery and invocation are not verified by archive checks.

## Claude

Claude Code: แตกไฟล์ `kumihan-th-Claude-Code-plugin-v0.1.1.zip` แล้วใช้ `claude --plugin-dir /absolute/path/kumihan-th` โดยต้องเห็นชื่อเทคนิค `kumihan-th` ไม่ใช่ `kumihan` หรือ `kumihan-ziheng`

Claude Code: extract the dedicated plugin ZIP; `.claude-plugin/plugin.json` and four `skills/*/SKILL.md` trees sit beneath its `kumihan-th` root. Local loading uses the command above. For a marketplace, register this product separately; this candidate does not modify the Japanese marketplace. Verify with your installed version's `claude plugin validate` before use. Native validation/invocation here: not-checked.

Claude Apps: use the four `*-Claude-skill-v0.1.1.zip` files, one skill per ZIP.

If your Claude interface supports custom Skills, import a standalone Skill ZIP through its documented Skills upload interface. The folder root includes SKILL.md and all dependencies. Availability varies by account and client; a chat attachment is not installation. This workflow is guidance, not a tested native-host result.

## Gemini

Gemini CLI: แตกไฟล์ `kumihan-th-Gemini-CLI-extension-v0.1.1.zip` แล้วใช้ `gemini extensions link /absolute/path/kumihan-th` ชื่อเทคนิค `kumihan-th` เท่านั้น

The dedicated CLI archive contains `gemini-extension.json`, `GEMINI.md` and four `skills/*/SKILL.md` trees. The documented Gemini manifest has no dedicated displayName field: the technical CLI identifier remains `kumihan-th`; the product heading is exactly KUMIHAN｜ดุลอักษร. Do not treat this as verified native UI naming or invocation.

Gemini Apps: four `*-Gemini-Apps-skill-v0.1.1.zip` archives are self-contained candidate skills. No Apps upload acceptance was tested. Use an import flow only if supported by your account/client; otherwise use the files as task context.

ใช้โฟลเดอร์ Skill ผ่านกลไกที่ไคลเอนต์ปัจจุบันรองรับเท่านั้น หากไม่มีตัวนำเข้า ให้ใช้ SKILL.md เป็นคำแนะนำและแนบไฟล์อ้างอิงที่จำเป็นด้วยตนเอง นี่เป็นวิธีใช้อ้างอิงแบบจำกัด ไม่ใช่การติดตั้งปลั๊กอินที่ทดสอบแล้ว

## Verify and update

Ask for a read-only review of a small Thai paragraph, confirm th-TH and the chosen medium, and verify that source bytes are unchanged. Confirm actual tool output separately from rendered evidence. Replace the complete versioned folder to update; avoid mixing files from different versions. Keep your previous installation until verification succeeds.

日本語: 各ホストの現行UIが対応する導入方法だけを使用してください。ZIP添付はインストールではありません。Geminiの手動参照は限定的な利用方法です。解凍後のルート、参照ファイル、バージョンとチェックサムを確認し、小さな原文保持テストで動作を検証します。

## Candidate source and provenance

ไฟล์ซอร์สสำหรับตรวจสอบ 15 ชุด ยังไม่เผยแพร่ ต้องอนุมัติรุ่นและแท็กก่อนเผยแพร่
15 source candidate archives: [downloads](https://github.com/landco-llc/kumihan/raw/refs/heads/feat/kumihan-th-host-parity-20261018/plugins/kumihan-th/downloads/MANIFEST.json), [SHA256SUMS](https://github.com/landco-llc/kumihan/raw/refs/heads/feat/kumihan-th-host-parity-20261018/plugins/kumihan-th/downloads/SHA256SUMS.txt). All ZIP names use literal `-v0.1.1.zip`. There are five archives for each host family. No Release assets have been uploaded by this correction.

The historical `kumihan-th-v0.1.0` tag remains unchanged and identifies the original five-archive source. This v0.1.1 candidate is not tagged, merged or published. Confirm the exact approved commit after the verification gate; never retag v0.1.0 or label older v0.1.0 ZIPs as v0.1.1.

Host contracts checked 2026-10-18: [Claude manifest](https://code.claude.com/docs/en/plugins-reference), [Gemini extension](https://geminicli.com/docs/extensions/reference/). These establish structural guidance, not installation evidence. Static checks, actual rendering, and native invocation are separate.
