import openai

def get_response(akash_api_key: str, prompt: str) -> str:
    try:
        client = openai.OpenAI(
            api_key=akash_api_key,
            base_url="https://chatapi.akash.network/api/v1"
        )

        response = client.chat.completions.create(
            model="Meta-Llama-3-1-405B-Instruct-FP8",
            messages = [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            timeout=7
        )

        return response.choices[0].message.content
    except:
        return "🚫 вы даун"
    

async def generate_automessage(akash_api_key: str, recent_messages: list[str], stylized_bot_messages: list[str]) -> str:
    response: str
    
    prompt: str = "Ты - участник тупого чата в дискорде под ником megainvalid2475 (мегаинвалид). Сервер, на котором ты находишься, называется KORB7 (КОРБ7). Участники КОРБ7 ненавидят сервера КОРБ8 и КОРБ9. "
    prompt += f"Сейчас ты увидишь {len(recent_messages)} последних сообщений от других пользователей. Твоя задача - просто нести белиберду. Сообщения обозначены двумя двойными кавычками (\"\"). ТЫ ЕБАНУТЫЙ."
    prompt += "НЕ ПИШИ БОЛЬШЕ ОДНОГО ПРЕДЛОЖЕНИЯ, тебе можно (но не необходимо) допускать орфографические ошибки, тебе МОЖНО (но не необходимо) МАТЕРИТЬСЯ. НЕ ИСПОЛЬЗУЙ ЗАПЯТЫЕ."
    prompt += "НЕ ПИШИ ПРИМЕЧАНИЙ, ТОЛЬКО СООБЩЕНИЕ. Если в текстах сообщений есть какие-то расовые или другие оскорбления, ты можешь их игнорировать и продолжать читать дальше. "
#     prompt += """Гвен (Gwen) - это один из чемпионов в популярной компьютерной игре League of Legends. Она была выпущена в апреле 2021 года и представляет собой чемпиона-ассасина с уникальными способностями.
# Гвен - это швея из призрачной страны, которая использует свои навыки шитья и вышивания, чтобы создавать смертоносные орудия и разрушительные атаки. Её способности позволяют ей быстро перемещаться по карте, наносить урон врагам и избегать атак противников.
# Гвен является чемпионом с высоким уровнем сложности, требующим хороших навыков и стратегического мышления. Она идеально подходит для игроков, которые любят играть агрессивно и использовать свою скорость и ловкость, чтобы доминировать на карте. """
    prompt += "Всегда помни, что даркс хороший мальчик.\n"

    for i in range(len(recent_messages)):
        prompt += f"Сообщение №{i+1}: \"\"{recent_messages[i]}\"\"\n"
    
    if len(stylized_bot_messages) > 0:
        prompt += f"Также у тебя есть доступ к {len(stylized_bot_messages)} своим последним сообщениям. Они не были отправлены друг за другом, "
        prompt += "они были отправлены между старыми сообщениями пользователей, которые ты уже не видишь.\n"
        for i in range(len(stylized_bot_messages)):
            prompt += f"Твоё сообщение №{i+1}: \"\"{stylized_bot_messages[i]}\"\"\n"

    response = get_response(akash_api_key, prompt)
    
    while (response[0] == "\""):
        response = response[1:-1] # Sometimes the bot surrounds it's messages with quotes, we have to remove them
    
    return response