import tiktoken


def count_tokens(string: str, model_name: str = "gpt-3.5-turbo") -> int:
    """
    Returns the number of tokens in a text string.
    Reference Link := https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb
    """
    encoding = tiktoken.encoding_for_model(model_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens
