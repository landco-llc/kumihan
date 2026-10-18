# KUMIHAN｜ดุลอักษร

เวอร์ชัน 0.1.1 · th-TH · L&Co. LLC · Apache-2.0

แนวทางจัดวางอักษรไทยสำหรับเว็บ เอกสาร งานนำเสนอ และการตรวจทานแบบอ่านอย่างเดียว รักษาข้อความต้นฉบับโดยไม่ปรับ Unicode หรือเปลี่ยนอักขระที่มองไม่เห็นโดยพลการ เริ่มจาก `kumihan-th` เพื่อเลือกสื่อ หรือเลือก `kumihan-th-web`, `kumihan-th-documents`, `kumihan-th-review` โดยตรง

แต่ละ Skill มีข้อมูลกฎ แหล่งอ้างอิง และเครื่องมือตรวจที่จำเป็นในตัว ไม่ต้องติดตั้งชุดภาษาญี่ปุ่นหรือ字衡 กฎด้านรูปลักษณ์และความหมายต้องใช้การตรวจภาพจริงหรือผู้ตรวจภาษาไทย ไม่มีการรับรองการจัดวางอัตโนมัติ

English: Four independent Thai typography skills with bounded, read-only checks. Static checks do not establish visual quality, native Thai editorial approval, or host installation success. See [installation](INSTALL.md).

日本語: タイ語組版の独立した4 Skillsです。原文を保持し、静的検査と描画・編集判断を区別します。[導入手順](INSTALL.md)を参照してください。

GitHub OSS publication, Pages deployment and provider marketplace listing are distinct events. Consult the actual tagged release and its checksums for publication evidence; host discovery/invocation requires separate verification.

## v0.1.1 — การแจกจ่าย / Distribution

แพ็กเกจเวอร์ชัน v0.1.1 สำหรับ ChatGPT/Codex, Claude และ Gemini มี ZIP 15 ไฟล์ (แต่ละโฮสต์ 5 ไฟล์) ดูที่ [GitHub Release](https://github.com/landco-llc/kumihan/releases/tag/kumihan-th-v0.1.1) พร้อม SHA256SUMS และ MANIFEST.json ก่อนติดตั้ง การติดตั้งและเรียกใช้ในโฮสต์จริงยังไม่ผ่านการทดสอบ

The v0.1.1 release supplies 15 host-specific ZIPs: an independent plugin or extension and four standalone Skills each for ChatGPT/Codex, Claude and Gemini. Thai-first/English descriptions and the versionless display name are preserved. Verify checksums and consult the [installation guide](INSTALL.md). Native host import/invocation is not verified; public OSS release is not a provider marketplace listing.

The historical v0.1.0 tag remains unchanged. Existing Japanese and ZiHeng distributions and their identities are independent.
