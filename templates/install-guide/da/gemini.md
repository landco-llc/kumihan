Sådan bruger du {{brand}} med Gemini CLI og Gemini-appen.

> **Om v{{version}}**
> Denne version er beregnet til, at du kan afprøve installationen i dit eget miljø. Funktionen i de enkelte værktøjer er endnu ikke kontrolleret tilstrækkeligt, så ikke alt virker nødvendigvis som forventet.

## 1. Vælg installationsmåde

| Hvor du vil bruge den | Anbefalet måde |
| --- | --- |
| Gemini CLI (alle fire på én gang) | [A. Installér som udvidelse](#a) |
| Gemini CLI (kun det, du har brug for) | [B. Vælg og installér skills](#b) |
| Gemini-appen (web, Mac, mobil) | [C. Upload skills](#c) |

## A. Gemini CLI: installér som udvidelse

Med denne måde installerer du alle fire skills på én gang.

1. Download [ZIP-filen med udvidelsen]({{plugin_url}}).
{{#if plugin_folder}}
2. Når du pakker ZIP-filen ud, får du mappen `{{plugin_folder}}`.
{{else}}
2. Opret en tom mappe med navnet `{{plugin}}`, og pak ZIP-filen ud i den.
{{/if}}
3. Installér fra den mappe:

   ```sh
   gemini extensions install "/absolute/path/{{plugin_dir}}"
   ```

Gennemse oplysningerne, når bekræftelsen vises, og fortsæt derefter. En installeret udvidelse er aktiv i alle projekter.

En udvidelse, der er installeret fra en ZIP-fil, opdateres ikke automatisk. Når der kommer en ny version, udskifter du ZIP-filen.

## B. Gemini CLI: vælg og installér skills

Med denne måde installerer du kun de skills, du har brug for, til ét projekt. Hvis du har brugt måde A, er dette trin ikke nødvendigt.

Hvis du for eksempel vil installere `{{first}}`, kører du følgende i projektet:

```sh
gemini skills install https://github.com/landco-llc/kumihan --path {{skills_path}}/{{first}} --scope workspace
```

Til andre skills ændrer du `--path` til:

{{gemini_paths}}

`--scope workspace` betyder, at den kun bruges i dette projekt. Uden den bliver den tilgængelig i alle dine projekter.

**Sådan opdaterer du**

Kør den samme kommando igen. Den installerede skill bliver erstattet, så gem først eventuelle egne ændringer.

## C. Gemini-appen: upload skills

1. Download ZIP-filerne til de skills, du vil bruge.
{{skills_list_indented}}
2. Åbn **Customize** (eller **More**, hvis du ikke kan se det) → **Skills** → **Upload** i Gemini.
3. Vælg én ZIP-fil ad gangen, gennemse oplysningerne, og vælg **Create**.

**Bemærk**

- Funktionen er tilgængelig for personlige Google-konti for brugere på 18 år eller derover. Arbejds- og skolekonti understøttes ikke i øjeblikket.
- **Keep Activity** skal være slået til.
- Funktionen udrulles gradvist og er måske endnu ikke synlig for dig. Se [Gemini Hjælp](https://support.google.com/gemini/answer/17094296?hl=da).
- ZIP-filen med udvidelsen (til Gemini CLI) virker ikke her.
- Uploadede skills opdateres ikke automatisk. Når der kommer en ny version, uploader du den igen.

## 2. Prøv det

Begynd gerne med en forespørgsel, der ikke ændrer nogen filer:

> Jeg planlægger en præsentation på dansk. Hvad skal jeg være opmærksom på? Lad være med at ændre filer.

## Kontrollér filerne (valgfrit)

Hvis du vil kontrollere, at de downloadede filer er intakte, bruger du [SHA256SUMS.txt]({{sums}}).

Læg SHA256SUMS.txt i samme mappe som de downloadede ZIP-filer, og kør derefter følgende kommando i en terminal. Hvis `shasum` ikke findes, kan du sammenligne SHA-256 med en tilsvarende kommando, for eksempel `Get-FileHash` i Windows PowerShell.

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

Hvis linjerne for de filer, du har downloadet, viser `OK`, er alt i orden.

---

Andre værktøjer: [ChatGPT / Codex]({{page_chatgpt}}) · [Claude]({{page_claude}})

Skærmbilleder og tilgængelighed kan ændre sig. Se den enkelte tjenestes officielle vejledning for de nyeste oplysninger (siden er kontrolleret: 14. oktober 2026).
