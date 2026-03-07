class MockClient:
    def generate(self, **kwargs):
        return '{"key": "value"}'
def test_llm_json_parsing():
    from models.llm_wrapper import LLMWrapper
    wrapper = LLMWrapper(MockClient(), "test", 0.2)
    result = wrapper.generate("test", expect_json=True)
    assert result["key"] == "value"