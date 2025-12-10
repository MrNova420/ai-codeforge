#!/usr/bin/env python3
"""
Enhanced Agent Chat Interface with streaming and tool access
"""

import os
import sys
from typing import List, Dict, Optional, Callable
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.live import Live
from rich.spinner import Spinner
from rich.status import Status

console = Console()


class Message:
    """Represents a chat message."""
    
    def __init__(self, role: str, content: str, agent_name: str = ""):
        self.role = role
        self.content = content
        self.agent_name = agent_name


class EnhancedAgentChat:
    """Enhanced chat with streaming and tool access."""
    
    def __init__(self, agent, config, file_manager=None, code_executor=None):
        self.agent = agent
        self.config = config
        self.file_manager = file_manager
        self.code_executor = code_executor
        self.messages: List[Message] = []
        
        # Get model configuration
        self.model_name = config.get_agent_model(agent.name)
        
        # Determine provider
        if self.model_name.startswith("gpt-"):
            self.model_type = "openai"
        elif self.model_name.startswith("gemini-"):
            self.model_type = "gemini"
        elif ":" in self.model_name or self.model_name in ["llama2", "codellama", "mistral"]:
            self.model_type = "local"
        else:
            self.model_type = self.model_name
        
        # Initialize with system prompt
        system_prompt = agent.get_system_prompt()
        if file_manager or code_executor:
            system_prompt += "\n\nYou have access to:\n"
            if file_manager:
                system_prompt += "- File operations: READ_FILE:<path>, WRITE_FILE:<path>, LIST_FILES\n"
            if code_executor:
                system_prompt += "- Code execution: EXECUTE_PYTHON:<code>, EXECUTE_JS:<code>\n"
        
        self.messages.append(Message("system", system_prompt))
    
    def send_message(self, content: str, stream: bool = False, 
                    on_token: Optional[Callable] = None) -> str:
        """Send message and get response."""
        self.messages.append(Message("user", content))
        
        if stream and self.model_type == "openai":
            response = self._openai_chat_stream(content, on_token)
        elif stream and self.model_type == "local":
            response = self._local_chat_stream(content, on_token)
        else:
            if self.model_type == "openai":
                response = self._openai_chat(content)
            elif self.model_type == "gemini":
                response = self._gemini_chat(content)
            else:
                response = self._local_chat(content)
        
        self.messages.append(Message("assistant", response, self.agent.name))
        return response
    
    def _openai_chat(self, content: str) -> str:
        """Non-streaming OpenAI chat."""
        try:
            import openai
            
            api_key = self.config.get('openai_api_key')
            if not api_key or api_key == "YOUR_OPENAI_API_KEY_HERE":
                return "Error: OpenAI API key not configured."
            
            client = openai.OpenAI(api_key=api_key)
            
            api_messages = [
                {"role": msg.role, "content": msg.content}
                for msg in self.messages
            ]
            
            model = self.model_name if self.model_name.startswith("gpt-") else "gpt-4"
            
            response = client.chat.completions.create(
                model=model,
                messages=api_messages,
                temperature=0.7,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            return f"Error: {e}"
    
    def _openai_chat_stream(self, content: str, on_token: Optional[Callable] = None) -> str:
        """Streaming OpenAI chat."""
        try:
            import openai
            
            api_key = self.config.get('openai_api_key')
            if not api_key or api_key == "YOUR_OPENAI_API_KEY_HERE":
                return "Error: OpenAI API key not configured."
            
            client = openai.OpenAI(api_key=api_key)
            
            api_messages = [
                {"role": msg.role, "content": msg.content}
                for msg in self.messages
            ]
            
            model = self.model_name if self.model_name.startswith("gpt-") else "gpt-4"
            
            stream = client.chat.completions.create(
                model=model,
                messages=api_messages,
                temperature=0.7,
                max_tokens=2000,
                stream=True
            )
            
            full_response = ""
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    token = chunk.choices[0].delta.content
                    full_response += token
                    if on_token:
                        on_token(token)
            
            return full_response
        
        except Exception as e:
            return f"Error: {e}"
    
    def _gemini_chat(self, content: str) -> str:
        """Gemini chat."""
        try:
            import google.generativeai as genai
            
            api_key = self.config.get('gemini_api_key')
            if not api_key or api_key == "YOUR_GEMINI_API_KEY_HERE":
                return "Error: Gemini API key not configured."
            
            genai.configure(api_key=api_key)
            
            model_name = self.model_name if self.model_name.startswith("gemini-") else "gemini-pro"
            model = genai.GenerativeModel(model_name)
            
            context = self.messages[0].content
            conversation = "\n\n".join([
                f"{msg.role.upper()}: {msg.content}"
                for msg in self.messages[1:]
            ])
            
            prompt = f"{context}\n\n{conversation}\n\nASSISTANT:"
            response = model.generate_content(prompt)
            return response.text
        
        except Exception as e:
            return f"Error: {e}"
    
    def _local_chat(self, content: str) -> str:
        """Local model chat."""
        try:
            import requests
            
            ollama_url = self.config.get('ollama_url', 'http://localhost:11434')
            model = self.model_name
            
            context = self.messages[0].content
            conversation = "\n\n".join([
                f"{'User' if msg.role == 'user' else 'Assistant'}: {msg.content}"
                for msg in self.messages[1:]
            ])
            
            prompt = f"{context}\n\n{conversation}\n\nAssistant:"
            
            # Dynamic timeout based on prompt length and settings
            import settings
            base_timeout = settings.AGENT_TIMEOUT
            
            # Adjust timeout based on prompt complexity
            prompt_words = len(prompt.split())
            if prompt_words > 500:
                timeout = base_timeout * 1.5
            elif prompt_words > 200:
                timeout = base_timeout * 1.2
            else:
                timeout = base_timeout
            
            response = requests.post(
                f"{ollama_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_predict": settings.MAX_RESPONSE_TOKENS,
                        "temperature": settings.RESPONSE_TEMPERATURE,
                        "top_p": 0.9,
                        "repeat_penalty": 1.1
                    }
                },
                timeout=int(timeout)
            )
            
            if response.status_code == 200:
                return response.json().get('response', 'No response')
            elif response.status_code == 404:
                # Model not found - system needs reconfiguration
                return (f"⚠️ Model '{model}' not found in Ollama.\n\n"
                       f"Run: ollama pull {model}\n"
                       f"Or use ./run (it auto-detects and fixes)")
            return f"Error: Status {response.status_code}"
        
        except requests.exceptions.ConnectionError:
            return ("❌ Cannot connect to Ollama!\n\n"
                   "To use free local models:\n"
                   "1. Install Ollama: https://ollama.ai\n"
                   "2. Run: ollama serve\n"
                   f"3. Pull model: ollama pull {self.model_name}\n\n"
                   "Or configure paid models (OpenAI/Gemini) with ./setup")
        except Exception as e:
            return f"Error: {e}"
    
    def _local_chat_stream(self, content: str, on_token: Optional[Callable] = None) -> str:
        """Streaming local model chat."""
        try:
            import requests
            
            ollama_url = self.config.get('ollama_url', 'http://localhost:11434')
            model = self.model_name
            
            context = self.messages[0].content
            conversation = "\n\n".join([
                f"{'User' if msg.role == 'user' else 'Assistant'}: {msg.content}"
                for msg in self.messages[1:]
            ])
            
            prompt = f"{context}\n\n{conversation}\n\nAssistant:"
            
            response = requests.post(
                f"{ollama_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": True
                },
                stream=True,
                timeout=60
            )
            
            full_response = ""
            for line in response.iter_lines():
                if line:
                    import json
                    data = json.loads(line)
                    if 'response' in data:
                        token = data['response']
                        full_response += token
                        if on_token:
                            on_token(token)
            
            return full_response
        
        except Exception as e:
            return f"Error: {e}"
    
    def execute_tool_calls(self, response: str) -> str:
        """Execute any tool calls in the response."""
        if not (self.file_manager or self.code_executor):
            return response
        
        augmented_response = response
        
        # Handle file operations
        if self.file_manager:
            if 'READ_FILE:' in response:
                for line in response.split('\n'):
                    if 'READ_FILE:' in line:
                        file_path = line.split('READ_FILE:')[1].strip()
                        content = self.file_manager.read_file(file_path)
                        if content:
                            augmented_response += f"\n\n[File: {file_path}]\n{content}\n"
            
            if 'LIST_FILES' in response:
                files = self.file_manager.list_files()
                augmented_response += f"\n\nFiles: {', '.join(files[:20])}"
        
        # Handle code execution
        if self.code_executor:
            if 'EXECUTE_PYTHON:' in response:
                import re
                match = re.search(r'EXECUTE_PYTHON:\s*```python\n(.*?)```', response, re.DOTALL)
                if match:
                    code = match.group(1)
                    result = self.code_executor.execute_python(code)
                    augmented_response += f"\n\n[Execution Result]\nOutput: {result.output}\n"
        
        return augmented_response
