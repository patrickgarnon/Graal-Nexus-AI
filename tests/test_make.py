from support_assistant.integrations.make import connect_to_make


def test_connect_to_make():
    result = connect_to_make("token", "123")
    assert result["status"] == "connected"
    assert result["scenario"] == "123"
