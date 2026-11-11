# 🚩 FIAP CTF — Hardware Hacking, OWASP IoTGoat & Digital Forensics

> Documentação técnica aprofundada dos desafios de Capture The Flag (CTF) focados em **Auditoria de Sistemas Embarcados (OWASP IoTGoat)**, **Engenharia Reversa de Firmware** e **Forense Digital de Artefatos**, desenvolvidos no curso de **Defesa Cibernética** (*Ethical Hacking, Forensics & Secure DevOps*) da FIAP.

---

## 📌 Visão Geral do Projeto

Este repositório reúne os relatórios técnicos (*write-ups*), comandos utilizados, raciocínio analítico e estratégias de exploração empregadas em desafios práticos de cibersegurança. As frentes de atuação concentram-se em:

* **Segurança em IoT & Sistemas Embarcados:** Extração e desmontagem de imagens de firmware baseadas em OpenWrt, auditoria de código-fonte de inicialização, quebra de rotinas criptográficas fracas e caça a portas de depuração/backdoors.
* **Forense Digital & Análise de Artefatos:** Engenharia reversa e perícia em cabeçalhos de e-mail (*anti-spoofing*) e inspeção profunda de metadados e fluxos ocultos em documentos digitais.

---

## 🛠️ Tecnologias & Ferramentas

| Domínio | Ferramentas & Utilitários |
| :--- | :--- |
| **Firmware & Extração** | `binwalk`, `squashfs-tools` (`unsquashfs`), `dd`, `file` |
| **Emulação & Ambiente** | QEMU, VirtualBox, Kali Linux, ambientes baseados em OpenWrt |
| **Criptoanálise & Binários** | `strings`, `hexdump`, `xxd`, `md5sum`, `sha256sum`, CyberChef, John the Ripper |
| **Forense & Metadados** | `exiftool`, `pdfid`, `pdf-parser`, visualizadores de RFC 822/MIME |

---

## 🧩 Detalhamento Técnico dos Desafios

### ⚡1. Import IoT & Setup
* **Foco:** Provisionamento e validação de integridade do ambiente vulnerável OWASP IoTGoat.
* **Metodologia:** Descompressão da imagem crua de disco, checagem da integridade de dados via hash criptográfico SHA-256 e montagem em ambiente isolado via emulador de arquitetura.
### ⚙Comandos Chave:
  ```bash
  sha256sum IoTGoat-x86.img.gz
  gunzip IoTGoat-x86.img.gz
  ```
**Write-up completo:** [`iot-firmware-hacking/import-iot-setup/`](iot-firmware-hacking/import-iot-setup/writeup.md)

### ⚡2. Hardware Hacking & Extração de Firmware
Foco: Reconstituição da árvore de diretórios do sistema de arquivos (rootfs) a partir de um dump binário bruto de memória flash.

Metodologia: Varredura por assinaturas mágicas para identificação do cabeçalho do kernel e localização da partição compactada em SquashFS, permitindo a extração completa dos binários offline.

### ⚙Comandos Chave:

 ```bash
# Varredura de assinaturas e descompressão recursiva
binwalk -Me firmware.bin

# Extração estruturada do sistema de arquivos
unsquashfs -d extracted_rootfs filesystem.squashfs
```
**Write-up completo:** [`iot-firmware-hacking/hardware-hacking-extracao/`](iot-firmware-hacking/hardware-hacking-extracao/writeup.md) · **Script de apoio:** [`scripts/extract_firmware.sh`](scripts/extract_firmware.sh)

### ⚡3. Goat Init
Foco: Auditoria em vetores de inicialização do sistema operacional embarcado.

Metodologia: Análise estática nos scripts executados durante a sequência de boot (/etc/init.d/ e /etc/rc.local) para identificar variáveis de ambiente desprotegidas, chamadas a binários customizados e chaves hardcoded.

### ⚙Comandos Chave:

 ```bash
cat extracted_rootfs/etc/rc.local
grep -rni "flag" extracted_rootfs/etc/init.d/
```
**Write-up completo:** [`iot-firmware-hacking/iotgoat-challenges/goat-init/`](iot-firmware-hacking/iotgoat-challenges/goat-init/writeup.md)

### ⚡4. Goat MD5
Foco: Criptoanálise de rotinas de verificação de integridade e autenticação.

Metodologia: Identificação de hashes MD5 estáticos inseridos no código de verificação do sistema e reversão via ataque de dicionário (wordlist attack).

### ⚙Comandos Chave:

 ```bash
# Verificação do hash e ataque de dicionário via John the Ripper
echo -n "hash_encontrado" > target_hash.txt
john --format=raw-md5 --wordlist=/usr/share/wordlists/rockyou.txt target_hash.txt
```
**Write-up completo:** [`iot-firmware-hacking/iotgoat-challenges/goat-md5/`](iot-firmware-hacking/iotgoat-challenges/goat-md5/writeup.md) · **Script de apoio:** [`scripts/hash_verifier.py`](scripts/hash_verifier.py)

### ⚡5. Goat Backdoor
Foco: Caça a serviços não convencionais e portas de depuração expostas.

Metodologia: Varredura recursiva nos diretórios de executáveis (/bin, /sbin, /usr/bin) em busca de utilitários como netcat configurados como listeners ocultos ou shells reversas configuradas para iniciar sem autenticação.

### ⚙Comandos Chave:

 ```bash
grep -rn "nc -l" extracted_rootfs/
strings extracted_rootfs/usr/bin/backdoor_bin | grep -E "(sh|bash|flag)"
```
**Write-up completo:** [`iot-firmware-hacking/iotgoat-challenges/goat-backdoor/`](iot-firmware-hacking/iotgoat-challenges/goat-backdoor/writeup.md)

### ⚡6. Goat Kernel
Foco: Inspeção de segurança em módulos de kernel compilados (.ko).

Metodologia: Auditoria de parâmetros de módulos proprietários inseridos em /lib/modules/, verificando configurações permissivas ou brechas de integridade em espaço de kernel (ring 0).

### ⚙Comandos Chave:

 ```bash
find extracted_rootfs/lib/modules/ -name "*.ko"
modinfo extracted_rootfs/lib/modules/*/custom_module.ko
```
**Write-up completo:** [`iot-firmware-hacking/iotgoat-challenges/goat-kernel/`](iot-firmware-hacking/iotgoat-challenges/goat-kernel/writeup.md)

### ⚡7. E-mail Suspeito
Foco: Forense em comunicações corporativas e detecção de phishing/spoofing.

Metodologia: Rastreamento estrutural de cabeçalhos RFC 822 de baixo para cima (Received:) para mapear os saltos SMTP reais, auditoria dos mecanismos de autenticação (SPF, DKIM, DMARC) e decodificação de payloads em Base64 contidos no corpo do e-mail.

### ⚙Comandos Chave:

 ```bash
grep -iE "(Received:|Received-SPF|Authentication-Results)" email_amostra.eml
base64 -d payload_encoded.txt
```
**Write-up completo:** [`forensics-artifacts/email-suspeito/`](forensics-artifacts/email-suspeito/writeup.md)

### ⚡8. Documento Perdido
Foco: File carving e extração de artefatos em camadas de metadados.

Metodologia: Perícia em documentos digitais (PDF/Office) para recuperar revisões anteriores, dados de autoria e fluxos (streams) ocultos ou ofuscados dentro da estrutura do arquivo.

### ⚙Comandos Chave:

 ```bash
# Auditoria completa de metadados não visíveis
exiftool -a -u documento_alvo.pdf

# Inspeção de objetos e fluxos internos em arquivos PDF
pdfid documento_alvo.pdf
pdf-parser --search "flag" documento_alvo.pdf
```
**Write-up completo:** [`forensics-artifacts/documento-perdido/`](forensics-artifacts/documento-perdido/writeup.md)
## 📋 Resumo das Fases & Status


| Desafio | Alvo / Vetor | Técnica Principal | Ferramentas Chave | Status | Write-up |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **Import IoT** | Ambiente IoTGoat | Provisionamento e validação de integridade | `sha256sum`, `gunzip`, QEMU | `[Concluído]` | [`import-iot-setup/`](iot-firmware-hacking/import-iot-setup/writeup.md) |
| **Hardware Hacking** | Dump de Firmware | Varredura de assinaturas e extração de rootfs | `binwalk`, `unsquashfs`, `dd` | `[Concluído]` | [`hardware-hacking-extracao/`](iot-firmware-hacking/hardware-hacking-extracao/writeup.md) |
| **Goat Init** | `/etc/rc.local` e `init.d` | Análise estática de rotinas e scripts de boot | `grep`, `cat`, editores Linux | `[Concluído]` | [`goat-init/`](iot-firmware-hacking/iotgoat-challenges/goat-init/writeup.md) |
| **Goat MD5** | Criptografia Estática | Reversão de hash via ataque de dicionário | `md5sum`, John the Ripper, RockYou | `[Concluído]` | [`goat-md5/`](iot-firmware-hacking/iotgoat-challenges/goat-md5/writeup.md) |
| **Goat Backdoor** | Binários e Daemons | Identificação de listeners e shells ocultas | `strings`, `netstat`, `nmap`, `grep` | `[Concluído]` | [`goat-backdoor/`](iot-firmware-hacking/iotgoat-challenges/goat-backdoor/writeup.md) |
| **Goat Kernel** | Módulos `.ko` | Inspeção de drivers e análise de privilégios | `modinfo`, `find`, `strings` | `[Concluído]` | [`goat-kernel/`](iot-firmware-hacking/iotgoat-challenges/goat-kernel/writeup.md) |
| **E-mail Suspeito** | RFC 822 / Cabeçalhos | Rastreamento SMTP e validação SPF/DKIM | Editores RFC, `grep`, CyberChef | `[Concluído]` | [`email-suspeito/`](forensics-artifacts/email-suspeito/writeup.md) |
| **Documento Perdido** | Estrutura de Arquivo | File carving e extração de metadados ocultos | `exiftool`, `pdfid`, `pdf-parser` | `[Concluído]` | [`documento-perdido/`](forensics-artifacts/documento-perdido/writeup.md) |

---

## 📁 Estrutura do Repositório
```text
.
├── iot-firmware-hacking/
│   ├── import-iot-setup/
│   │   └── writeup.md
│   ├── hardware-hacking-extracao/
│   │   └── writeup.md
│   └── iotgoat-challenges/
│       ├── goat-init/writeup.md
│       ├── goat-md5/writeup.md
│       ├── goat-backdoor/writeup.md
│       └── goat-kernel/writeup.md
├── forensics-artifacts/
│   ├── email-suspeito/
│   │   └── writeup.md
│   └── documento-perdido/
│       └── writeup.md
├── scripts/
│   ├── hash_verifier.py
│   └── extract_firmware.sh
└── README.md
```
👤 Autor
Pedro Henrique Ferrante Prado — Defesa Cibernética, FIAP
