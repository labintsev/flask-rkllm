def make_prompt(messages):
    """Create a prompt from the messages."""
    prompt = ""
    for message in messages:
        if message['role'] == 'user':
            prompt += f"User: {message['content']}\n"
        elif message['role'] == 'system':
            prompt += f"System: {message['content']}\n"
        elif message['role'] == 'assistant':
            prompt += f"Assistant: {message['content']}\n"
    return prompt
