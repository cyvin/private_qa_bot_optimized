# llm/deepseek_llm.py

from langchain.llms.base import LLM
from typing import Optional, List
import requests
import os
from dotenv import load_dotenv

# 加载 .env 文件中的 API 密钥
load_dotenv()

class DeepSeekLLM(LLM):
    model: str = "deepseek-chat"
    api_key: str = os.getenv("DEEPSEEK_API_KEY")
    endpoint: str = "https://api.deepseek.com/chat/completions"

    @property
    def _llm_type(self) -> str:
        return "deepseek"

    def _call(self, prompt: str, stop: Optional[List[str]] = None, **kwargs) -> str:
        if not self.api_key:
            raise ValueError("请在 .env 文件中设置 DEEPSEEK_API_KEY")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }

        response = requests.post(self.endpoint, json=payload, headers=headers)

        if response.status_code != 200:
            raise Exception(f"DeepSeek API 调用失败: {response.status_code} - {response.text}")

        return response.json()["choices"][0]["message"]["content"]
