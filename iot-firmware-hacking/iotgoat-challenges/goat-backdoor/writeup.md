# 🐐 Goat Backdoor

**Categoria:** Caça a Backdoors / Serviços Ocultos
**Alvo:** Binários e daemons do rootfs extraído
**Status:** ✅ Concluído

## Objetivo

Localizar serviços não convencionais e portas de depuração/*backdoors* deixados no firmware, frequentemente usados por fabricantes para suporte remoto e esquecidos (ou deliberadamente ocultados) no firmware de produção.

## Metodologia

1. **Varredura de listeners ocultos:** busca recursiva nos diretórios de executáveis (`/bin`, `/sbin`, `/usr/bin`) por invocações de `netcat` (`nc -l`) configuradas como *listener*, um padrão clássico de shell reversa/backdoor leve embutido em scripts de inicialização ou binários customizados.
2. **Análise de strings de binários suspeitos:** extração de strings legíveis de executáveis não padrão do sistema (nomeados de forma genérica, como `backdoor_bin`), filtrando por indícios de shells (`sh`, `bash`) ou referências diretas à flag.
3. **Confirmação:** a combinação de um binário com nome atípico, strings referenciando execução de shell e ausência de qualquer mecanismo de autenticação confirma a presença de um backdoor funcional.

### Execução

```bash
grep -rn "nc -l" extracted_rootfs/
strings extracted_rootfs/usr/bin/backdoor_bin | grep -E "(sh|bash|flag)"
```

## Lição aprendida

Backdoors em firmware costumam ser triviais de localizar estaticamente (sem precisar executar o dispositivo) porque dependem de binários padrão do sistema (`netcat`) ou de nomes de arquivo pouco cuidadosos. Builds de produção devem remover utilitários de debug/suporte remoto antes do empacotamento final do firmware — não basta "escondê-los", pois qualquer extração do sistema de arquivos os expõe.
