# 📧 E-mail Suspeito

**Categoria:** Forense Digital / Anti-Spoofing
**Alvo:** Cabeçalhos RFC 822 de uma mensagem de e-mail (`.eml`)
**Status:** ✅ Concluído

## Objetivo

Realizar perícia em uma comunicação corporativa suspeita para determinar sua autenticidade (ou falta dela) e extrair qualquer payload oculto no corpo da mensagem.

## Metodologia

1. **Rastreamento estrutural dos cabeçalhos `Received:`:** cabeçalhos de e-mail são empilhados de baixo para cima a cada salto SMTP — o cabeçalho mais próximo do remetente original fica no final da pilha. Ler nessa ordem (de baixo para cima) reconstrói o caminho real percorrido pela mensagem pela rede, revelando servidores intermediários não declarados ou inconsistentes com o domínio alegado do remetente.
2. **Auditoria dos mecanismos de autenticação de e-mail:** verificação dos resultados de **SPF** (Sender Policy Framework), **DKIM** (DomainKeys Identified Mail) e **DMARC** no cabeçalho `Authentication-Results` — os três mecanismos padrão de mercado para validar que um e-mail realmente partiu do domínio que afirma ter enviado.
3. **Extração de payload:** o corpo da mensagem continha um bloco codificado em **Base64**, decodificado para revelar seu conteúdo real.

### Execução

```bash
grep -iE "(Received:|Received-SPF|Authentication-Results)" email_amostra.eml
base64 -d payload_encoded.txt
```

## Lição aprendida

A validação de um e-mail nunca deve se basear apenas no campo `From:` visível na caixa de entrada — ele é trivialmente falsificável. Os cabeçalhos `Received:` (caminho real) e os resultados de SPF/DKIM/DMARC são as fontes de verdade técnicas para confirmar (ou refutar) a origem alegada de uma mensagem, e devem ser o primeiro ponto de verificação em qualquer investigação de phishing/spoofing.
