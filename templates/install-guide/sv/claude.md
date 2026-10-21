Så här använder du {{brand}} med Claude Code och Claude-chatten.

> **Om v{{version}}**
> Den här versionen är till för att du ska kunna prova installationen i din egen miljö. Funktionen i de olika verktygen är ännu inte tillräckligt kontrollerad, så allt fungerar kanske inte som väntat.

## 1. Välj installationssätt

| Där du vill använda den | Rekommenderat sätt |
| --- | --- |
{{#if marketplace}}
| Claude Code | [A. Installera från GitHub](#a) (enkelt att uppdatera) |
{{/if}}
| Claude Code (installation från ZIP) | [{{L_zip}}. Installera från en ZIP-fil](#{{l_zip}}) |
| Claude-chatten (claude.ai och apparna) | [{{L_chat}}. Ladda upp färdigheter](#{{l_chat}}) |

Claude Code och Claude-chatten installeras på olika sätt.

{{#if marketplace}}
## A. Claude Code: installera från GitHub

1. Lägg till KUMIHAN:s distributionskälla i terminalen.

   ```sh
   claude plugin marketplace add "https://github.com/landco-llc/kumihan.git#main"
   ```

2. Skriv följande i en konversation i Claude Code:

   ```text
   /plugin install {{plugin}}@kumihan-marketplace
   ```

3. Granska uppgifterna, välj omfattning (bara du, bara det här projektet och så vidare) och installera.

När installationen är klar kan du använda följande kommandon:

{{claude_commands}}

{{/if}}
## {{L_zip}}. Claude Code: installera från en ZIP-fil

1. Ladda ned [ZIP-filen med pluginen för Claude Code]({{plugin_url}}).
{{#if plugin_folder}}
2. När du packar upp ZIP-filen får du mappen `{{plugin_folder}}`.
{{else}}
2. Skapa en tom mapp med namnet `{{plugin}}` och packa upp ZIP-filen i den.
{{/if}}
3. Starta Claude Code med den mappen:

   ```sh
   claude --plugin-dir "/absolute/path/{{plugin_dir}}"
   ```

**Observera**

- Använd mappens innehåll som det är. Ta inte bort filer och lägg inte till andra filer.
- Det här sättet uppdateras inte automatiskt. När en ny version kommer byter du ut ZIP-filen.

## {{L_chat}}. Claude-chatten: ladda upp färdigheter

Det här sättet gäller claude.ai och Claude-apparna.

1. Ladda ned ZIP-filerna för de färdigheter du vill använda.
{{skills_list_indented}}
2. Öppna **Customize → Skills** i Claude och välj **Upload a skill** via knappen för att lägga till.
3. Ladda upp ZIP-filerna en i taget och aktivera färdigheterna.

**Observera**

- ZIP-filen med pluginen för Claude Code fungerar inte här. Använd ZIP-filerna för de enskilda färdigheterna.
- Ladda upp ZIP-filerna utan att byta namn på dem.
- För att använda färdigheter måste kodkörning vara aktiverad i inställningarna. Läs mer i [Claudes officiella anvisningar](https://support.claude.com/en/articles/12512180-use-skills-in-claude).
- På organisationskonton kan funktionen vara otillgänglig beroende på administratörens inställningar.
- Uppladdade färdigheter uppdateras inte automatiskt. När en ny version kommer laddar du upp den igen.

## 2. Prova

Börja gärna med en förfrågan som inte ändrar några filer:

> Jag planerar en webbsida på svenska. Vad bör jag tänka på? Ändra inga filer.

## Kontrollera filerna (valfritt)

Om du vill kontrollera att de nedladdade filerna är hela använder du [SHA256SUMS.txt]({{sums}}).

Lägg SHA256SUMS.txt i samma mapp som de nedladdade ZIP-filerna och kör sedan följande kommando i en terminal. Om `shasum` saknas kan du jämföra SHA-256 med ett motsvarande kommando, till exempel `Get-FileHash` i Windows PowerShell.

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

Om raderna för de filer du laddat ned visar `OK` är allt i ordning.

---

Andra verktyg: [ChatGPT / Codex]({{page_chatgpt}}) · [Gemini]({{page_gemini}})

Skärmar och tillgänglighet kan ändras. Se respektive tjänsts officiella anvisningar för den senaste informationen (sidan kontrollerad: 14 oktober 2026).
