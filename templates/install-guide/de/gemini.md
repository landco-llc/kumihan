Diese Anleitung erklärt, wie Sie {{brand}} mit Gemini CLI und der Gemini-App verwenden.

> **Über v{{version}}**
> Diese Version ist dafür gedacht, die Einrichtung in Ihrer eigenen Umgebung auszuprobieren. Das Verhalten in den einzelnen Werkzeugen ist noch nicht ausreichend geprüft, daher funktioniert womöglich nicht alles wie erwartet.

## 1. Einrichtungsweg wählen

| Wo Sie es verwenden möchten | Empfohlener Weg |
| --- | --- |
| Gemini CLI (alle vier gemeinsam) | [A. Als Erweiterung einrichten](#a) |
| Gemini CLI (nur die benötigten) | [B. Skills auswählen und einrichten](#b) |
| Gemini-App (Web, Mac, Smartphone) | [C. Skills hochladen](#c) |

## A. Gemini CLI: als Erweiterung einrichten

Mit diesem Weg richten Sie alle vier Skills auf einmal ein.

1. Laden Sie die [ZIP-Datei der Erweiterung]({{plugin_url}}) herunter.
{{#if plugin_folder}}
2. Beim Entpacken entsteht der Ordner `{{plugin_folder}}`.
{{else}}
2. Legen Sie einen leeren Ordner `{{plugin}}` an und entpacken Sie die ZIP-Datei dort hinein.
{{/if}}
3. Installieren Sie aus diesem Ordner:

   ```sh
   gemini extensions install "/absolute/path/{{plugin_dir}}"
   ```

Wenn eine Bestätigung angezeigt wird, prüfen Sie die Angaben und fahren Sie fort. Nach der Installation ist die Erweiterung in allen Projekten aktiv.

Eine per ZIP installierte Erweiterung wird nicht automatisch aktualisiert. Ersetzen Sie sie bei einer neuen Version durch die neue ZIP-Datei.

## B. Gemini CLI: Skills auswählen und einrichten

Mit diesem Weg richten Sie nur die benötigten Skills für ein einzelnes Projekt ein. Wenn Sie Weg A verwendet haben, ist dieser Schritt nicht nötig.

Um zum Beispiel `{{first}}` einzurichten, führen Sie im betreffenden Projekt Folgendes aus:

```sh
gemini skills install https://github.com/landco-llc/kumihan --path {{skills_path}}/{{first}} --scope workspace
```

Für andere Skills ändern Sie `--path` wie folgt:

{{gemini_paths}}

`--scope workspace` beschränkt den Skill auf dieses Projekt. Ohne diese Option ist er in allen Ihren Projekten verfügbar.

**Aktualisieren**

Führen Sie denselben Befehl erneut aus. Der installierte Skill wird ersetzt; sichern Sie daher zuvor eigene Änderungen daran.

## C. Gemini-App: Skills hochladen

1. Laden Sie die ZIP-Dateien der Skills herunter, die Sie verwenden möchten.
{{skills_list_indented}}
2. Öffnen Sie in Gemini **Customize** (falls nicht sichtbar: **More**) → **Skills** → **Upload**.
3. Wählen Sie die ZIP-Dateien einzeln aus, prüfen Sie die Angaben und klicken Sie auf **Create**.

**Hinweise**

- Verfügbar für private Google-Konten von Personen ab 18 Jahren. Arbeits- und Schulkonten werden derzeit nicht unterstützt.
- „Keep Activity“ (Aktivitäten speichern) muss aktiviert sein.
- Die Funktion wird schrittweise eingeführt und ist bei Ihnen womöglich noch nicht verfügbar. Siehe [Gemini-Hilfe](https://support.google.com/gemini/answer/17094296?hl=de).
- Die ZIP-Datei der Erweiterung (für Gemini CLI) funktioniert hier nicht.
- Hochgeladene Skills werden nicht automatisch aktualisiert. Laden Sie bei einer neuen Version die Dateien erneut hoch.

## 2. Ausprobieren

Beginnen Sie am besten mit einer Anfrage, die keine Dateien verändert:

> Ich plane eine Präsentation auf Deutsch. Worauf sollte ich achten? Bitte ändere keine Dateien.

## Dateien prüfen (optional)

Wenn Sie prüfen möchten, ob die heruntergeladenen Dateien unbeschädigt sind, verwenden Sie [SHA256SUMS.txt]({{sums}}).

Legen Sie SHA256SUMS.txt in denselben Ordner wie die heruntergeladenen ZIP-Dateien und führen Sie im Terminal den folgenden Befehl aus. Wenn `shasum` nicht verfügbar ist, vergleichen Sie die SHA-256-Werte zum Beispiel mit `Get-FileHash` in Windows PowerShell.

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

Wenn in den Zeilen Ihrer heruntergeladenen Dateien `OK` steht, ist alles in Ordnung.

---

Andere Werkzeuge: [ChatGPT / Codex]({{page_chatgpt}}) · [Claude]({{page_claude}})

Oberflächen und Verfügbarkeit können sich ändern. Aktuelle Informationen finden Sie in den offiziellen Anleitungen der jeweiligen Dienste (Stand dieser Seite: 14. Oktober 2026).
