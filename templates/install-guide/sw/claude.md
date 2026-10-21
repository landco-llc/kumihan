Mwongozo huu unaeleza jinsi ya kutumia {{brand}} kwenye Claude Code na gumzo la Claude.

> **Kuhusu v{{version}}**
> Toleo hili ni kwa ajili ya kujaribu usakinishaji katika mazingira yako mwenyewe. Utendaji katika kila zana bado haujathibitishwa kikamilifu, kwa hiyo baadhi ya hatua huenda zisifanye kazi kama inavyotarajiwa.

## 1. Chagua njia ya usakinishaji

| Mahali unapotaka kuitumia | Njia inayopendekezwa |
| --- | --- |
{{#if marketplace}}
| Claude Code | [A. Sakinisha kutoka GitHub](#a) (rahisi kusasisha) |
{{/if}}
| Claude Code (ikiwa unataka kusakinisha kutoka ZIP) | [{{L_zip}}. Sakinisha kutoka ZIP](#{{l_zip}}) |
| Gumzo la Claude (claude.ai na programu) | [{{L_chat}}. Pakia skill](#{{l_chat}}) |

Claude Code na gumzo la Claude zina njia tofauti za usakinishaji.

{{#if marketplace}}
## A. Claude Code: sakinisha kutoka GitHub

1. Kwenye terminal, sajili chanzo cha usambazaji cha KUMIHAN.

   ```sh
   claude plugin marketplace add "https://github.com/landco-llc/kumihan.git#main"
   ```

2. Katika mazungumzo ya Claude Code, andika yafuatayo:

   ```text
   /plugin install {{plugin}}@kumihan-marketplace
   ```

3. Kagua maelezo, chagua upeo wa matumizi (wewe peke yako, mradi huu tu, n.k.), kisha usakinishe.

Baada ya kusakinisha, amri zifuatazo zitapatikana:

{{claude_commands}}

{{/if}}
## {{L_zip}}. Claude Code: sakinisha kutoka ZIP

1. Pakua [faili ya ZIP ya programu-jalizi ya Claude Code]({{plugin_url}}).
{{#if plugin_folder}}
2. Ukifungua faili ya ZIP, utapata folda `{{plugin_folder}}`.
{{else}}
2. Unda folda tupu `{{plugin}}` na ufungue faili ya ZIP ndani yake.
{{/if}}
3. Anzisha Claude Code ukibainisha folda hiyo.

   ```sh
   claude --plugin-dir "/absolute/path/{{plugin_dir}}"
   ```

**Tahadhari**

- Tumia yaliyomo kwenye folda kama yalivyo. Usiondoe faili wala kuchanganya faili nyingine ndani yake.
- Njia hii haisasishi yenyewe. Toleo jipya likitoka, badilisha kwa faili mpya ya ZIP.

## {{L_chat}}. Gumzo la Claude: pakia skill

Hii ni njia ya kutumia kwenye claude.ai na programu za Claude.

1. Pakua faili za ZIP za skill unazotaka kutumia.
{{skills_list_indented}}
2. Kwenye Claude, fungua **Customize → Skills**, kisha uchague **Upload a skill** kutoka kitufe cha kuongeza.
3. Pakia faili za ZIP moja baada ya nyingine, kisha uwashe kila skill.

**Tahadhari**

- Faili ya ZIP ya programu-jalizi ya Claude Code haifanyi kazi hapa. Tumia faili za ZIP za skill.
- Pakia faili za ZIP bila kubadilisha majina yake.
- Ili kutumia skill, “utekelezaji wa msimbo” (code execution) lazima uwe umewashwa kwenye mipangilio. Kwa maelezo zaidi, angalia [mwongozo rasmi wa Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude).
- Kwa akaunti za mashirika, huenda isipatikane kulingana na mipangilio ya msimamizi.
- Skill ulizopakia hazisasishwi zenyewe. Toleo jipya likitoka, zipakie tena.

## 2. Ijaribu

Tunapendekeza uanze na ombi lisilobadilisha faili yoyote.

> Ninapanga kutengeneza ukurasa wa wavuti kwa Kiswahili. Ni mambo gani ninapaswa kuzingatia? Tafadhali usibadilishe faili yoyote.

## Thibitisha kuwa faili ni sahihi (hiari)

Ikiwa unataka kuhakikisha kuwa faili ulizopakua hazijaharibika, tumia [SHA256SUMS.txt]({{sums}}).

Weka SHA256SUMS.txt kwenye folda ileile yenye faili za ZIP ulizopakua, kisha endesha amri ifuatayo kwenye terminal. Ikiwa `shasum` haipatikani, linganisha SHA-256 kwa amri nyingine kama `Get-FileHash` ya Windows PowerShell.

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

Ikiwa mistari ya faili ulizopakua inaonyesha `OK`, hakuna tatizo.

---

Zana nyingine: [ChatGPT / Codex]({{page_chatgpt}}) · [Gemini]({{page_gemini}})

Skrini na masharti ya upatikanaji yanaweza kubadilika. Tafadhali angalia mwongozo rasmi wa kila huduma kwa taarifa za hivi karibuni (ukurasa huu ulikaguliwa tarehe 14 Oktoba 2026).
