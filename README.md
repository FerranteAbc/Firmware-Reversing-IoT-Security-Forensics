# 🚩 FIAP CTF — Firmware Reversing, IoT Security & Forensics (Guia Explicativo)

> Repositório com detalhamento técnico das metodologias, comandos executados, raciocínio analítico e ferramentas empregadas nos desafios práticos de **OWASP IoTGoat**, **Engenharia Reversa de Firmware** e **Forense Digital**.

---

## 🛠️ Toolkit Geral Empregado

* **Análise de Firmware & Reversing:** `binwalk`, `squashfs-tools` (`unsquashfs`), `qemu-user-static`, `chroot`.
* **Inspeção de Binários & Criptografia:** `strings`, `hexdump`, `xxd`, `md5sum`, `sha256sum`, CyberChef, John the Ripper.
* **Forense de Arquivos & Artefatos:** `exiftool`, `pdfid`, `pdf-parser`, `foremost`, editores hexadecimais.
* **Análise de Mensagens & Headers:** `grep`, visualizadores de RFC 822/email, validadores de SPF/DKIM/DMARC.

---

## 🧩 Detalhamento Técnico dos Desafios

### 1. Import IoT (Provisionamento e Extração de Imagem)
* **O que foi feito:** Configuração e preparação do ambiente para auditoria do ecossistema vulnerável OWASP IoTGoat (baseado em OpenWrt). Realizou-se a importação da imagem crua de disco e firmware, validação de integridade por hash e montagem das interfaces de rede virtuais para comunicação entre a máquina atacante e o dispositivo emulado.
* **Ferramentas:** VirtualBox / VMware / QEMU, `sha256sum`, scripts de bridge de rede Linux.
* **Raciocínio & Procedimento:** O arquivo compactado do IoTGoat foi baixado, seu hash SHA-256 foi checado contra o repositório oficial e a imagem de disco foi associada ao virtualizador para permitir inspeção tanto via sistema em execução quanto offline.

```bash
# Validação do arquivo baixado e extração inicial
sha256sum IoTGoat-x86.img.gz
gunzip IoTGoat-x86.img.gz
```

📋 Resumo das Fases & StatusDesafioFoco OperacionalFerramentas ChaveStatusImport IoTEmulação e setup de rede de testesQEMU, sha256sum[Concluído]Hardware HackingDescompressão e extração de SquashFSBinwalk, unsquashfs[Concluído]Goat InitAuditoria de scripts de inicializaçãogrep, cat, rc.local[Concluído]Goat MD5Reversão de hash e análise de integridadeJohn, CyberChef, md5sum[Concluído]Goat BackdoorIdentificação de portas e binários ocultosstrings, nmap, grep[Concluído]Goat KernelInspeção de módulos .ko e configuraçõesmodinfo, strings[Concluído]E-mail SuspeitoForense de headers e validação SPF/DKIMEditores RFC 822, Base64[Concluído]Documento PerdidoInspeção de metadados e streams em arquivosExifTool, pdf-parser[Concluído]
👤 AutorPedro Henrique Ferrante Prado — Defesa Cibernética, FIAP
