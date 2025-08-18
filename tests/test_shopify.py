from support_assistant.integrations.shopify import connect_to_shopify


def test_connect_to_shopify():
    result = connect_to_shopify("key", "password")
    assert result["status"] == "connected"
