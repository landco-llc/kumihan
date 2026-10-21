Ipinapaliwanag ng gabay na ito kung paano gamitin ang {{brand}} sa ChatGPT at Codex.

> **Tungkol sa v{{version}}**
> Inilabas ang bersiyong ito para masubukan mo ang pag-install sa sarili mong environment. Hindi pa lubos na nasusuri ang gawi nito sa bawat tool, kaya maaaring may mga hakbang na hindi gumana gaya ng inaasahan.

## 1. Pumili ng paraan ng pag-install

| Saan mo ito gagamitin | Inirerekomendang paraan |
| --- | --- |
| ChatGPT (kung may opsiyong mag-upload ng skill) | [A. Magdagdag ng skill isa-isa](#a) |
| ChatGPT (bilang sarili mong pribadong plugin) | [B. Irehistro bilang plugin](#b) |
| Codex (sa iyong computer) | [C. Kopyahin ang mga folder ng skill](#c) |

Ang **skill** ay isang feature. Pinagsasama ng **plugin** ang apat na skill sa iisang package.

## 2. I-download ang mga file

Nasa [pahina ng release]({{release}}) ang lahat ng file. Pindutin ang link para i-download ang ZIP file.

**Plugin (lahat ng apat na skill)**

- {{plugin_link}}

**Mga skill (isa-isa)**

{{skills_list}}

## A. Magdagdag ng skill sa ChatGPT

Gamitin ang paraang ito kung may **Skills** at opsiyong mag-upload sa iyong ChatGPT.

1. Mag-upload ng isang ZIP ng skill.
2. Suriin ang mga detalye at idagdag ito.
3. Ulitin para sa bawat skill na gusto mong gamitin.

**Paalala**

- Hindi gumagana rito ang ZIP ng plugin. Gamitin ang mga ZIP ng bawat skill.
- Hindi naii-install bilang skill ang file na ilalakip lang sa chat.
- Kung hindi mo makita ang opsiyon, maaaring hindi pa ito available sa iyong plan o app. Tingnan ang [gabay ng OpenAI](https://learn.chatgpt.com/docs/build-skills).

## B. Magrehistro ng plugin sa ChatGPT

Sa paraang ito, irerehistro ang apat na skill bilang sarili mong pribadong plugin.

1. Magsimula ng bagong usapan sa ChatGPT at piliin ang `@plugin-creator`.
2. Ilakip ang ZIP ng plugin.
3. Hilingin ito:

   > Pakirehistro ang package na ito bilang aking pribadong plugin. Huwag itong isumite sa pampublikong direktoryo.

4. Kapag nairehistro na, lalabas ang **{{display}}** sa Plugins, sa "Personal" o "Created by me".
5. I-install ito kung kailangan, saka i-enable sa bagong usapan.

**Paalala**

- Maaaring mai-save ang plugin sa workspace ng iyong team. Kung gusto mong para sa iyo lang ito, tingnan muna kung saan ito mase-save bago magrehistro.
- Maaaring hindi available ang feature na ito depende sa iyong plan o sa setting ng workspace. Tingnan ang [Build plugins](https://learn.chatgpt.com/docs/build-plugins) at [Plugins](https://learn.chatgpt.com/docs/plugins).
- Ang plugin na nairehistro sa paraang ito ay magagamit lamang ng iyong account. Hindi ito ililista sa pampublikong direktoryo.

## C. Kopyahin ang mga folder ng skill para sa Codex

Kapag in-extract ang ZIP ng skill, magkakaroon ka ng folder gaya ng `{{first}}`. Kopyahin ang folder na iyon sa lugar na binabasa ng Codex para sa mga skill.

| Saklaw | Lalagyan |
| --- | --- |
| Isang proyekto lamang | `.agents/skills/` sa loob ng proyekto |
| Lahat ng proyekto | `~/.agents/skills/` sa iyong home folder |

Halimbawa, para idagdag ang `{{first}}` sa isang proyekto:

```sh
mkdir -p /path/to/your-project/.agents/skills
cp -R {{first}} /path/to/your-project/.agents/skills/
```

**Paalala**

- Kopyahin ang buong folder kasama ang lahat ng laman nito. Hindi gagana nang tama ang skill kung ilang file lang ang kinopya.
- Kung may folder nang may parehong pangalan, tingnan muna ang laman nito bago patungan.

## 3. Subukan ito

Magbukas ng bagong usapan at tawagin ang skill.

| Tool | Paano tawagin |
| --- | --- |
| ChatGPT | Piliin mula sa `@` |
| Codex | Piliin mula sa `$` o `/skills` |

Inirerekomenda naming magsimula sa kahilingang hindi nagbabago ng anumang file:

> Gagawa ako ng ulat sa {{lang}}. Ano ang dapat kong tandaan? Pakiusap, huwag baguhin ang anumang file.

## Tiyakin ang mga na-download (opsiyonal)

Para matiyak na buo at hindi sira ang mga na-download mo, gamitin ang [SHA256SUMS.txt]({{sums}}).

Ilagay ang SHA256SUMS.txt sa parehong folder ng mga na-download na ZIP file, saka patakbuhin ito sa terminal. Kung walang `shasum`, gumamit ng katumbas na SHA-256 command gaya ng `Get-FileHash` ng PowerShell sa Windows:

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

Kung `OK` ang lumabas sa mga linya ng mga na-download mong file, buo ang mga ito.

---

Iba pang tool: [Claude]({{page_claude}}) · [Gemini]({{page_gemini}})

Maaaring magbago ang mga screen at availability. Tingnan ang opisyal na gabay ng bawat serbisyo para sa pinakabagong impormasyon (huling sinuri: Oktubre 14, 2026).
