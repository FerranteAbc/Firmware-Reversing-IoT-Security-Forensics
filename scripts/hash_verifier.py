#!/usr/bin/env python3
"""
hash_verifier.py

Utilitário genérico de verificação/quebra de hash por ataque de dicionário,
usado como apoio no desafio "Goat MD5" (ver
iot-firmware-hacking/iotgoat-challenges/goat-md5/writeup.md).

Suporta qualquer algoritmo disponível em hashlib (md5, sha1, sha256, ...)
e aplica variações simples de capitalização e sufixos comuns sobre cada
palavra da wordlist, antes de recorrer a ferramentas dedicadas como o
John the Ripper para ataques maiores.

Uso:
    python3 hash_verifier.py <hash> <wordlist.txt> [--algo md5]
"""

import argparse
import hashlib
import sys
from typing import Optional


def generate_candidates(word: str):
    """Gera variações simples de capitalização e sufixos para uma palavra."""
    suffixes = ["", "!", "123", "2024", "2025", "2026"]
    bases = {word, word.lower(), word.capitalize(), word.upper()}
    for base in bases:
        for suffix in suffixes:
            yield base + suffix


def crack(target_hash: str, wordlist_path: str, algo: str) -> Optional[str]:
    target_hash = target_hash.strip().lower()
    hasher = getattr(hashlib, algo, None)
    if hasher is None:
        raise ValueError(f"Algoritmo não suportado por hashlib: {algo}")

    with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as fh:
        for line in fh:
            word = line.strip()
            if not word:
                continue
            for candidate in generate_candidates(word):
                digest = hasher(candidate.encode("utf-8")).hexdigest()
                if digest == target_hash:
                    return candidate
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target_hash", help="Hash alvo (hexadecimal)")
    parser.add_argument("wordlist", help="Caminho para a wordlist (ex.: rockyou.txt)")
    parser.add_argument("--algo", default="md5", help="Algoritmo hashlib (md5, sha1, sha256, ...)")
    args = parser.parse_args()

    result = crack(args.target_hash, args.wordlist, args.algo)
    if result:
        print(f"[+] Match encontrado: {result}")
        sys.exit(0)
    else:
        print("[-] Nenhum candidato correspondeu ao hash fornecido.")
        sys.exit(1)


if __name__ == "__main__":
    main()
