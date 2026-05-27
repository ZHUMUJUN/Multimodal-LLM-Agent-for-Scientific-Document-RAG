import config


class ProviderFactory:

    @staticmethod
    def create_chat_model(model_name: str | None = None):
        provider = config.LLM_PROVIDER
        selected_model = model_name or config.LLM_MODEL

        if provider == "ollama":
            from langchain_ollama import ChatOllama

            kwargs = {
                "model": selected_model,
                "temperature": config.LLM_TEMPERATURE,
            }
            if config.OLLAMA_BASE_URL:
                kwargs["base_url"] = config.OLLAMA_BASE_URL
            return ChatOllama(**kwargs)

        if provider in {"openai", "local-vllm", "vllm"}:
            try:
                from langchain_openai import ChatOpenAI
            except ImportError as exc:
                raise RuntimeError(
                    f"LLM_PROVIDER={provider} requires 'langchain-openai'. Install it before starting the app."
                ) from exc

            kwargs = {
                "model": selected_model,
                "temperature": config.LLM_TEMPERATURE,
            }
            if provider in {"local-vllm", "vllm"}:
                kwargs["api_key"] = config.LOCAL_VLLM_API_KEY
                kwargs["base_url"] = config.LOCAL_VLLM_BASE_URL
            elif config.OPENAI_API_KEY:
                kwargs["api_key"] = config.OPENAI_API_KEY
            if provider == "openai" and config.OPENAI_BASE_URL:
                kwargs["base_url"] = config.OPENAI_BASE_URL
            return ChatOpenAI(**kwargs)

        if provider == "google":
            try:
                from langchain_google_genai import ChatGoogleGenerativeAI
            except ImportError as exc:
                raise RuntimeError(
                    "LLM_PROVIDER=google requires 'langchain-google-genai'. Install it before starting the app."
                ) from exc

            kwargs = {
                "model": selected_model,
                "temperature": config.LLM_TEMPERATURE,
            }
            if config.GOOGLE_API_KEY:
                kwargs["google_api_key"] = config.GOOGLE_API_KEY
            return ChatGoogleGenerativeAI(**kwargs)

        raise ValueError(f"Unsupported LLM_PROVIDER: {provider}")
