#!/usr/bin/env python3
"""
Range-inspired traffic where the malicious signal lives mainly in the TWO
attacker-controllable features (request rate, payload entropy), plus two noisy
features. A bounded evasion attack lowers the controllable features toward the
benign boundary — faintly enough that adversarial training can still recover.
"""
from __future__ import annotations
import numpy as np

FEATURES = ["rate", "entropy", "noise1", "noise2"]
MUTABLE = {0: 0.42, 1: 0.50}   # push rate & entropy toward the benign boundary

def sample(n, seed):
    rng = np.random.default_rng(seed)
    X, y = [], []
    for _ in range(n):
        mal = rng.random() < 0.3
        if mal:
            rate, ent = rng.normal(0.72, 0.10), rng.normal(0.70, 0.10)
        else:
            rate, ent = rng.normal(0.30, 0.10), rng.normal(0.38, 0.10)
        X.append([rate, ent, rng.normal(0.5, 0.25), rng.normal(0.5, 0.25)])
        y.append(int(mal))
    return np.clip(np.array(X), 0, 1), np.array(y)

def evade(model, X_mal, steps=5, lr=0.3):
    """Budget-limited evasion toward the benign boundary (MITRE ATLAS AML.T0015)."""
    X = X_mal.copy().astype(float)
    for i in range(len(X)):
        for _ in range(steps):
            if model.predict(X[i:i+1])[0] == 0:
                break
            for idx, tgt in MUTABLE.items():
                X[i, idx] += (tgt - X[i, idx]) * lr
    return X
