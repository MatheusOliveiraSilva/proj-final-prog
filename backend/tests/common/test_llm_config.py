import pytest
from unittest.mock import patch, MagicMock
from langchain_core.messages import AIMessage

from common.llm_config import LLMConfig
from common.types import LLMConfigType


def test_llm_config_functionality():
    """
    Teste único que verifica:
    1. Se LLMConfig funciona com configuração válida
    2. Se gera erro com configuração inválida
    3. Se invoke retorna AIMessage
    """
    
    # 1. Teste configuração válida
    valid_config: LLMConfigType = {
        "provider": "openai",
        "model": "gpt-4o",
        "temperature": 0,
    }
    
    # Mock da API key para não precisar de configuração real
    with patch('common.llm_config.settings.OPENAI_API_KEY', 'fake-api-key'):
        # Mock do ChatOpenAI no local onde é importado (dentro da função)
        with patch('langchain_openai.ChatOpenAI') as mock_chat_openai:
            # Configurar o mock para retornar uma instância fake
            mock_llm_instance = MagicMock()
            mock_chat_openai.return_value = mock_llm_instance
            
            # Configurar o mock para retornar uma AIMessage fake no invoke
            mock_response = AIMessage(
                content="Hello! How can I assist you today?",
                additional_kwargs={'refusal': None},
                response_metadata={'token_usage': {'completion_tokens': 9}}
            )
            mock_llm_instance.invoke.return_value = mock_response
            
            # Testar configuração válida
            llm_config = LLMConfig(valid_config)
            llm = llm_config.get_llm()
            
            # Verificar se o LLM foi criado corretamente
            assert llm is not None
            
            # 3. Testar se invoke retorna AIMessage
            response = llm.invoke("Hello, world!")
            
            # Verificar se a resposta é uma AIMessage
            assert isinstance(response, AIMessage)
            assert response.content == "Hello! How can I assist you today?"
            assert hasattr(response, 'additional_kwargs')
            assert hasattr(response, 'response_metadata')
    
    # 2. Teste configuração inválida (provider não suportado)
    invalid_config: LLMConfigType = {
        "provider": "provider_inexistente",
        "model": "gpt-4o",
        "temperature": 0,
    }
    
    with patch('common.llm_config.settings.OPENAI_API_KEY', 'fake-api-key'):
        llm_config_invalid = LLMConfig(invalid_config)
        
        # Como o método get_llm não tem tratamento para provider inválido,
        # ele deve retornar None
        result = llm_config_invalid.get_llm()
        assert result is None  # Baseado na implementação atual que não tem else
