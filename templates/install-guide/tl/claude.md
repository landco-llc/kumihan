Ipinapaliwanag ng gabay na ito kung paano gamitin ang {{brand}} sa Claude Code at Claude chat.

> **Tungkol sa v{{version}}**
> Inilabas ang bersiyong ito para masubukan mo ang pag-install sa sarili mong environment. Hindi pa lubos na nasusuri ang gawi nito sa bawat tool, kaya maaaring may mga hakbang na hindi gumana gaya ng inaasahan.

## 1. Pumili ng paraan ng pag-install

| Saan mo ito gagamitin | Inirerekomendang paraan |
| --- | --- |
{{#if marketplace}}
| Claude Code | [A. Mag-install mula sa GitHub](#a) (madaling i-update) |
{{/if}}
| Claude Code (mula sa ZIP) | [{{L_zip}}. Mag-install mula sa ZIP](#{{l_zip}}) |
| Claude chat (claude.ai at mga app) | [{{L_chat}}. Mag-upload ng mga skill](#{{l_chat}}) |

Magkaiba ang paraan ng pag-install sa Claude Code at sa Claude chat.

{{#if marketplace}}
## A. Claude Code: mag-install mula sa GitHub

1. Sa terminal, idagdag ang marketplace ng KUMIHAN.

   ```sh
   claude plugin marketplace add "https://github.com/landco-llc/kumihan.git#main"
   ```

2. Sa isang usapan sa Claude Code, ilagay ito:

   ```text
   /plugin install {{plugin}}@kumihan-marketplace
   ```

3. Suriin ang mga detalye, pumili ng saklaw (ikaw lang, ang proyektong ito, at iba pa), at i-install.

Kapag na-install na, magagamit na ang mga command na ito:

{{claude_commands}}

{{/if}}
## {{L_zip}}. Claude Code: mag-install mula sa ZIP

1. I-download ang [ZIP ng plugin para sa Claude Code]({{plugin_url}}).
{{#if plugin_folder}}
2. I-extract ito para makuha ang folder na `{{plugin_folder}}`.
{{else}}
2. Gumawa ng walang lamang folder na `{{plugin}}` at doon i-extract ang ZIP.
{{/if}}
3. Simulan ang Claude Code gamit ang folder na iyon:

   ```sh
   claude --plugin-dir "/absolute/path/{{plugin_dir}}"
   ```

**Paalala**

- Gamitin ang folder kung ano ito. Huwag magbawas ng file o magdagdag ng ibang file dito.
- Hindi awtomatikong nag-a-update ang paraang ito. Kapag may bagong bersiyon, palitan ang folder gamit ang bagong ZIP.

## {{L_chat}}. Claude chat: mag-upload ng mga skill

Gamitin ang paraang ito para sa claude.ai at sa mga Claude app.

1. I-download ang mga ZIP ng skill na gusto mong gamitin.
{{skills_list_indented}}
2. Sa Claude, buksan ang **Customize → Skills**, saka piliin ang **Upload a skill** mula sa add button.
3. I-upload ang mga ZIP isa-isa at i-enable ang bawat skill.

**Paalala**

- Hindi gumagana rito ang ZIP ng plugin para sa Claude Code. Gamitin ang mga ZIP ng bawat skill.
- I-upload ang mga ZIP nang hindi pinapalitan ang pangalan ng file.
- Kailangang naka-on ang code execution sa iyong settings para magamit ang mga skill. Tingnan ang [gabay ng Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude).
- Sa mga account ng organisasyon, maaaring nakadepende ang availability sa settings ng iyong admin.
- Hindi awtomatikong nag-a-update ang mga na-upload na skill. Kapag may bagong bersiyon, i-upload itong muli.

## 2. Subukan ito

Inirerekomenda naming magsimula sa kahilingang hindi nagbabago ng anumang file:

> Gagawa ako ng web page sa {{lang}}. Ano ang dapat kong tandaan? Pakiusap, huwag baguhin ang anumang file.

## Tiyakin ang mga na-download (opsiyonal)

Para matiyak na buo at hindi sira ang mga na-download mo, gamitin ang [SHA256SUMS.txt]({{sums}}).

Ilagay ang SHA256SUMS.txt sa parehong folder ng mga na-download na ZIP file, saka patakbuhin ito sa terminal. Kung walang `shasum`, gumamit ng katumbas na SHA-256 command gaya ng `Get-FileHash` ng PowerShell sa Windows:

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

Kung `OK` ang lumabas sa mga linya ng mga na-download mong file, buo ang mga ito.

---

Iba pang tool: [ChatGPT / Codex]({{page_chatgpt}}) · [Gemini]({{page_gemini}})

Maaaring magbago ang mga screen at availability. Tingnan ang opisyal na gabay ng bawat serbisyo para sa pinakabagong impormasyon (huling sinuri: Oktubre 14, 2026).
