# AI Debugger - aidbg

`A minimal, event-driven, multi-language AI debugging engine for modern developers.`

![PyPI](https://img.shields.io/pypi/v/aidbg)
![Python](https://img.shields.io/pypi/pyversions/aidbg)
![License](https://img.shields.io/pypi/l/aidbg)
![CI](https://github.com/KNIHAL/aidbg/actions/workflows/ci.yml/badge.svg)

**aidbg** is a local-first, CLI-based AI debugging tool that works across multiple programming languages.

It wraps program execution, detects runtime failures, collects minimal diagnostic context, and returns a structured debugging explanation using an LLM — without running background processes or monitoring your system.

aidbg activates only when your program crashes, analyzes the error, prints a concise fix, and exits immediately.

---

## 🌍 Supported Languages

* Python (.py)
* JavaScript (Node.js) (.js)
* Go (.go)
* Java (.java)

Each language is handled through a lightweight adapter architecture.

---

## ✨ Why aidbg?

Modern developers often copy-paste errors into AI tools to debug problems.

aidbg removes that friction.

**Instead of:**

```bash
python app.py
# copy error
# open browser
# paste into AI
```

**You do:**

```bash
aidbg run app.py
```

Or:

```bash
aidbg run app.js
aidbg run main.go
aidbg run Test.java
```

**And get:**

* Root Cause
* Fix
* Short Explanation

All inside your terminal.

---

## 🔍 Key Features

* CLI-based execution wrapper
* Event-driven (no background daemon)
* Zero idle CPU usage
* Multi-language adapter architecture
* Minimal context collection
* Token-controlled LLM responses
* Guardrails against unsafe or hacky fixes
* Multi-provider support:

  * Groq
  * OpenAI
  * Ollama (local)
* Global and project-level configuration
* Fully open-source core

---

## 🧠 How It Works

Execution Flow:

```
aidbg run file.ext
  → detect language adapter
  → execute runtime (python/node/go/java)
  → detect crash (non-zero exit)
  → extract failure location
  → collect minimal context
  → send structured prompt to LLM
  → print debugging result
  → exit
```

**aidbg never:**

* Runs continuously
* Monitors your system
* Sends your full repository
* Collects environment variables
* Reads .env files
* Uploads datasets

---

## 📦 Installation

Basic installation:

```bash
pip install aidbg
```

With provider extras:

```bash
pip install aidbg[groq]
pip install aidbg[openai]
pip install aidbg[ollama]
```

---

## ⚙️ Configuration

Initialize configuration:

```bash
aidbg init
```

Project-specific config:

```bash
aidbg init --local
```

Config priority:

1. Project config (.aidbg/config.json)
2. Global config (~/.aidbg/config.json)

---

## 🛠 Usage

```bash
aidbg run app.py
aidbg run app.js
aidbg run main.go
aidbg run Test.java
```

Example output:

```
Root Cause:
Division by zero.

Fix:
Validate the divisor before performing the division.

Explanation:
The program does not check for zero before division.
```

---

## 🔐 Runtime Requirements

Depending on language used:

* Python 3.9+
* Node.js (for .js files)
* Go (for .go files)
* Java JDK (for .java files)

---

## 🔐 Privacy Model

Collected:

* Relevant traceback or runtime error
* Failing file + line number
* Code snippet around failure
* Shallow project structure (depth ≤ 2)
* Runtime version and OS
* Lightweight dependency info

Never collected:

* Full repository
* Secrets
* Environment variables
* Binary files
* Historical logs

---

## 🧩 Project Structure

```
aidbg/
│
├─ cli.py                # CLI entrypoint
├─ runner.py             # Runtime execution per language
├─ trigger.py            # Crash detection + LLM orchestration
├─ init.py               # Interactive configuration
├─ config.py             # Config resolution logic
├─ prompt.py             # Prompt construction
│
├─ languages/            # Language adapters
│   ├─ base.py
│   ├─ python.py
│   ├─ javascript.py
│   ├─ go.py
│   ├─ java.py
│   └─ resolver.py
│
├─ context/              # Context extraction modules
│   ├─ collector.py
│   ├─ project_tree.py
│   ├─ environment.py
│   └─ dependencies.py
│
├─ logic/
│   ├─ complexity.py
│   └─ token_budget.py
│
├─ llm/
│   ├─ base.py
│   ├─ groq.py
│   ├─ openai.py
│   └─ ollama.py
│
└─ tests/
```

---

## 🧪 Testing

```bash
pytest
```

---

## 📈 Roadmap

v0.2

* Multi-language support
* Adapter-based architecture

v0.3 (Planned)

* Interactive terminal mode
* Improved error classification

v1.0 (Future)

* Custom lightweight debugging model
* Optional hosted API
* Core CLI remains open-source

---

## 📄 License

MIT License.

The open-source CLI tool is released under MIT.
Future hosted APIs or proprietary debugging models may be released under separate commercial terms.

---

## 🤝 Contributing

Pull requests welcome.
Keep contributions minimal, testable, and consistent with the local-first philosophy.
