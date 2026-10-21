Ta instrukcja wyjaśnia, jak używać {{brand}} w ChatGPT i Codex.

> **O wersji v{{version}}**
> Ta wersja służy do wypróbowania instalacji we własnym środowisku. Działanie w poszczególnych narzędziach nie zostało jeszcze w pełni sprawdzone, więc niektóre kroki mogą nie działać zgodnie z oczekiwaniami.

## 1. Wybierz sposób instalacji

| Gdzie chcesz używać | Zalecany sposób |
| --- | --- |
| ChatGPT (jeśli można przesyłać umiejętności) | [A. Dodaj umiejętności pojedynczo](#a) |
| ChatGPT (jako własny, prywatny plugin) | [B. Zarejestruj wszystko jako plugin](#b) |
| Codex (na komputerze) | [C. Skopiuj foldery](#c) |

**Umiejętność** (Skill) to jedna funkcja, a **plugin** to pakiet łączący wszystkie cztery umiejętności.

## 2. Pobierz pliki

Wszystkie pliki są na [stronie wydania]({{release}}). Kliknij link, aby pobrać plik ZIP.

**Plugin (wszystkie cztery umiejętności)**

- {{plugin_link}}

**Umiejętności (pojedynczo)**

{{skills_list}}

## A. Dodaj umiejętności do ChatGPT

Z tego sposobu możesz skorzystać, jeśli w ChatGPT widzisz sekcję „Skills” z opcją przesyłania.

1. Wybierz jeden plik ZIP umiejętności i prześlij go.
2. Sprawdź wyświetlone informacje i dodaj umiejętność.
3. Powtórz te kroki dla każdej potrzebnej umiejętności.

**Uwagi**

- Plik ZIP pluginu nie działa w tym sposobie. Użyj plików ZIP pojedynczych umiejętności.
- Samo załączenie pliku do czatu nie dodaje go jako umiejętności.
- Jeśli nie widzisz tej opcji, być może nie jest jeszcze dostępna w Twoim planie lub aplikacji. Zobacz [oficjalny przewodnik OpenAI](https://learn.chatgpt.com/docs/build-skills).

## B. Zarejestruj plugin w ChatGPT

Ten sposób rejestruje wszystkie cztery umiejętności razem jako Twój własny, prywatny plugin.

1. Otwórz w ChatGPT nową rozmowę i wybierz `@plugin-creator`.
2. Załącz plik ZIP pluginu.
3. Poproś na przykład tak:

   > Zarejestruj, proszę, ten pakiet jako mój prywatny plugin. Nie zgłaszaj go do publicznego katalogu.

4. Po rejestracji **{{display}}** pojawi się w sekcji Plugins, w „Personal” lub „Created by me”.
5. W razie potrzeby zainstaluj plugin i włącz go w nowej rozmowie.

**Uwagi**

- Plugin może zostać zapisany w przestrzeni roboczej Twojego zespołu. Jeśli ma być tylko dla Ciebie, przed rejestracją sprawdź miejsce zapisu.
- W zależności od planu lub ustawień przestrzeni roboczej ta funkcja może być niedostępna. Zobacz [Build plugins](https://learn.chatgpt.com/docs/build-plugins) i [Plugins](https://learn.chatgpt.com/docs/plugins).
- Plugin zarejestrowany w ten sposób jest dostępny tylko na Twoim koncie. Nie pojawi się w publicznym katalogu.

## C. Skopiuj foldery dla Codex

Po rozpakowaniu pliku ZIP umiejętności powstaje folder, na przykład `{{first}}`. Skopiuj ten folder do miejsca, z którego Codex wczytuje umiejętności.

| Zakres | Miejsce docelowe |
| --- | --- |
| Tylko w wybranym projekcie | `.agents/skills/` w projekcie |
| We wszystkich projektach | `~/.agents/skills/` w folderze domowym |

Na przykład, aby dodać `{{first}}` do projektu:

```sh
mkdir -p /path/to/your-project/.agents/skills
cp -R {{first}} /path/to/your-project/.agents/skills/
```

**Uwagi**

- Skopiuj cały folder wraz z całą zawartością. Z samymi wybranymi plikami umiejętność nie będzie działać poprawnie.
- Jeśli folder o tej samej nazwie już istnieje, sprawdź jego zawartość przed nadpisaniem.

## 3. Wypróbuj

Po instalacji otwórz nową rozmowę i wywołaj umiejętność.

| Narzędzie | Sposób wywołania |
| --- | --- |
| ChatGPT | wybierz z `@` |
| Codex | wybierz z `$` lub `/skills` |

Na początek najlepiej wypróbować prośbę, która nie zmienia żadnych plików:

> Planuję raport w języku polskim. Na co warto zwrócić uwagę? Proszę, nie zmieniaj żadnych plików.

## Sprawdź poprawność plików (opcjonalnie)

Jeśli chcesz sprawdzić, czy pobrane pliki nie są uszkodzone, użyj [SHA256SUMS.txt]({{sums}}).

Umieść SHA256SUMS.txt w tym samym folderze co pobrane pliki ZIP i uruchom w terminalu poniższe polecenie. Jeśli `shasum` jest niedostępne, porównaj sumy SHA-256 w inny sposób, na przykład za pomocą `Get-FileHash` w Windows PowerShell.

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

Jeśli przy pobranych plikach widać `OK`, wszystko jest w porządku.

---

Inne narzędzia: [Claude]({{page_claude}}) · [Gemini]({{page_gemini}})

Wygląd ekranów i warunki dostępności mogą się zmieniać. Aktualne informacje znajdziesz w oficjalnych przewodnikach poszczególnych usług (data sprawdzenia tej strony: 14 października 2026 r.).
