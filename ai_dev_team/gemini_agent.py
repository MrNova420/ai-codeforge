import os
import google.generativeai as genai

class GeminiAgent:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable not found. Please set it to your API key.")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.chat = self.model.start_chat(history=[])

    def send_message(self, message):
        """
        Sends a message to the Gemini chat and streams the response.
        """
        try:
            # The stream=True parameter is crucial for interactive chat
            response = self.chat.send_message(message, stream=True)
            for chunk in response:
                # Directly print the text part of the chunk to the console
                print(chunk.text, end="", flush=True)
            print() # Print a newline at the end of the full response
        except Exception as e:
            print(f"\n[ERROR] Failed to communicate with Gemini API: {e}")

    def get_chat_history(self):
        return self.chat.history
