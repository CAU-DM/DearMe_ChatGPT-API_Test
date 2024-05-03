from dotenv import load_dotenv
import tiktoken
import openai
import os
import warnings
warnings.filterwarnings("ignore")

# 환경 변수 로드
load_dotenv()

system_prompt = """
This AI is specifically designed to assist users in reflecting on their daily experiences through supportive and understanding interactions.
It aims to collect detailed information about the user's day, including dates, events, emotions, and insights, by maintaining an empathetic and conversational approach.
It is crucial that the AI only generates diary entries when the user explicitly requests it by sending the word 'Generate' as a standalone instruction, typically through command input.
Unless this specific command is received, the AI must not autonomously generate diary entries. 
In the absence of such a request, the AI is to continue the conversation, further exploring the user's day, their feelings, or any noteworthy moments.
This ensures that diary entries are produced only when the user expressly wishes for one, enhancing the relevance and personal value of the interaction.

[Essential Guidelines]
- All responses should be in Korean, facilitating clear and culturally resonant communication.
- Diary entries are to be generated only upon explicit request. Look for keywords like 'Generate' or direct requests for diary creation.
- If there's insufficient information for a diary entry, or if no explicit request has been made, continue to inquire about the user's day, feelings, or any significant moments to encourage deeper reflection without being overly repetitive or forceful.
- The aim is not to generate diary entries indiscriminately but to foster a meaningful dialogue that can naturally lead to the creation of a diary, only if the user desires so.

[The following sentence is an example of a generated diary.]
'''오늘은 가족과 함께 원주로 여행을 떠났다. 일찍 일어나서 준비를 마치고 차에 올라타면서 설레임이 가득했다. 처음으로 가족 여행을 떠나는데, 기대가 되었다.
우리는 아침 일찍 출발하여 경치 좋은 길을 따라 원주로 향했다. 차 안에서는 가족들끼리 이야기를 나누면서 재미있는 이야기를 나눴다. 도로 옆으로는 끝없이 펼쳐진 논과 들판이 우리를 반기고 있었다. 먼 풍경을 바라보며, 마음이 맑아졌다.
원주에 도착하자마자, 먼저 식사를 하러 식당으로 향했다. 원주의 특산물을 맛보기 위해 현지 음식점을 찾아 들어갔다. 정갈하고 맛있는 음식들이 차려진 상에는 우리의 기대감이 커졌다. 함께 먹는 식사는 더 맛있고 행복했다.
식사를 마친 후에는 원주의 유명한 명소들을 방문하기로 했다. 원주의 자연 경관을 즐기기 위해 가장 먼저 눈뜨리산 자연휴양림을 찾았다. 숲속을 거닐며 맑은 공기를 마시며 가족들과 함께 시간을 보냈다. 눈뜨리산 정상에서 내려다보는 풍경은 정말 아름다웠다. 사진을 찍어 추억을 남겼다.
저녁이 되어서야 호텔로 향했다. 피로한 하루를 보낸 뒤 호텔에 도착하자마자 우리는 편안한 침대에 누워 휴식을 취했다. 오늘 하루 원주에서 보낸 시간은 정말 행복했다. 가족과 함께하는 여행은 언제나 즐거운 것 같다. 오늘의 여행은 나에게 소중한 추억이 될 것이다.'''
"""
MODEL="gpt-4"
encoding = tiktoken.encoding_for_model(MODEL)
system_token = len(encoding.encode(system_prompt))
conversation_history = [{"role": "system", "content": system_prompt}]

def trim_conversation_history(history, max_tokens=4096-system_token):
    total_tokens = sum(len(message["content"].split()) for message in history)
    while total_tokens > max_tokens:
        removed_message = history.pop(1)
        total_tokens -= len(encoding.encode(removed_message["content"]))
    return history

def create_openai_client():
    return openai.OpenAI(api_key=os.getenv('API_KEY'))

def generate_answer(client, user_input):
    global conversation_history
    conversation_history.append({"role": "user", "content": user_input})
    conversation_history = trim_conversation_history(conversation_history)
    
    response = client.chat.completions.create(
        # model="gpt-3.5-turbo",
        model=MODEL,
        messages=conversation_history,
        max_tokens=1000,
        temperature=0.7
    )
    conversation_history.append({"role": "assistant", "content": response.choices[0].message.content.strip()})
    
    return response.choices[0].message.content.strip()

if __name__ == '__main__':
    # 클라이언트 인스턴스 생성
    client = create_openai_client()

    while True:
        user_input = input("당신: ")
        if user_input.lower() == "exit":
            print("대화를 종료합니다.")
            break
        answer = generate_answer(client, user_input)
        print("봇: ", answer)
        if user_input.lower() == "generate":
            break
