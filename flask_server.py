import sys
import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request, jsonify, Response, render_template
from rkllm_chat import RKLLM, chat, chat_generator
from models import db, ChatHistory
from utils import make_prompt

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
file_handler = RotatingFileHandler(
    'app.log', 
    maxBytes=1024*1024*5,           # 5 MB to file
    backupCount=3                   # Num of backup files 
)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db.init_app(app)

# Fix frequency
# command = "sudo bash fix_freq_{}.sh".format(args.target_platform)
# subprocess.run(command, shell=True)

# Set resource limit
# resource.setrlimit(resource.RLIMIT_NOFILE, (102400, 102400))

logger.debug("Initialize RKLLM model")

model_path = "DeepSeek-R1-Distill-Qwen-1.5B_W8A8_RK3588.rkllm"
lora_model_path = None
prompt_cache_path = None
rkllm_model = RKLLM(model_path, lora_model_path, prompt_cache_path)

logger.debug("RKLLM Model has been initialized successfully！")


@app.route('/v1/chat/completions', methods=['POST'])
def chat_rkllm():
    """OpenAI API compat"""
    data = request.json
    if data and 'messages' in data:
        prompt = make_prompt(data['messages'])
        
        if not "stream" in data.keys() or data["stream"] == False:
            rkllm_output = chat(prompt, rkllm_model)
            logger.debug('Return: %s', rkllm_output)
            return jsonify(rkllm_output), 200
        else:
            return Response(chat_generator(prompt, rkllm_model), content_type='text/plain')
    else:
        logger.error('No messages in data!')
        return jsonify({'status': 'error', 'message': 'No messages in data!'}), 400


@app.route('/')
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=False)
    logger.debug("RKLLM model inference completed, releasing RKLLM model resources...")
    rkllm_model.release()
