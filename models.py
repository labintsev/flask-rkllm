from flask_sqlalchemy import SQLAlchemy


# Инициализируем SQLAlchemy для работы с базой данных через Flask
db = SQLAlchemy()

class ChatHistory(db.Model):
    """
    Модель SQLAlchemy для хранения истории общения пользователя с LLM.

    Атрибуты:
        id (int): Уникальный идентификатор записи.
        user_message (str): Сообщение пользователя.
        llm_reply (str): Ответ языковой модели.
        timestamp (datetime): Время создания записи.
    """
    id = db.Column(db.Integer, primary_key=True)  # Уникальный идентификатор
    user_message = db.Column(db.Text, nullable=False)  # Текст сообщения пользователя
    llm_reply = db.Column(db.Text, nullable=False)  # Ответ модели
    timestamp = db.Column(db.DateTime, server_default=db.func.now())  # Временная метка создания записи
