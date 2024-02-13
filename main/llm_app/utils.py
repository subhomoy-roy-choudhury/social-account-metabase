import tiktoken
from django.conf import settings
import openai
from langchain.llms import GooglePalm
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks import StdOutCallbackHandler
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from langchain.chains.summarize import load_summarize_chain

from llm_app.prompt_templates import SUMMERIZATION_PROMPT_TEMPLATE

# Callbacks support token-wise streaming
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])


# Palm LLM
def get_llm(type: str = "google-palm"):
    if type == "google-palm":
        return GooglePalm(
            temperature=float(settings.TEMPERATURE),
            max_tokens=int(settings.MAX_TOKENS),
            top_p=float(settings.TOP_P),
            callback_manager=callback_manager,
        )
    elif type == "google-gemini":
        return ChatGoogleGenerativeAI(
            model="gemini-pro",
            google_api_key=settings.GOOGLE_API_KEY
            # temperature=float(settings.TEMPERATURE),
            # max_tokens=int(settings.MAX_TOKENS),
            # top_p=float(settings.TOP_P),
            # callbacks=[StdOutCallbackHandler()],
        )
    return None


# OpenAI
openai.api_key = settings.OPENAI_API_KEY


def count_tokens(string: str, model_name: str = "gpt-3.5-turbo") -> int:
    """
    Returns the number of tokens in a text string.
    Reference Link := https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb
    """
    encoding = tiktoken.encoding_for_model(model_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def generate_summarizer(
    prompt,
    person_type,
):
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        max_tokens=int(settings.MAX_TOKENS),
        temperature=float(settings.TEMPERATURE),
        top_p=float(settings.TOP_P),
        frequency_penalty=float(settings.FREQUENCY_PENALTY),
        # request_timeout=15,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant for text summarization.",
            },
            {
                "role": "user",
                "content": f"Summarize this for a {person_type} within 20 words: {prompt}",
            },
        ],
    )
    return res["choices"][0]["message"]["content"]


def run_summerise_text(context, prompt_template=SUMMERIZATION_PROMPT_TEMPLATE):
    prompt = PromptTemplate.from_template(prompt_template)

    # Split text
    text_splitter = CharacterTextSplitter()
    texts = text_splitter.split_text(context)

    # Create multiple documents
    docs = [Document(page_content=t) for t in texts]

    # Text summarization
    # llm = get_llm("google-gemini")
    llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=settings.GOOGLE_API_KEY)
    chain = LLMChain(llm=llm, prompt=prompt, verbose=True)
    return chain.run(text=docs)
    # chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)

    # return chain.run(docs)
