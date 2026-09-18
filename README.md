# Digital Twin

Un assistente conversazionale basato sull'intelligenza artificiale che rappresenta il profilo professionale di Andrei Vlad Paul. Il progetto permette a visitatori, recruiter e potenziali collaboratori di fare domande su esperienza, competenze, progetti e percorso professionale attraverso un'interfaccia web semplice e accessibile.

Il Digital Twin non si presenta come la persona reale: dichiara di essere un sistema AI e risponde utilizzando esclusivamente le informazioni professionali fornite come contesto.

## Funzionalita

- Chat conversazionale con cronologia della sessione.
- Risposte basate su curriculum, profilo LinkedIn e sintesi del percorso professionale.
- Gestione delle domande fuori contesto e delle informazioni non disponibili.
- Registrazione delle richieste di contatto tramite email e note.
- Limite di 20 messaggi per sessione e controllo anti-spam.
- Comunicazione con un modello OpenRouter tramite endpoint compatibile con OpenAI.
- Interfaccia web pronta per il deploy su Streamlit Cloud.

## Stack tecnologico

- **Python**: linguaggio principale.
- **Streamlit**: interfaccia web e gestione della sessione utente.
- **OpenAI Agents SDK**: definizione dell'agente, esecuzione dei turni e function tool.
- **OpenRouter**: accesso al modello linguistico tramite API compatibile con OpenAI.
- **python-dotenv**: caricamento delle variabili d'ambiente in locale.
- **pypdf**: estrazione del testo dal PDF del profilo LinkedIn.
- **AsyncOpenAI**: client asincrono configurato con l'endpoint OpenRouter.

## Architettura

```text
Visitatore
	 |
	 v
Streamlit (app.py)
	 |
	 v
Agent SDK (agent.py)
	 | \
	 |  +--> Function tool: record_user_details()
	 |
	 +----> OpenRouter API

Contesto dell'agente:
	 - summary.txt
	 - linkedin.pdf
```

I file `summary.txt` e `linkedin.pdf` vengono letti da `context.py` e trasformati nelle istruzioni dell'agente. Quando un utente lascia i propri dati per essere ricontattato, `tools.py` aggiunge le informazioni a `user_details.txt`.

## Struttura del progetto

| File | Responsabilita |
| --- | --- |
| `app.py` | Avvia l'interfaccia Streamlit, carica i secret e gestisce la chat. |
| `agent.py` | Configura il Digital Twin e il client OpenRouter. |
| `context.py` | Costruisce il prompt usando il PDF e la sintesi professionale. |
| `tools.py` | Contiene il tool per registrare richieste di contatto. |
| `summary.txt` | Sintesi del percorso professionale e delle competenze. |
| `linkedin.pdf` | Fonte aggiuntiva di informazioni professionali. |
| `requirements.txt` | Dipendenze Python del progetto. |
| `app_gradio_backup.py` | Versione precedente dell'interfaccia, conservata come backup. |


## Avvio locale

1. Clona la repository e spostati nella directory del progetto:

	```bash
	git clone https://github.com/andreivladpaul/twin.git
	cd twin
	```

2. Crea e attiva un ambiente virtuale:

	```bash
	python -m venv .venv
	source .venv/bin/activate
	```

	Su Windows, attiva l'ambiente con `.venv\\Scripts\\activate`.

3. Installa le dipendenze:

	```bash
	pip install -r requirements.txt
	```

4. Crea un file `.env` nella root del progetto:

	```env
	OPENROUTER_API_KEY=la_tua_chiave_openrouter
	OPENROUTER_MODEL=openai/gpt-4o-mini
	```

	`OPENROUTER_API_KEY` e il nome della variabile richiesto dall'applicazione. Il valore deve essere una chiave OpenRouter, non una chiave OpenAI. `OPENROUTER_MODEL` e opzionale.

5. Avvia l'applicazione:

	```bash
	streamlit run app.py
	```

## Licenza

Il progetto e destinato a uso personale e dimostrativo. Per informazioni su riutilizzo, distribuzione o collaborazione, contatta l'autore della repository.
