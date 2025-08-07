def format_prompt(user_query, response_mode):
    if response_mode == "Concise":
        mode_instruction = "Answer briefly and provide only key points."
    elif response_mode == "Detailed":
        mode_instruction = "Give a thorough and detailed explanation, including examples if applicable."
    else:
        mode_instruction = "Be helpful."

    return f"""{mode_instruction}

User question: {user_query}
"""