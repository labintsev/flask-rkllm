import sys
import os
import argparse
from flask import Flask, request, jsonify, Response, render_template
from chat_stub import RKLLM, chat, chat_generator
from models import db, ChatHistory

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
    print("Error: Please provide the correct rkllm model path, and ensure it is the absolute path on the board.")
    sys.stdout.flush()
    exit()

if not (args.target_platform in ["rk3588", "rk3576"]):
    print("Error: Please specify the correct target platform: rk3588/rk3576.")
    sys.stdout.flush()
    exit()

if args.lora_model_path:
    if not os.path.exists(args.lora_model_path):
        print("Error: Please provide the correct lora_model path, and advise it is the absolute path on the board.")
        sys.stdout.flush()
        exit()

if args.prompt_cache_path:
    if not os.path.exists(args.prompt_cache_path):
        print("Error: Please provide the correct prompt_cache_file path, and advise it is the absolute path on the board.")
        sys.stdout.flush()
        exit()

# Fix frequency
# command = "sudo bash fix_freq_{}.sh".format(args.target_platform)
# subprocess.run(command, shell=True)

# Set resource limit
# resource.setrlimit(resource.RLIMIT_NOFILE, (102400, 102400))

# Initialize RKLLM model
print("=========init....===========")
sys.stdout.flush()
model_path = args.rkllm_model_path
rkllm_model = RKLLM(model_path, args.lora_model_path, args.prompt_cache_path)
print("RKLLM Model has been initialized successfully！")
print("==============================")
sys.stdout.flush()

# Create a function to receive data sent by the user using a request
@app.route('/chat', methods=['POST'])
def chat_rkllm():
    # Get JSON data from the POST request.
    data = request.json
    if data and 'messages' in data:
        messages = data['messages']
        print("Received messages:", messages)
        if not "stream" in data.keys() or data["stream"] == False:
            # Process the received data here.
            for message in messages:
                input_prompt = message['content']
                rkllm_output = chat(input_prompt, rkllm_model)
            print('Return: ', rkllm_output)
            response = {"message": rkllm_output}
            return jsonify(response), 200
        else:
            for message in messages:
                input_prompt = message['content']

            return Response(chat_generator(input_prompt, rkllm_model), content_type='text/plain')
    else:
        return jsonify({'status': 'error', 'message': 'Invalid JSON data!'}), 400


@app.route('/')
def home():
    return render_template("index.html")

# Start the Flask application.

app.run(host='0.0.0.0', port=8080, threaded=True)

print("====================")
print("RKLLM model inference completed, releasing RKLLM model resources...")
rkllm_model.release()
print("====================")
