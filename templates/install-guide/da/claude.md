Sådan bruger du {{brand}} med Claude Code og Claude-chat.

> **Om v{{version}}**
> Denne version er beregnet til, at du kan afprøve installationen i dit eget miljø. Funktionen i de enkelte værktøjer er endnu ikke kontrolleret tilstrækkeligt, så ikke alt virker nødvendigvis som forventet.

## 1. Vælg installationsmåde

| Hvor du vil bruge den | Anbefalet måde |
| --- | --- |
{{#if marketplace}}
| Claude Code | [A. Installér fra GitHub](#a) (let at opdatere) |
{{/if}}
| Claude Code (installation fra ZIP) | [{{L_zip}}. Installér fra en ZIP-fil](#{{l_zip}}) |
| Claude-chat (claude.ai og apps) | [{{L_chat}}. Upload skills](#{{l_chat}}) |

Claude Code og Claude-chat installeres på forskellige måder.

{{#if marketplace}}
## A. Claude Code: installér fra GitHub

1. Tilføj KUMIHAN's distributionskilde i terminalen.

   ```sh
   claude plugin marketplace add "https://github.com/landco-llc/kumihan.git#main"
   ```

2. Skriv følgende i en samtale i Claude Code:

   ```text
   /plugin install {{plugin}}@kumihan-marketplace
   ```

3. Gennemse oplysningerne, vælg omfang (kun dig, kun dette projekt osv.), og installér.

Når installationen er færdig, kan du bruge disse kommandoer:

{{claude_commands}}

{{/if}}
## {{L_zip}}. Claude Code: installér fra en ZIP-fil

1. Download [ZIP-filen med pluginet til Claude Code]({{plugin_url}}).
{{#if plugin_folder}}
2. Når du pakker ZIP-filen ud, får du mappen `{{plugin_folder}}`.
{{else}}
2. Opret en tom mappe med navnet `{{plugin}}`, og pak ZIP-filen ud i den.
{{/if}}
3. Start Claude Code med den mappe:

   ```sh
   claude --plugin-dir "/absolute/path/{{plugin_dir}}"
   ```

**Bemærk**

- Brug mappens indhold, som det er. Fjern ikke filer, og tilføj ikke andre filer.
- Denne måde opdateres ikke automatisk. Når der kommer en ny version, udskifter du ZIP-filen.

## {{L_chat}}. Claude-chat: upload skills

Denne måde gælder claude.ai og Claude-apps.

1. Download ZIP-filerne til de skills, du vil bruge.
{{skills_list_indented}}
2. Åbn **Customize → Skills** i Claude, og vælg **Upload a skill** via knappen til at tilføje.
3. Upload ZIP-filerne én ad gangen, og aktivér hver skill.

**Bemærk**

- ZIP-filen med pluginet til Claude Code virker ikke her. Brug ZIP-filerne til de enkelte skills.
- Upload ZIP-filerne uden at omdøbe dem.
- For at bruge skills skal kodekørsel være slået til i indstillingerne. Se [Claudes officielle vejledning](https://support.claude.com/en/articles/12512180-use-skills-in-claude).
- På organisationskonti kan funktionen være utilgængelig, afhængigt af administratorens indstillinger.
- Uploadede skills opdateres ikke automatisk. Når der kommer en ny version, uploader du den igen.

## 2. Prøv det

Begynd gerne med en forespørgsel, der ikke ændrer nogen filer:

> Jeg planlægger en webside på dansk. Hvad skal jeg være opmærksom på? Lad være med at ændre filer.

## Kontrollér filerne (valgfrit)

Hvis du vil kontrollere, at de downloadede filer er intakte, bruger du [SHA256SUMS.txt]({{sums}}).

Læg SHA256SUMS.txt i samme mappe som de downloadede ZIP-filer, og kør derefter følgende kommando i en terminal. Hvis `shasum` ikke findes, kan du sammenligne SHA-256 med en tilsvarende kommando, for eksempel `Get-FileHash` i Windows PowerShell.

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

Hvis linjerne for de filer, du har downloadet, viser `OK`, er alt i orden.

---

Andre værktøjer: [ChatGPT / Codex]({{page_chatgpt}}) · [Gemini]({{page_gemini}})

Skærmbilleder og tilgængelighed kan ændre sig. Se den enkelte tjenestes officielle vejledning for de nyeste oplysninger (siden er kontrolleret: 14. oktober 2026).
