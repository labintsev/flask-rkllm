# Flask rkllm chat

## Overview

This repository demonstrates how to run an RKLLM-based model server using Flask. 
It provides a simple web interface to interact with models in RKLLM format, making it easy to deploy and test your models on edge devices. 
Orange Pi 5 with RK3588 supports only. 

### Requirements

- Orange PI 5 board with latest Armbian and rknpu driver 0.9.8, Python 3.12
- X86 host machine to covert RKLLM model (e.g., `.rkllm` files)


### Installation

On the board: 

```bash
git clone https://github.com/labintsev/flask-rkllm.git
cd flask-rkllm
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Getting Started 

RKLLM mode must been converted on host X86 machine.  
[Here example](https://github.com/labintsev/rknn-llm/blob/main/models/convert.py)  
Then you need to copy .rkllm file to Orange Pi board. 
You can use S3 storage via s3.py script. 
Connect to Orange Pi via ssh and copy .rkllm model file to the board. 

## Usage

To start the Flask server with a specific RKLLM model, run:

```bash
python flask_server.py --rkllm_model_path DeepSeek-R1-Distill-Qwen-1.5B_W8A8_RK3588.rkllm
```

The server will start and you can open web UI in brawser.
VsCode is recommended, because you can test web app via localhost with port forwarding. 

---

## File Structure

- `flask_server.py` — Main Flask server script
- `rkllm_chat.py` - RKLLM utils to interact with model
- `s3.py` - script to download .rkllm models from s3 
- `*.rkllm` — Example model files
- `templates/` — Jinja2 templates for Flask 
- `static/` — Frontend assets (HTML, CSS, JS)

---

## Contributing

Contributions, suggestions, and bug reports are welcome! Please open an issue or submit a pull request.

---

## License

Apache 2.0.  
See the LICENSE file for more details.
