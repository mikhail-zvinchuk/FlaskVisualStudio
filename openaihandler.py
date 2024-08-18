from openai import OpenAI
import logging



class OpenAIHandler:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = None

    def _initialize_client(self):
        if self.client is None:
            self.client = OpenAI(api_key=self.api_key)

    def translate_text(self, original_text: str, target_language: str) -> str:
        try:
            self._initialize_client()

            prompt = f"Translate the following 'English' text to '{target_language}': {original_text}"
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that translates text."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,  
                n=1,
                stop=None,
                temperature=0.5
            )
            return response.choices[0].message.content

        except Exception as e:
            logging.error(f"Failed to translate text: {str(e)}")
            return f"Error: {str(e)}"
