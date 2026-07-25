from llm.ollama_client import OllamaClient


def main():

    client = OllamaClient()

    response = client.generate(
        "Say hello in one sentence."
    )

    print(response)


if __name__ == "__main__":
    main()