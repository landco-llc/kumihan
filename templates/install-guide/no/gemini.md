Denne veiledningen forklarer hvordan du bruker {{brand}} i Gemini CLI og Gemini-appen.

> **Om v{{version}}**
> Denne versjonen er ment for at du skal kunne prøve installasjonen i ditt eget miljø. Hvordan den fungerer i de enkelte verktøyene, er ennå ikke godt nok kontrollert, så noe kan virke annerledes enn forventet.

## 1. Velg installasjonsmåte

| Der du vil bruke det | Anbefalt måte |
| --- | --- |
| Gemini CLI (alle fire samlet) | [A. Installer som utvidelse](#a) |
| Gemini CLI (bare det du trenger) | [B. Velg og installer skills](#b) |
| Gemini-appen (nett, Mac og mobil) | [C. Last opp skills](#c) |

## A. Gemini CLI: installer som utvidelse

Med denne måten installerer du alle de fire skillsene samlet.

1. Last ned [ZIP-filen for utvidelsen]({{plugin_url}}).
{{#if plugin_folder}}
2. Når du pakker ut ZIP-filen, får du mappen `{{plugin_folder}}`.
{{else}}
2. Opprett en tom mappe med navnet `{{plugin}}`, og pakk ut ZIP-filen i den.
{{/if}}
3. Installer ved å angi mappen.

   ```sh
   gemini extensions install "/absolute/path/{{plugin_dir}}"
   ```

Hvis det vises en bekreftelse, kontrollerer du opplysningene før du går videre. En installert utvidelse er aktiv i alle prosjekter.

En utvidelse som er installert fra en ZIP-fil, oppdateres ikke automatisk. Når en ny versjon kommer, erstatter du den med den nye ZIP-filen.

## B. Gemini CLI: velg og installer skills

Med denne måten installerer du bare de skillsene du trenger, prosjekt for prosjekt. Hvis du har brukt måte A, trenger du ikke dette trinnet.

For å installere for eksempel `{{first}}` kjører du dette i prosjektet:

```sh
gemini skills install https://github.com/landco-llc/kumihan --path {{skills_path}}/{{first}} --scope workspace
```

For andre skills endrer du `--path` slik:

{{gemini_paths}}

`--scope workspace` betyr at skillen bare brukes i dette prosjektet. Hvis du utelater det, blir skillen tilgjengelig i alle prosjekter.

**Slik oppdaterer du**

Kjør den samme kommandoen på nytt. Installerte skills blir erstattet, så lagre eventuelle egne endringer først.

## C. Gemini-appen: last opp skills

1. Last ned ZIP-filene for de skillsene du vil bruke.
{{skills_list_indented}}
2. Åpne **Customize** (eller **More** hvis du ikke ser det) → **Skills** → **Upload** i Gemini.
3. Velg ZIP-filene én og én, kontroller innholdet, og trykk på **Create**.

**Merk**

- Funksjonen er tilgjengelig for personlige Google-kontoer for personer over 18 år. Jobb- og skolekontoer støttes foreløpig ikke.
- «Keep Activity» (lagring av aktivitet) må være slått på.
- Funksjonen rulles ut gradvis, så det kan hende at du ikke ser den ennå. Se [den offisielle hjelpen for Gemini](https://support.google.com/gemini/answer/17094296?hl=no).
- ZIP-filen for utvidelsen (for Gemini CLI) fungerer ikke her.
- Skills du har lastet opp, oppdateres ikke automatisk. Når en ny versjon kommer, laster du dem opp på nytt.

## 2. Prøv det

Det er lurt å begynne med en forespørsel som ikke endrer filer:

> Jeg skal lage en presentasjon på norsk. Hva bør jeg passe på? Ikke endre noen filer.

## Kontroller filene (valgfritt)

Hvis du vil kontrollere at filene du har lastet ned, er uskadde, bruker du [SHA256SUMS.txt]({{sums}}).

Legg SHA256SUMS.txt i samme mappe som ZIP-filene du har lastet ned, og kjør denne kommandoen i terminalen. Hvis `shasum` ikke finnes, kan du for eksempel sammenligne SHA-256-verdiene med `Get-FileHash` i Windows PowerShell.

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

Hvis det står `OK` på linjene for filene du har lastet ned, er alt i orden.

---

Andre verktøy: [ChatGPT / Codex]({{page_chatgpt}}) · [Claude]({{page_claude}})

Skjermbilder og tilgjengelighet kan endre seg. Den nyeste informasjonen finner du i den offisielle veiledningen for hver tjeneste (siden ble sist kontrollert 14. oktober 2026).
