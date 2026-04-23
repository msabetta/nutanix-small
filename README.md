# Nutanix Small Project – Infrastructure as Code (IaC)

Gestione base dell’infrastruttura Nutanix tramite **Terraform** e **Ansible**. Questo progetto consente di creare macchine virtuali, configurare reti e gestire categorie/etichette sui guest OS in modo automatizzato.

## 🔹 Prerequisiti

Assicurati di avere installato:

* **Terraform ≥ 1.9**
* **Ansible ≥ 2.14** + collection `nutanix.ncp`

  ```bash
  ansible-galaxy collection install ansible.utils:==2.6.1
  ansible-galaxy collection install -r ansible/collections/requirements.yml --no-cache
  ansible-galaxy collection install nutanix.ncp
  ```
* Accesso a **Prism Central** con permessi sufficienti per creare VM, reti e categorie.
* **Python ≥ 3.12.12**
* Configurazione del **Virtual Environment** nella cartella principale del progetto (nutanix-small/)

  ```bash
  python -m venv venv
  source venv/bin/activate
  pip install ntnx-prism-py-client
  ```

## 🔹 Struttura del progetto

```
nutanix-small/
├─ terraform/        # Definizioni VM, reti e categorie
├─ ansible/          # Playbook per categorie e configurazione guest OS
├─ scripts/          # Script Python ausiliari
├─ docs/             # Documentazione aggiuntiva
└─ README.md
```

### Terraform

* Crea VM, network e assegna categorie (se già esistenti)
* Configurazione tramite `terraform.tfvars`

### Ansible

* Crea categorie e assegna tag alle VM
* Configura guest OS (es. installazione software, impostazioni di base)

### Prism Lab

Per i test del codice sviluppato su Ansible e Terraform viene proposta l'implementazione di un sito web di test (frontend + backend) nella cartella **prism-lab**.

#### Startup

Per avviare i container **prism-backend** e **prism-frontend** lanciare il seguente comando 

```bash
   docker compose up --build
```

#### Tear Down

Per interrompere e rimuovere i container **prism-backend** e **prism-frontend** lanciare il seguente comando 

```bash
   docker compose down
```

### Nutanix Clone

Seconda pagina web sperimentale (frontend + backend) per i test in locale.

#### Backend

Per installare il backend da terminale eseguire i seguenti comandi:

```bash
cd backend
npm init -y
npm install express cors
```

Per l'esecuzione del backend eseguire il seguente comando:

```bash
node server.js
```

#### Frontend

Per installare il frontend da terminale eseguire i seguenti comandi:

```bash
cd frontend
npm install
npm install axios react-router-dom
```
Per l'esecuzione del backend eseguire il seguente comando:

```bash
npm run dev
```

#### Note addizionali

Eseguire backend e frontend in due terminali distinti.

## 🔹 Flusso consigliato

1. Copia il file di esempio e valorizza le variabili:

   ```bash
   cp terraform.tfvars.example terraform.tfvars
   ```
2. Applica Terraform:

   ```bash
   cd terraform
   terraform init
   terraform apply
   ```
3. Configura le variabili Ansible (`group_vars/all.yml` o tramite vault)
4. Crea categorie con Ansible:

   ```bash
   cd ansible
   ansible-playbook -i inventory.yml playbooks/00_create_categories.yml
   ```
5. Assegna tag alle VM:

   ```bash
   ansible-playbook -i inventory.yml playbooks/10_tag_vms.yml
   ```

## 🔹 Contributi

Contributi benvenuti!

* Apri un **issue** per bug o nuove feature
* Invia una **pull request** seguendo le linee guida del repository

## 🔹 Risorse

* [Terraform](https://www.terraform.io/) – tool per IaC
* [Ansible](https://www.ansible.com/) – tool per automazione e configurazione
* [Nutanix for Developers](https://www.nutanix.dev/) - piattaforma tecnica dedicata agli sviluppatori e ai team di infrastruttura, dove puoi trovare risorse utili su tecnologie Nutanix, come documentazione API, esempi di codice, articoli tecnici, guide, laboratori pratici e strumenti di automazione.
* [Node.js](https://nodejs.org/learn) - ambiente di esecuzione JavaScript lato server basato sul motore V8 che consente lo sviluppo backend
* [Express.js 5.x API](https://expressjs.com/it/5x/api.html) - ramework minimalista per Node.js che semplifica la gestione di server web, API e routing tramite un sistema flessibile di middleware (versione 5.x delle API)
* [Vite Dev Guide](https://vite.dev/guide/) - moderno build tool e dev server per applicazioni frontend rapide e ottimizzate 
* [React Dev Guide](https://react.dev/learn) - libreria JavaScript per la creazione di interfacce utente component-based e reattive

