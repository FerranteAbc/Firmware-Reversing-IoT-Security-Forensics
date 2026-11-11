#!/usr/bin/env bash
#
# extract_firmware.sh
#
# Automatiza a varredura de assinaturas e extração de um dump de firmware,
# usado como apoio no desafio "Hardware Hacking & Extração de Firmware"
# (ver iot-firmware-hacking/hardware-hacking-extracao/writeup.md).
#
# Uso:
#   ./extract_firmware.sh <firmware.bin> [diretorio_saida]

set -euo pipefail

FIRMWARE_FILE="${1:-}"
OUTPUT_DIR="${2:-extracted_rootfs}"

if [[ -z "$FIRMWARE_FILE" ]]; then
  echo "Uso: $0 <firmware.bin> [diretorio_saida]" >&2
  exit 1
fi

if ! command -v binwalk >/dev/null 2>&1; then
  echo "[-] binwalk não encontrado no PATH. Instale-o antes de continuar." >&2
  exit 1
fi

echo "[*] Varredura de assinaturas em: $FIRMWARE_FILE"
binwalk "$FIRMWARE_FILE"

echo "[*] Extração recursiva (binwalk -Me)..."
binwalk -Me "$FIRMWARE_FILE"

# O binwalk cria uma pasta _<arquivo>.extracted/ — localiza qualquer
# sistema de arquivos SquashFS dentro dela para extração estruturada.
EXTRACTED_DIR="_$(basename "$FIRMWARE_FILE").extracted"

if [[ -d "$EXTRACTED_DIR" ]]; then
  SQUASHFS_FILE=$(find "$EXTRACTED_DIR" -iname "*.squashfs" -o -iname "*squashfs*" 2>/dev/null | head -n1 || true)
  if [[ -n "$SQUASHFS_FILE" ]] && command -v unsquashfs >/dev/null 2>&1; then
    echo "[*] Sistema de arquivos SquashFS encontrado: $SQUASHFS_FILE"
    echo "[*] Extraindo rootfs para: $OUTPUT_DIR"
    unsquashfs -d "$OUTPUT_DIR" "$SQUASHFS_FILE"
  else
    echo "[!] Nenhum SquashFS localizado automaticamente — inspecione $EXTRACTED_DIR manualmente."
  fi
else
  echo "[!] Diretório de extração do binwalk não encontrado: $EXTRACTED_DIR"
fi

echo "[+] Concluído."
