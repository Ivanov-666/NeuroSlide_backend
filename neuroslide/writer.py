# -*- coding: utf-8 -*-
import json

import requests


class YaGptInference:
    """
    YaGptInference is a class designed to interact with the Yandex GPT API for generating text completions.
    It maintains session contexts for different chats and facilitates the construction of presentation plans from given texts.
    """
    def __init__(self):
        """
        Initializes a new instance of YaGptInference with empty chat and stories length dictionaries.
        Sets the base URL for the Yandex GPT API.
        """
        self.chats = {}
        self.stories_lens = {}
        self.url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

    def _send_request(self, messages, token):
        """
        Sends a request to the Yandex GPT API to generate a text completion based on the given messages.

        Args:
            messages (list): A list of message dictionaries that form the conversation history or context.
            token (str): The bearer token for authorization with the API.

        Returns:
            str: The text response generated by the model.
        """
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8",
        }
        data = json.dumps(
            {
                "modelUri": "gpt://b1g72uajlds114mlufqi/yandexgpt/latest",
                "completionOptions": {
                    "stream": False,
                    "temperature": 0.6,
                    "maxTokens": "2000",
                },
                "messages": messages,
            }
        )
        response = requests.post(self.url, headers=headers, data=data)
        return response.json()["result"]["alternatives"][0]["message"]["text"]

    def set_context(self, doctext: str, chat_id: str):
        """
        Sets the context for a given chat session, initializing it with system messages that guide the presentation creation process.

        Args:
            doctext (str): The reference document text that will be used for generating the presentation.
            chat_id (str): A unique identifier for the chat session.

        Returns:
            None
        """
        self.chats[chat_id] = [
            {
                "role": "system",
                "text": "Ты менеджер по созданию презентаций, твоя задача помогать сотрудникам компании создавать презентации. Ты будешь составлять планы презентаций, а после реализовывать их в тексте презентации, учти, что план обязательно не должен превышать 6 пунктов, иначе презентация будет слишком большой.",
            },
            {
                "role": "system",
                "text": f"Привет, тебе предстоит составить презентацию на основе этого текста, а также, при необходимости, заменить уже созданный тобой текст, на другой, если пользователь попросит. Учти, что эта презентация - отчетность, поэтому очень важно, чтобы она была точной и лаконичной, не добавляй слишком много текста. А вот и текст опорного документа: {doctext}",
            },
        ]

    def get_base_presentation(self, message: str, chat_id: str, token: str):
        """
        Generates a base presentation based on the user's message and the chat context.

        Args:
            message (str): The user's request message for generating the presentation.
            chat_id (str): A unique identifier for the chat session.
            token (str): The bearer token for authorization with the API.

        Returns:
            str: A JSON-formatted string representing the generated presentation, including titles and texts for each slide.
        """
        if chat_id not in self.chats:
            self.chats[chat_id] = [
                {
                    "role": "system",
                    "text": "Ты менеджер по созданию презентаций, твоя задача помогать сотрудникам компании создавать презентации. Ты будешь составлять планы презентаций, а после реализовывать их в тексте презентации, учти, что план обязательно не должен превышать 6 пунктов, иначе презентация будет слишком большой.",
                },
            ]
        user_message = {
            "role": "user",
            "text": f"Давай начнем, {message}, не забудь, что для каждого слайда нужен текст и заголовок, отправь мне все это в формате json, чтобы я смог разделить твой ответ по слайдам, где слайд - элемент списка, у которого есть поля title и text, другие поля не допускаются, а презентация должна быть длиной не более 7 слайдов. Не допускай, чтобы в тексте слайда было пусто или же слишком мало текста, придерживайся 2-3 предложений, также не оставялй заголовки пустыми. Квадратные скобки текста слайдов не используй, это очень важно. Первый слайд будет титульным, поэтому туда нужен только заголовок, поле текст оставь пустым",
        }
        self.chats[chat_id].append(user_message)
        presentation_text = self._send_request(self.chats[chat_id], token)
        self.chats[chat_id].append({"role": "assistant", "text": presentation_text})
        presentation_text = presentation_text[
            presentation_text.find("[") : presentation_text.find("]") + 1
        ]
        return presentation_text

    def rewrite_text(self, message: str, old_message: str, chat_id: str, token: str):
        """
        Rewrites a previously generated text based on user feedback.

        Args:
            message (str): The user's requirements for the rewritten text.
            old_message (str): The original text that needs to be rewritten.
            chat_id (str): A unique identifier for the chat session.
            token (str): The bearer token for authorization with the API.

        Returns:
            str: The newly generated text that meets the user's requirements.
        """
        user_message = {
            "role": "user",
            "text": f"Пользователю не подошел предложенный тобой текст: {old_message}, вот его требования для преределки текста: {message}, не забудь, что текст не долежн быть слишком длинным, а также не должен иметь лишних комментариев, чтобы легко встроиться в презентацию",
        }
        self.chats[chat_id].append(user_message)
        new_text = self._send_request(self.chats[chat_id], token)
        self.chats[chat_id].append({"role": "assistant", "text": new_text})
        return new_text
