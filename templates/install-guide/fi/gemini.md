Tämä opas kertoo, miten {{brand}} otetaan käyttöön Gemini CLI:ssä ja Gemini-sovelluksessa.

> **Tietoa versiosta v{{version}}**
> Tämä versio on tarkoitettu kokeiltavaksi omassa ympäristössäsi. Toimintaa eri työkaluissa ei ole vielä varmennettu kattavasti, joten kaikki vaiheet eivät välttämättä toimi odotetusti.

## 1. Valitse asennustapa

| Missä haluat käyttää | Suositeltu tapa |
| --- | --- |
| Gemini CLI (kaikki neljä taitoa) | [A. Asenna laajennuksena](#a) |
| Gemini CLI (vain tarvitsemasi taidot) | [B. Valitse ja asenna taidot](#b) |
| Gemini-sovellus (verkko, Mac, mobiili) | [C. Lähetä taidot](#c) |

## A. Gemini CLI: asenna laajennuksena

Tällä tavalla asennat kaikki neljä taitoa kerralla.

1. Lataa [laajennuksen ZIP]({{plugin_url}}).
{{#if plugin_folder}}
2. Pura se, niin saat kansion `{{plugin_folder}}`.
{{else}}
2. Luo tyhjä kansio `{{plugin}}` ja pura ZIP sen sisään.
{{/if}}
3. Asenna kyseisestä kansiosta:

   ```sh
   gemini extensions install "/absolute/path/{{plugin_dir}}"
   ```

Tarkista vahvistuskehote ennen kuin jatkat. Asennuksen jälkeen laajennus on käytössä kaikissa projekteissa.

ZIP-tiedostosta asennettu laajennus ei päivity automaattisesti. Kun uusi versio julkaistaan, korvaa se uudella ZIP-tiedostolla.

## B. Gemini CLI: valitse ja asenna taidot

Tällä tavalla asennat vain tarvitsemasi taidot yhteen projektiin. Tätä ei tarvita, jos käytit tapaa A.

Esimerkiksi `{{first}}`-taidon asentamiseksi suorita projektissasi:

```sh
gemini skills install https://github.com/landco-llc/kumihan --path {{skills_path}}/{{first}} --scope workspace
```

Muita taitoja varten vaihda `--path`-arvoksi:

{{gemini_paths}}

`--scope workspace` rajaa taidon tähän projektiin. Ilman sitä taito on käytettävissä kaikissa projekteissasi.

**Päivittäminen**

Suorita sama komento uudelleen. Asennettu taito korvataan, joten tallenna ensin mahdolliset omat muutoksesi.

## C. Gemini-sovellus: lähetä taidot

1. Lataa niiden taitojen ZIP-tiedostot, joita haluat käyttää.
{{skills_list_indented}}
2. Avaa Geminissä **Customize** (tai **More**, jos sitä ei näy) → **Skills** → **Upload**.
3. Valitse ZIP-tiedostot yksi kerrallaan, tarkista tiedot ja valitse **Create**.

**Huomioita**

- Käytettävissä vähintään 18-vuotiaiden käyttäjien henkilökohtaisilla Google-tileillä. Työ- ja oppilaitostilejä ei toistaiseksi tueta.
- **Keep Activity** -asetuksen on oltava päällä.
- Ominaisuutta otetaan käyttöön vähitellen, joten se ei ehkä ole vielä saatavilla sinulle. Katso [Geminin virallinen ohje](https://support.google.com/gemini/answer/17094296?hl=ja).
- Laajennuksen ZIP (Gemini CLI:lle) ei toimi tässä.
- Lähetetyt taidot eivät päivity automaattisesti. Kun uusi versio julkaistaan, lähetä se uudelleen.

## 2. Kokeile

Suosittelemme aloittamaan pyynnöllä, joka ei muuta tiedostoja:

> Suunnittelen esitystä, jonka kieli on {{lang}}. Mitä minun kannattaa ottaa huomioon? Älä muuta mitään tiedostoja.

## Tarkista lataukset (valinnainen)

Voit varmistaa, että lataamasi tiedostot ovat ehjiä, [SHA256SUMS.txt]({{sums}})-tiedoston avulla.

Laita SHA256SUMS.txt samaan kansioon lataamiesi ZIP-tiedostojen kanssa ja suorita päätteessä seuraava komento. Jos `shasum` ei ole käytettävissä, käytä vastaavaa SHA-256-komentoa, kuten Windowsin PowerShellin `Get-FileHash`:

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

Jos lataamiesi tiedostojen riveillä näkyy `OK`, tiedostot ovat ehjiä.

---

Muut työkalut: [ChatGPT / Codex]({{page_chatgpt}}) · [Claude]({{page_claude}})

Näkymät ja saatavuus voivat muuttua. Tarkista ajantasaiset tiedot kunkin palvelun virallisista ohjeista (tarkistettu viimeksi 14.10.2026).
