# 🐐 Goat Init

**Categoria:** Auditoria de Boot / Sistemas Embarcados
**Alvo:** `/etc/init.d/` e `/etc/rc.local` do rootfs extraído
**Status:** ✅ Concluído

## Objetivo

Auditar os vetores de inicialização do sistema operacional embarcado (OpenWrt/IoTGoat) em busca de segredos ou comportamentos inseguros deixados nos scripts de boot.

## Metodologia

1. **Análise estática dos scripts de boot:** inspeção direta do conteúdo de `/etc/rc.local` e dos scripts em `/etc/init.d/`, que são executados automaticamente durante a sequência de inicialização do sistema.
2. **Busca dirigida:** em vez de ler cada script manualmente linha a linha, uma varredura recursiva por palavras-chave (`flag`, variáveis de ambiente suspeitas, chamadas a binários customizados) acelera a identificação do script relevante.
3. **Identificação de exposição:** scripts de inicialização que fixam variáveis de ambiente sensíveis ou chaves diretamente no código-fonte (*hardcoded secrets*) ficam permanentemente expostos a qualquer um com acesso de leitura ao rootfs — não é necessário executar o sistema para extrair o segredo.

### Execução

```bash
cat extracted_rootfs/etc/rc.local
grep -rni "flag" extracted_rootfs/etc/init.d/
```

## Lição aprendida

Scripts de boot em sistemas embarcados são um dos primeiros lugares a inspecionar em qualquer auditoria, pois frequentemente carregam configurações, credenciais de serviço ou chaves de API diretamente em texto plano — algo que nunca deveria estar fora de um mecanismo seguro de gerenciamento de segredos (vault, variáveis injetadas em tempo de execução).
