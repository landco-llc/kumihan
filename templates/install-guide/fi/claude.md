Tämä opas kertoo, miten {{brand}} otetaan käyttöön Claude Codessa ja Claude-chatissa.

> **Tietoa versiosta v{{version}}**
> Tämä versio on tarkoitettu kokeiltavaksi omassa ympäristössäsi. Toimintaa eri työkaluissa ei ole vielä varmennettu kattavasti, joten kaikki vaiheet eivät välttämättä toimi odotetusti.

## 1. Valitse asennustapa

| Missä haluat käyttää | Suositeltu tapa |
| --- | --- |
{{#if marketplace}}
| Claude Code | [A. Asenna GitHubista](#a) (helppo päivittää) |
{{/if}}
| Claude Code (ZIP-tiedostosta) | [{{L_zip}}. Asenna ZIP-tiedostosta](#{{l_zip}}) |
| Claude-chat (claude.ai ja sovellukset) | [{{L_chat}}. Lähetä taidot](#{{l_chat}}) |

Claude Codeen ja Claude-chattiin asennetaan eri tavoin.

{{#if marketplace}}
## A. Claude Code: asenna GitHubista

1. Lisää päätteessä KUMIHANin marketplace.

   ```sh
   claude plugin marketplace add "https://github.com/landco-llc/kumihan.git#main"
   ```

2. Kirjoita Claude Coden keskusteluun:

   ```text
   /plugin install {{plugin}}@kumihan-marketplace
   ```

3. Tarkista tiedot, valitse käyttöalue (vain sinä, tämä projekti jne.) ja asenna.

Asennuksen jälkeen nämä komennot ovat käytettävissä:

{{claude_commands}}

{{/if}}
## {{L_zip}}. Claude Code: asenna ZIP-tiedostosta

1. Lataa [Claude Coden lisäosan ZIP]({{plugin_url}}).
{{#if plugin_folder}}
2. Pura se, niin saat kansion `{{plugin_folder}}`.
{{else}}
2. Luo tyhjä kansio `{{plugin}}` ja pura ZIP sen sisään.
{{/if}}
3. Käynnistä Claude Code kyseisellä kansiolla:

   ```sh
   claude --plugin-dir "/absolute/path/{{plugin_dir}}"
   ```

**Huomioita**

- Käytä kansiota sellaisenaan. Älä poista siitä tiedostoja äläkä lisää siihen muita tiedostoja.
- Tämä tapa ei päivity automaattisesti. Kun uusi versio julkaistaan, korvaa kansio uudella ZIP-tiedostolla.

## {{L_chat}}. Claude-chat: lähetä taidot

Käytä tätä tapaa claude.aissa ja Clauden sovelluksissa.

1. Lataa niiden taitojen ZIP-tiedostot, joita haluat käyttää.
{{skills_list_indented}}
2. Avaa Claudessa **Customize → Skills** ja valitse lisäyspainikkeesta **Upload a skill**.
3. Lähetä ZIP-tiedostot yksi kerrallaan ja ota jokainen taito käyttöön.

**Huomioita**

- Claude Coden lisäosan ZIP ei toimi tässä. Käytä yksittäisten taitojen ZIP-tiedostoja.
- Lähetä ZIP-tiedostot nimeämättä niitä uudelleen.
- Taidot edellyttävät, että koodin suoritus on otettu käyttöön asetuksissa. Katso [Clauden ohje](https://support.claude.com/en/articles/12512180-use-skills-in-claude).
- Organisaation tileillä saatavuus voi riippua ylläpitäjän asetuksista.
- Lähetetyt taidot eivät päivity automaattisesti. Kun uusi versio julkaistaan, lähetä se uudelleen.

## 2. Kokeile

Suosittelemme aloittamaan pyynnöllä, joka ei muuta tiedostoja:

> Suunnittelen verkkosivua, jonka kieli on {{lang}}. Mitä minun kannattaa ottaa huomioon? Älä muuta mitään tiedostoja.

## Tarkista lataukset (valinnainen)

Voit varmistaa, että lataamasi tiedostot ovat ehjiä, [SHA256SUMS.txt]({{sums}})-tiedoston avulla.

Laita SHA256SUMS.txt samaan kansioon lataamiesi ZIP-tiedostojen kanssa ja suorita päätteessä seuraava komento. Jos `shasum` ei ole käytettävissä, käytä vastaavaa SHA-256-komentoa, kuten Windowsin PowerShellin `Get-FileHash`:

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

Jos lataamiesi tiedostojen riveillä näkyy `OK`, tiedostot ovat ehjiä.

---

Muut työkalut: [ChatGPT / Codex]({{page_chatgpt}}) · [Gemini]({{page_gemini}})

Näkymät ja saatavuus voivat muuttua. Tarkista ajantasaiset tiedot kunkin palvelun virallisista ohjeista (tarkistettu viimeksi 14.10.2026).
