def test_dashboard(client):
    assert client.get("/").status_code==200
def test_metrics_api(client):
    r=client.get("/api/metrics")
    assert r.status_code==200 and isinstance(r.get_json(),list)
