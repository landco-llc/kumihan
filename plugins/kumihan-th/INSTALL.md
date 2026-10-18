# การติดตั้ง / Installation / 導入

ดาวน์โหลดจาก [Thai v0.1.0 release](https://github.com/landco-llc/kumihan/releases/tag/kumihan-th-v0.1.0) เมื่อเผยแพร่แล้ว ตรวจ SHA256SUMS.txt และ MANIFEST.json ก่อนแตกไฟล์ ใช้ ZIP ของ Skill เดียวหรือปลั๊กอินรวมตามรูปแบบที่โฮสต์รองรับ

## ChatGPT / Codex

ChatGPT: ใช้การนำเข้า Skill หรือปลั๊กอินเฉพาะเมื่อบัญชีและอินเทอร์เฟซปัจจุบันรองรับเท่านั้น การแนบ ZIP ในแชตไม่ได้ติดตั้งปลั๊กอิน และไม่ยืนยันการขึ้นรายการสาธารณะ

Codex: Full plugin ZIP contains portable plugin.json and .codex-plugin/plugin.json plus four local skills. Use the host's supported local plugin import workflow. When only local Skills are supported, extract a standalone ZIP into the configured skills directory, preserving its named root folder. Reload/discover skills, invoke its exact name and check that its local references resolve. Native plugin discovery and invocation are not verified by archive checks.

## Claude

If your Claude interface supports custom Skills, import a standalone Skill ZIP through its documented Skills upload interface. The folder root includes SKILL.md and all dependencies. Availability varies by account and client; a chat attachment is not installation. This workflow is guidance, not a tested native-host result.

## Gemini

ใช้โฟลเดอร์ Skill ผ่านกลไกที่ไคลเอนต์ปัจจุบันรองรับเท่านั้น หากไม่มีตัวนำเข้า ให้ใช้ SKILL.md เป็นคำแนะนำและแนบไฟล์อ้างอิงที่จำเป็นด้วยตนเอง นี่เป็นวิธีใช้อ้างอิงแบบจำกัด ไม่ใช่การติดตั้งปลั๊กอินที่ทดสอบแล้ว

## Verify and update

Ask for a read-only review of a small Thai paragraph, confirm th-TH and the chosen medium, and verify that source bytes are unchanged. Confirm actual tool output separately from rendered evidence. Replace the complete versioned folder to update; avoid mixing files from different versions. Keep your previous installation until verification succeeds.

日本語: 各ホストの現行UIが対応する導入方法だけを使用してください。ZIP添付はインストールではありません。Geminiの手動参照は限定的な利用方法です。解凍後のルート、参照ファイル、バージョンとチェックサムを確認し、小さな原文保持テストで動作を検証します。
