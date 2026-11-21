from app.services.prediction_service import predict_cpu
def test_prediction_baseline(client):
    with client.application.app_context():
        result=predict_cpu()
        assert 0 <= result.predicted_value <= 100
