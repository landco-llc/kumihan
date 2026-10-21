Ta instrukcja wyjaśnia, jak używać {{brand}} w Gemini CLI i aplikacji Gemini.

> **O wersji v{{version}}**
> Ta wersja służy do wypróbowania instalacji we własnym środowisku. Działanie w poszczególnych narzędziach nie zostało jeszcze w pełni sprawdzone, więc niektóre kroki mogą nie działać zgodnie z oczekiwaniami.

## 1. Wybierz sposób instalacji

| Gdzie chcesz używać | Zalecany sposób |
| --- | --- |
| Gemini CLI (wszystkie cztery naraz) | [A. Zainstaluj jako rozszerzenie](#a) |
| Gemini CLI (tylko potrzebne) | [B. Wybierz i zainstaluj umiejętności](#b) |
| Aplikacja Gemini (web, Mac, smartfon) | [C. Prześlij umiejętności](#c) |

## A. Gemini CLI: instalacja jako rozszerzenie

Ten sposób instaluje wszystkie cztery umiejętności naraz.

1. Pobierz [plik ZIP rozszerzenia]({{plugin_url}}).
{{#if plugin_folder}}
2. Po rozpakowaniu pliku ZIP powstanie folder `{{plugin_folder}}`.
{{else}}
2. Utwórz pusty folder `{{plugin}}` i rozpakuj do niego plik ZIP.
{{/if}}
3. Zainstaluj, wskazując ten folder:

   ```sh
   gemini extensions install "/absolute/path/{{plugin_dir}}"
   ```

Gdy pojawi się ekran potwierdzenia, sprawdź informacje i kontynuuj. Po instalacji rozszerzenie jest aktywne we wszystkich projektach.

Rozszerzenie zainstalowane z pliku ZIP nie aktualizuje się automatycznie. Gdy pojawi się nowa wersja, zastąp je nowym plikiem ZIP.

## B. Gemini CLI: wybór i instalacja umiejętności

Ten sposób instaluje tylko potrzebne umiejętności, osobno dla każdego projektu. Jeśli użyto sposobu A, ten krok nie jest potrzebny.

Na przykład, aby zainstalować `{{first}}`, uruchom w wybranym projekcie:

```sh
gemini skills install https://github.com/landco-llc/kumihan --path {{skills_path}}/{{first}} --scope workspace
```

Aby zainstalować inne umiejętności, zmień `--path` w następujący sposób:

{{gemini_paths}}

`--scope workspace` ogranicza umiejętność do tego projektu. Bez tej opcji będzie dostępna we wszystkich Twoich projektach.

**Aktualizacja**

Uruchom ponownie to samo polecenie. Zainstalowana umiejętność zostanie zastąpiona, więc najpierw zapisz wprowadzone w niej własne zmiany.

## C. Aplikacja Gemini: przesyłanie umiejętności

1. Pobierz pliki ZIP umiejętności, których chcesz używać.
{{skills_list_indented}}
2. W Gemini otwórz **Customize** (jeśli go nie widać, **More**) → **Skills** → **Upload**.
3. Wybieraj pliki ZIP pojedynczo, sprawdź informacje i kliknij **Create**.

**Uwagi**

- Funkcja jest dostępna dla osobistych kont Google użytkowników w wieku od 18 lat. Konta służbowe i szkolne nie są obecnie obsługiwane.
- Musi być włączona opcja „Keep Activity” („Zapisuj aktywność”).
- Funkcja jest udostępniana stopniowo, więc może jeszcze nie być widoczna. Zobacz [oficjalną pomoc Gemini](https://support.google.com/gemini/answer/17094296?hl=pl).
- Plik ZIP rozszerzenia (dla Gemini CLI) nie działa w tym miejscu.
- Przesłane umiejętności nie aktualizują się automatycznie. Gdy pojawi się nowa wersja, prześlij je ponownie.

## 2. Wypróbuj

Na początek najlepiej wypróbować prośbę, która nie zmienia żadnych plików:

> Planuję prezentację w języku polskim. Na co warto zwrócić uwagę? Proszę, nie zmieniaj żadnych plików.

## Sprawdź poprawność plików (opcjonalnie)

Jeśli chcesz sprawdzić, czy pobrane pliki nie są uszkodzone, użyj [SHA256SUMS.txt]({{sums}}).

Umieść SHA256SUMS.txt w tym samym folderze co pobrane pliki ZIP i uruchom w terminalu poniższe polecenie. Jeśli `shasum` jest niedostępne, porównaj sumy SHA-256 w inny sposób, na przykład za pomocą `Get-FileHash` w Windows PowerShell.

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

Jeśli przy pobranych plikach widać `OK`, wszystko jest w porządku.

---

Inne narzędzia: [ChatGPT / Codex]({{page_chatgpt}}) · [Claude]({{page_claude}})

Wygląd ekranów i warunki dostępności mogą się zmieniać. Aktualne informacje znajdziesz w oficjalnych przewodnikach poszczególnych usług (data sprawdzenia tej strony: 14 października 2026 r.).
