Tämä opas kertoo, miten {{brand}} otetaan käyttöön ChatGPT:ssä ja Codexissa.

> **Tietoa versiosta v{{version}}**
> Tämä versio on tarkoitettu kokeiltavaksi omassa ympäristössäsi. Toimintaa eri työkaluissa ei ole vielä varmennettu kattavasti, joten kaikki vaiheet eivät välttämättä toimi odotetusti.

## 1. Valitse asennustapa

| Missä haluat käyttää | Suositeltu tapa |
| --- | --- |
| ChatGPT (jos taitojen lähettäminen on käytettävissä) | [A. Lisää taidot yksi kerrallaan](#a) |
| ChatGPT (omana yksityisenä lisäosana) | [B. Rekisteröi lisäosana](#b) |
| Codex (omalla tietokoneella) | [C. Kopioi taitokansiot](#c) |

**Taito** on yksi toiminto. **Lisäosa** kokoaa kaikki neljä taitoa yhteen pakettiin.

## 2. Lataa tiedostot

Kaikki tiedostot ovat [julkaisusivulla]({{release}}). Lataa ZIP-tiedosto valitsemalla linkki.

**Lisäosa (kaikki neljä taitoa)**

- {{plugin_link}}

**Yksittäiset taidot**

{{skills_list}}

## A. Lisää taitoja ChatGPT:hen

Käytä tätä tapaa, jos ChatGPT:ssäsi näkyy **Skills** ja lähetysvaihtoehto.

1. Lähetä yhden taidon ZIP-tiedosto.
2. Tarkista tiedot ja lisää taito.
3. Toista jokaiselle taidolle, jota haluat käyttää.

**Huomioita**

- Lisäosan ZIP ei toimi tässä. Käytä yksittäisten taitojen ZIP-tiedostoja.
- Tiedoston liittäminen keskusteluun ei asenna sitä taidoksi.
- Jos vaihtoehtoa ei näy, se ei ehkä ole vielä käytettävissä tilauksessasi tai sovelluksessasi. Katso [OpenAI:n ohje](https://learn.chatgpt.com/docs/build-skills).

## B. Rekisteröi lisäosa ChatGPT:hen

Tällä tavalla kaikki neljä taitoa rekisteröidään omaksi yksityiseksi lisäosaksesi.

1. Aloita ChatGPT:ssä uusi keskustelu ja valitse `@plugin-creator`.
2. Liitä lisäosan ZIP-tiedosto.
3. Pyydä näin:

   > Rekisteröi tämä paketti yksityiseksi lisäosakseni. Älä lähetä sitä julkiseen hakemistoon.

4. Kun rekisteröinti on valmis, **{{display}}** näkyy Plugins-kohdassa, kohdassa ”Personal” tai ”Created by me”.
5. Asenna se tarvittaessa ja ota se käyttöön uudessa keskustelussa.

**Huomioita**

- Lisäosa saatetaan tallentaa tiimisi työtilaan. Jos haluat sen vain omaan käyttöösi, tarkista tallennuspaikka ennen rekisteröintiä.
- Toiminto ei ehkä ole käytettävissä tilauksesi tai työtilan asetusten vuoksi. Katso [Build plugins](https://learn.chatgpt.com/docs/build-plugins) ja [Plugins](https://learn.chatgpt.com/docs/plugins).
- Näin rekisteröity lisäosa on vain tilisi käytettävissä. Sitä ei näytetä julkisessa hakemistossa.

## C. Kopioi taitokansiot Codexia varten

Kun purat taidon ZIP-tiedoston, saat kansion, kuten `{{first}}`. Kopioi kansio paikkaan, josta Codex etsii taitoja.

| Käyttöalue | Kohde |
| --- | --- |
| Vain yksi projekti | `.agents/skills/` projektin sisällä |
| Kaikki projektit | `~/.agents/skills/` kotikansiossasi |

Esimerkiksi kun lisäät `{{first}}`-taidon projektiin:

```sh
mkdir -p /path/to/your-project/.agents/skills
cp -R {{first}} /path/to/your-project/.agents/skills/
```

**Huomioita**

- Kopioi koko kansio kaikkine tiedostoineen. Taito ei toimi oikein, jos mukana on vain osa tiedostoista.
- Jos samanniminen kansio on jo olemassa, tarkista sen sisältö ennen korvaamista.

## 3. Kokeile

Avaa uusi keskustelu ja kutsu taitoa.

| Työkalu | Näin kutsut |
| --- | --- |
| ChatGPT | Valitse `@`-valikosta |
| Codex | Valitse `$`- tai `/skills`-valikosta |

Suosittelemme aloittamaan pyynnöllä, joka ei muuta tiedostoja:

> Suunnittelen raporttia, jonka kieli on {{lang}}. Mitä minun kannattaa ottaa huomioon? Älä muuta mitään tiedostoja.

## Tarkista lataukset (valinnainen)

Voit varmistaa, että lataamasi tiedostot ovat ehjiä, [SHA256SUMS.txt]({{sums}})-tiedoston avulla.

Laita SHA256SUMS.txt samaan kansioon lataamiesi ZIP-tiedostojen kanssa ja suorita päätteessä seuraava komento. Jos `shasum` ei ole käytettävissä, käytä vastaavaa SHA-256-komentoa, kuten Windowsin PowerShellin `Get-FileHash`:

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

Jos lataamiesi tiedostojen riveillä näkyy `OK`, tiedostot ovat ehjiä.

---

Muut työkalut: [Claude]({{page_claude}}) · [Gemini]({{page_gemini}})

Näkymät ja saatavuus voivat muuttua. Tarkista ajantasaiset tiedot kunkin palvelun virallisista ohjeista (tarkistettu viimeksi 14.10.2026).
