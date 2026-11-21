def test_anomaly_api(client):
    r=client.get("/api/anomalies")
    assert r.status_code==200 and isinstance(r.get_json(),list)
