Ecco i passaggi per usare {{brand}} con ChatGPT e Codex.

> **Informazioni sulla v{{version}}**
> Questa versione serve a provare l’installazione nel tuo ambiente. Il funzionamento nei singoli strumenti non è ancora stato verificato a sufficienza, quindi alcuni passaggi potrebbero non funzionare come previsto.

## 1. Scegli il metodo di installazione

| Dove vuoi usarlo | Metodo consigliato |
| --- | --- |
| ChatGPT (se è possibile caricare skill) | [A. Aggiungere le skill una alla volta](#a) |
| ChatGPT (per registrarlo come tuo plugin personale) | [B. Registrare tutto come plugin](#b) |
| Codex (sul tuo computer) | [C. Copiare le cartelle](#c) |

Una **skill** corrisponde a una singola funzione; il **plugin** è un pacchetto che riunisce tutte e quattro le skill.

## 2. Scarica i file

I file si trovano nella [pagina della release]({{release}}). Facendo clic su un link, il file ZIP viene scaricato.

**Plugin (tutte e quattro le skill insieme)**

- {{plugin_link}}

**Skill (una alla volta)**

{{skills_list}}

## A. Aggiungere skill a ChatGPT

Puoi usare questo metodo se nella schermata di ChatGPT compare «Skills» con un’opzione di caricamento.

1. Scegli un file ZIP di una skill e caricalo.
2. Controlla le informazioni visualizzate e aggiungila.
3. Ripeti gli stessi passaggi per ogni skill che ti serve.

**Attenzione**

- Lo ZIP del plugin non funziona con questo metodo. Usa gli ZIP delle skill.
- Allegare un file a una chat non lo aggiunge come skill.
- Se l’opzione non compare, potrebbe non essere ancora disponibile per il tuo piano o la tua app. Consulta la [guida ufficiale di OpenAI](https://learn.chatgpt.com/docs/build-skills).

## B. Registrare un plugin in ChatGPT

Con questo metodo le quattro skill vengono registrate insieme come tuo plugin personale.

1. Apri una nuova chat in ChatGPT e seleziona `@plugin-creator`.
2. Allega il file ZIP del plugin.
3. Fai una richiesta come questa:

   > Registra questo pacchetto come mio plugin privato. Non inviarlo alla directory pubblica.

4. Una volta completata la registrazione, **{{display}}** compare in Plugins, sotto «Personal» o «Created by me».
5. Se necessario, installalo e attivalo in una nuova chat.

**Attenzione**

- Il plugin potrebbe essere registrato nello spazio di lavoro del tuo team. Se vuoi che resti solo tuo, controlla la destinazione prima di registrarlo.
- In base al piano o alle impostazioni dello spazio di lavoro, questa funzione potrebbe non essere disponibile. Per i dettagli, consulta [Build plugins](https://learn.chatgpt.com/docs/build-plugins) e [Plugins](https://learn.chatgpt.com/docs/plugins).
- Un plugin registrato in questo modo è utilizzabile solo dal tuo account. Non viene pubblicato nella directory pubblica.

## C. Copiare le cartelle in Codex

Estraendo lo ZIP di una skill ottieni una cartella come `{{first}}`. Copia questa cartella nella posizione letta da Codex.

| Ambito | Destinazione |
| --- | --- |
| Solo un progetto specifico | `.agents/skills/` all’interno del progetto |
| Tutti i progetti | `~/.agents/skills/` nella tua cartella home |

Per esempio, per aggiungere `{{first}}` a un progetto:

```sh
mkdir -p /path/to/your-project/.agents/skills
cp -R {{first}} /path/to/your-project/.agents/skills/
```

**Attenzione**

- Copia la cartella intera, con tutto il suo contenuto. Con solo una parte dei file la skill non funziona correttamente.
- Se esiste già una cartella con lo stesso nome, controllane il contenuto prima di sovrascriverla.

## 3. Prova

Dopo l’installazione, apri una nuova chat e richiama la skill.

| Strumento | Come richiamarla |
| --- | --- |
| ChatGPT | Selezionala da `@` |
| Codex | Selezionala da `$` o `/skills` |

Per iniziare, ti consigliamo una richiesta che non modifichi alcun file.

> Sto preparando un report in italiano. A quali aspetti devo fare attenzione? Non modificare nessun file.

## Verifica dei file (facoltativa)

Se vuoi controllare che i file scaricati non siano danneggiati, usa [SHA256SUMS.txt]({{sums}}).

Metti SHA256SUMS.txt nella stessa cartella dei file ZIP scaricati ed esegui il seguente comando in un terminale. Se `shasum` non è disponibile, confronta lo SHA-256 con uno strumento equivalente, come `Get-FileHash` di Windows PowerShell.

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

Se nelle righe dei file scaricati compare `OK`, è tutto a posto.

---

Altri strumenti: [Claude]({{page_claude}}) · [Gemini]({{page_gemini}})

Le schermate e le condizioni del servizio possono cambiare. Per le informazioni più aggiornate consulta le indicazioni ufficiali di ciascun servizio (ultima verifica di questa pagina: 14 ottobre 2026).
