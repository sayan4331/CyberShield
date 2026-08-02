def test_plain_text_file_is_clean(client):
    r = client.post("/api/malware/scan", files={"file": ("notes.txt", b"hello world", "text/plain")})
    assert r.status_code == 200
    data = r.json()
    assert data["verdict"] == "Clean"
    assert len(data["sha256"]) == 64


def test_exe_extension_flagged_suspicious_or_worse(client):
    r = client.post("/api/malware/scan", files={
        "file": ("evil.exe", b"MZ" + b"\x00" * 50, "application/octet-stream")
    })
    assert r.status_code == 200
    data = r.json()
    assert data["verdict"] in ("Suspicious", "Malicious")
    assert data["risk_score"] > 0


def test_mismatched_signature_detected(client):
    # PNG magic bytes wearing a .exe extension.
    r = client.post("/api/malware/scan", files={
        "file": ("fake.png", b"MZ" + b"\x90" * 20, "image/png")
    })
    assert r.status_code == 200
    data = r.json()
    assert any("does not match" in f for f in data["flags"])


def test_history_records_file_scan(client):
    client.post("/api/malware/scan", files={"file": ("sample.txt", b"abc", "text/plain")})
    r = client.get("/api/history", params={"scan_type": "file", "limit": 5})
    assert r.status_code == 200
    data = r.json()
    assert data["total"] >= 1
    assert data["items"][0]["scan_type"] == "file"
