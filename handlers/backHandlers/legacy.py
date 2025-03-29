def handler(content_dict: dict, path: str) -> str:
    """
    Takes in dict 'content_dict' where keys are the prompts and values are the respective LLM responses.
    Generates images under 'path' if needed.
    Returns text in QTI-compatible format.
    """

    return "\n\n".join(content_dict.values())
