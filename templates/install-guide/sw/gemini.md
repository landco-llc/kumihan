Mwongozo huu unaeleza jinsi ya kutumia {{brand}} kwenye Gemini CLI na programu ya Gemini.

> **Kuhusu v{{version}}**
> Toleo hili ni kwa ajili ya kujaribu usakinishaji katika mazingira yako mwenyewe. Utendaji katika kila zana bado haujathibitishwa kikamilifu, kwa hiyo baadhi ya hatua huenda zisifanye kazi kama inavyotarajiwa.

## 1. Chagua njia ya usakinishaji

| Mahali unapotaka kuitumia | Njia inayopendekezwa |
| --- | --- |
| Gemini CLI (zote nne pamoja) | [A. Sakinisha kama kiendelezi](#a) |
| Gemini CLI (unazohitaji tu) | [B. Chagua na usakinishe skill](#b) |
| Programu ya Gemini (wavuti, Mac, simu janja) | [C. Pakia skill](#c) |

## A. Gemini CLI: sakinisha kama kiendelezi

Njia hii inasakinisha skill zote nne kwa pamoja.

1. Pakua [faili ya ZIP ya kiendelezi]({{plugin_url}}).
{{#if plugin_folder}}
2. Ukifungua faili ya ZIP, utapata folda `{{plugin_folder}}`.
{{else}}
2. Unda folda tupu `{{plugin}}` na ufungue faili ya ZIP ndani yake.
{{/if}}
3. Sakinisha ukibainisha folda hiyo.

   ```sh
   gemini extensions install "/absolute/path/{{plugin_dir}}"
   ```

Skrini ya uthibitisho ikionekana, kagua maelezo kabla ya kuendelea. Baada ya kusakinishwa, kiendelezi kinafanya kazi katika miradi yote.

Ukisakinisha kutoka ZIP, hakitasasishwa chenyewe. Toleo jipya likitoka, badilisha kwa faili mpya ya ZIP.

## B. Gemini CLI: chagua na usakinishe skill

Njia hii inasakinisha skill unazohitaji tu, kwa kila mradi. Ikiwa umesakinisha kwa njia A, huhitaji hatua hii.

Kwa mfano, ili kusakinisha `{{first}}`, endesha amri ifuatayo ndani ya mradi husika:

```sh
gemini skills install https://github.com/landco-llc/kumihan --path {{skills_path}}/{{first}} --scope workspace
```

Ili kusakinisha skill nyingine, badilisha `--path` kama ifuatavyo:

{{gemini_paths}}

`--scope workspace` ni mpangilio wa kutumia skill “katika mradi huu tu”. Ukiuacha, skill itapatikana katika miradi yako yote.

**Kusasisha**

Endesha amri ileile tena. Skill iliyosakinishwa itabadilishwa, kwa hiyo ikiwa umefanya mabadiliko yako mwenyewe, yahifadhi kwanza.

## C. Programu ya Gemini: pakia skill

1. Pakua faili za ZIP za skill unazotaka kutumia.
{{skills_list_indented}}
2. Kwenye Gemini, fungua **Customize** (au **More** ikiwa huioni) → **Skills** → **Upload**.
3. Chagua faili moja ya ZIP kwa wakati mmoja, kagua maelezo, kisha ubofye **Create**.

**Tahadhari**

- Inapatikana kwa akaunti binafsi za Google za watu wenye umri wa miaka 18 au zaidi. Akaunti za kazini na za shule hazitumiki kwa sasa.
- “Keep Activity (Hifadhi Shughuli)” lazima iwe imewashwa.
- Kipengele hiki kinatolewa hatua kwa hatua, kwa hiyo huenda bado hakijaonekana kwako. Kwa maelezo zaidi, angalia [msaada rasmi wa Gemini](https://support.google.com/gemini/answer/17094296?hl=sw).
- Faili ya ZIP ya kiendelezi (kwa ajili ya Gemini CLI) haifanyi kazi hapa.
- Skill ulizopakia hazisasishwi zenyewe. Toleo jipya likitoka, zipakie tena.

## 2. Ijaribu

Tunapendekeza uanze na ombi lisilobadilisha faili yoyote.

> Ninapanga kuandaa slaidi za wasilisho kwa Kiswahili. Ni mambo gani ninapaswa kuzingatia? Tafadhali usibadilishe faili yoyote.

## Thibitisha kuwa faili ni sahihi (hiari)

Ikiwa unataka kuhakikisha kuwa faili ulizopakua hazijaharibika, tumia [SHA256SUMS.txt]({{sums}}).

Weka SHA256SUMS.txt kwenye folda ileile yenye faili za ZIP ulizopakua, kisha endesha amri ifuatayo kwenye terminal. Ikiwa `shasum` haipatikani, linganisha SHA-256 kwa amri nyingine kama `Get-FileHash` ya Windows PowerShell.

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

Ikiwa mistari ya faili ulizopakua inaonyesha `OK`, hakuna tatizo.

---

Zana nyingine: [ChatGPT / Codex]({{page_chatgpt}}) · [Claude]({{page_claude}})

Skrini na masharti ya upatikanaji yanaweza kubadilika. Tafadhali angalia mwongozo rasmi wa kila huduma kwa taarifa za hivi karibuni (ukurasa huu ulikaguliwa tarehe 14 Oktoba 2026).
