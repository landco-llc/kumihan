Diese Anleitung erklärt, wie Sie {{brand}} mit ChatGPT und Codex verwenden.

> **Über v{{version}}**
> Diese Version ist dafür gedacht, die Einrichtung in Ihrer eigenen Umgebung auszuprobieren. Das Verhalten in den einzelnen Werkzeugen ist noch nicht ausreichend geprüft, daher funktioniert womöglich nicht alles wie erwartet.

## 1. Einrichtungsweg wählen

| Wo Sie es verwenden möchten | Empfohlener Weg |
| --- | --- |
| ChatGPT (wenn Skills hochgeladen werden können) | [A. Skills einzeln hinzufügen](#a) |
| ChatGPT (als eigenes, privates Plugin) | [B. Als Plugin gesammelt registrieren](#b) |
| Codex (auf Ihrem Computer) | [C. Ordner kopieren](#c) |

Ein **Skill** ist eine einzelne Funktion, das **Plugin** ist ein Paket, das alle vier Skills bündelt.

## 2. Dateien herunterladen

Alle Dateien finden Sie auf der [Release-Seite]({{release}}). Ein Klick auf einen Link lädt die ZIP-Datei herunter.

**Plugin (alle vier Skills)**

- {{plugin_link}}

**Skills (einzeln)**

{{skills_list}}

## A. Skills zu ChatGPT hinzufügen

Dieser Weg funktioniert, wenn ChatGPT Ihnen „Skills“ mit einer Upload-Möglichkeit anzeigt.

1. Wählen Sie eine Skill-ZIP-Datei aus und laden Sie sie hoch.
2. Prüfen Sie die angezeigten Angaben und fügen Sie den Skill hinzu.
3. Wiederholen Sie diese Schritte für jeden Skill, den Sie benötigen.

**Hinweise**

- Die Plugin-ZIP-Datei funktioniert hier nicht. Verwenden Sie die ZIP-Dateien der einzelnen Skills.
- Wenn Sie eine Datei nur an einen Chat anhängen, wird sie nicht als Skill hinzugefügt.
- Wenn Sie die Option nicht finden, ist sie für Ihren Tarif oder Ihre App womöglich noch nicht verfügbar. Siehe [Anleitung von OpenAI](https://learn.chatgpt.com/docs/build-skills).

## B. In ChatGPT als Plugin registrieren

Mit diesem Weg registrieren Sie alle vier Skills gemeinsam als Ihr eigenes, privates Plugin.

1. Öffnen Sie in ChatGPT eine neue Unterhaltung und wählen Sie `@plugin-creator`.
2. Hängen Sie die Plugin-ZIP-Datei an.
3. Bitten Sie zum Beispiel:

   > Bitte registriere dieses Paket als mein privates Plugin. Reiche es nicht beim öffentlichen Verzeichnis ein.

4. Nach der Registrierung erscheint **{{display}}** unter Plugins in „Personal“ oder „Created by me“.
5. Installieren Sie es bei Bedarf und aktivieren Sie es in einer neuen Unterhaltung.

**Hinweise**

- Das Plugin wird womöglich im Workspace Ihres Teams gespeichert. Wenn es nur für Sie sein soll, prüfen Sie vor der Registrierung den Speicherort.
- Je nach Tarif oder Workspace-Einstellungen ist diese Funktion womöglich nicht verfügbar. Siehe [Build plugins](https://learn.chatgpt.com/docs/build-plugins) und [Plugins](https://learn.chatgpt.com/docs/plugins).
- Ein so registriertes Plugin ist nur in Ihrem Konto verfügbar. Es wird nicht im öffentlichen Verzeichnis aufgeführt.

## C. Ordner für Codex kopieren

Wenn Sie eine Skill-ZIP-Datei entpacken, erhalten Sie einen Ordner wie `{{first}}`. Kopieren Sie diesen Ordner an den Ort, an dem Codex nach Skills sucht.

| Geltungsbereich | Zielort |
| --- | --- |
| Nur in einem bestimmten Projekt | `.agents/skills/` im Projekt |
| In allen Projekten | `~/.agents/skills/` in Ihrem Home-Ordner |

So fügen Sie zum Beispiel `{{first}}` zu einem Projekt hinzu:

```sh
mkdir -p /path/to/your-project/.agents/skills
cp -R {{first}} /path/to/your-project/.agents/skills/
```

**Hinweise**

- Kopieren Sie den Ordner vollständig mit seinem gesamten Inhalt. Mit nur einzelnen Dateien funktioniert der Skill nicht richtig.
- Wenn bereits ein Ordner mit demselben Namen existiert, prüfen Sie seinen Inhalt, bevor Sie ihn überschreiben.

## 3. Ausprobieren

Öffnen Sie nach der Einrichtung eine neue Unterhaltung und rufen Sie einen Skill auf.

| Werkzeug | Aufruf |
| --- | --- |
| ChatGPT | über `@` auswählen |
| Codex | über `$` oder `/skills` auswählen |

Beginnen Sie am besten mit einer Anfrage, die keine Dateien verändert:

> Ich plane einen Bericht auf Deutsch. Worauf sollte ich achten? Bitte ändere keine Dateien.

## Dateien prüfen (optional)

Wenn Sie prüfen möchten, ob die heruntergeladenen Dateien unbeschädigt sind, verwenden Sie [SHA256SUMS.txt]({{sums}}).

Legen Sie SHA256SUMS.txt in denselben Ordner wie die heruntergeladenen ZIP-Dateien und führen Sie im Terminal den folgenden Befehl aus. Wenn `shasum` nicht verfügbar ist, vergleichen Sie die SHA-256-Werte zum Beispiel mit `Get-FileHash` in Windows PowerShell.

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

Wenn in den Zeilen Ihrer heruntergeladenen Dateien `OK` steht, ist alles in Ordnung.

---

Andere Werkzeuge: [Claude]({{page_claude}}) · [Gemini]({{page_gemini}})

Oberflächen und Verfügbarkeit können sich ändern. Aktuelle Informationen finden Sie in den offiziellen Anleitungen der jeweiligen Dienste (Stand dieser Seite: 14. Oktober 2026).
