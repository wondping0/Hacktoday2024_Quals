<div align="center">

# Hacktoday2024_Quals

**Crypto challenges from the HackToday 2024 CTF qualifier, with solve scripts where available.**

![Python](https://img.shields.io/badge/Python-3-38E1FF?style=flat-square&labelColor=0A1428&logo=python&logoColor=38E1FF)
![SageMath](https://img.shields.io/badge/SageMath-Curve%20Enjoyer-38E1FF?style=flat-square&labelColor=0A1428)
![Category](https://img.shields.io/badge/CTF-crypto-38E1FF?style=flat-square&labelColor=0A1428)

</div>

---

## Overview

The `crypto/` folder holds six challenges from the HackToday 2024 qualifier.
Three include a solve script (`solver.py`). The other three contain only the challenge source and output.

| Challenge | Topic | Solver |
| --- | --- | --- |
| [Curve Enjoyer](crypto/Curve%20Enjoyer) | ECDLP on curves with smooth order: Pohlig–Hellman + CRT | yes |
| [Split and Splice](crypto/Split%20and%20Splice) | Inverting iterated XOR-of-shifts (Gray-code-like) maps | yes |
| [tercuri](crypto/tercuri) | Small-exponent RSA broadcast (Håstad) | yes |
| [Super Guesser](crypto/Super%20Guesser) | AES-CBC padding oracle with a noisy, probabilistic answer | no |
| [knapsack RSA](crypto/knapsack%20RSA) | RSA-encrypted knapsack blocks + AES-CBC | no |
| [komputernasa](crypto/komputernasa) | XOR with keys derived from huge polynomial sums | no (experiment only) |

## Challenges

### Curve Enjoyer

`server.py` picks a fresh random prime `p` of a bit length you choose, takes a random point `P` on `y^2 = x^3 + ax + b` over `F_p`, and prints `P` and `Q = flag * P`.
The flag is padded with 100 random bytes.

`solver.py` asks for 300 curves over 128-bit primes. For each curve it:

1. recovers `a` and `b` from the two points;
2. computes the curve order in Sage and factors out its small prime powers (trial division up to 20000);
3. brute-forces the discrete log in each small subgroup.

The residues are combined with CRT to rebuild the flag.
The solver reads the base point after a `G = ` label from the competition service, while the included `server.py` prints `P = `. Adjust that line for a local run (`io = process(["python3","server.py"])` is left commented in the script).

### Split and Splice

`script.py` splits the flag in half. It applies `x ^ (x>>1) ^ (x>>2)` to the first half 1000 times and `(2x) ^ x ^ (x>>1) ^ (x>>2)` to the second half 1000 times.
It then prints the two decimal results glued together (`file.txt`).

Both maps are linear over GF(2). `solver.py` inverts each one by finding the map's period at the given bit length and applying it period−1 more times.
It also tries different split points of the decimal string to separate the two halves (the loop is left at the split index that worked).
`notes.txt` holds the hand-worked bit-matrix iterations used to understand the period.

### tercuri

`server.py` encrypts a random suspect name from a list with RSA, using a new 1024-bit modulus and a 5-bit prime `e` on every connection.

`data.py` collects 500 `n:e:c` samples from the service per run (it writes `data3.txt`, which is empty in the repo). `solver.py` reads the saved samples in `data.txt`, `data1.txt` and `data2.txt` and runs Håstad's broadcast attack:

1. keep the samples that share the most common `e`;
2. filter out samples that belong to suspects already recovered;
3. randomly pick 9 ciphertexts, combine them with CRT and check whether the result is a perfect `e`-th root.

`flagged` holds the result string the author saved.

### Super Guesser (challenge only)

AES-CBC encrypts the flag, and the service tells you whether a submitted ciphertext has valid padding.
The answer goes through a random Gaussian check with different bounds for valid and invalid padding, so the oracle is noisy and must be queried statistically.

### knapsack RSA (challenge only)

The first half of the flag is split into 40-bit blocks. Each bit selects a random 512-bit number, and the selected numbers are RSA-encrypted with `e = 11`.
Published values: the encrypted numbers (unselected slots filled with random values), the per-block sums of the encrypted numbers (`weight`) and the column-wise sums of the selected numbers across blocks (`sums`).
The XOR of the selected numbers, hashed with SHA-256, is the AES-CBC key for the second half. All values are in `output.txt`.

### komputernasa (challenge only)

The flag is XORed with three keys taken from the digits of `sum_{x=1..n} eq_k(x)` modulo products of large constants, for very large `n`.
`encrypt.py` gives the polynomials. `enc.txt` is the ciphertext.
`lab.py` is an experiment that computes the first sum with matrix exponentiation and checks it against the direct sum for `n = 100`.

## Files

```
crypto/
├── Curve Enjoyer/     server.py, secret.py (redacted), solver.py, flag
├── Split and Splice/  script.py, file.txt, notes.txt, solver.py, flag
├── Super Guesser/     server.py
├── knapsack RSA/      chall.py, output.txt
├── komputernasa/      encrypt.py, enc.txt, lab.py
└── tercuri/           server.py, data.py, data*.txt, solver.py, flagged
```

## Requirements

Python 3 plus the packages imported by the scripts:

| Package | Used by |
| --- | --- |
| `pycryptodome` | all challenges (`Crypto.Util.number`, `Crypto.Cipher.AES`, …) |
| `sympy` | Curve Enjoyer (`sqrt_mod`, `crt`), tercuri (`crt`) |
| `ecdsa` | Curve Enjoyer |
| `pwntools` | Curve Enjoyer solver, tercuri `data.py` |
| [SageMath](https://www.sagemath.org/) | Curve Enjoyer solver (`EllipticCurve`, `factor_trial_division`) |
| `gmpy2` | tercuri solver |
| `numpy` | Super Guesser, komputernasa `lab.py` |

```bash
pip install pycryptodome sympy ecdsa pwntools gmpy2 numpy
```

## Usage

Offline solvers (the data is in the repo):

```bash
cd "crypto/Split and Splice" && python solver.py
cd crypto/tercuri && python solver.py     # loops, printing each recovered plaintext
```

Curve Enjoyer needs a running service. Point `solver.py` at a local `server.py` (see the note above), then:

```bash
cd "crypto/Curve Enjoyer" && sage -python solver.py
```

The remote addresses in `solver.py` and `data.py` were the competition servers and may no longer be reachable.

---

<div align="center">

Part of [wondping0](https://github.com/wondping0)'s cryptography notebooks · [wondping0.github.io](https://wondping0.github.io)

</div>
