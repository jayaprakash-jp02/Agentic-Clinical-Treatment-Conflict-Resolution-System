import ollama

response = ollama.chat(
    model="qwen2.5:7b",
    messages=[
        {
            "role": "user",
            "content": "Say hello."
        }
    ]
)

print(response["message"]["content"])