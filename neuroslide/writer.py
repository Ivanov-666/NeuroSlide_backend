import requests
import json

class GigachatInference:
    def __init__(self, chat_len):
        self.conversation_histories = {}
        self.stories_lens = {}
        self.url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
        self.chat_len = chat_len

    def get_text(self, message, chat_id, token):
        if chat_id not in self.conversation_histories:
            self.conversation_histories[chat_id] = [
                {
                    "role": "system",
                    "content": "Ты писатель книжек для детей. Тебе нужно сочинить сказку во время интерактивного общения с пользователем. Помни, что пользователь - ребенок, и он общается проще, чем взрослый, поэтому твоя задача сочинить понятную для него сказку. Также отвечай одним предложением, чтобы ребенок мог продолжить твою сказку самостоятельно. Обязательно заканчивай свои слова каждый раз вопросом, чтобы ребенок мог ответить, продолжив тем самым сказку."
                }
            ]
            self.stories_lens[chat_id] = 0

        user_message = {
            "role": "user",
            "content": message
        }
        self.conversation_histories[chat_id].append(user_message)
        self.stories_lens[chat_id] += 1
        if self.stories_lens[chat_id] == self.chat_len:
            user_message = [user_message, {
                "role": "system",
                "content": "Это будет последний твой ответ, твоя задача в нём - закончить историю, сделай это так, чтобы в истории была поучительная часть"
            }]
        
        payload = json.dumps({
            "model": "GigaChat",
            "messages": self.conversation_histories[chat_id],
            "n": 1,
            "stream": False,
            "update_interval": 0
        })
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        
        response = requests.post(self.url, headers=headers, data=payload, verify=False)
        story_content = response.json()['choices'][0]['message']['content']
        self.conversation_histories[chat_id].append({
            "role": "assistant",
            "content": story_content
        })

        return story_content, self.stories_lens[chat_id] == self.chat_len
