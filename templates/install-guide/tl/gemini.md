Ipinapaliwanag ng gabay na ito kung paano gamitin ang {{brand}} sa Gemini CLI at sa Gemini app.

> **Tungkol sa v{{version}}**
> Inilabas ang bersiyong ito para masubukan mo ang pag-install sa sarili mong environment. Hindi pa lubos na nasusuri ang gawi nito sa bawat tool, kaya maaaring may mga hakbang na hindi gumana gaya ng inaasahan.

## 1. Pumili ng paraan ng pag-install

| Saan mo ito gagamitin | Inirerekomendang paraan |
| --- | --- |
| Gemini CLI (lahat ng apat na skill) | [A. I-install bilang extension](#a) |
| Gemini CLI (ang mga skill na kailangan mo lang) | [B. Pumili at mag-install ng mga skill](#b) |
| Gemini app (web, Mac, mobile) | [C. Mag-upload ng mga skill](#c) |

## A. Gemini CLI: i-install bilang extension

Sabay-sabay nitong ini-install ang apat na skill.

1. I-download ang [ZIP ng extension]({{plugin_url}}).
{{#if plugin_folder}}
2. I-extract ito para makuha ang folder na `{{plugin_folder}}`.
{{else}}
2. Gumawa ng walang lamang folder na `{{plugin}}` at doon i-extract ang ZIP.
{{/if}}
3. Mag-install mula sa folder na iyon:

   ```sh
   gemini extensions install "/absolute/path/{{plugin_dir}}"
   ```

Suriin ang lalabas na kumpirmasyon bago magpatuloy. Kapag na-install na, aktibo ang extension sa lahat ng proyekto.

Hindi awtomatikong nag-a-update ang extension na in-install mula sa ZIP. Kapag may bagong bersiyon, palitan ito gamit ang bagong ZIP.

## B. Gemini CLI: pumili at mag-install ng mga skill

Ini-install nito ang mga skill na kailangan mo lang, para sa iisang proyekto. Hindi mo na ito kailangan kung ginamit mo ang paraang A.

Halimbawa, para i-install ang `{{first}}`, patakbuhin ito sa iyong proyekto:

```sh
gemini skills install https://github.com/landco-llc/kumihan --path {{skills_path}}/{{first}} --scope workspace
```

Para sa ibang skill, palitan ang `--path` ng:

{{gemini_paths}}

Nililimitahan ng `--scope workspace` ang skill sa proyektong ito. Kung wala ito, magagamit ang skill sa lahat ng iyong proyekto.

**Para mag-update**

Patakbuhin muli ang parehong command. Papalitan ang naka-install na skill, kaya i-save muna ang anumang binago mo rito.

## C. Gemini app: mag-upload ng mga skill

1. I-download ang mga ZIP ng skill na gusto mong gamitin.
{{skills_list_indented}}
2. Sa Gemini, buksan ang **Customize** (o **More** kung hindi mo ito makita) → **Skills** → **Upload**.
3. Pumili ng isang ZIP sa bawat pagkakataon, suriin ang mga detalye, at piliin ang **Create**.

**Paalala**

- Para lamang sa mga personal na Google account ng mga user na 18 taong gulang pataas. Hindi pa sinusuportahan sa ngayon ang mga account para sa trabaho at paaralan.
- Kailangang naka-on ang **Keep Activity**.
- Unti-unting inilalabas ang feature na ito, kaya maaaring hindi pa ito available sa iyo. Tingnan ang [opisyal na tulong ng Gemini](https://support.google.com/gemini/answer/17094296?hl=ja).
- Hindi gumagana rito ang ZIP ng extension (para sa Gemini CLI).
- Hindi awtomatikong nag-a-update ang mga na-upload na skill. Kapag may bagong bersiyon, i-upload itong muli.

## 2. Subukan ito

Inirerekomenda naming magsimula sa kahilingang hindi nagbabago ng anumang file:

> Gagawa ako ng presentasyon sa {{lang}}. Ano ang dapat kong tandaan? Pakiusap, huwag baguhin ang anumang file.

## Tiyakin ang mga na-download (opsiyonal)

Para matiyak na buo at hindi sira ang mga na-download mo, gamitin ang [SHA256SUMS.txt]({{sums}}).

Ilagay ang SHA256SUMS.txt sa parehong folder ng mga na-download na ZIP file, saka patakbuhin ito sa terminal. Kung walang `shasum`, gumamit ng katumbas na SHA-256 command gaya ng `Get-FileHash` ng PowerShell sa Windows:

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

Kung `OK` ang lumabas sa mga linya ng mga na-download mong file, buo ang mga ito.

---

Iba pang tool: [ChatGPT / Codex]({{page_chatgpt}}) · [Claude]({{page_claude}})

Maaaring magbago ang mga screen at availability. Tingnan ang opisyal na gabay ng bawat serbisyo para sa pinakabagong impormasyon (huling sinuri: Oktubre 14, 2026).
