Sådan bruger du {{brand}} med ChatGPT og Codex.

> **Om v{{version}}**
> Denne version er beregnet til, at du kan afprøve installationen i dit eget miljø. Funktionen i de enkelte værktøjer er endnu ikke kontrolleret tilstrækkeligt, så ikke alt virker nødvendigvis som forventet.

## 1. Vælg installationsmåde

| Hvor du vil bruge den | Anbefalet måde |
| --- | --- |
| ChatGPT (hvis du kan uploade skills) | [A. Tilføj skills én ad gangen](#a) |
| ChatGPT (som dit eget private plugin) | [B. Registrér det hele som et plugin](#b) |
| Codex (på din computer) | [C. Kopiér mapper](#c) |

En **skill** er én enkelt funktion. **Pluginet** er en pakke med alle fire skills.

## 2. Download filerne

Filerne ligger på [udgivelsessiden]({{release}}). Vælg et link for at downloade ZIP-filen.

**Plugin (alle fire skills)**

- {{plugin_link}}

**Skills (én ad gangen)**

{{skills_list}}

## A. Tilføj skills i ChatGPT

Denne måde virker, hvis ChatGPT viser **Skills** med mulighed for upload.

1. Upload én ZIP-fil med en skill.
2. Gennemse oplysningerne, og tilføj den.
3. Gentag for hver skill, du har brug for.

**Bemærk**

- Pluginets ZIP-fil virker ikke her. Brug ZIP-filerne til de enkelte skills.
- En fil, der blot vedhæftes i en chat, bliver ikke installeret som skill.
- Hvis muligheden ikke vises, er den måske endnu ikke tilgængelig for dit abonnement eller din app. Se [OpenAI's vejledning](https://learn.chatgpt.com/docs/build-skills).

## B. Registrér et plugin i ChatGPT

Med denne måde registrerer du alle fire skills som dit eget private plugin.

1. Start en ny samtale i ChatGPT, og vælg `@plugin-creator`.
2. Vedhæft pluginets ZIP-fil.
3. Bed om følgende:

   > Registrér denne pakke som mit private plugin. Indsend den ikke til det offentlige katalog.

4. Når registreringen er gennemført, vises **{{display}}** under Plugins, i »Personal« eller »Created by me«.
5. Installér det efter behov, og aktivér det derefter i en ny samtale.

**Bemærk**

- Pluginet kan blive gemt i dit teams arbejdsområde. Hvis det kun skal være dit, så kontrollér placeringen, før du registrerer det.
- Funktionen er måske ikke tilgængelig, afhængigt af dit abonnement eller arbejdsområdets indstillinger. Se [Build plugins](https://learn.chatgpt.com/docs/build-plugins) og [Plugins](https://learn.chatgpt.com/docs/plugins).
- Et plugin, der er registreret på denne måde, kan kun bruges med din konto. Det vises ikke i det offentlige katalog.

## C. Kopiér mapper til Codex

Når du pakker en skills ZIP-fil ud, får du en mappe som `{{first}}`. Kopiér mappen derhen, hvor Codex leder efter skills.

| Omfang | Destination |
| --- | --- |
| Kun ét bestemt projekt | `.agents/skills/` i projektet |
| Alle projekter | `~/.agents/skills/` i din hjemmemappe |

Sådan tilføjer du for eksempel `{{first}}` til et projekt:

```sh
mkdir -p /path/to/your-project/.agents/skills
cp -R {{first}} /path/to/your-project/.agents/skills/
```

**Bemærk**

- Kopiér hele mappen med alt indhold. En skill virker ikke korrekt med kun nogle af filerne.
- Hvis der allerede findes en mappe med samme navn, så kontrollér indholdet, før du overskriver den.

## 3. Prøv det

Når installationen er færdig, åbner du en ny samtale og kalder en skill.

| Værktøj | Sådan kalder du den |
| --- | --- |
| ChatGPT | Vælg den via `@` |
| Codex | Vælg den via `$` eller `/skills` |

Begynd gerne med en forespørgsel, der ikke ændrer nogen filer:

> Jeg planlægger en rapport på dansk. Hvad skal jeg være opmærksom på? Lad være med at ændre filer.

## Kontrollér filerne (valgfrit)

Hvis du vil kontrollere, at de downloadede filer er intakte, bruger du [SHA256SUMS.txt]({{sums}}).

Læg SHA256SUMS.txt i samme mappe som de downloadede ZIP-filer, og kør derefter følgende kommando i en terminal. Hvis `shasum` ikke findes, kan du sammenligne SHA-256 med en tilsvarende kommando, for eksempel `Get-FileHash` i Windows PowerShell.

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

Hvis linjerne for de filer, du har downloadet, viser `OK`, er alt i orden.

---

Andre værktøjer: [Claude]({{page_claude}}) · [Gemini]({{page_gemini}})

Skærmbilleder og tilgængelighed kan ændre sig. Se den enkelte tjenestes officielle vejledning for de nyeste oplysninger (siden er kontrolleret: 14. oktober 2026).
