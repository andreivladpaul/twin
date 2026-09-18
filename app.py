import asyncio
import os
import threading
import time

import streamlit as st
from dotenv import load_dotenv

# --- Config -----------------------------------------------------------------

MAX_TURNS_PER_SESSION = 20   # messaggi per sessione prima dello stop
MAX_CHARS = 1000             # lunghezza massima di un messaggio
MIN_SECONDS_BETWEEN = 2      # anti-spam fra due invii

# --- Secrets ----------------------------------------------------------------

# IMPORTANTE: questo blocco deve stare PRIMA di importare agent.py.
# agent.py fa os.environ["OPENAI_API_KEY"] al momento dell'import:
# se la chiave non c'e' ancora, solleva KeyError e l'app muore
# prima di poter mostrare qualsiasi messaggio d'errore leggibile.
#
# Nota: la chiave si chiama OPENAI_API_KEY ma punta a OpenRouter
# (vedi base_url in agent.py). Il nome e' fuorviante, il valore no.
load_dotenv(override=True)

try:
    for _key in ("OPENAI_API_KEY", "OPENROUTER_MODEL"):
        if _key in st.secrets and not os.getenv(_key):
            os.environ[_key] = str(st.secrets[_key])
except Exception:
    # Nessun secrets.toml: normale in locale, dove basta il .env.
    pass

# --- UI ---------------------------------------------------------------------

st.set_page_config(page_title="Digital Twin", page_icon="💬")
st.title("Digital Twin")
st.caption("Talk to my AI twin")

if not os.getenv("OPENAI_API_KEY"):
    st.error(
        "Manca OPENAI_API_KEY (la chiave OpenRouter). In locale mettila nel "
        "file .env, su Streamlit Cloud in Settings → Secrets."
    )
    st.stop()


@st.cache_resource(show_spinner="Carico il twin…")
def load_twin():
    # Import qui dentro: context.py legge linkedin.pdf e summary.txt
    # all'import, quindi lo facciamo una volta sola per processo
    # e dopo aver verificato che la chiave ci sia.
    from agents import Runner
    from agent import digital_twin

    # Un solo event loop, vivo per tutta la vita del processo, su un
    # thread dedicato.
    #
    # PERCHE: agent.py crea un client AsyncOpenAI una volta sola, e quel
    # client si lega al primo event loop che lo usa. Runner.run_sync
    # invece apre un loop NUOVO a ogni chiamata: dal secondo messaggio
    # in poi il client si ritrova su un loop diverso dal proprio e
    # solleva "is bound to a different event loop".
    #
    # run_coroutine_threadsafe e anche l'unico modo sicuro di usare un
    # loop condiviso da piu sessioni Streamlit, che girano su thread
    # diversi.
    loop = asyncio.new_event_loop()
    threading.Thread(
        target=loop.run_forever, daemon=True, name="agent-loop"
    ).start()

    return Runner, digital_twin, loop


try:
    Runner, digital_twin, agent_loop = load_twin()
except Exception as exc:
    st.error(f"Impossibile inizializzare il twin: {exc}")
    st.stop()

# --- Stato ------------------------------------------------------------------

# messages    = cronologia da mostrare a schermo
# agent_input = cronologia nel formato che il Runner si aspetta al turno dopo
if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent_input" not in st.session_state:
    st.session_state.agent_input = []
if "turns" not in st.session_state:
    st.session_state.turns = 0
if "last_sent_at" not in st.session_state:
    st.session_state.last_sent_at = 0.0

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Input ------------------------------------------------------------------

limit_reached = st.session_state.turns >= MAX_TURNS_PER_SESSION

if limit_reached:
    st.info(
        f"Limite di {MAX_TURNS_PER_SESSION} messaggi raggiunto per questa "
        "sessione. Ricarica la pagina per ricominciare."
    )

prompt = st.chat_input(
    "Scrivi un messaggio…",
    max_chars=MAX_CHARS,
    disabled=limit_reached,
)

if prompt:
    now = time.monotonic()
    if now - st.session_state.last_sent_at < MIN_SECONDS_BETWEEN:
        st.warning("Un attimo prima del messaggio successivo.")
        st.stop()
    st.session_state.last_sent_at = now

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Sto pensando…"):
            try:
                # Passiamo tutta la cronologia: nella versione Gradio il
                # parametro history veniva ricevuto e mai usato, quindi il
                # twin ripartiva da zero a ogni messaggio.
                future = asyncio.run_coroutine_threadsafe(
                    Runner.run(
                        digital_twin,
                        st.session_state.agent_input
                        + [{"role": "user", "content": prompt}],
                    ),
                    agent_loop,
                )
                # Il timeout evita che una chiamata appesa blocchi la
                # sessione per sempre.
                result = future.result(timeout=120)
            except Exception as exc:
                # Il turno fallito non entra nella cronologia dell'agente,
                # cosi' il messaggio successivo riparte da uno stato valido.
                st.error(f"Errore nel generare la risposta: {exc}")
            else:
                st.markdown(result.final_output)
                st.session_state.agent_input = result.to_input_list()
                st.session_state.messages.append(
                    {"role": "assistant", "content": result.final_output}
                )
                st.session_state.turns += 1
