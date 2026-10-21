Ecco i passaggi per usare {{brand}} con Gemini CLI e l’app Gemini.

> **Informazioni sulla v{{version}}**
> Questa versione serve a provare l’installazione nel tuo ambiente. Il funzionamento nei singoli strumenti non è ancora stato verificato a sufficienza, quindi alcuni passaggi potrebbero non funzionare come previsto.

## 1. Scegli il metodo di installazione

| Dove vuoi usarlo | Metodo consigliato |
| --- | --- |
| Gemini CLI (tutte e quattro insieme) | [A. Installare come estensione](#a) |
| Gemini CLI (solo quelle che ti servono) | [B. Scegliere e installare le skill](#b) |
| App Gemini (web, Mac, smartphone) | [C. Caricare le skill](#c) |

## A. Gemini CLI: installare come estensione

Con questo metodo installi tutte e quattro le skill in una volta.

1. Scarica lo [ZIP dell’estensione]({{plugin_url}}).
{{#if plugin_folder}}
2. Estraendo lo ZIP si ottiene la cartella `{{plugin_folder}}`.
{{else}}
2. Crea una cartella `{{plugin}}` vuota ed estrai lo ZIP al suo interno.
{{/if}}
3. Installa indicando quella cartella.

   ```sh
   gemini extensions install "/absolute/path/{{plugin_dir}}"
   ```

Se compare una schermata di conferma, controllane il contenuto prima di procedere. Una volta installata, l’estensione è attiva in tutti i progetti.

Se l’hai installata da uno ZIP, non si aggiorna automaticamente. Quando esce una nuova versione, sostituiscila con il nuovo ZIP.

## B. Gemini CLI: scegliere e installare le skill

Con questo metodo installi solo le skill che ti servono, progetto per progetto. Se hai usato il metodo A, questo passaggio non è necessario.

Per esempio, per installare `{{first}}`, esegui quanto segue nel progetto interessato:

```sh
gemini skills install https://github.com/landco-llc/kumihan --path {{skills_path}}/{{first}} --scope workspace
```

Per installare altre skill, modifica `--path` in questo modo:

{{gemini_paths}}

`--scope workspace` limita l’uso a «solo questo progetto». Se lo ometti, la skill sarà disponibile in tutti i tuoi progetti.

**Per aggiornare**

Esegui di nuovo lo stesso comando. La skill installata viene sostituita, quindi, se l’hai modificata, salva prima le tue modifiche.

## C. App Gemini: caricare le skill

1. Scarica gli ZIP delle skill che vuoi usare.
{{skills_list_indented}}
2. In Gemini, apri **Customize** (o **More** se non lo trovi) → **Skills** → **Upload**.
3. Scegli gli ZIP uno alla volta, controlla le informazioni e premi **Create**.

**Attenzione**

- Possono usarla solo gli account Google personali di utenti maggiorenni (18 anni o più). Al momento non funziona con gli account di lavoro o della scuola.
- L’opzione «Keep Activity» (salvataggio dell’attività) deve essere attiva.
- La funzione viene resa disponibile in modo graduale, quindi potrebbe non comparire ancora. Per i dettagli, consulta la [guida ufficiale di Gemini](https://support.google.com/gemini/answer/17094296?hl=it).
- Lo ZIP dell’estensione (per Gemini CLI) non funziona qui.
- Le skill caricate non si aggiornano automaticamente. Quando esce una nuova versione, caricale di nuovo.

## 2. Prova

Per iniziare, ti consigliamo una richiesta che non modifichi alcun file.

> Sto preparando una presentazione in italiano. A quali aspetti devo fare attenzione? Non modificare nessun file.

## Verifica dei file (facoltativa)

Se vuoi controllare che i file scaricati non siano danneggiati, usa [SHA256SUMS.txt]({{sums}}).

Metti SHA256SUMS.txt nella stessa cartella dei file ZIP scaricati ed esegui il seguente comando in un terminale. Se `shasum` non è disponibile, confronta lo SHA-256 con uno strumento equivalente, come `Get-FileHash` di Windows PowerShell.

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

Se nelle righe dei file scaricati compare `OK`, è tutto a posto.

---

Altri strumenti: [ChatGPT / Codex]({{page_chatgpt}}) · [Claude]({{page_claude}})

Le schermate e le condizioni del servizio possono cambiare. Per le informazioni più aggiornate consulta le indicazioni ufficiali di ciascun servizio (ultima verifica di questa pagina: 14 ottobre 2026).
