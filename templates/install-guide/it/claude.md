Ecco i passaggi per usare {{brand}} con Claude Code e la chat di Claude.

> **Informazioni sulla v{{version}}**
> Questa versione serve a provare l’installazione nel tuo ambiente. Il funzionamento nei singoli strumenti non è ancora stato verificato a sufficienza, quindi alcuni passaggi potrebbero non funzionare come previsto.

## 1. Scegli il metodo di installazione

| Dove vuoi usarlo | Metodo consigliato |
| --- | --- |
{{#if marketplace}}
| Claude Code | [A. Installare da GitHub](#a) (aggiornamenti semplici) |
{{/if}}
| Claude Code (se preferisci installarlo da uno ZIP) | [{{L_zip}}. Installare da uno ZIP](#{{l_zip}}) |
| Chat di Claude (claude.ai e app) | [{{L_chat}}. Caricare le skill](#{{l_chat}}) |

Claude Code e la chat di Claude si installano in modo diverso.

{{#if marketplace}}
## A. Claude Code: installare da GitHub

1. In un terminale, registra la fonte di distribuzione di KUMIHAN.

   ```sh
   claude plugin marketplace add "https://github.com/landco-llc/kumihan.git#main"
   ```

2. In una conversazione di Claude Code, digita quanto segue:

   ```text
   /plugin install {{plugin}}@kumihan-marketplace
   ```

3. Controlla le informazioni, scegli l’ambito (solo per te, solo per questo progetto e così via) e installa.

Dopo l’installazione potrai usare i seguenti comandi.

{{claude_commands}}

{{/if}}
## {{L_zip}}. Claude Code: installare da uno ZIP

1. Scarica lo [ZIP del plugin per Claude Code]({{plugin_url}}).
{{#if plugin_folder}}
2. Estraendo lo ZIP si ottiene la cartella `{{plugin_folder}}`.
{{else}}
2. Crea una cartella `{{plugin}}` vuota ed estrai lo ZIP al suo interno.
{{/if}}
3. Avvia Claude Code indicando quella cartella.

   ```sh
   claude --plugin-dir "/absolute/path/{{plugin_dir}}"
   ```

**Attenzione**

- Usa il contenuto della cartella così com’è. Non eliminare file e non aggiungerne altri.
- Con questo metodo non ci sono aggiornamenti automatici. Quando esce una nuova versione, sostituiscila con il nuovo ZIP.

## {{L_chat}}. Chat di Claude: caricare le skill

Questo metodo vale per claude.ai e per le app di Claude.

1. Scarica gli ZIP delle skill che vuoi usare.
{{skills_list_indented}}
2. In Claude, apri **Customize → Skills** e scegli **Upload a skill** dal pulsante di aggiunta.
3. Carica gli ZIP uno alla volta e attiva ciascuna skill.

**Attenzione**

- Lo ZIP del plugin per Claude Code non funziona qui. Usa gli ZIP delle skill.
- Carica gli ZIP senza cambiarne il nome.
- Per usare le skill, l’esecuzione del codice deve essere attivata nelle impostazioni. Per i dettagli, consulta la [guida ufficiale di Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude).
- Con gli account di un’organizzazione, la funzione potrebbe non essere disponibile in base alle impostazioni dell’amministratore.
- Le skill caricate non si aggiornano automaticamente. Quando esce una nuova versione, caricale di nuovo.

## 2. Prova

Per iniziare, ti consigliamo una richiesta che non modifichi alcun file.

> Sto preparando una pagina web in italiano. A quali aspetti devo fare attenzione? Non modificare nessun file.

## Verifica dei file (facoltativa)

Se vuoi controllare che i file scaricati non siano danneggiati, usa [SHA256SUMS.txt]({{sums}}).

Metti SHA256SUMS.txt nella stessa cartella dei file ZIP scaricati ed esegui il seguente comando in un terminale. Se `shasum` non è disponibile, confronta lo SHA-256 con uno strumento equivalente, come `Get-FileHash` di Windows PowerShell.

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

Se nelle righe dei file scaricati compare `OK`, è tutto a posto.

---

Altri strumenti: [ChatGPT / Codex]({{page_chatgpt}}) · [Gemini]({{page_gemini}})

Le schermate e le condizioni del servizio possono cambiare. Per le informazioni più aggiornate consulta le indicazioni ufficiali di ciascun servizio (ultima verifica di questa pagina: 14 ottobre 2026).
