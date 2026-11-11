# ⚙️ Hardware Hacking & Extração de Firmware

**Categoria:** Engenharia Reversa de Firmware
**Alvo:** Dump binário bruto de memória flash
**Status:** ✅ Concluído

## Objetivo

Reconstituir a árvore de diretórios do sistema de arquivos (*rootfs*) a partir de um dump binário bruto, sem qualquer metadado ou cabeçalho de arquivo explícito indicando seu conteúdo.

## Metodologia

1. **Varredura por assinaturas mágicas:** uso do `binwalk` para escanear o binário em busca de *magic bytes* conhecidos — assinaturas que identificam o início de estruturas reconhecíveis (cabeçalho de kernel Linux, superblocos de sistemas de arquivos, etc.) embutidas em qualquer offset do arquivo.
2. **Localização da partição SquashFS:** a varredura identificou o offset de uma partição comprimida em **SquashFS**, formato read-only extremamente comum em firmwares embarcados por sua alta taxa de compressão.
3. **Extração recursiva:** o `binwalk -Me` não apenas identifica, mas extrai e descomprime recursivamente qualquer camada aninhada encontrada, reconstruindo a árvore de diretórios completa do rootfs para análise offline.

### Execução

```bash
# Varredura de assinaturas e descompressão recursiva
binwalk -Me firmware.bin

# Extração estruturada do sistema de arquivos
unsquashfs -d extracted_rootfs filesystem.squashfs
```

## Lição aprendida

Firmwares embarcados raramente escondem o sistema de arquivos com qualquer proteção real — a compressão (SquashFS, Gzip, LZMA) é para economia de espaço em flash, não para segurança. Ferramentas de identificação de assinatura binária (`binwalk`) tornam a extração quase mecânica, o que reforça que nenhum segredo (credencial, chave privada) deve ser deixado em claro dentro da imagem de firmware distribuída.
