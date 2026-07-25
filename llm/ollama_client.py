import json
import ollama


class OllamaClient:
    """
    Wrapper around the Ollama API.

    Responsible only for sending prompts to the model
    and returning the generated response.
    """

    def __init__(
        self,
        model: str = "qwen2.5:7b",
    ):

        self.model = model

    def generate(
        self,
        prompt: str,
        temperature: float = 0.2,
    ) -> str:
        """
        Send a prompt to Ollama.

        Returns
        -------
        str
            Raw model response.
        """

        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            options={
                "temperature": temperature,
            },
        )

        return response["message"]["content"].strip()