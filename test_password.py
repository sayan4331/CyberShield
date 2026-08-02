def test_weak_password_flagged_low(client):
    r = client.post("/api/password/check", json={"password": "password"})
    assert r.status_code == 200
    data = r.json()
    assert data["strength"] in ("Very Weak", "Weak")
    assert data["checks"]["not_common"] is False


def test_strong_password_scores_high(client):
    r = client.post("/api/password/check", json={"password": "Tr0ub4dor&3-Zephyr!"})
    assert r.status_code == 200
    data = r.json()
    assert data["score"] >= 70
    assert data["checks"]["has_upper"] is True
    assert data["checks"]["has_symbol"] is True


def test_empty_password(client):
    r = client.post("/api/password/check", json={"password": ""})
    assert r.status_code == 200
    assert r.json()["strength"] == "None"
