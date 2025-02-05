# llm_handler.py
from openai import OpenAI
from anthropic import Anthropic
import os

class LLMHandler:
    def __init__(self):
        # Initialize API clients
        self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.anthropic_client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
    
    def process_text(self, text, provider):
        """Process text through selected LLM provider"""
        if not text:
            return None
            
        try:
            if provider == 'openai':
                response = self.openai_client.chat.completions.create(
                    model="gpt-4",
                    messages=[{
                        "role": "system",
                        "content": "Analyze the following conversation snippet and provide key insights."
                    }, {
                        "role": "user",
                        "content": text
                    }]
                )
                return response.choices[0].message.content

            elif provider == 'anthropic':
                response = self.anthropic_client.messages.create(
                    model="claude-3-opus-20240229",
                    max_tokens=1024,
                    messages=[{
                        "role": "user",
                        "content": f"Analyze this conversation: {text}"
                    }]
                )
                return response.content[0].text

            elif provider == 'deepseek':
                # Implement DeepSeek API call here
                pass

        except Exception as e:
            print(f"LLM API error: {e}")
            return None