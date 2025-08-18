from support_assistant.integrations.runway import connect_to_runway


def test_connect_to_runway():
    result = connect_to_runway("key")
    assert result["status"] == "connected"
