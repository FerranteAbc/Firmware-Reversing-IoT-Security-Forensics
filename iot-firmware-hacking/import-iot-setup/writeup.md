# ⚡ Import IoT & Setup

**Categoria:** Provisionamento de Ambiente
**Alvo:** OWASP IoTGoat (imagem x86)
**Status:** ✅ Concluído

## Objetivo

Provisionar e validar a integridade do ambiente vulnerável **OWASP IoTGoat** antes de iniciar qualquer análise — garantir que a imagem de disco baixada não foi corrompida ou adulterada no download, e deixá-la pronta para montagem/emulação.

## Metodologia

1. **Checagem de integridade:** cálculo do hash **SHA-256** da imagem comprimida e comparação com o valor publicado oficialmente, descartando corrupção de transferência antes de qualquer análise.
2. **Descompressão:** extração do arquivo `.img.gz` para obter a imagem de disco bruta.
3. **Montagem/emulação:** carregamento da imagem em ambiente isolado (QEMU/VirtualBox), permitindo interação com o sistema OpenWrt do IoTGoat sem risco à máquina de análise.

### Execução

```bash
sha256sum IoTGoat-x86.img.gz
gunzip IoTGoat-x86.img.gz
```

## Lição aprendida

Validar a integridade de uma imagem antes de qualquer análise forense ou de engenharia reversa é um passo de higiene básica, mas essencial: uma imagem corrompida pode produzir falsos negativos (uma partição que falha ao montar não significa ausência de dados, pode ser corrupção de download) e invalidar toda a cadeia de evidências subsequente.
