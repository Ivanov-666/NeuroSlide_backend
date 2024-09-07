# -*- coding: utf-8 -*-
import json

import requests


class YaGptInference:
    def __init__(self):
        self.chats = {}
        self.stories_lens = {}
        self.url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

    def _send_request(self, messages, token):
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
        user_message = {
            "role": "user",
            "text": f"Пользователю не подошел предложенный тобой текст: {old_message}, вот его требования для преределки текста: {message}, не забудь, что текст не долежн быть слишком длинным, а также не должен иметь лишних комментариев, чтобы легко встроиться в презентацию",
        }
        self.chats[chat_id].append(user_message)
        new_text = self._send_request(self.chats[chat_id], token)
        self.chats[chat_id].append({"role": "assistant", "text": new_text})
        return new_text
