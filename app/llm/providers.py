import json

from app.config.settings import get_settings
from app.llm.base import LLMClient


class RuleBasedFallbackClient(LLMClient):
    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        return json.dumps(
            {
                "summary": "Fallback response generated because no LLM provider is configured.",
                "system_prompt": system_prompt[:120],
                "recommendation": "Configure OPENAI_API_KEY, GEMINI_API_KEY, or ANTHROPIC_API_KEY.",
            }
        )


class OpenAIClient(LLMClient):
    def __init__(self, model: str) -> None:
        self.model = model

    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        from openai import AsyncOpenAI

        settings = get_settings()
        client = AsyncOpenAI(api_key=settings.openai_api_key)
        response = await client.chat.completions.create(
            model=self.model,
            temperature=0.2,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        return response.choices[0].message.content or ""


def get_llm_client() -> LLMClient:
    settings = get_settings()
    llm_config = settings.yaml_config.get("llm", {})
    provider = llm_config.get("provider", "fallback")
    model = llm_config.get("model", "gpt-4o-mini")
    if provider == "openai" and settings.openai_api_key:
        return OpenAIClient(model=model)
    return RuleBasedFallbackClient()

