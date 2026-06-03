# Risk-Aware-Semantic-Grounding

This repository contains the experimental code and data used in our paper on risk-aware semantic grounding for smart-home task planning.

## Scope

- Build and run planning baselines.
- Generate and evaluate query-decision datasets.
- Compare model behavior under risk-aware constraints.

## Repository Layout

- `models/` - baseline and planner model implementations.
- `dataset/` - smart-home map, ground-truth datasets, and result files.
- `results/` - exported experiment outputs.
- `generate_dataset.py` - dataset construction script.
- `planners_runner.py`, `planner_risk_aware_runner.py` - main scripts for running planner experiments.
- `risk_assessment_agent.py`, `decision_layer.py` - neccessary tools for proposel model -  Risk aware-Planner.
- `analysis dataset.ipynb`, `smart_home_design.ipynb` - analysis and design notebooks.

## Quick Start

1. Create and activate a Python environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run experiments:

```bash
python planners_runner.py
python planner_risk_aware_runner.py

```

4. (Optional) Regenerate dataset:

```bash
python generate_dataset.py
```

## Notes

- This codebase is research-oriented and intended for reproducible experiments.
- File names in `dataset/` and `results/` correspond to the variants reported in the paper.