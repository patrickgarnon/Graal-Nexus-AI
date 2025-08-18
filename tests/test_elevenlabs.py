from support_assistant.integrations.elevenlabs import connect_to_elevenlabs


def test_connect_to_elevenlabs():
    result = connect_to_elevenlabs("key")
    assert result["status"] == "connected"
