def test_safe_url_is_low_risk(client):
    r = client.post("/api/url/scan", json={"url": "https://www.wikipedia.org"})
    assert r.status_code == 200
    data = r.json()
    assert data["verdict"] in ("Likely Safe", "Low Risk")


def test_phishing_shaped_url_is_high_risk(client):
    r = client.post("/api/url/scan", json={
        "url": "http://paypal-secure-login.verify-account.tk/@evil.com/login"
    })
    assert r.status_code == 200
    data = r.json()
    assert data["verdict"] in ("Medium Risk", "High Risk")
    assert data["risk_score"] > 40
    assert len(data["flags"]) > 1


def test_ip_based_url_flagged(client):
    r = client.post("/api/url/scan", json={"url": "http://192.168.1.50/login"})
    assert r.status_code == 200
    data = r.json()
    assert any("IP address" in f for f in data["flags"])


def test_empty_url_rejected(client):
    r = client.post("/api/url/scan", json={"url": "   "})
    assert r.status_code == 400
