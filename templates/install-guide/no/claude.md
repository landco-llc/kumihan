Denne veiledningen forklarer hvordan du bruker {{brand}} i Claude Code og Claude-chatten.

> **Om v{{version}}**
> Denne versjonen er ment for at du skal kunne prøve installasjonen i ditt eget miljø. Hvordan den fungerer i de enkelte verktøyene, er ennå ikke godt nok kontrollert, så noe kan virke annerledes enn forventet.

## 1. Velg installasjonsmåte

| Der du vil bruke det | Anbefalt måte |
| --- | --- |
{{#if marketplace}}
| Claude Code | [A. Installer fra GitHub](#a) (enkelt å oppdatere) |
{{/if}}
| Claude Code (fra en ZIP-fil) | [{{L_zip}}. Installer fra en ZIP-fil](#{{l_zip}}) |
| Claude-chatten (claude.ai og appene) | [{{L_chat}}. Last opp skills](#{{l_chat}}) |

Claude Code og Claude-chatten installeres på ulike måter.

{{#if marketplace}}
## A. Claude Code: installer fra GitHub

1. Legg til KUMIHANs distribusjonskilde i terminalen.

   ```sh
   claude plugin marketplace add "https://github.com/landco-llc/kumihan.git#main"
   ```

2. Skriv inn følgende i en samtale i Claude Code:

   ```text
   /plugin install {{plugin}}@kumihan-marketplace
   ```

3. Kontroller opplysningene, velg omfang (bare deg, bare dette prosjektet osv.), og installer.

Når installasjonen er ferdig, kan du bruke disse kommandoene:

{{claude_commands}}

{{/if}}
## {{L_zip}}. Claude Code: installer fra en ZIP-fil

1. Last ned [plugin-ZIP-filen for Claude Code]({{plugin_url}}).
{{#if plugin_folder}}
2. Når du pakker ut ZIP-filen, får du mappen `{{plugin_folder}}`.
{{else}}
2. Opprett en tom mappe med navnet `{{plugin}}`, og pakk ut ZIP-filen i den.
{{/if}}
3. Start Claude Code med denne mappen.

   ```sh
   claude --plugin-dir "/absolute/path/{{plugin_dir}}"
   ```

**Merk**

- Bruk innholdet i mappen slik det er. Ikke fjern filer, og ikke bland inn andre filer.
- Denne måten gir ingen automatiske oppdateringer. Når en ny versjon kommer, erstatter du mappen med den nye ZIP-filen.

## {{L_chat}}. Claude-chatten: last opp skills

Denne måten gjelder claude.ai og Claude-appene.

1. Last ned ZIP-filene for de skillsene du vil bruke.
{{skills_list_indented}}
2. Åpne **Customize → Skills** i Claude, og velg **Upload a skill** fra legg til-knappen.
3. Last opp ZIP-filene én og én, og aktiver skillsene.

**Merk**

- Plugin-ZIP-filen for Claude Code fungerer ikke her. Bruk ZIP-filene for de enkelte skillsene.
- Ikke endre navnet på ZIP-filene før du laster dem opp.
- For å bruke skills må kodekjøring være slått på i innstillingene. Se [den offisielle veiledningen for Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude).
- I organisasjonskontoer kan det hende at administratorens innstillinger hindrer bruk.
- Skills du har lastet opp, oppdateres ikke automatisk. Når en ny versjon kommer, laster du dem opp på nytt.

## 2. Prøv det

Det er lurt å begynne med en forespørsel som ikke endrer filer:

> Jeg skal lage en nettside på norsk. Hva bør jeg passe på? Ikke endre noen filer.

## Kontroller filene (valgfritt)

Hvis du vil kontrollere at filene du har lastet ned, er uskadde, bruker du [SHA256SUMS.txt]({{sums}}).

Legg SHA256SUMS.txt i samme mappe som ZIP-filene du har lastet ned, og kjør denne kommandoen i terminalen. Hvis `shasum` ikke finnes, kan du for eksempel sammenligne SHA-256-verdiene med `Get-FileHash` i Windows PowerShell.

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

Hvis det står `OK` på linjene for filene du har lastet ned, er alt i orden.

---

Andre verktøy: [ChatGPT / Codex]({{page_chatgpt}}) · [Gemini]({{page_gemini}})

Skjermbilder og tilgjengelighet kan endre seg. Den nyeste informasjonen finner du i den offisielle veiledningen for hver tjeneste (siden ble sist kontrollert 14. oktober 2026).
