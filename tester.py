import requests
import random
import csv
from pathlib import Path

# ----------------------------------------------------------
# CONFIGURAZIONE
# ----------------------------------------------------------
BASE_URL = "http://localhost/api"
API_KEY = "secret"  # Deve corrispondere alla chiave nel backend

NUM_USERS = 10
SESSIONS_PER_USER = 30  # numero medio di sessioni per ogni utente

EXERCISES = [
    "shoulder_abduction",
    "knee_flexion",
    "ankle_dorsiflexion",
    "hip_extension",
    "elbow_flexion",
    "wrist_extension",
    "finger_flexion",
    "balance_standing",
    "step_up",
    "seated_marching"
]

# Directory per i CSV
OUTPUT_DIR = Path("test_output")
OUTPUT_DIR.mkdir(exist_ok=True)


# ----------------------------------------------------------
# FUNZIONE PER GENERARE UNA SESSIONE CASUALE
# ----------------------------------------------------------
def genera_sessione(user_id: str) -> dict:
    return {
        "user_id": user_id,
        "exercise_type": random.choice(EXERCISES),
        "duration_seconds": random.randint(20, 300),
        "repetitions": random.randint(5, 20),
        "quality_score": round(random.uniform(10.0, 100.0), 1)
    }


# ----------------------------------------------------------
# LISTA UTENTI
# ----------------------------------------------------------
users = [f"user_{i+1}" for i in range(NUM_USERS)]


# ----------------------------------------------------------
# INVIO SESSIONI AL BACKEND
# ----------------------------------------------------------
print("\n=== INVIO SESSIONI DI PROVA AL BACKEND ===")

for user_id in users:
    for _ in range(SESSIONS_PER_USER):

        sessione = genera_sessione(user_id)

        response = requests.post(
            f"{BASE_URL}/sessions",
            json=sessione,
            headers={"x-key": API_KEY}
        )

        if response.status_code == 201:
            print(f"[OK] Sessione creata per {user_id} ({sessione['exercise_type']})")
        else:
            print(f"[ERRORE] {user_id}: {response.status_code} - {response.text}")


# ----------------------------------------------------------
# RECUPERO SESSIONI + STATS PER OGNI UTENTE
# ----------------------------------------------------------
csv_sessions_path = OUTPUT_DIR / "tutte_le_sessioni.csv"
csv_stats_path = OUTPUT_DIR / "statistiche_utenti.csv"

print("\n=== ESPORTAZIONE CSV ===")

# ----- CSV con tutte le sessioni -----
with csv_sessions_path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "user_id", "exercise_type", "duration_seconds",
        "repetitions", "quality_score", "created_at"
    ])

    for user_id in users:
        response = requests.get(
            f"{BASE_URL}/sessions",
            headers={"x-key": API_KEY},
            params={"user_id": user_id}
        )

        if response.status_code == 200:
            sessions = response.json()
            print(f"[OK] Recuperate {len(sessions)} sessioni per {user_id}")

            for s in sessions:
                writer.writerow([
                    s["user_id"],
                    s["exercise_type"],
                    s["duration_seconds"],
                    s["repetitions"],
                    s["quality_score"],
                    s.get("created_at", "")
                ])
        else:
            print(f"[ERRORE] impossibile recuperare sessioni per {user_id}: {response.text}")

print(f"[SALVATO] CSV sessioni → {csv_sessions_path}")


# ----- CSV con le statistiche utente -----
with csv_stats_path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "user_id", "total_sessions", "avg_duration_seconds", "avg_quality_score"
    ])

    for user_id in users:
        response = requests.get(
            f"{BASE_URL}/users/{user_id}/stats",
            headers={"x-key": API_KEY}
        )

        if response.status_code == 200:
            stats = response.json()
            print(f"[OK] Statistiche calcolate per {user_id}")

            writer.writerow([
                stats["user_id"],
                stats["total_sessions"],
                stats.get("avg_duration_seconds", 0),
                stats.get("avg_quality_score", 0)
            ])
        else:
            print(f"[ERRORE] statistiche per {user_id}: {response.text}")

print(f"[SALVATO] CSV statistiche → {csv_stats_path}")

print("\n=== COMPLETATO! ===")
