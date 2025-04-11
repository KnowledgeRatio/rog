# Rog Research: Content Verification Tool

A tool that uses a research preview of rog (based on Phi-4) combined with llm-axe to verify content authenticity with internet access.

## Overview

Rog Research is a content verification tool designed to help identify disinformation and verify the authenticity of content. It combines the power of local LLM (Large Language Model) inference through Ollama with internet access capabilities via llm-axe.

The project features:

- A command-line interface for content verification
- A web-based interface for easy interaction
- Internet-connected LLM responses for evidence-based verification
- Customizable prompts and verification criteria

## Requirements

- Python 3.x
- Ollama installed and configured
- llm-axe Python package
- Flask (for the web interface)
- Node.js (for JavaScript helpers)

## Setup

### 1. Install Ollama

If you haven't already, [install Ollama](https://ollama.ai/download) for your platform.

### 2. Build the rog-research Model

The project uses a customized Ollama model based on Phi-4. Build it using:

```bash
node build-model.js
```

Or manually:

```bash
ollama create rog-research -f Modelfile
```

### 3. Install Python Dependencies

```bash
pip install llm-axe flask
```

### 4. Install Node.js Dependencies

```bash
npm install
```

## Usage

### Command Line Interface

Run the Python script to use the command-line interface:

```bash
python rog_online.py
```

This will start an interactive session where you can input content to verify.

### Web Interface

For a more user-friendly experience, use the Flask web application:

```bash
python web_interface.py
```

Then open your browser and navigate to:
http://127.0.0.1:5000/ or http://localhost:5000/

## How It Works

### The Rog Model

The rog-research model is built on Phi-4 with specific tuning to identify disinformation. Its system prompt directs it to:

- Evaluate content sources and authors for credibility
- Analyze language patterns that may indicate disinformation
- Verify claims against reliable evidence
- Examine contextual presentation of information
- Identify potential bias or one-sided perspectives
- Provide evidence-based assessments with citations

### Internet Integration

The llm-axe tool connects the Ollama model to the internet, allowing it to:

1. Search for relevant information online
2. Compare content against current knowledge
3. Find supporting or contradicting evidence
4. Retrieve up-to-date information to verify claims

## Project Structure

```
├── Modelfile             # Definition file for the rog-research Ollama model
├── build-model.js        # Script to build the custom Ollama model
├── ollama-test.js        # Basic test script for Ollama API
├── package.json          # Node.js project configuration
├── rog_online.py         # Command-line interface for content verification
├── web_interface.py      # Flask web application for the web interface
└── templates/            # Web interface HTML templates
    └── index.html        # Main web interface page
```

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to improve the tool.

## License

[MIT License](LICENSE)

## Acknowledgements

- This project uses [Ollama](https://ollama.ai/) for local LLM inference
- Internet connectivity is provided by [llm-axe](https://github.com/langchain-ai/llm-axe)
- The base model is [Phi-4](https://www.microsoft.com/en-us/research/blog/phi-4-advancing-reasoning-with-next-generation-language-models/) from Microsoft