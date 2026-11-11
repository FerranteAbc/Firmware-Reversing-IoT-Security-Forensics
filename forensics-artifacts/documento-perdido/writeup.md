# 📄 Documento Perdido

**Categoria:** File Carving / Forense de Documentos
**Alvo:** Estrutura interna de um arquivo PDF
**Status:** ✅ Concluído

## Objetivo

Recuperar artefatos ocultos em camadas de metadados e na estrutura interna de um documento digital (PDF), incluindo revisões anteriores, dados de autoria e fluxos (*streams*) ofuscados.

## Metodologia

1. **Auditoria completa de metadados:** uso do `exiftool` com flags para exibir **todos** os campos de metadados, inclusive os não exibidos por padrão (tags proprietárias, histórico de edição, software de criação) — dados de autoria ou revisões anteriores frequentemente permanecem no arquivo mesmo após edições "finais".
2. **Inspeção da estrutura interna do PDF:** diferente de abrir o arquivo em um leitor, o `pdfid` cataloga todos os objetos e elementos estruturais presentes no PDF (streams, JavaScript embutido, anexos), funcionando como uma primeira triagem de "o que existe" dentro do arquivo.
3. **Busca dirigida em objetos/streams:** o `pdf-parser` permite buscar diretamente por palavras-chave dentro dos objetos e streams internos do PDF (inclusive os comprimidos), localizando conteúdo que não aparece na renderização visual do documento.

### Execução

```bash
# Auditoria completa de metadados não visíveis
exiftool -a -u documento_alvo.pdf

# Inspeção de objetos e fluxos internos em arquivos PDF
pdfid documento_alvo.pdf
pdf-parser --search "flag" documento_alvo.pdf
```

## Lição aprendida

Um documento PDF é um contêiner com múltiplas camadas — texto renderizado, metadados, objetos internos e streams comprimidos — e cada camada pode reter informação que o autor acreditava ter removido. Antes de distribuir qualquer documento sensível, é necessário limpar metadados explicitamente (não basta "salvar como" ou exportar a versão final), pois ferramentas forenses padrão (`exiftool`, `pdfid`, `pdf-parser`) recuperam essas camadas trivialmente.
