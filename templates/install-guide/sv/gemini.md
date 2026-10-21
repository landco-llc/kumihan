Så här använder du {{brand}} med Gemini CLI och Gemini-appen.

> **Om v{{version}}**
> Den här versionen är till för att du ska kunna prova installationen i din egen miljö. Funktionen i de olika verktygen är ännu inte tillräckligt kontrollerad, så allt fungerar kanske inte som väntat.

## 1. Välj installationssätt

| Där du vill använda den | Rekommenderat sätt |
| --- | --- |
| Gemini CLI (alla fyra på en gång) | [A. Installera som tillägg](#a) |
| Gemini CLI (bara det du behöver) | [B. Välj och installera färdigheter](#b) |
| Gemini-appen (webb, Mac, mobil) | [C. Ladda upp färdigheter](#c) |

## A. Gemini CLI: installera som tillägg

Med det här sättet installerar du alla fyra färdigheterna på en gång.

1. Ladda ned [ZIP-filen med tillägget]({{plugin_url}}).
{{#if plugin_folder}}
2. När du packar upp ZIP-filen får du mappen `{{plugin_folder}}`.
{{else}}
2. Skapa en tom mapp med namnet `{{plugin}}` och packa upp ZIP-filen i den.
{{/if}}
3. Installera från den mappen:

   ```sh
   gemini extensions install "/absolute/path/{{plugin_dir}}"
   ```

Granska uppgifterna när bekräftelsen visas och fortsätt sedan. Ett installerat tillägg är aktivt i alla projekt.

Ett tillägg som installerats från en ZIP-fil uppdateras inte automatiskt. När en ny version kommer byter du ut ZIP-filen.

## B. Gemini CLI: välj och installera färdigheter

Med det här sättet installerar du bara de färdigheter du behöver, för ett enskilt projekt. Om du har använt sätt A behövs inte detta steg.

Om du till exempel vill installera `{{first}}` kör du följande i projektet:

```sh
gemini skills install https://github.com/landco-llc/kumihan --path {{skills_path}}/{{first}} --scope workspace
```

För andra färdigheter ändrar du `--path` till:

{{gemini_paths}}

`--scope workspace` innebär att färdigheten bara används i det här projektet. Utan det blir den tillgänglig i alla dina projekt.

**Så uppdaterar du**

Kör samma kommando igen. Den installerade färdigheten ersätts, så spara först eventuella egna ändringar.

## C. Gemini-appen: ladda upp färdigheter

1. Ladda ned ZIP-filerna för de färdigheter du vill använda.
{{skills_list_indented}}
2. Öppna **Customize** (eller **More** om det inte syns) → **Skills** → **Upload** i Gemini.
3. Välj en ZIP-fil i taget, granska uppgifterna och välj **Create**.

**Observera**

- Funktionen är tillgänglig för personliga Google-konton för personer som är 18 år eller äldre. Jobb- och skolkonton stöds inte för närvarande.
- **Keep Activity** måste vara aktiverat.
- Funktionen införs successivt och kanske inte syns för dig ännu. Läs mer i [Gemini-hjälpen](https://support.google.com/gemini/answer/17094296?hl=sv).
- ZIP-filen med tillägget (för Gemini CLI) fungerar inte här.
- Uppladdade färdigheter uppdateras inte automatiskt. När en ny version kommer laddar du upp den igen.

## 2. Prova

Börja gärna med en förfrågan som inte ändrar några filer:

> Jag planerar en presentation på svenska. Vad bör jag tänka på? Ändra inga filer.

## Kontrollera filerna (valfritt)

Om du vill kontrollera att de nedladdade filerna är hela använder du [SHA256SUMS.txt]({{sums}}).

Lägg SHA256SUMS.txt i samma mapp som de nedladdade ZIP-filerna och kör sedan följande kommando i en terminal. Om `shasum` saknas kan du jämföra SHA-256 med ett motsvarande kommando, till exempel `Get-FileHash` i Windows PowerShell.

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

Om raderna för de filer du laddat ned visar `OK` är allt i ordning.

---

Andra verktyg: [ChatGPT / Codex]({{page_chatgpt}}) · [Claude]({{page_claude}})

Skärmar och tillgänglighet kan ändras. Se respektive tjänsts officiella anvisningar för den senaste informationen (sidan kontrollerad: 14 oktober 2026).
