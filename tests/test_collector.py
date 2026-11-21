from app.services.collector_service import collect_snapshot
def test_collector_values_are_percentages():
    m=collect_snapshot()
    assert 0 <= m.cpu_percent <= 100
    assert 0 <= m.memory_percent <= 100
    assert 0 <= m.disk_percent <= 100
