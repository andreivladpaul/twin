# Digital Twin

An AI-powered conversational assistant that represents the professional profile of Andrei Vlad Paul. The project lets visitors, recruiters, and potential collaborators ask questions about his experience, skills, projects, and career path through a simple, accessible web interface.

The Digital Twin does not pose as the real person: it states that it is an AI system and answers exclusively on the basis of the professional information provided as context.

## Features

- Conversational chat with session history.
- Answers grounded in the CV, LinkedIn profile, and a career summary.
- Handling of off-topic questions and unavailable information.
- Logging of contact requests via email and notes.
- 20-message limit per session and anti-spam control.
- Communication with an OpenRouter model through an OpenAI-compatible endpoint.
- Web interface ready to deploy on Streamlit Cloud.

## Tech stack

- **Python**: main language.
- **Streamlit**: web interface and user session management.
- **OpenAI Agents SDK**: agent definition, turn execution, and function tools.
- **OpenRouter**: access to the language model through an OpenAI-compatible API.
- **python-dotenv**: loading of environment variables in local development.
- **pypdf**: text extraction from the LinkedIn profile PDF.
- **AsyncOpenAI**: asynchronous client configured with the OpenRouter endpoint.

## Architecture

```text
Visitor
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

Agent context:
	 - summary.txt
	 - linkedin.pdf
```

The files `summary.txt` and `linkedin.pdf` are read by `context.py` and turned into the agent's instructions. When a user leaves their details to be contacted, `tools.py` appends the information to `user_details.txt`.

## Project structure

| File | Responsibility |
| --- | --- |
| `app.py` | Launches the Streamlit interface, loads the secrets, and manages the chat. |
| `agent.py` | Configures the Digital Twin and the OpenRouter client. |
| `context.py` | Builds the prompt from the PDF and the professional summary. |
| `tools.py` | Contains the tool for logging contact requests. |
| `summary.txt` | Summary of the career path and skills. |
| `linkedin.pdf` | Additional source of professional information. |
| `requirements.txt` | Python dependencies of the project. |
| `app_gradio_backup.py` | Previous version of the interface, kept as a backup. |

## Running locally

1. Clone the repository and move into the project directory:

```bash
	git clone https://github.com/andreivladpaul/twin.git
	cd twin
```

2. Create and activate a virtual environment:

```bash
	python -m venv .venv
	source .venv/bin/activate
```

	On Windows, activate the environment with `.venv\\Scripts\\activate`.

3. Install the dependencies:

```bash
	pip install -r requirements.txt
```

4. Create a `.env` file in the project root:

```env
	OPENROUTER_API_KEY=your_openrouter_key
	OPENROUTER_MODEL=openai/gpt-4o-mini
```

	`OPENROUTER_API_KEY` is the variable name required by the application. The value must be an OpenRouter key, not an OpenAI key. `OPENROUTER_MODEL` is optional.

5. Start the application:

```bash
	streamlit run app.py
```

## License

The project is intended for personal and demonstration use. For information on reuse, distribution, or collaboration, contact the repository author.
