import sys
import os
import argparse
import logging
from flask import Flask, request, jsonify, Response, render_template
from rkllm_chat import RKLLM, chat, chat_generator
from models import db, ChatHistory

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db.init_app(app)

parser = argparse.ArgumentParser()
parser.add_argument('--rkllm_model_path', 
    type=str, 
    required=True, 
    help='Absolute path of the converted RKLLM model on the Linux board;')
    
parser.add_argument('--target_platform', type=str, default='rk3588', help='Target platform: e.g., rk3588/rk3576;')
parser.add_argument('--lora_model_path', type=str, help='Absolute path of the lora_model on the Linux board;')
parser.add_argument('--prompt_cache_path', type=str, help='Absolute path of the prompt_cache file on the Linux board;')
args = parser.parse_args()

if not os.path.exists(args.rkllm_model_path):
    logger.error("Error: Please provide the correct rkllm model path, and ensure it is the absolute path on the board.")
    exit()

if not (args.target_platform in ["rk3588", "rk3576"]):
    logger.error("Error: Please specify the correct target platform: rk3588/rk3576.")
    exit()

if args.lora_model_path:
    if not os.path.exists(args.lora_model_path):
        logger.error("Error: Please provide the correct lora_model path, and advise it is the absolute path on the board.")
        exit()

if args.prompt_cache_path:
    if not os.path.exists(args.prompt_cache_path):
        logger.error("Error: Please provide the correct prompt_cache_file path, and advise it is the absolute path on the board.")
        exit()

# Fix frequency
# command = "sudo bash fix_freq_{}.sh".format(args.target_platform)
# subprocess.run(command, shell=True)

# Set resource limit
# resource.setrlimit(resource.RLIMIT_NOFILE, (102400, 102400))

# Initialize RKLLM model
logger.debug("=========init....===========")

model_path = args.rkllm_model_path
rkllm_model = RKLLM(model_path, args.lora_model_path, args.prompt_cache_path)
logger.debug("RKLLM Model has been initialized successfully！")
logger.debug("==============================")


def make_prompt(messages):
    """Create a prompt from the messages."""
    prompt = ""
    for message in messages:
        if message['role'] == 'user':
            prompt += f"User: {message['content']}\n"
        elif message['role'] == 'system':
            prompt += f"System: {message['content']}\n"
        elif message['role'] == 'assistant':
            prompt += f"Assistant: {message['content']}\n"
    return prompt


# Create a function to receive data sent by the user using a request
@app.route('/v1/chat/completions', methods=['POST'])
def chat_rkllm():
    # Get JSON data from the POST request.
    data = request.json
    if data and 'messages' in data:
        prompt = make_prompt(data['messages'])
        
        if not "stream" in data.keys() or data["stream"] == False:
            # Process the received data here.
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

# Start the Flask application.

app.run(host='0.0.0.0', port=8080, debug=False)

logger.debug("====================")
logger.debug("RKLLM model inference completed, releasing RKLLM model resources...")
rkllm_model.release()
