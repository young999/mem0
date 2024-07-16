from typing import Dict, List, Optional

from openai import OpenAI

from mem0.llms.base import LLMBase


class OpenAILLM(LLMBase):
    def __init__(self, model="gpt-4o"):
        self.client = OpenAI()
        self.model = model

    def generate_response(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict]] = None,
        tool_choice: str = "auto",
    ):
        """
        Generate a response based on the given messages using OpenAI.

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
