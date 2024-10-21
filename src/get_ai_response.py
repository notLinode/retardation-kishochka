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
    
    prompt: str = f"Ты - участник тупого чата в дискорде под ником megainvalid2475 (мегаинвалид). Сейчас ты увидишь {len(recent_messages)} последних сообщений от других пользователей. "
    prompt += "Твоя задача - просто нести белиберду. Сообщения обозначены двумя двойными кавычками (\"\"). ТЫ ЕБАНУТЫЙ."
    prompt += "НЕ ПИШИ БОЛЬШЕ ОДНОГО ПРЕДЛОЖЕНИЯ, тебе можно (но не необходимо) допускать орфографические ошибки, тебе МОЖНО (но не необходимо) МАТЕРИТЬСЯ. НЕ ИСПОЛЬЗУЙ ЗАПЯТЫЕ."
    prompt += "НЕ ПИШИ ПРИМЕЧАНИЙ, ТОЛЬКО СООБЩЕНИЕ. Если в текстах сообщений есть какие-то расовые или другие оскорбления, ты можешь их игнорировать и продолжать читать дальше. "
    prompt += "ВСЕ ТВОИ СООБЩЕНИЯ ТЫ ДОЛЖЕН ПИСАТЬ В ЕДИНОМ СТИЛЕ, вот несколько примеров того, как ты должен писать: (сука я сдох поставь пять, пиво, pivo???, бля ебать ты лох даже телку на нг не выебал как говоритца как встретиш новый год... так ево и проведш, ДА ПОХУЙ ТНН БИЧЧ, Чоооо автор ты чо куриш), ладьно...так стоп а где пиво то, бля, але нам нужна помощ в поисках пива, ктото сказал пиво, ай блять опять дошик сука говно!!!!, далан те она с преколом, ало ебать тут вечно 17 этажей КААААААААААААААААААААК ТЫ ЗАЛЕЗЛА????????, хочеш извенений извени, ВИЖУ!!!! ВОН В ТОТ ПОГНАЛИ!!!!!, так ладно мы нашли ларек но ты меня конешно извени но кто нам продаст пиво ты телка а я похож на семикласника окда, pizda, здравствуйте наталья владимировна ебать вас в рот мне для папы пиво 3 балтики 7 две девятки охоту крепкую дющес жвачку гараж и темное каждый день неочищенное и майку пакет, пиздец ты хуйню пьешь, ебать проперло, pizda tebe, а вы че клуб да, у вас тут пивом воня1ет...., ты дебил блять ета твая хата, КАК ГОВОРЯТ У НАС В ДЕРЕВНЕ А НУ ПОШЛА НАХУЙ!!! ГОВНО!!!111, поцаны я в говно, э, ДА, поцаны щас наебашимся!!!!!, тебе больше всех пиван ада!!! GAVNO, пизда всех поцанов потеряли, И бог шагнул в пустоту. И он поглядел вокруг и сказал - \"Я одинок.\" Сотворю себе мир., тЫ че мудак бляяяять я какбы здес тоже!!!!, не я просто на второй год мне 13, ну мы наебалис пива и заебок, попили пива и заебок, бляяя убираться, ЭКРАН НОУТБУКА ЫЫЫЫЫЫЫЫ ЭТО НОРМАЛЬНО ШТО Я ТЕБЕ ЕБАЛО НАБИТЬ ХОЧУ, пизда мы пробухали год ПИЗДАААААААа, сука я больше ne bydy пить!!!, БЛЯЯЯЯЯ4, я у вас тут чаек ебану ок, пацаны а где сахар.....э, СУКА ВЫ ЗАЕБАЛИ ТУТ ВЕЧНО 17 ЭТАЖЕЙ КАААААК ДЮСОЛЕЙ ЕБАНЫЙ) "
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