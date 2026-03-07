from hypothesis_agent.config.settings import load_config

def test_config_loads():
    config = load_config()
    assert config.model.temperature >= 0