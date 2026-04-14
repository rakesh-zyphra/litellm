"""
Translate from OpenAI's `/v1/chat/completions` to Zyphra's `/v1/chat/completions`
"""

from typing import Any, AsyncIterator, Iterator, Optional, Tuple, Union

from litellm.llms.openai.chat.gpt_transformation import (
    OpenAIChatCompletionStreamingHandler,
    OpenAIGPTConfig,
)
from litellm.secret_managers.main import get_secret_str
from litellm.types.utils import ModelResponse, ModelResponseStream


class ZyphraChatConfig(OpenAIGPTConfig):
    @property
    def custom_llm_provider(self) -> Optional[str]:
        return "zyphra"

    def _get_openai_compatible_provider_info(
        self, api_base: Optional[str], api_key: Optional[str]
    ) -> Tuple[Optional[str], Optional[str]]:
        api_base = (
            api_base
            or get_secret_str("ZYPHRA_API_BASE")
            or "https://uyppidoc.zyphracloud.com/v1"
        )
        dynamic_api_key = api_key or get_secret_str("ZYPHRA_API_KEY")
        return api_base, dynamic_api_key

    def get_complete_url(
        self,
        api_base: Optional[str],
        api_key: Optional[str],
        model: str,
        optional_params: dict,
        litellm_params: dict,
        stream: Optional[bool] = None,
    ) -> str:
        if not api_base:
            api_base = "https://uyppidoc.zyphracloud.com/v1"

        if not api_base.endswith("/chat/completions"):
            api_base = f"{api_base.rstrip('/')}/chat/completions"

        return api_base

    def get_supported_openai_params(self, model: str) -> list:
        return [
            "temperature",
            "top_p",
            "max_tokens",
            "max_completion_tokens",
            "stop",
            "stream",
        ]

    def should_fake_stream(
        self,
        model: str,
        stream: Optional[bool],
        custom_llm_provider: Optional[str] = None,
    ) -> bool:
        """
        Zyphra API only supports streaming. For non-streaming requests,
        use fake_stream to internally stream and collect the full response.
        """
        if stream is False or stream is None:
            return True
        return False

    def get_model_response_iterator(
        self,
        streaming_response: Union[Iterator[str], AsyncIterator[str], ModelResponse],
        sync_stream: bool,
        json_mode: Optional[bool] = False,
    ) -> Any:
        return ZyphraChatCompletionStreamingHandler(
            streaming_response=streaming_response,
            sync_stream=sync_stream,
            json_mode=json_mode,
        )


class ZyphraChatCompletionStreamingHandler(OpenAIChatCompletionStreamingHandler):
    def chunk_parser(self, chunk: dict) -> ModelResponseStream:
        # Map Zyphra's 'reasoning' field to LiteLLM's 'reasoning_content' field
        choices = chunk.get("choices", [])
        for choice in choices:
            delta = choice.get("delta", {})
            if "reasoning" in delta:
                delta["reasoning_content"] = delta.pop("reasoning")

        return super().chunk_parser(chunk)
