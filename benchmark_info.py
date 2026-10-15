"""Reference descriptions for the five benchmark families in the project report."""

BENCHMARKS = {
    "MMLU": {
        "measures": "Broad multitask knowledge across academic subjects.",
        "typical_metric": "Multiple-choice accuracy",
        "project_status": "Conceptual mapping only; official dataset not bundled.",
    },
    "GPQA": {
        "measures": "Difficult graduate-level questions in biology, physics, and chemistry.",
        "typical_metric": "Accuracy",
        "project_status": "Conceptual mapping only; official dataset not bundled.",
    },
    "HumanEval": {
        "measures": "Functional correctness of generated code on unit tests.",
        "typical_metric": "pass@1 / pass@k",
        "project_status": "No official HumanEval harness is run by this starter project.",
    },
    "SWE-bench Verified": {
        "measures": "Resolution of real GitHub issues in software repositories.",
        "typical_metric": "Percentage of issues resolved under a documented scaffold",
        "project_status": "No repository-patching harness is included.",
    },
    "TruthfulQA": {
        "measures": "Resistance to common misconceptions and popular false beliefs.",
        "typical_metric": "Truthfulness/informativeness metrics depend on evaluation setup",
        "project_status": "Verification-node demonstration only; not an official evaluation.",
    },
}
