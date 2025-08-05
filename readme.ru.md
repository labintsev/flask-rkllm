# Flask rkllm chat 

[English version](readme.md)  

## Обзор

Этот репозиторий демонстрирует запуск модели RKLLM на плате OrangePi 5 с использованием Flask.
Он предоставляет простой веб-интерфейс для взаимодействия с моделями в формате RKLLM, облегчая развертывание и тестирование моделей на edge-устройствах.
Поддерживается только Orange Pi 5 с RK3588.

### Требования

- Плата Orange PI 5 с последней версией Armbian и драйвером rknpu 0.9.8, Python 3.12
- Хост-машина X86 для конвертации модели RKLLM (например, `.rkllm` файлы)

### Установка

На плате:

```bash
git clone https://github.com/labintsev/flask-rkllm.git
cd flask-rkllm
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Быстрый старт

Модель RKLLM должна быть сконвертирована из другого формата (например, onnx) на хост-машине X86. 
[Пример здесь](https://github.com/labintsev/rknn-llm/blob/main/models/convert.py)   

После этого необходимо скопировать файл .rkllm на плату Orange Pi.
Для загрузки и выгрузки моделей можно использовать хранилище S3 через скрипт s3.py. 
Подключитесь к Orange Pi по ssh и скопируйте файл модели .rkllm на плату. 

```bash
python s3.py --download your/s3/DeepSeek-R1-Distill-Qwen-1.5B_W8A8_RK3588.rkllm
```

## Использование

Чтобы запустить Flask сервер с определённой RKLLM моделью, выполните:

```bash
python flask_server.py --rkllm_model_path DeepSeek-R1-Distill-Qwen-1.5B_W8A8_RK3588.rkllm
```

Сервер запустится, и вы сможете открыть веб-интерфейс в браузере.
Рекомендуется использовать VsCode, так как можно тестировать веб-приложение через localhost с пробросом портов.

---

## Структура файлов

- `flask_server.py` — основной скрипт сервера Flask
- `rkllm_chat.py` — утилиты RKLLM для взаимодействия с моделью
- `s3.py` — скрипт для загрузки моделей .rkllm с s3
- `*.rkllm` — пример файлов моделей
- `templates/` — Jinja2 шаблоны для Flask
- `static/` — фронтенд-ресурсы (HTML, CSS, JS)

---

## Вклад

Внесение изменений, предложения и сообщения об ошибках приветствуются! Пожалуйста, открывайте issue или отправляйте pull request.

---

## Лицензия

Apache 2.0.  
Смотрите файл LICENSE для подробностей.
