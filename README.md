# Aegis 🛡️

**Hardening ML detectors against adversarial evasion** via adversarial training. Aegis takes a detector that [Mirage](https://github.com/vars-alt/mirage) has broken, retrains it on the evasive attack patterns, and restores detection — without sacrificing clean performance.

> Project **[4]** in a portfolio on adversarial ML & AI security. Aegis is the defender that closes the loop: **The Range → Sentinel → Mirage → Aegis.**

---

## Result

A detector is broken by bounded evasion, then hardened by adversarial training. Both are tested on the **same frozen attack set**:

| | Undefended | Hardened |
|---|---|---|
| Recall on evasive traffic | **0.3%** | **99.4%** |
| Recall on clean traffic | 99.2% | 99.6% |

Adversarial training recovers **+99 points** of robustness on the attack set while keeping clean performance within 0.3%. That trade-off — and the honesty about it — is the whole point.

## Quickstart

```bash
pip install -r requirements.txt
make run
```

## Method

1. Train a baseline detector.
2. Craft bounded evasive attacks against it (Mirage-style) and **freeze** them as the evaluation set.
3. Retrain including evaded samples relabeled malicious (adversarial training).
4. Compare both models on the frozen attack set and on clean traffic.

The attack budget is deliberately bounded: an attacker with unlimited freedom can push samples into genuinely benign territory, where *no* classifier can separate them. Aegis defends the realistic, bounded regime — and the code is explicit about that limit.

- `aegis/data.py` — traffic + the bounded evasion routine
- `run.py` — the full before/after comparison

## License

MIT — see [LICENSE](LICENSE).
