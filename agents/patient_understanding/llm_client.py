import ollama

from config import OLLAMA_MODEL, TEMPERATURE


def call_model(prompt: str) -> str:
    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        format="json",
        options={
            "temperature": TEMPERATURE,
        },
    )

    return response["message"]["content"]