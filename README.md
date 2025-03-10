# Herald: A Natural Language Annotated Lean 4 Dataset

## Introduction

We release our annotated dataset from Mathlib 4 and our latest translator model for autoformalization.

## Dataset Downloads

| Dataset | Download |
| --- | --- |
| Herald Statements: | [HuggingFace](https://huggingface.co/datasets/FrenzyMath/Herald_statements) |
| Herald Proofs | [HuggingFace](https://huggingface.co/datasets/FrenzyMath/Herald_proofs) |

## Model

| Model | Download |
| --- | --- |
| Herald Translator | [HuggingFace](https://huggingface.co/FrenzyMath/HeraldTranslator) |

## Evaluation Results

|   | miniF2F-test | miniF2F-valid | extract-theorems | college-math-CoT |
| --- | --- | --- | --- | --- |
| TheoremLlama | 50.1% | 55.6% | 4.0% | 3.0% |
| InternLM2-Math-Plus-7B | 73.0% | 80.1% | 7.5% | 6.5% |
| Herald | 96.7% | 96.3% | 23.5% | 16.0% |

You can find our own test sets in `./data` directory

## Quick Start

### Requirements

1. Our code is tested on `vllm >= 0.6.6`
2. To run the inference, you will need a `leantest` environment with `repl` included for Lean compiler check. Our code is tested on `v4.11.0` You can obtain our version [here](https://github.com/frenzymath/lean_test_v4110).

### Simple Inference

1. You can configure your preferred models and settings for back-translation and NLI-check in `config.py`. Our test environment use InternLM2-Math-Plus 7B for back-translation and Deepseek V2.5 for NLI-check.

2. Then use the script to run the model.

    ```bash
    # Translate and verify translated statements
    python -m run_translate_verify example/test.json example/test_result.json
    # Do back-translation and NLI-check
    python -m run_backtrans_nli example/test_result.json
    ```

### Experiment on Dataset
Finish configurations in `config.py` and run script `bash run_pipeline.sh <data.json>`. You can also place your own dataset under `./data`. Check results in `./data/results`.