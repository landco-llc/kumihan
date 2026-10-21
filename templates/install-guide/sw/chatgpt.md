Mwongozo huu unaeleza jinsi ya kutumia {{brand}} kwenye ChatGPT na Codex.

> **Kuhusu v{{version}}**
> Toleo hili ni kwa ajili ya kujaribu usakinishaji katika mazingira yako mwenyewe. Utendaji katika kila zana bado haujathibitishwa kikamilifu, kwa hiyo baadhi ya hatua huenda zisifanye kazi kama inavyotarajiwa.

## 1. Chagua njia ya usakinishaji

| Mahali unapotaka kuitumia | Njia inayopendekezwa |
| --- | --- |
| ChatGPT (ikiwa kupakia skill kunawezekana) | [A. Ongeza skill moja moja](#a) |
| ChatGPT (ikiwa unataka kuisajili kama programu-jalizi yako binafsi) | [B. Sajili zote pamoja kama programu-jalizi](#b) |
| Codex (kwenye kompyuta yako) | [C. Nakili folda](#c) |

**Skill** ni kipengele kimoja, na **programu-jalizi** (plugin) ni kifurushi kinachounganisha skill zote nne.

## 2. Pakua faili

Faili zote ziko kwenye [ukurasa wa toleo]({{release}}). Ukibofya kiungo, faili ya ZIP itapakuliwa.

**Programu-jalizi (skill zote nne pamoja)**

- {{plugin_link}}

**Skill (moja moja)**

{{skills_list}}

## A. Ongeza skill kwenye ChatGPT

Tumia njia hii ikiwa skrini yako ya ChatGPT ina **Skills** pamoja na chaguo la kupakia.

1. Chagua faili moja ya ZIP ya skill na uipakie.
2. Kagua maelezo yanayoonyeshwa, kisha uiongeze.
3. Rudia hatua hizo kwa kila skill unayohitaji.

**Tahadhari**

- Faili ya ZIP ya programu-jalizi haifanyi kazi kwa njia hii. Tumia faili za ZIP za skill.
- Kuambatisha faili kwenye gumzo pekee hakuiongezi kama skill.
- Ikiwa huoni chaguo hilo, huenda bado halipatikani kwa mpango au programu unayotumia. Angalia [mwongozo rasmi wa OpenAI](https://learn.chatgpt.com/docs/build-skills).

## B. Sajili kama programu-jalizi kwenye ChatGPT

Njia hii inaunganisha skill zote nne na kuzisajili kama programu-jalizi ya matumizi yako binafsi.

1. Fungua mazungumzo mapya kwenye ChatGPT na uchague `@plugin-creator`.
2. Ambatisha faili ya ZIP ya programu-jalizi.
3. Omba hivi:

   > Tafadhali sajili kifurushi hiki kama programu-jalizi yangu binafsi. Usikiwasilishe kwenye saraka ya umma.

4. Usajili ukikamilika, **{{display}}** itaonekana chini ya Plugins, katika “Personal” au “Created by me”.
5. Isakinishe ikihitajika, kisha uiwashe katika mazungumzo mapya.

**Tahadhari**

- Programu-jalizi inaweza kuhifadhiwa kwenye workspace ya timu yako. Ikiwa unataka iwe yako peke yako, kagua mahali itakapohifadhiwa kabla ya kusajili.
- Kipengele hiki huenda kisipatikane kulingana na mpango wako au mipangilio ya workspace. Kwa maelezo zaidi, angalia [Build plugins](https://learn.chatgpt.com/docs/build-plugins) na [Plugins](https://learn.chatgpt.com/docs/plugins).
- Programu-jalizi iliyosajiliwa kwa njia hii inapatikana kwa akaunti yako pekee. Haiorodheshwi kwenye saraka ya umma.

## C. Nakili folda kwa ajili ya Codex

Ukifungua (extract) faili ya ZIP ya skill, utapata folda kama `{{first}}`. Nakili folda hiyo mahali ambapo Codex husoma skill.

| Upeo wa matumizi | Mahali pa kunakili |
| --- | --- |
| Mradi mmoja tu | `.agents/skills/` ndani ya mradi |
| Miradi yote | `~/.agents/skills/` kwenye folda ya nyumbani (home) |

Kwa mfano, ili kuongeza `{{first}}` kwenye mradi:

```sh
mkdir -p /path/to/your-project/.agents/skills
cp -R {{first}} /path/to/your-project/.agents/skills/
```

**Tahadhari**

- Nakili folda nzima pamoja na yaliyomo yote. Skill haitafanya kazi ipasavyo ikiwa kuna baadhi ya faili tu.
- Ikiwa tayari kuna folda yenye jina hilohilo, kagua yaliyomo kabla ya kuifuta na kuiandika upya.

## 3. Ijaribu

Baada ya kusakinisha, fungua mazungumzo mapya na uite skill.

| Zana | Jinsi ya kuita |
| --- | --- |
| ChatGPT | Chagua kutoka `@` |
| Codex | Chagua kutoka `$` au `/skills` |

Tunapendekeza uanze na ombi lisilobadilisha faili yoyote.

> Ninapanga kuandaa ripoti kwa Kiswahili. Ni mambo gani ninapaswa kuzingatia? Tafadhali usibadilishe faili yoyote.

## Thibitisha kuwa faili ni sahihi (hiari)

Ikiwa unataka kuhakikisha kuwa faili ulizopakua hazijaharibika, tumia [SHA256SUMS.txt]({{sums}}).

Weka SHA256SUMS.txt kwenye folda ileile yenye faili za ZIP ulizopakua, kisha endesha amri ifuatayo kwenye terminal. Ikiwa `shasum` haipatikani, linganisha SHA-256 kwa amri nyingine kama `Get-FileHash` ya Windows PowerShell.

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

Ikiwa mistari ya faili ulizopakua inaonyesha `OK`, hakuna tatizo.

---

Zana nyingine: [Claude]({{page_claude}}) · [Gemini]({{page_gemini}})

Skrini na masharti ya upatikanaji yanaweza kubadilika. Tafadhali angalia mwongozo rasmi wa kila huduma kwa taarifa za hivi karibuni (ukurasa huu ulikaguliwa tarehe 14 Oktoba 2026).
