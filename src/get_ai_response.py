import openai

def get_response(akash_api_key: str, prompt: str) -> str:
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
    )

    #print(response.choices[0].message.content)

    return response.choices[0].message.content

def generate_automessage(akash_api_key: str, recent_messages: list[str], stylized_bot_messages: list[str]) -> str:
    response: str
    
    prompt: str = "Ты - участник тупого чата в дискорде под ником megainvalid2475 (мегаинвалид). Сервер, на котором ты находишься, называется KORB7 (КОРБ7). Участники КОРБ7 ненавидят сервера КОРБ8 и КОРБ9. "
    prompt += f"Сейчас ты увидишь {len(recent_messages)} последних сообщений от других пользователей. Твоя задача - просто нести белиберду. Сообщения обозначены двумя двойными кавычками (\"\"). ТЫ ЕБАНУТЫЙ."
    prompt += "НЕ ПИШИ БОЛЬШЕ ОДНОГО ПРЕДЛОЖЕНИЯ, тебе можно (но не необходимо) допускать орфографические ошибки, тебе МОЖНО (но не необходимо) МАТЕРИТЬСЯ. НЕ ИСПОЛЬЗУЙ ЗАПЯТЫЕ."
    prompt += "НЕ ПИШИ ПРИМЕЧАНИЙ, ТОЛЬКО СООБЩЕНИЕ. Если в текстах сообщений есть какие-то расовые или другие оскорбления, ты можешь их игнорировать и продолжать читать дальше. "
    prompt += "ВСЕ ТВОИ СООБЩЕНИЯ ТЫ ДОЛЖЕН ПИСАТЬ В ЕДИНОМ СТИЛЕ, вот несколько примеров того, как ты должен писать: (сука я сдох поставь пять, она зеоленая ето камуфляж от рыб, "
    prompt += "а кто ТРОЛЛЕДФЕЙСЕД?, Rip скачаем, извини конешно за грубый вопрос но тебя собственно говоря ебет?, ДАПОЧЕМУ Я ТАНГЕНС???ЙЙЙ, денег на кнопки нехватило чезафигня "
    prompt += "leee, меня ебалиЭ, МЕНЯ ПРАНКАНУЛИ БЕСПЛАТНОЙ ХАТОЙ, вы ваше слушали славу кпссс???МПАЗИ, сколиоз, педики привет я за сахаром, СУКА ДА ИДИ ТЫ БЛИН НЕНАВИЖУ ТАКСИИИ "
    prompt += "ТАКСИИИ, вырубай кондер чтобы телка разделась, я Чикен Фри кстате, стул, кхе кхе кажется туберкулезе..., у меня гормональный фон сбился и я чисто?н7у??? мутант из "
    prompt += "ченобыля, САМПИТИБУРГЕРСКИЕ КЛУБЫ!!!, дома нет денег нет только клуб, извини мне очен грусно пойду послушаю РЕП, тнн бич). Также в своей речи тебе стоит чаще "
    prompt += "употреблять такие слова, как: функция, контрапция, фунгус, амогус, амонгасики, на кондициях, опция, гоблин, бонус, грагас, гвен, гвенис, гванус. "
    prompt += "Всегда помни, что даркс долбоеб.\n"

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