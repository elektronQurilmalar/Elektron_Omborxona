# ElektronKomponentlarUchoti/utils/config_manager.py
import json
import os

# --- Определяем базовую директорию относительно текущего файла ---
# Это более надежный способ, чем полагаться на __file__ из main.py
CURRENT_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
# BASE_DIR будет родительской папкой для папки utils, т.е. корень проекта ElektronKomponentlarUchoti
BASE_DIR = os.path.dirname(CURRENT_FILE_DIR)

CONFIG_DIR_NAME = "config"
CONFIG_FILE_NAME = "settings.json"

CONFIG_DIR_PATH = os.path.join(BASE_DIR, CONFIG_DIR_NAME)
CONFIG_FILE_PATH = os.path.join(CONFIG_DIR_PATH, CONFIG_FILE_NAME)


# --- Функция для создания директории конфигурации ---
def ensure_config_dir_exists():
    """Гарантирует, что директория для конфигурационных файлов существует."""
    if not os.path.exists(CONFIG_DIR_PATH):
        try:
            os.makedirs(CONFIG_DIR_PATH, exist_ok=True)
            print(f"INFO: Config directory created: {CONFIG_DIR_PATH}")
        except OSError as e:
            print(f"XATOLIK KRITIK: Konfiguratsiya papkasini yaratib bo'lmadi '{CONFIG_DIR_PATH}': {e}")
            # В случае критической ошибки здесь можно было бы завершить программу или использовать временные настройки
            return False
    return True


# --- Стандартные настройки ---
DEFAULT_SETTINGS = {
    "theme": "System (Light)",  # Используем новое имя для светлой темы
    "confirm_delete": True,
    "default_datasheet_dir": "",
    "last_import_dir": os.path.expanduser("~"),
    "last_export_dir": os.path.expanduser("~"),
}


def load_settings():
    """Sozlamalarni JSON fayldan yuklaydi."""
    if not ensure_config_dir_exists():  # Убедимся, что папка есть перед чтением
        print("OGOHLANTIRISH: Konfiguratsiya papkasi mavjud emas. Standart sozlamalar ishlatiladi.")
        # Возвращаем копию, чтобы изменения в APP_SETTINGS не влияли на DEFAULT_SETTINGS
        return DEFAULT_SETTINGS.copy()

    try:
        if os.path.exists(CONFIG_FILE_PATH):
            with open(CONFIG_FILE_PATH, 'r', encoding='utf-8') as f:
                settings = json.load(f)
                # Объединяем с DEFAULT_SETTINGS, чтобы добавить новые ключи, если они появились
                for key, value in DEFAULT_SETTINGS.items():
                    settings.setdefault(key, value)
                return settings
        else:
            # Если файл не существует, создаем его со стандартными настройками
            print(f"INFO: Sozlamalar fayli topilmadi. '{CONFIG_FILE_PATH}' da standart sozlamalar yaratiladi.")
            # Сначала сохраняем, потом возвращаем (или возвращаем копию DEFAULT_SETTINGS, а save_settings вернет True/False)
            if save_settings(DEFAULT_SETTINGS.copy()):  # Передаем копию, чтобы не изменять DEFAULT_SETTINGS напрямую
                return DEFAULT_SETTINGS.copy()
            else:  # Если даже сохранить не удалось
                print("XATOLIK: Standart sozlamalarni saqlab bo'lmadi. Vaqtinchalik sozlamalar ishlatiladi.")
                return DEFAULT_SETTINGS.copy()

    except (IOError, json.JSONDecodeError) as e:
        print(f"Sozlamalarni yuklashda xatolik ({CONFIG_FILE_PATH}): {e}. Standart sozlamalar ishlatiladi.")
        return DEFAULT_SETTINGS.copy()  # Возвращаем копию


def save_settings(settings_dict):
    """Sozlamalarni JSON faylga saqlaydi."""
    if not ensure_config_dir_exists():  # Убедимся, что папка есть перед записью
        print(f"XATOLIK: Konfiguratsiya papkasi mavjud emas. Sozlamalarni '{CONFIG_FILE_PATH}' ga saqlab bo'lmadi.")
        return False

    try:
        # Записываем во временный файл, потом переименовываем - для атомарности
        temp_file_path = CONFIG_FILE_PATH + ".tmp"
        with open(temp_file_path, 'w', encoding='utf-8') as f:
            json.dump(settings_dict, f, indent=4, ensure_ascii=False)

        # Пытаемся удалить старый файл (если он есть), затем переименовать временный
        # Это более безопасно, чем просто перезапись
        if os.path.exists(CONFIG_FILE_PATH):
            os.remove(CONFIG_FILE_PATH)
        os.rename(temp_file_path, CONFIG_FILE_PATH)

        print(f"Sozlamalar muvaffaqiyatli saqlandi: {CONFIG_FILE_PATH}")
        return True
    except (IOError, OSError) as e:  # OSError для проблем с переименованием/удалением
        print(f"Sozlamalarni '{CONFIG_FILE_PATH}' ga saqlashda xatolik: {e}")
        # Пытаемся удалить временный файл, если он остался
        if os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except OSError:
                pass  # Игнорируем ошибку удаления временного файла
        return False


# --- Глобальная переменная для хранения текущих настроек приложения ---
# Загружаем настройки при импорте модуля
APP_SETTINGS = load_settings()


def get_setting(key, default=None):
    """Berilgan kalit bo'yicha sozlamani qaytaradi."""
    # Если default не предоставлен, используем значение из DEFAULT_SETTINGS
    default_value_from_master = DEFAULT_SETTINGS.get(key)
    return APP_SETTINGS.get(key, default if default is not None else default_value_from_master)


def set_setting(key, value):
    """Berilgan kalit uchun sozlamani o'rnatadi va faylga saqlaydi."""
    APP_SETTINGS[key] = value
    return save_settings(APP_SETTINGS)  # Сохраняем весь словарь APP_SETTINGS


if __name__ == '__main__':
    print("Testing config_manager...")
    print(f"Project Base Directory: {BASE_DIR}")
    print(f"Config Directory: {CONFIG_DIR_PATH}")
    print(f"Config File: {CONFIG_FILE_PATH}")

    print("\nDefault settings:", DEFAULT_SETTINGS)

    current_settings = load_settings()  # Загрузит из файла или создаст новый
    print("Loaded settings:", current_settings)

    # Тест сохранения
    print("\nAttempting to save settings...")
    test_key_original_value = current_settings.get("test_key")  # Сохраним старое значение, если есть

    if set_setting("test_key", "test_value_123"):
        print("Set_setting 'test_key' successful.")
        reloaded_settings = load_settings()
        print("Settings after set and reload:", reloaded_settings)
        if reloaded_settings.get("test_key") == "test_value_123":
            print("VERIFIED: 'test_key' was saved and reloaded correctly.")
        else:
            print("ERROR: 'test_key' was NOT saved or reloaded correctly.")
    else:
        print("ERROR: Set_setting 'test_key' failed.")

    # Восстановим оригинальное значение или удалим тестовый ключ
    if test_key_original_value is not None:
        set_setting("test_key", test_key_original_value)
    elif "test_key" in APP_SETTINGS:  # Если ключа не было, но он создался
        del APP_SETTINGS["test_key"]
        save_settings(APP_SETTINGS)  # Сохраняем удаление
    print("\nTest finished. Check config/settings.json")