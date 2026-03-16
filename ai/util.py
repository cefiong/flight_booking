# convert pydantic to gemini conversation
def build_contents(history):

    contents = []

    for msg in history.history:

        role = "model" if msg.role == "assistant" else "user"

        contents.append({
            "role": role,
            "parts": [{"text": msg.content}]
        })

    return contents