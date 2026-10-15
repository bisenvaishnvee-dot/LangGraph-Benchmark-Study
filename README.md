# LangGraph: A Benchmark-Based Study of a Graph-Based Agent Orchestration Framework

**TA-2 project starter implementation**  
Student: Vaishnavee Bisen | Roll No.: 19 | Section: B | Semester: VII  
Subject: Large Language Model (UNAIL411)  
Institution: G H Raisoni College of Engineering

## 1. Project overview

This project demonstrates how a graph-based agent workflow can route a question, generate a draft, verify it, and return a final answer. It is inspired by the accompanying TAE-I report, which discusses five benchmark families: MMLU, GPQA, HumanEval, SWE-bench Verified, and TruthfulQA.

**Important scope note:** LangGraph is an orchestration framework, not a foundation model. This repository does not claim to reproduce official benchmark scores. The included questions are small illustrative examples for checking that the application runs. Official benchmark evaluation requires the relevant datasets, evaluation harnesses, model access, and a controlled experimental setup.

## 2. Architecture

```text
User question
    |
    v
Router node
    |
    +---- coding question ------> Coding node ----+
    |                                             |
    +---- science/general ------> Answer node ----+--> Verification node
                                                  |          |
                                                  +----------+
                                                             v
                                                        Final answer
```

LangGraph concepts demonstrated:
- **Nodes:** routing, answering/coding, verification, and final response.
- **Edges:** explicit control flow between steps.
- **State:** typed shared data passed between nodes.
- **Conditional routing:** sends coding questions to the coding path.
- **Verification:** a simple application-level review step.

## 3. Features

- Runs in **demo mode** without an API key.
- Optionally uses an OpenAI-compatible chat model through `langchain-openai`.
- Includes a small local evaluation runner that reports exact-match accuracy where applicable, pass rate, latency, and token usage when available.
- Keeps benchmark descriptions separate from official benchmark results.
- Includes basic tests for graph execution.

## 4. Requirements

- Python 3.10 or newer (Python 3.11 recommended)
- Internet connection only if installing packages or calling a hosted model

## 5. Setup

### Windows (PowerShell)

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If PowerShell blocks activation, use Command Prompt:

```bat
.venv\Scripts\activate.bat
pip install -r requirements.txt
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 6. Run in demo mode

No API key is required for demo mode:

```bash
python app.py
```

Type a question, for example:
- `Write a Python function to add two numbers`
- `What is photosynthesis?`
- `What is MMLU?`

Type `exit` to quit. Demo responses are illustrative and are not model-generated answers.

## 7. Optional: use a hosted LLM

Set your API key in the environment; never commit it to GitHub.

**Windows PowerShell**
```powershell
$env:OPENAI_API_KEY="your-key-here"
$env:LLM_MODEL="gpt-4o-mini"
python app.py
```

**macOS / Linux**
```bash
export OPENAI_API_KEY="your-key-here"
export LLM_MODEL="gpt-4o-mini"
python app.py
```

The application uses a hosted model only when `OPENAI_API_KEY` is set. Model availability and pricing depend on your provider/account.

## 8. Run the local illustrative evaluation

```bash
python -m benchmarks.run_evaluation
```

This uses `data/sample_questions.json`, a tiny demonstration dataset. It is **not** MMLU, GPQA, HumanEval, SWE-bench Verified, or TruthfulQA, and its output must not be reported as an official benchmark score. Results are saved to `results/benchmark_results.csv`.

## 9. Benchmark mapping

| Benchmark | Capability discussed in the report | What this starter project provides |
|---|---|---|
| MMLU | Broad knowledge across subjects | Conceptual mapping only; no official MMLU dataset included |
| GPQA | Graduate-level science reasoning | Conceptual mapping only; no official GPQA dataset included |
| HumanEval | Functional correctness of generated code | Small illustrative code-task metadata; no official HumanEval run |
| SWE-bench Verified | Real GitHub issue resolution | Conceptual mapping only; no repository issue-resolution harness |
| TruthfulQA | Truthfulness and misconceptions | A verification-node demonstration; not an official TruthfulQA evaluation |

## 10. Repository structure

```text
LangGraph-Benchmark-Study/
├── app.py
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── graph.py
│   ├── nodes.py
│   └── state.py
├── benchmarks/
│   ├── __init__.py
│   ├── benchmark_info.py
│   └── run_evaluation.py
├── data/
│   └── sample_questions.json
├── tests/
│   └── test_graph.py
└── results/
    └── .gitkeep
```

## 11. Limitations and future work

- The demo path uses fixed illustrative responses and is not a real LLM.
- The verification node is a lightweight review, not a guarantee of truth.
- Official benchmark datasets and harnesses are not bundled.
- Future work can add retrieval, human approval, persistent checkpoints, model comparisons, and a reproducible evaluation protocol.

## 12. Academic integrity note

Clearly distinguish **implemented features**, **illustrative tests**, and **official benchmark results** in your TA-2 report. Do not claim official scores unless the relevant benchmark was actually run under documented conditions.
