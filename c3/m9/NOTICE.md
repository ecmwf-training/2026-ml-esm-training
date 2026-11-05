# Changes made to the upstream notebook

`causal_discovery.ipynb` and `causal_discovery_solved.ipynb` are derived from
[`M_Causal_MOOC.ipynb`](https://github.com/tbeucler/2026_ECMWF_MOOC) (MIT,
© 2026 Tom Beucler). The MIT notice is preserved in `LICENSE`.

The intention was to carry the original notebook over as faithfully as possible.
Explanatory prose, the exercise questions, the interpretation guides and the
closing sections are the original authors' text, unchanged except where the
items below forced an edit.

## Bug fixes (the upstream notebook does not run end to end)

- `data_layout` and `raw_storm_dict` were referenced but never defined, raising
  `NameError` in Q1.5. The dead "pooled storm dictionary" branch is removed and
  the notebook uses the `Xnorml['train'/'valid'/'test']` partitions that the
  prepared fold files actually ship (184/31/31 storms).
- Upstream Part II re-split the 184 M-PC *training* storms 70/15/15, so the
  "unseen test storms" of Parts IV-VI were inside M-PC's own discovery set. All
  parts now use the same supplied partitions, so held-out storms are genuinely
  held out. Reported scores therefore differ from the upstream saved outputs.
- The Q4.1 exercise cell began with a bare `fill and complete the code` line
  (a `SyntaxError`).
- The MLP evaluation cell used `y_tr_pred`/`y_val_pred`/`y_te_pred`, which no cell
  defined, and the MLP is fitted on a standardised target, so predictions now go
  through `scaler_y.inverse_transform`.
- `shap` and `networkx` were missing from the install cell (`tigramite.models`
  imports `networkx` without declaring it; Colab ships it, a clean env does not),
  and `tigramite.__version__` does not exist.
- The MLP hyperparameters named in the text `(32, 16)`, `alpha=0.01`,
  `max_iter=500` did not match those used `(512, 512, 512, 512)`, `max_iter=1000`.
  The text now describes the settings the cell actually uses.
- Question numbering: the final SHAP question was labelled `Q7` with no Q6;
  questions are renumbered contiguously, and the missing SHAP "Step 3" is added.

## Course-structure changes

- Split into an exercise notebook and a `_solved` counterpart, per repo
  convention. Nine fill-in-the-blank exercises stay open in the exercise version;
  the inline "Possible solution" cells that previously sat directly beneath each
  blank now live in the solved notebook instead. The exercise prompts and hints
  are the original Q-cell text, condensed where two questions merged into one.
- Standard course header: authors, last-tested date, About and
  "Running this notebook" dropdowns, Colab/Kaggle/GitHub badges.
- `requirements.txt` installed from the raw GitHub URL, as in the other modules.
- The 365 MB `git clone` of the CausalSHIPS repository is replaced by a targeted
  download (two helper modules plus one ~21 MB fold archive), pinned to upstream
  commit `f7c42d5`.
- The 1.4 MB base64 figure embedded in the notebook moved to
  `assets/causal_workflow.png` (full resolution, 4000x2757) and referenced by URL
  so it renders on Colab and Kaggle.
- The M-PC sweep result is cached in `_resources/mpc_sweep_fold3.json` so Parts
  IV-VI run in minutes; set `RUN_FULL_SWEEP = True` to recompute it. The full
  sweep was measured at 472 s (19 alpha values, 5.6 s at alpha=0.001 rising to
  166 s at alpha=0.9, as looser thresholds retain more parents).

## Effect of the split fix on the reported numbers

M-PC discovery itself is unchanged - it always ran on the 184 training storms, and
still selects the same 38 predictors at `pc_alpha = 0.8`. What changes is the
downstream evaluation, which now uses genuinely held-out storms:

| Method | Predictors | Val R2 | Test R2 (unseen) |
|---|---|---|---|
| All 214 features (no FS) | 214 | **0.348** | **0.008** |
| Causal M-PC + MLR | 38 | 0.292 | 0.321 |
| Random Forest FS + MLR | 30 | 0.272 | 0.297 |
| Correlation FS + MLR | 28 | 0.266 | 0.207 |
| Causal M-PC + MLP | 38 | 0.246 | 0.353 |

The full-predictor model now tops the validation table and then collapses on
unseen storms. Under the upstream leaky split it appeared to win on both.

Verified end to end: `causal_discovery_solved.ipynb` executes with zero errors
(Python 3.12, tigramite 5.2.10.1), 31/31 code cells.
