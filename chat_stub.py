import time

def RKLLM(model_path, lora_model_path, prompt_cache_path):
    print('Stub RKLLM')


def chat(msg, rkllm_model, request_id=None):
    rkllm_output = f'Just a stub {msg}'
    role = 'user'
    enable_thinking = False

    return {
        "id": request_id,
        "object": "chat.completion",
        "created": int(time.time()),
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": rkllm_output
                },
                "finish_reason": "stop"
            }
        ]
    }


def chat_generator(msg, rkmodel):
    out = f'Just a stub {msg}'
    content = ""
    for s in out:
        time.sleep(0.1)
        content += s
        # OpenAI stream format: each chunk is a JSON line with 'choices'
        yield f'''{{
            "choices": [
                {{
                    "delta": {{"content": "{s}"}},
                    "index": 0,
                    "finish_reason": null
                }}
            ]
        }}\n'''
    # Send finish_reason at the end
    yield '''{
        "choices": [
            {
                "delta": {},
                "index": 0,
                "finish_reason": "stop"
            }
        ]
    }'''
