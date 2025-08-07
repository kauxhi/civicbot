def format_response(text, mode="concise"):
    if mode == "concise":
        return text[:1000] + "..." if len(text) > 1000 else text
    else:
        return text
