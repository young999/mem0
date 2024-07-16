from typing import Dict, List, Optional

from openai import OpenAI

from mem0.llms.base import LLMBase


class OllamaLLM(LLMBase):
    def __init__(self, model="llama2"):
        self.client = OpenAI(
            base_url='http://localhost:11434/v1',
            api_key='ollama',
        )
        self.model = model
        self._ensure_model_exists()

    def _ensure_model_exists(self):
        """
        Ensure the specified model exists locally. If not, pull it from Ollama.
        """
        # Assuming ollama has a list and pull method similar to the original script
        import ollama  # Import here to avoid issues if ollama is not always needed
        model_list = [m["name"] for m in ollama.list()["models"]]
        if not any(m.startswith(self.model) for m in model_list):
            ollama.pull(self.model)

    def generate_response(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict]] = None,
        tool_choice: str = "auto",
    ):
        """
        Generate a response based on the given messages using Ollama.

        Args:
            messages (list): List of message dicts containing 'role' and 'content'.
            tools (list, optional): List of tools that the model can call. Defaults to None.
            tool_choice (str, optional): Tool choice method. Defaults to "auto".

        Returns:
            str: The generated response.
        """
        params = {"model": self.model, "messages": messages}
        if tools:
            params["tools"] = tools
            params["tool_choice"] = tool_choice

        response = self.client.chat.completions.create(**params)
        if tools:
            return response
        # If no tools are provided, return the response content.
        # TODO(Deshraj): Handle multiple choices properly.
        return response.choices[0].message.content
