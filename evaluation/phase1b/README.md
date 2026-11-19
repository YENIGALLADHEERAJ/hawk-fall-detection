# Phase 1B experiment provenance

All footage is unmodified; source hashes and binary labels remain in
`datasets/holdout.json`. No training or extra model installation occurred.

- `original-results.json` / `original-report.md`: preserved first held-out evaluation.
- `A`: fresh original-algorithm run with diagnostic recording.
- `B`: track retention / capped prediction / conservative reattachment only.
- `C`: final temporal sequence logic with the original tracker.
- `D`: final tracker + temporal logic; selected default.
- `C-initial`, `D-initial`: preserved runs before removing the compact-low branch.
- `E`: exploratory 0.15 detection floor for continuing tracks, with the initial
  temporal logic. Rejected as default after visual inspection of an oversized box.
- `development`: full 25-clip real-inference run of the initial combined logic.
- `development-final-replay.json`: final temporal rule run over that recorded real
  detection/motion evidence. No new detector inference and no FPS claim. Both new
  negative failure clips are additionally tested with full real inference.
- `ablation.json`: measured per-variant and per-clip summaries.
- `source-hashes.json`: hashes of the final source files; archived baseline/initial
  temporal code is in `baseline-source`. Defaults and diagnostic fields evolved;
  each run's JSON records its actual parameter values.

Reproduce current A–D into fresh result folders (the raw run folders are always unique):

```powershell
.\.venv\Scripts\python.exe -m evaluation.run --manifest datasets/holdout.json --variant baseline --output evaluation/repeat/A
.\.venv\Scripts\python.exe -m evaluation.run --manifest datasets/holdout.json --variant tracking --output evaluation/repeat/B
.\.venv\Scripts\python.exe -m evaluation.run --manifest datasets/holdout.json --variant temporal --output evaluation/repeat/C
.\.venv\Scripts\python.exe -m evaluation.run --manifest datasets/holdout.json --variant combined --output evaluation/repeat/D
.\.venv\Scripts\python.exe -m evaluation.diagnose evaluation/repeat/D/results.json
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

The optional current `--continuation-threshold 0.15` detector experiment uses the
final temporal logic; the historical E used the archived initial logic. Do not
present a new run as byte-identical to E. No replay includes fabricated detections.

The same five clips now guide development. Their new scores are regression results,
not independent evidence of generalization. The next evaluation gate requires fresh
subjects/scenes and annotations adequate for localization and identity assessment.
