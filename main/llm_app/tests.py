from django.test import SimpleTestCase
from llm_app.utils import get_llm


# Create your tests here.
class LLMUtilityTests(SimpleTestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

    def test_palm_llm(self):
        palm_llm = get_llm("google-palm")
        result = palm_llm.invoke("Write a ballad about LangChain")
        assert isinstance(result, str)

    def test_gemini_llm(self):
        gemini_llm = get_llm("google-gemini")
        result = gemini_llm.invoke("Write a ballad about LangChain")
        assert isinstance(result.content, str)
