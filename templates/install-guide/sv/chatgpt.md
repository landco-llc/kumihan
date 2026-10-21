Så här använder du {{brand}} med ChatGPT och Codex.

> **Om v{{version}}**
> Den här versionen är till för att du ska kunna prova installationen i din egen miljö. Funktionen i de olika verktygen är ännu inte tillräckligt kontrollerad, så allt fungerar kanske inte som väntat.

## 1. Välj installationssätt

| Där du vill använda den | Rekommenderat sätt |
| --- | --- |
| ChatGPT (om det går att ladda upp färdigheter) | [A. Lägg till färdigheter en i taget](#a) |
| ChatGPT (som din egen privata plugin) | [B. Registrera allt som en plugin](#b) |
| Codex (på din dator) | [C. Kopiera mappar](#c) |

En **färdighet** (skill) är en enskild funktion. **Pluginen** är ett paket med alla fyra färdigheterna.

## 2. Ladda ned filerna

Filerna finns på [utgivningssidan]({{release}}). Välj en länk för att ladda ned ZIP-filen.

**Plugin (alla fyra färdigheterna)**

- {{plugin_link}}

**Färdigheter (en i taget)**

{{skills_list}}

## A. Lägg till färdigheter i ChatGPT

Det här sättet fungerar om ChatGPT visar **Skills** med ett alternativ för uppladdning.

1. Ladda upp en ZIP-fil med en färdighet.
2. Granska uppgifterna som visas och lägg till färdigheten.
3. Upprepa för varje färdighet du behöver.

**Observera**

- Pluginens ZIP-fil fungerar inte här. Använd ZIP-filerna för de enskilda färdigheterna.
- Att bifoga en fil i en chatt installerar den inte som färdighet.
- Om alternativet inte syns är det kanske ännu inte tillgängligt för din plan eller app. Läs [OpenAI:s anvisningar](https://learn.chatgpt.com/docs/build-skills).

## B. Registrera en plugin i ChatGPT

Med det här sättet registrerar du alla fyra färdigheterna som din egen privata plugin.

1. Öppna en ny konversation i ChatGPT och välj `@plugin-creator`.
2. Bifoga pluginens ZIP-fil.
3. Be om följande:

   > Registrera det här paketet som min privata plugin. Skicka inte in det till den offentliga katalogen.

4. När registreringen är klar visas **{{display}}** under Plugins, i ”Personal” eller ”Created by me”.
5. Installera den vid behov och aktivera den sedan i en ny konversation.

**Observera**

- Pluginen kan sparas i teamets arbetsyta. Om den bara ska vara din, kontrollera var den sparas innan du registrerar den.
- Funktionen kan saknas beroende på din plan eller arbetsytans inställningar. Läs [Build plugins](https://learn.chatgpt.com/docs/build-plugins) och [Plugins](https://learn.chatgpt.com/docs/plugins).
- En plugin som registreras på det här sättet kan bara användas med ditt konto. Den visas inte i den offentliga katalogen.

## C. Kopiera mappar till Codex

När du packar upp en färdighets ZIP-fil får du en mapp, till exempel `{{first}}`. Kopiera mappen dit där Codex letar efter färdigheter.

| Omfattning | Mål |
| --- | --- |
| Bara ett visst projekt | `.agents/skills/` i projektet |
| Alla projekt | `~/.agents/skills/` i din hemmapp |

Så här lägger du till exempel till `{{first}}` i ett projekt:

```sh
mkdir -p /path/to/your-project/.agents/skills
cp -R {{first}} /path/to/your-project/.agents/skills/
```

**Observera**

- Kopiera hela mappen med allt innehåll. Färdigheten fungerar inte korrekt med bara några av filerna.
- Om det redan finns en mapp med samma namn, kontrollera innehållet innan du skriver över den.

## 3. Prova

När installationen är klar öppnar du en ny konversation och anropar en färdighet.

| Verktyg | Så anropar du |
| --- | --- |
| ChatGPT | Välj den via `@` |
| Codex | Välj den via `$` eller `/skills` |

Börja gärna med en förfrågan som inte ändrar några filer:

> Jag planerar en rapport på svenska. Vad bör jag tänka på? Ändra inga filer.

## Kontrollera filerna (valfritt)

Om du vill kontrollera att de nedladdade filerna är hela använder du [SHA256SUMS.txt]({{sums}}).

Lägg SHA256SUMS.txt i samma mapp som de nedladdade ZIP-filerna och kör sedan följande kommando i en terminal. Om `shasum` saknas kan du jämföra SHA-256 med ett motsvarande kommando, till exempel `Get-FileHash` i Windows PowerShell.

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

Om raderna för de filer du laddat ned visar `OK` är allt i ordning.

---

Andra verktyg: [Claude]({{page_claude}}) · [Gemini]({{page_gemini}})

Skärmar och tillgänglighet kan ändras. Se respektive tjänsts officiella anvisningar för den senaste informationen (sidan kontrollerad: 14 oktober 2026).
