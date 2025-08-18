import os
import sqlite3
from typing import List, Dict

import requests

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(BASE_DIR, "videos.db")


def init_db(db_path: str = DB_PATH) -> None:
    """Create the videos table if it does not already exist."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id TEXT,
            video_url TEXT,
            created_at TEXT
        )
        """
    )
    conn.commit()
    conn.close()


def fetch_jobs(api_key: str) -> List[Dict]:
    """Retrieve jobs from the Runway API."""
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(
        "https://api.runwayml.com/v1/jobs", headers=headers, timeout=10
    )
    response.raise_for_status()
    data = response.json()
    return data.get("results", [])


def store_jobs(jobs: List[Dict], db_path: str = DB_PATH) -> None:
    """Store job data containing videos into the database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    for job in jobs:
        video_url = job.get("output", {}).get("video")
        if not video_url:
            continue
        cursor.execute(
            "INSERT INTO videos (job_id, video_url, created_at) VALUES (?, ?, ?)",
            (job.get("id"), video_url, job.get("created_at")),
        )
    conn.commit()
    conn.close()


def sync_jobs(api_key: str, db_path: str = DB_PATH) -> None:
    """Fetch jobs from Runway and store them in the local database."""
    jobs = fetch_jobs(api_key)
    store_jobs(jobs, db_path)


def get_history(db_path: str = DB_PATH) -> List[Dict]:
    """Return the stored video generations."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT job_id, video_url, created_at FROM videos ORDER BY id DESC"
    )
    rows = cursor.fetchall()
    conn.close()
    return [
        {"job_id": job_id, "video_url": video_url, "created_at": created_at}
        for job_id, video_url, created_at in rows
    ]
