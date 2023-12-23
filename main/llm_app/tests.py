from django.test import TestCase
from llm_app.utils import get_llm


# Create your tests here.
class LLMUtilityTests(TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

    def test_palm_llm(self, text):
        palm_llm = get_llm("google-palm")
        result = palm_llm.invoke("Write a ballad about LangChain")
        assert isinstance(result.content, str)

    def test_gemini_llm(self, text):
        gemini_llm = get_llm("google-gemini")
        result = gemini_llm.invoke("Write a ballad about LangChain")
        assert isinstance(result.content, str)
