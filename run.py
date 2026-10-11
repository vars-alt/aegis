#!/usr/bin/env python3
"""
Aegis: adversarial training. Break a baseline detector with a bounded evasion
attack, then retrain including those evaded patterns and test BOTH models on the
SAME fixed evaded set (standard adversarial-training evaluation).

    python run.py
"""
from __future__ import annotations
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import recall_score

from aegis.data import sample, evade

def main():
    Xtr, ytr = sample(6000, seed=0)
    base = GradientBoostingClassifier(random_state=0).fit(Xtr, ytr)

    # fixed evaluation attack set: evade the BASE model, then freeze it
    Xev_te, yev_te = sample(3000, seed=42)
    Xm_te = Xev_te[yev_te == 1]
    Xm_te_adv = evade(base, Xm_te)                      # frozen attack set

    base_ev = recall_score(np.ones(len(Xm_te_adv)), base.predict(Xm_te_adv))

    # adversarial training: add evaded TRAIN attacks (vs base) back as malicious
    Xm_tr = Xtr[ytr == 1]
    Xm_tr_adv = evade(base, Xm_tr)
    X_aug = np.vstack([Xtr, Xm_tr_adv])
    y_aug = np.concatenate([ytr, np.ones(len(Xm_tr_adv), dtype=int)])
    hardened = GradientBoostingClassifier(random_state=0).fit(X_aug, y_aug)

    hard_ev = recall_score(np.ones(len(Xm_te_adv)), hardened.predict(Xm_te_adv))
    Xcl, ycl = sample(3000, seed=7)
    base_clean = recall_score(ycl, base.predict(Xcl))
    hard_clean = recall_score(ycl, hardened.predict(Xcl))

    print("Aegis — adversarial training against bounded evasion\n" + "-"*54)
    print(f"{'':24}{'undefended':>12}{'hardened':>12}")
    print(f"{'evasive recall':24}{base_ev:>12.1%}{hard_ev:>12.1%}")
    print(f"{'clean recall':24}{base_clean:>12.1%}{hard_clean:>12.1%}")
    print("-"*54)
    print(f"robustness recovered: {hard_ev - base_ev:+.1%} on the frozen attack set,")
    print(f"clean performance kept within {abs(hard_clean - base_clean):.1%}.")
    print("Closes the Range -> Sentinel -> Mirage -> Aegis loop.")

if __name__ == "__main__":
    main()
