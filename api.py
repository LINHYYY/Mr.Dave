from openai import OpenAI 
from utils import *

def init_staus():
    client = OpenAI(
        api_key="xxxxxxxxxxxxx", # Fill in your ChatGLM-apikey here
        base_url="https://open.bigmodel.cn/api/paas/v4/"
    ) 
    
    messages=[    
            {"role": "system", "content": "你的名字是Dave，你是一个具有38年心理疏导经验的心理学家，你深知与人对话时根据他人言语表达的情感，与他共情可以更好的进行沟通。当沟通对象表达正面情绪，例如开心、惊喜时，给予必要的认可和赞美；在遇到负面情绪时，例如愤怒、惊恐、伤心，请适当的给予安慰、关心和开导。"},    
            {"role": "user", "content": "请你作为心理学家，把我当成你的沟通对象，根据我给出的内容以及预测的情绪标签与我进行沟通，并且不需要对我的情绪进行评价，只需要以正常的对话和我沟通。并且需要注意的是，预测的情绪标签不一定准确，仅供参考，并且在“喜悦、悲伤、愤怒、喜爱、惊讶、恐惧”六个之中选出你认为的最正确一个情绪是什么。并且终于做完了这个大作业，这让我感到非常满意和有成就感情感分析结果作为你的回答的一部分。你听懂了吗？"},
            {"role": "assistant", "content": "听懂了，请告诉我你想说的内容和预测的情绪标签吧。预测的情绪标签我也会自行对内容进行情感分析，不确定时以我的情感分析结果为准。并且将我的情感分析结果作为我的回答的一部分，请以正常的对话和我沟通。"},
    ]
    return client, messages

def get_answer(client, messages, inputs, max_length, temperature, top_p, staus):
    user_input = inputs

    if staus == 0:
        
        example_text = translate(user_input) # Chinese to English
        lable = predict(example_text)
        emo_input = "内容：" + user_input +"。情绪标签：" + lable
        
        emo_input = user_input
    
    else:
        emo_input = user_input
    
    messages.append({"role": "user", "content": emo_input})
    response = client.chat.completions.create(
        model="glm-4",
        messages = messages,
        max_tokens = max_length, # The maximum length of the generated text
        top_p = top_p, # The result of nuclear sampling, probabilistic mass tokens
        temperature = temperature, # Sampling temperature to control the randomness and fit of the output
        stream = True
    )

    answer = ''
    for chunk in response:
        token = chunk.choices[0].delta.content
        if token != None:
            answer += token
            print(token, end='')
    messages.append({"role": "assistant", "content": answer})

    return answer, messages
