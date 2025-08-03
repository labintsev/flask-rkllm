def RKLLM(model_path, lora_model_path, prompt_cache_path):
    print('Stub RKLLM')


def chat(msg, rkmodel):
    return f'Just a stub {msg}'


def chat_generator(msg, rkmodel):
    out = f'Just a stub {msg}'
    for s in out:
        yield s
