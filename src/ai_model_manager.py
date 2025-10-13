"""
AI Model Manager - Multi-Provider AI Model Management

This module manages multiple AI providers (OpenAI, Claude, Gemini, Groq, etc.)
and provides a unified interface for model selection and usage.

Features:
- Support for multiple AI providers
- Connection testing for each model
- Model selection interface
- Default model configuration
"""

import logging
import yaml
from typing import Dict, List, Optional, Any
from pathlib import Path
import openai
from anthropic import Anthropic
import requests

logger = logging.getLogger(__name__)


class AIModel:
    """Represents a single AI model configuration."""
    
    def __init__(self, name: str, provider: str, config: Dict, is_default: bool = False):
        """
        Initialize AI model.
        
        Args:
            name: Display name for the model
            provider: Provider type (openai, claude, gemini, groq, etc.)
            config: Configuration dictionary for this model
            is_default: Whether this is the default model
        """
        self.name = name
        self.provider = provider
        self.config = config
        self.is_default = is_default
        self.is_connected = False
        self.error_message = None
    
    def test_connection(self) -> bool:
        """
        Test connection to this model.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            if self.provider == "openai":
                return self._test_openai()
            elif self.provider == "openai_compatible":
                return self._test_openai_compatible()
            elif self.provider == "anthropic":
                return self._test_anthropic()
            elif self.provider == "gemini":
                return self._test_gemini()
            elif self.provider == "groq":
                return self._test_groq()
            else:
                self.error_message = f"Unknown provider: {self.provider}"
                return False
                
        except Exception as e:
            self.error_message = str(e)
            logger.error(f"Connection test failed for {self.name}: {e}")
            return False
    
    def _test_openai(self) -> bool:
        """Test OpenAI connection."""
        try:
            api_key = self.config.get('api_key', '')
            base_url = self.config.get('base_url', 'https://api.openai.com/v1')
            
            if not api_key or api_key.startswith('env:'):
                self.error_message = "API key not configured"
                return False
            
            client = openai.OpenAI(api_key=api_key, base_url=base_url)
            
            # Simple test request
            response = client.chat.completions.create(
                model=self.config.get('model', 'gpt-3.5-turbo'),
                messages=[{"role": "user", "content": "test"}],
                max_tokens=5
            )
            
            self.is_connected = True
            return True
            
        except Exception as e:
            self.error_message = str(e)
            return False
    
    def _test_openai_compatible(self) -> bool:
        """Test OpenAI-compatible API connection."""
        try:
            api_key = self.config.get('api_key', '')
            base_url = self.config.get('base_url', '')
            
            if not api_key or api_key.startswith('env:'):
                self.error_message = "API key not configured"
                return False
            
            if not base_url:
                self.error_message = "Base URL not configured"
                return False
            
            client = openai.OpenAI(api_key=api_key, base_url=base_url)
            
            # Simple test request
            response = client.chat.completions.create(
                model=self.config.get('model', 'gpt-3.5-turbo'),
                messages=[{"role": "user", "content": "test"}],
                max_tokens=5
            )
            
            self.is_connected = True
            return True
            
        except Exception as e:
            self.error_message = str(e)
            return False
    
    def _test_anthropic(self) -> bool:
        """Test Anthropic (Claude) connection."""
        try:
            api_key = self.config.get('api_key', '')
            
            if not api_key or api_key.startswith('env:'):
                self.error_message = "API key not configured"
                return False
            
            client = Anthropic(api_key=api_key)
            
            # Simple test request
            response = client.messages.create(
                model=self.config.get('model', 'claude-3-haiku-20240307'),
                max_tokens=5,
                messages=[{"role": "user", "content": "test"}]
            )
            
            self.is_connected = True
            return True
            
        except Exception as e:
            self.error_message = str(e)
            return False
    
    def _test_gemini(self) -> bool:
        """Test Google Gemini connection."""
        try:
            api_key = self.config.get('api_key', '')
            
            if not api_key or api_key.startswith('env:'):
                self.error_message = "API key not configured"
                return False
            
            # Test with simple request to Gemini API
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.config.get('model', 'gemini-pro')}:generateContent"
            
            headers = {'Content-Type': 'application/json'}
            params = {'key': api_key}
            data = {
                'contents': [{'parts': [{'text': 'test'}]}]
            }
            
            response = requests.post(url, headers=headers, params=params, json=data, timeout=10)
            
            if response.status_code == 200:
                self.is_connected = True
                return True
            else:
                self.error_message = f"HTTP {response.status_code}: {response.text[:100]}"
                return False
            
        except Exception as e:
            self.error_message = str(e)
            return False
    
    def _test_groq(self) -> bool:
        """Test Groq connection."""
        try:
            api_key = self.config.get('api_key', '')
            
            if not api_key or api_key.startswith('env:'):
                self.error_message = "API key not configured"
                return False
            
            # Groq uses OpenAI-compatible API
            client = openai.OpenAI(
                api_key=api_key,
                base_url='https://api.groq.com/openai/v1'
            )
            
            # Simple test request
            response = client.chat.completions.create(
                model=self.config.get('model', 'llama3-8b-8192'),
                messages=[{"role": "user", "content": "test"}],
                max_tokens=5
            )
            
            self.is_connected = True
            return True
            
        except Exception as e:
            self.error_message = str(e)
            return False
    
    def get_client(self):
        """
        Get API client for this model.
        
        Returns:
            Configured API client
        """
        if self.provider == "openai":
            return openai.OpenAI(
                api_key=self.config.get('api_key', ''),
                base_url=self.config.get('base_url', 'https://api.openai.com/v1')
            )
        elif self.provider == "openai_compatible":
            return openai.OpenAI(
                api_key=self.config.get('api_key', ''),
                base_url=self.config.get('base_url', '')
            )
        elif self.provider == "anthropic":
            return Anthropic(api_key=self.config.get('api_key', ''))
        elif self.provider == "groq":
            return openai.OpenAI(
                api_key=self.config.get('api_key', ''),
                base_url='https://api.groq.com/openai/v1'
            )
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")


class AIModelManager:
    """Manages multiple AI models and provides selection interface."""
    
    def __init__(self, config_path: str = 'config.yaml'):
        """
        Initialize AI Model Manager.
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path
        self.models: Dict[str, AIModel] = {}
        self.default_model: Optional[AIModel] = None
        
        self._load_models()
    
    def _load_models(self):
        """Load models from configuration file."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            models_config = config.get('ai_models', {})
            default_model_name = models_config.get('default', None)
            
            # Load each model
            for model_name, model_config in models_config.items():
                if model_name == 'default':
                    continue
                
                provider = model_config.get('provider', '')
                is_default = (model_name == default_model_name)
                
                model = AIModel(
                    name=model_name,
                    provider=provider,
                    config=model_config,
                    is_default=is_default
                )
                
                self.models[model_name] = model
                
                if is_default:
                    self.default_model = model
            
            logger.info(f"✅ Loaded {len(self.models)} AI model(s)")
            if self.default_model:
                logger.info(f"   Default model: {self.default_model.name}")
        
        except Exception as e:
            logger.error(f"Failed to load models: {e}")
            raise
    
    def test_all_connections(self) -> Dict[str, bool]:
        """
        Test connections to all configured models.
        
        Returns:
            Dictionary mapping model names to connection status
        """
        results = {}
        
        print("\n🔌 Testing AI model connections...")
        print("-" * 70)
        
        for name, model in self.models.items():
            print(f"   Testing {name} ({model.provider})... ", end='', flush=True)
            
            is_connected = model.test_connection()
            results[name] = is_connected
            
            if is_connected:
                print("✅ Connected")
                if model.is_default:
                    print(f"      (Default model)")
            else:
                print(f"❌ Failed: {model.error_message}")
        
        print("-" * 70)
        
        connected_count = sum(1 for v in results.values() if v)
        print(f"\n✅ {connected_count}/{len(self.models)} model(s) connected successfully\n")
        
        return results
    
    def get_connected_models(self) -> List[AIModel]:
        """
        Get list of successfully connected models.
        
        Returns:
            List of connected AIModel instances
        """
        return [model for model in self.models.values() if model.is_connected]
    
    def select_model_interactive(self, purpose: str = "") -> Optional[AIModel]:
        """
        Interactive model selection with connection status.
        
        Args:
            purpose: Description of what the model will be used for
            
        Returns:
            Selected AIModel or None if cancelled
        """
        connected_models = self.get_connected_models()
        
        if not connected_models:
            print("\n❌ No connected models available!")
            return None
        
        print(f"\n{'='*70}")
        if purpose:
            print(f"🤖 Select AI Model for: {purpose}")
        else:
            print(f"🤖 Select AI Model")
        print(f"{'='*70}\n")
        
        # Show options
        for idx, model in enumerate(connected_models, 1):
            default_marker = " [DEFAULT]" if model.is_default else ""
            print(f"  [{idx}] {model.name} ({model.provider}){default_marker}")
        
        if self.default_model and self.default_model.is_connected:
            print(f"\n  [0] Use default model ({self.default_model.name})")
        
        print(f"\n{'-'*70}")
        
        # Get selection
        while True:
            try:
                choice = input("\nYour selection: ").strip()
                
                if choice == '0' and self.default_model and self.default_model.is_connected:
                    print(f"✅ Using default model: {self.default_model.name}")
                    return self.default_model
                
                idx = int(choice)
                if 1 <= idx <= len(connected_models):
                    selected = connected_models[idx - 1]
                    print(f"✅ Selected: {selected.name}")
                    return selected
                else:
                    print(f"❌ Invalid selection. Please enter 1-{len(connected_models)}")
            
            except ValueError:
                print(f"❌ Invalid input. Please enter a number.")
            except KeyboardInterrupt:
                print("\n❌ Selection cancelled")
                return None
    
    def get_model(self, name: str) -> Optional[AIModel]:
        """
        Get model by name.
        
        Args:
            name: Model name
            
        Returns:
            AIModel instance or None if not found
        """
        return self.models.get(name)
    
    def get_default_model(self) -> Optional[AIModel]:
        """
        Get default model.
        
        Returns:
            Default AIModel or None
        """
        return self.default_model
    
    def use_default_for_all(self) -> bool:
        """
        Ask user if they want to use default model for all operations.
        
        Returns:
            True if user wants to use default, False otherwise
        """
        if not self.default_model or not self.default_model.is_connected:
            return False
        
        print(f"\n{'='*70}")
        print(f"🤖 AI Model Selection")
        print(f"{'='*70}")
        print(f"\nDefault model: {self.default_model.name} ({self.default_model.provider})")
        print(f"\nWould you like to use the default model for all operations?")
        print(f"  [Y] Yes, use default for everything")
        print(f"  [N] No, let me choose for each operation")
        print(f"\n{'-'*70}")
        
        while True:
            choice = input("\nYour choice (Y/n): ").strip().lower()
            
            if choice in ['', 'y', 'yes']:
                print(f"✅ Will use {self.default_model.name} for all operations")
                return True
            elif choice in ['n', 'no']:
                print(f"✅ You'll be asked to select model for each operation")
                return False
            else:
                print("❌ Invalid choice. Please enter Y or N.")

