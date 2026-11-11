# 🐐 Goat Kernel

**Categoria:** Inspeção de Módulos de Kernel
**Alvo:** Módulos `.ko` em `/lib/modules/`
**Status:** ✅ Concluído

## Objetivo

Inspecionar módulos de kernel compilados (`.ko`) presentes no firmware, em busca de drivers proprietários com configurações permissivas ou brechas de integridade executando em espaço de kernel (*ring 0*).

## Metodologia

1. **Enumeração de módulos:** varredura do diretório `/lib/modules/` do rootfs extraído em busca de todos os arquivos com extensão `.ko`, que representam módulos carregáveis do kernel Linux.
2. **Inspeção de metadados do módulo:** uso do `modinfo` para extrair informações declaradas pelo próprio módulo — autor, licença, parâmetros aceitos e descrição — sem precisar carregar o módulo em um kernel real.
3. **Avaliação de risco:** módulos de kernel executam com privilégios máximos do sistema operacional; qualquer parâmetro mal validado ou lógica proprietária sem auditoria representa uma superfície de ataque crítica, pois uma falha ali compromete todo o sistema, não apenas um processo isolado.

### Execução

```bash
find extracted_rootfs/lib/modules/ -name "*.ko"
modinfo extracted_rootfs/lib/modules/*/custom_module.ko
```

## Lição aprendida

Módulos de kernel customizados (fora da árvore oficial do Linux) exigem auditoria redobrada: diferente de um binário de espaço de usuário, um bug em um módulo de kernel não causa apenas a falha de um processo — pode comprometer o sistema inteiro. `modinfo` é a forma mais segura de inspecionar um módulo desconhecido sem o risco de carregá-lo em um kernel ativo.
