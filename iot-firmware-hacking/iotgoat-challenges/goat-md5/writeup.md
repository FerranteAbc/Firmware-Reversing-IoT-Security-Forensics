# 🐐 Goat MD5

**Categoria:** Criptoanálise de Rotinas de Integridade
**Alvo:** Hash MD5 estático embutido no código de verificação
**Status:** ✅ Concluído

## Objetivo

Reverter um hash MD5 estático encontrado no código de verificação/autenticação do sistema embarcado, recuperando a senha ou chave original em texto plano.

## Metodologia

1. **Localização do hash:** identificação, durante a auditoria do código-fonte do sistema, de uma rotina de verificação de integridade que compara a entrada do usuário contra um hash **MD5** fixo no binário/script.
2. **Classificação do algoritmo:** o formato do hash (32 caracteres hexadecimais) confirma MD5 — algoritmo criptograficamente quebrado e rápido o suficiente para ataques de dicionário em larga escala.
3. **Ataque de dicionário:** uso do **John the Ripper** contra o hash extraído, com a wordlist **RockYou** (coleção de +14 milhões de senhas vazadas em incidentes reais), que cobre a grande maioria de senhas fracas/reutilizadas usadas em sistemas embarcados de demonstração.

### Execução

```bash
# Verificação do hash e ataque de dicionário via John the Ripper
echo -n "hash_encontrado" > target_hash.txt
john --format=raw-md5 --wordlist=/usr/share/wordlists/rockyou.txt target_hash.txt
```

## Lição aprendida

MD5 não deve ser usado para verificação de senhas ou integridade de segredos — é rápido o suficiente para que ataques de dicionário com GPUs comuns testem bilhões de candidatos por segundo. A combinação de um algoritmo de hash rápido com uma senha previsível (presente em wordlists públicas como RockYou) é a receita mais comum de comprometimento em sistemas embarcados reais, não apenas em CTFs.
