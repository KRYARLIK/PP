from app.services.config_service import load_config


def test_load_config():
    config = load_config("parking_1")
    assert config.camera_id == "parking_1"
    assert len(config.places) > 0
