Diese Anleitung erklärt, wie Sie {{brand}} mit Claude Code und dem Claude-Chat verwenden.

> **Über v{{version}}**
> Diese Version ist dafür gedacht, die Einrichtung in Ihrer eigenen Umgebung auszuprobieren. Das Verhalten in den einzelnen Werkzeugen ist noch nicht ausreichend geprüft, daher funktioniert womöglich nicht alles wie erwartet.

## 1. Einrichtungsweg wählen

| Wo Sie es verwenden möchten | Empfohlener Weg |
| --- | --- |
{{#if marketplace}}
| Claude Code | [A. Über GitHub einrichten](#a) (einfach zu aktualisieren) |
{{/if}}
| Claude Code (Einrichtung per ZIP) | [{{L_zip}}. Per ZIP einrichten](#{{l_zip}}) |
| Claude-Chat (claude.ai und Apps) | [{{L_chat}}. Skills hochladen](#{{l_chat}}) |

Claude Code und der Claude-Chat werden auf unterschiedliche Weise eingerichtet.

{{#if marketplace}}
## A. Claude Code: über GitHub einrichten

1. Fügen Sie im Terminal die Bezugsquelle von KUMIHAN hinzu.

   ```sh
   claude plugin marketplace add "https://github.com/landco-llc/kumihan.git#main"
   ```

2. Geben Sie in einer Unterhaltung in Claude Code Folgendes ein:

   ```text
   /plugin install {{plugin}}@kumihan-marketplace
   ```

3. Prüfen Sie die Angaben, wählen Sie den Geltungsbereich (nur für Sie, nur für dieses Projekt usw.) und installieren Sie.

Nach der Einrichtung stehen Ihnen diese Befehle zur Verfügung:

{{claude_commands}}

{{/if}}
## {{L_zip}}. Claude Code: per ZIP einrichten

1. Laden Sie die [Plugin-ZIP-Datei für Claude Code]({{plugin_url}}) herunter.
{{#if plugin_folder}}
2. Beim Entpacken entsteht der Ordner `{{plugin_folder}}`.
{{else}}
2. Legen Sie einen leeren Ordner `{{plugin}}` an und entpacken Sie die ZIP-Datei dort hinein.
{{/if}}
3. Starten Sie Claude Code mit diesem Ordner:

   ```sh
   claude --plugin-dir "/absolute/path/{{plugin_dir}}"
   ```

**Hinweise**

- Verwenden Sie den Ordnerinhalt unverändert. Entfernen Sie keine Dateien und fügen Sie keine anderen hinzu.
- Bei diesem Weg gibt es keine automatischen Updates. Ersetzen Sie bei einer neuen Version den Ordner durch die neue ZIP-Datei.

## {{L_chat}}. Claude-Chat: Skills hochladen

Dieser Weg gilt für claude.ai und die Claude-Apps.

1. Laden Sie die ZIP-Dateien der Skills herunter, die Sie verwenden möchten.
{{skills_list_indented}}
2. Öffnen Sie in Claude **Customize → Skills** und wählen Sie über die Schaltfläche zum Hinzufügen **Upload a skill**.
3. Laden Sie die ZIP-Dateien einzeln hoch und aktivieren Sie jeden Skill.

**Hinweise**

- Die Plugin-ZIP-Datei für Claude Code funktioniert hier nicht. Verwenden Sie die ZIP-Dateien der einzelnen Skills.
- Laden Sie die ZIP-Dateien hoch, ohne sie umzubenennen.
- Für Skills muss in den Einstellungen die Codeausführung aktiviert sein. Siehe [Anleitung von Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude).
- Bei Organisationskonten hängt die Verfügbarkeit womöglich von den Einstellungen der Administration ab.
- Hochgeladene Skills werden nicht automatisch aktualisiert. Laden Sie bei einer neuen Version die Dateien erneut hoch.

## 2. Ausprobieren

Beginnen Sie am besten mit einer Anfrage, die keine Dateien verändert:

> Ich plane eine Webseite auf Deutsch. Worauf sollte ich achten? Bitte ändere keine Dateien.

## Dateien prüfen (optional)

Wenn Sie prüfen möchten, ob die heruntergeladenen Dateien unbeschädigt sind, verwenden Sie [SHA256SUMS.txt]({{sums}}).

Legen Sie SHA256SUMS.txt in denselben Ordner wie die heruntergeladenen ZIP-Dateien und führen Sie im Terminal den folgenden Befehl aus. Wenn `shasum` nicht verfügbar ist, vergleichen Sie die SHA-256-Werte zum Beispiel mit `Get-FileHash` in Windows PowerShell.

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

Wenn in den Zeilen Ihrer heruntergeladenen Dateien `OK` steht, ist alles in Ordnung.

---

Andere Werkzeuge: [ChatGPT / Codex]({{page_chatgpt}}) · [Gemini]({{page_gemini}})

Oberflächen und Verfügbarkeit können sich ändern. Aktuelle Informationen finden Sie in den offiziellen Anleitungen der jeweiligen Dienste (Stand dieser Seite: 14. Oktober 2026).
