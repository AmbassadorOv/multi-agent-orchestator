from relay import RelayAgent, RelayError

REGISTRY = {
    "research": {"capabilities": ["web_research", "source_analysis"], "accepts": ["REQUEST"], "returns": ["RESULT"]},
    "documents": {"capabilities": ["document_generation"], "accepts": ["REQUEST"], "returns": ["RESULT"]},
}

def test_routes_by_capability_and_preserves_task_thread():
    seen = {}
    def document_handler(message):
        seen.update(message)
        return {"result_id": "RES-001", "source_message_id": message["message_id"], "verification_state": "NOT_YET_VERIFIED"}

    relay = RelayAgent(REGISTRY, {"documents": document_handler})
    msg = relay.create_request(
        task_id="TASK-001", source_agent="research-agent", source_group="research",
        capability="document_generation", payload={"title": "test"},
        context={"task": "create document", "secret": "do-not-forward"},
        context_refs=["task"],
    )
    assert msg["destination_group"] == "documents"
    assert msg["context"] == {"task": "create document"}
    assert "secret" not in msg["context"]
    result = relay.send(msg["message_id"])
    assert result["source_message_id"] == msg["message_id"]
    assert relay.tasks["TASK-001"] == "COMPLETED"
    assert relay.thread("TASK-001")[0]["message_id"] == msg["message_id"]

def test_human_approval_blocks_delivery():
    called = False
    def handler(message):
        nonlocal called
        called = True
        return {"ok": True}
    relay = RelayAgent(REGISTRY, {"documents": handler})
    msg = relay.create_request(
        task_id="TASK-002", source_agent="research-agent", source_group="research",
        capability="document_generation", payload={"publish": True},
        requires_human_approval=True,
    )
    try:
        relay.send(msg["message_id"])
        assert False, "expected RelayError"
    except RelayError:
        pass
    assert called is False
    assert relay.tasks["TASK-002"] == "WAITING"
