Ta instrukcja wyjaśnia, jak używać {{brand}} w Claude Code i czacie Claude.

> **O wersji v{{version}}**
> Ta wersja służy do wypróbowania instalacji we własnym środowisku. Działanie w poszczególnych narzędziach nie zostało jeszcze w pełni sprawdzone, więc niektóre kroki mogą nie działać zgodnie z oczekiwaniami.

## 1. Wybierz sposób instalacji

| Gdzie chcesz używać | Zalecany sposób |
| --- | --- |
{{#if marketplace}}
| Claude Code | [A. Zainstaluj z GitHuba](#a) (łatwe aktualizacje) |
{{/if}}
| Claude Code (instalacja z pliku ZIP) | [{{L_zip}}. Zainstaluj z pliku ZIP](#{{l_zip}}) |
| Czat Claude (claude.ai i aplikacje) | [{{L_chat}}. Prześlij umiejętności](#{{l_chat}}) |

Claude Code i czat Claude instaluje się na różne sposoby.

{{#if marketplace}}
## A. Claude Code: instalacja z GitHuba

1. W terminalu dodaj źródło dystrybucji KUMIHAN.

   ```sh
   claude plugin marketplace add "https://github.com/landco-llc/kumihan.git#main"
   ```

2. W rozmowie w Claude Code wpisz:

   ```text
   /plugin install {{plugin}}@kumihan-marketplace
   ```

3. Sprawdź informacje, wybierz zakres (tylko Ty, tylko ten projekt itp.) i zainstaluj.

Po instalacji dostępne będą następujące polecenia:

{{claude_commands}}

{{/if}}
## {{L_zip}}. Claude Code: instalacja z pliku ZIP

1. Pobierz [plik ZIP pluginu dla Claude Code]({{plugin_url}}).
{{#if plugin_folder}}
2. Po rozpakowaniu pliku ZIP powstanie folder `{{plugin_folder}}`.
{{else}}
2. Utwórz pusty folder `{{plugin}}` i rozpakuj do niego plik ZIP.
{{/if}}
3. Uruchom Claude Code, wskazując ten folder:

   ```sh
   claude --plugin-dir "/absolute/path/{{plugin_dir}}"
   ```

**Uwagi**

- Używaj zawartości folderu bez zmian. Nie usuwaj plików i nie dodawaj innych.
- W tym sposobie aktualizacje nie są automatyczne. Gdy pojawi się nowa wersja, zastąp folder zawartością nowego pliku ZIP.

## {{L_chat}}. Czat Claude: przesyłanie umiejętności

Ten sposób dotyczy claude.ai i aplikacji Claude.

1. Pobierz pliki ZIP umiejętności, których chcesz używać.
{{skills_list_indented}}
2. W Claude otwórz **Customize → Skills** i przyciskiem dodawania wybierz **Upload a skill**.
3. Prześlij pliki ZIP pojedynczo i włącz każdą umiejętność.

**Uwagi**

- Plik ZIP pluginu dla Claude Code nie działa w tym miejscu. Użyj plików ZIP pojedynczych umiejętności.
- Prześlij pliki ZIP bez zmiany ich nazw.
- Aby korzystać z umiejętności, w ustawieniach musi być włączone wykonywanie kodu. Zobacz [oficjalny przewodnik Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude).
- Na kontach organizacji dostępność może zależeć od ustawień administratora.
- Przesłane umiejętności nie aktualizują się automatycznie. Gdy pojawi się nowa wersja, prześlij je ponownie.

## 2. Wypróbuj

Na początek najlepiej wypróbować prośbę, która nie zmienia żadnych plików:

> Planuję stronę internetową w języku polskim. Na co warto zwrócić uwagę? Proszę, nie zmieniaj żadnych plików.

## Sprawdź poprawność plików (opcjonalnie)

Jeśli chcesz sprawdzić, czy pobrane pliki nie są uszkodzone, użyj [SHA256SUMS.txt]({{sums}}).

Umieść SHA256SUMS.txt w tym samym folderze co pobrane pliki ZIP i uruchom w terminalu poniższe polecenie. Jeśli `shasum` jest niedostępne, porównaj sumy SHA-256 w inny sposób, na przykład za pomocą `Get-FileHash` w Windows PowerShell.

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

Jeśli przy pobranych plikach widać `OK`, wszystko jest w porządku.

---

Inne narzędzia: [ChatGPT / Codex]({{page_chatgpt}}) · [Gemini]({{page_gemini}})

Wygląd ekranów i warunki dostępności mogą się zmieniać. Aktualne informacje znajdziesz w oficjalnych przewodnikach poszczególnych usług (data sprawdzenia tej strony: 14 października 2026 r.).
