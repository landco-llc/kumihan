---
name: kumihan-th-documents
description: "ใช้จัดทำหรือตรวจเอกสารและสไลด์ภาษาไทยโดยรักษาต้นฉบับ | Create or review Thai documents and presentations while preserving source text."
---

# ดุลอักษรสำหรับเอกสาร · KUMIHAN｜ดุลอักษร

ใช้ locale `th-TH` อย่างชัดเจน เริ่มจาก [ขั้นตอนทำงาน](references/workflow.md) และ [บทบาทนี้](references/documents.md). เลือกหนึ่งใน [หก medium profiles](locales/th-TH.json) และอ่านไฟล์ที่ตรงกับงานใน locales/profiles/.

อ่าน [Web](references/web.md), [Documents](references/documents.md) และ [Read-only review](references/review.md) ตามสื่อจริง เก็บต้นฉบับ ชื่อเฉพาะ ตัวเลข เว้นวรรค และลำดับ Unicode ไว้ครบถ้วน ไม่แก้ข้อความที่ได้รับการคุ้มครองโดยอัตโนมัติ ไม่กำหนดฟอนต์ตายตัว และไม่อ้างผลที่ยังไม่ได้ตรวจ

This standalone skill includes its own [32-rule coverage](references/coverage.md), [catalog](rules/catalog.json), [sources](sources.json), [report schema](schemas/report.schema.json), six profiles and optional read-only runtime/check_source.py. It requires no installed Japanese, Chinese or sibling plugin. Runtime bytes/protected-span evidence is distinct from linguistic or rendered evidence. Do not mark missing segmentation/rendering/editorial evidence passed. Native host invocation, instruction-guided use and installed-host testing must be reported separately.
