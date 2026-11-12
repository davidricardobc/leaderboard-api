from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app
from app.store import STORE

client = TestClient(app)


def setup_function() -> None:
    STORE.reset()


def test_health() -> None:
    assert client.get("/health").json() == {"ok": True}


def test_add_score_accumulates() -> None:
    client.post("/scores", json={"name": "ana", "points": 10})
    r = client.post("/scores", json={"name": "ana", "points": 5})
    assert r.json() == {"name": "ana", "total": 15}


def test_leaderboard_sorted() -> None:
    client.post("/scores", json={"name": "ana", "points": 10})
    client.post("/scores", json={"name": "leo", "points": 30})
    top = client.get("/leaderboard").json()
    assert top[0] == {"name": "leo", "points": 30}


def test_reading_a_total_does_not_add_a_player() -> None:
    assert STORE.total("ghost") == 0
    assert client.get("/leaderboard").json() == []


def test_rejects_bad_input() -> None:
    assert client.post("/scores", json={"name": "", "points": 10}).status_code == 422
    assert client.get("/leaderboard?limit=0").status_code == 422


def test_audit_starts_at_zero() -> None:
    r = client.get("/audit")
    assert r.status_code == 200
    assert r.json() == {"accepted": 0}


def test_audit_counts_accepted_posts() -> None:
    client.post("/scores", json={"name": "ana", "points": 10})
    client.post("/scores", json={"name": "leo", "points": 5})
    assert client.get("/audit").json() == {"accepted": 2}


def test_audit_ignores_rejected_posts() -> None:
    r = client.post("/scores", json={"name": "ana", "points": 1001})
    assert r.status_code == 422
    assert client.get("/audit").json() == {"accepted": 0}


def test_audit_leaks_no_body_content() -> None:
    client.post("/scores", json={"name": "zelda", "points": 777})
    r = client.get("/audit")
    assert list(r.json()) == ["accepted"]
    assert "zelda" not in r.text
    assert "777" not in r.text


def test_post_writes_no_log_file() -> None:
    client.post("/scores", json={"name": "ana", "points": 10})
    assert not Path("logs").exists()
