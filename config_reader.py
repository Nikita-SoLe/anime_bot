from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    # Желательно использовать SecretStr для конфиденциальных данных
    bot_token: SecretStr
    admin_id_nikita: int
    chat_id: int

    # Вложенный класс с доп. указаниями для настройки
    class Config:
        # Имя файла, откуда будут прочитаны данные
        # (Относительно текущей рабочей директории)
        env_file = '.env'
        # Кодировка читаемого файла
        env_file_encoding = 'utf-8'


config = Settings()

if __name__ == "__main__":
    pass
