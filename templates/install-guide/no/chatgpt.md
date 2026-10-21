Denne veiledningen forklarer hvordan du bruker {{brand}} i ChatGPT og Codex.

> **Om v{{version}}**
> Denne versjonen er ment for at du skal kunne prøve installasjonen i ditt eget miljø. Hvordan den fungerer i de enkelte verktøyene, er ennå ikke godt nok kontrollert, så noe kan virke annerledes enn forventet.

## 1. Velg installasjonsmåte

| Der du vil bruke det | Anbefalt måte |
| --- | --- |
| ChatGPT (når du kan laste opp skills) | [A. Legg til skills én og én](#a) |
| ChatGPT (som din egen, private plugin) | [B. Registrer alt samlet som en plugin](#b) |
| Codex (på din egen datamaskin) | [C. Kopier mappen](#c) |

En **skill** er én enkelt funksjon, mens **pluginen** er en pakke som samler alle de fire skillsene.

## 2. Last ned filene

Du finner filene på [utgivelsessiden]({{release}}). Når du klikker på en lenke, lastes ZIP-filen ned.

**Plugin (alle fire skills)**

- {{plugin_link}}

**Skills (én og én)**

{{skills_list}}

## A. Legg til skills i ChatGPT

Denne måten fungerer når ChatGPT viser deg «Skills» med mulighet for opplasting.

1. Velg én skill-ZIP-fil og last den opp.
2. Kontroller opplysningene som vises, og legg til skillen.
3. Gjenta trinnene for hver skill du trenger.

**Merk**

- Plugin-ZIP-filen fungerer ikke her. Bruk ZIP-filene for de enkelte skillsene.
- Hvis du bare legger ved en fil i en chat, blir den ikke lagt til som skill.
- Hvis du ikke finner valget, er det kanskje ikke tilgjengelig ennå for abonnementet eller appen din. Se [veiledningen fra OpenAI](https://learn.chatgpt.com/docs/build-skills).

## B. Registrer en plugin i ChatGPT

Med denne måten registrerer du alle de fire skillsene samlet som din egen, private plugin.

1. Åpne en ny samtale i ChatGPT, og velg `@plugin-creator`.
2. Legg ved plugin-ZIP-filen.
3. Be for eksempel om dette:

   > Registrer denne pakken som min private plugin. Ikke send den inn til den offentlige katalogen.

4. Når registreringen er ferdig, vises **{{display}}** under Plugins i «Personal» eller «Created by me».
5. Installer den ved behov, og aktiver den i en ny samtale.

**Merk**

- Pluginen kan bli lagret i teamets arbeidsområde. Hvis den bare skal være for deg, bør du kontrollere lagringsstedet før du registrerer den.
- Avhengig av abonnement eller innstillingene for arbeidsområdet kan det hende at funksjonen ikke er tilgjengelig. Se [Build plugins](https://learn.chatgpt.com/docs/build-plugins) og [Plugins](https://learn.chatgpt.com/docs/plugins).
- En plugin som er registrert på denne måten, er bare tilgjengelig i kontoen din. Den vises ikke i den offentlige katalogen.

## C. Kopier mappen til Codex

Når du pakker ut en skill-ZIP-fil, får du en mappe som `{{first}}`. Kopier denne mappen dit Codex leter etter skills.

| Omfang | Plassering |
| --- | --- |
| Bare i ett bestemt prosjekt | `.agents/skills/` i prosjektet |
| I alle prosjekter | `~/.agents/skills/` i hjemmemappen din |

Slik legger du for eksempel `{{first}}` til i et prosjekt:

```sh
mkdir -p /path/to/your-project/.agents/skills
cp -R {{first}} /path/to/your-project/.agents/skills/
```

**Merk**

- Kopier hele mappen med alt innholdet. Med bare enkelte filer fungerer ikke skillen som den skal.
- Hvis det allerede finnes en mappe med samme navn, bør du kontrollere innholdet før du overskriver den.

## 3. Prøv det

Når installasjonen er ferdig, åpner du en ny samtale og kaller opp en skill.

| Verktøy | Slik kaller du den opp |
| --- | --- |
| ChatGPT | velg via `@` |
| Codex | velg via `$` eller `/skills` |

Det er lurt å begynne med en forespørsel som ikke endrer filer:

> Jeg skal lage en rapport på norsk. Hva bør jeg passe på? Ikke endre noen filer.

## Kontroller filene (valgfritt)

Hvis du vil kontrollere at filene du har lastet ned, er uskadde, bruker du [SHA256SUMS.txt]({{sums}}).

Legg SHA256SUMS.txt i samme mappe som ZIP-filene du har lastet ned, og kjør denne kommandoen i terminalen. Hvis `shasum` ikke finnes, kan du for eksempel sammenligne SHA-256-verdiene med `Get-FileHash` i Windows PowerShell.

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

Hvis det står `OK` på linjene for filene du har lastet ned, er alt i orden.

---

Andre verktøy: [Claude]({{page_claude}}) · [Gemini]({{page_gemini}})

Skjermbilder og tilgjengelighet kan endre seg. Den nyeste informasjonen finner du i den offisielle veiledningen for hver tjeneste (siden ble sist kontrollert 14. oktober 2026).
