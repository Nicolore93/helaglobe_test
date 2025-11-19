# **Nicola Lorenzini – HELAGLOBE Architecture & Deployment Guide**

Questo repository contiene un esempio di architettura completa basata su **Docker**, composta da:

* **Backend FastAPI** (microservizio HTTP per gestione sessioni riabilitative)
* **PostgreSQL** (database relazionale)
* **pgAdmin** (interfaccia grafica per l’amministrazione del DB)
* **Nginx** (reverse proxy / static server)
* **Tester Python** per generare sessioni simulate

La struttura è progettata per essere semplice, modulare e facilmente estendibile.

---

## 📁 **Struttura del progetto**

```
HELAGLOBE/
├── docker-compose.yml
├── src/
│   ├── nginx/
│   ├── pgadmin/
│   └── simple_backend/
├── tester.py
└── tslog/
```

### **Componenti principali**

* **src/simple_backend/** → codice FastAPI + ORM SQLAlchemy
* **src/nginx/** → configurazione Nginx
* **src/pgadmin/** → configurazione pgAdmin
* **docker-compose.yml** → file descrittivo dei container
* **tester.py** → script per generare dati simulati e testarli

---

## 🧱 **Prerequisiti**

Per eseguire il progetto è necessario installare sul sistema:

* **Docker ≥ 20.x**
* **Docker Compose ≥ 2.x**
* (Opzionale) **Python 3.10+** se si desidera eseguire `tester.py`

### Link download

* **Windows:** [https://docs.docker.com/desktop/setup/install/windows-install/](https://docs.docker.com/desktop/setup/install/windows-install/)
* **Linux (Ubuntu/Debian):** [https://docs.docker.com/engine/install/debian/](https://docs.docker.com/engine/install/debian/)
* **macOS (NON TESTATO):** [https://docs.docker.com/desktop/setup/install/mac-install/](https://docs.docker.com/desktop/setup/install/mac-install/)

Python: [https://www.python.org/downloads/](https://www.python.org/downloads/)

### Verifica installazioni

Apri un terminale ed esegui:

```bash
docker -v
docker compose version   # oppure: docker-compose version
python --version
```

---

## 🚀 **Avvio dell’ambiente**

Avviare tutti i servizi tramite Docker Compose:

Entrare nella cartella di progetto, da terminale:

```bash
docker compose up --build -d
```

### Servizi disponibili

| Servizio                     | URL                                                 |
| ---------------------------- | --------------------------------------------------- |
| **Backend FastAPI**    | [http://localhost/api/](http://localhost/api/)         |
| **Documentazione API** | [http://localhost/api/docs](http://localhost/api/docs) |
| **pgAdmin**            | [http://localhost](http://localhost:5050)/pgadmin      |

> Nota: il backend è esposto da Nginx tramite il path `/api/`.

---

## 🧪 **Testare il backend**

È possibile generare automaticamente **sessioni riabilitative simulate** con:

```bash
python tester.py
```

Lo script esegue:

* generazione di ~10 utenti
* creazione di 30–40 sessioni per ciascun utente
* invio delle sessioni via POST al backend
* verifica delle statistiche tramite `/users/{user_id}/stats`

---

## 🗂️ **Database PostgreSQL + PgAdmin**

Il database viene creato automaticamente dal container.

Credenziali predefinite  per accesso tramite PgAdmin (modificabili in `docker-compose.yml`):

```
USER: admin@helaglobe.com
PASS: HelaGlobe2025
url: http://localhost/pgadmin
```

## 🧹 **Pulizia dell’ambiente e Stop**

Arrestare i servizi:

```bash
docker compose down
docker system prune -a 
```
