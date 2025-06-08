import settings
from langchain_core.language_models.chat_models import BaseChatModel
from common.types import LLMConfigType

class LLMConfig:
    provider: str = "azure"
    DEFAULT_OPENAI_MODEL: str = "gpt-4o"
    DEFAULT_TEMPERATURE: float = 0

    def __init__(self, llm_config: LLMConfigType):
        self.OPENAI_API_KEY = settings.OPENAI_API_KEY
        self.config = llm_config

    def get_llm(self) -> BaseChatModel:
        """
        Returns the LLM based on the provider.
        """
        if self.config.get("provider", self.provider) == "openai":
            return self.get_openai_llm(self.config)
        # TODO: Add other providers logic here

    def get_openai_llm(self, llm_config: LLMConfigType) -> BaseChatModel:
        llm_config = self.sanatize_openai_config(llm_config)

        params = {
            "openai_api_key": self.OPENAI_API_KEY
        }
        
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(**params, **llm_config)
    
    def sanatize_openai_config(self, llm_config: LLMConfigType) -> dict:

        model_name = llm_config.get("model_name", self.DEFAULT_OPENAI_MODEL)

        if model_name.startswith("o"):
            llm_config["temperature"] = 1
            llm_config["disabled_params"] = {"parallel_tool_calls": None}

            # check if have reasoning_effort, if not set low
            if not llm_config.get("reasoning_effort"):
                llm_config["reasoning_effort"] = "low"

        llm_config.pop("provider", None)

        return llm_config
