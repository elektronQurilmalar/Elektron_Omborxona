# ElektronKomponentlarUchoti/ui/settings_dialog.py
from PyQt5.QtWidgets import (QApplication, QDialog, QVBoxLayout, QFormLayout, QComboBox,
                             QCheckBox, QPushButton, QDialogButtonBox, QLabel,
                             QLineEdit, QHBoxLayout, QFileDialog, QMessageBox, QScrollArea,
                             QWidget)
from PyQt5.QtCore import Qt
import os

# import qt_material # Больше не используется для тем

try:
    # Удаляем этот проблемный импорт:
    # from ElektronKomponentlarUchoti.main import LIGHT_THEME_NAME, DARK_THEME_NAME

    from utils.config_manager import APP_SETTINGS, set_setting, save_settings, load_settings
except ImportError:
    print("XATOLIK: config_manager.py topilmadi (settings_dialog.py).")
    # Заглушки на случай, если config_manager не импортируется
    APP_SETTINGS = {"theme": "System (Light)", "confirm_delete": True, "default_datasheet_dir": ""}
    # Определяем константы здесь как запасной вариант, если они не переданы
    _DEFAULT_LIGHT_THEME_NAME = "System (Light)"
    _DEFAULT_DARK_THEME_NAME = "Dark"


    def set_setting(key, value):
        print("Xatolik: Sozlama saqlanmadi."); return False


    def save_settings(s):
        print("Xatolik: Sozlamalar saqlanmadi."); return False


    def load_settings():
        return APP_SETTINGS


class SettingsDialog(QDialog):
    def __init__(self, parent=None, available_themes=None):
        super().__init__(parent)
        self.setWindowTitle("Sozlamalar")
        self.setMinimumWidth(500)
        self.setModal(True)
        self.main_window_ref = parent

        self.ui_settings = APP_SETTINGS.copy()

        self.main_layout = QVBoxLayout(self)
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.form_layout = QFormLayout(self.scroll_widget)
        scroll_area.setWidget(self.scroll_widget)
        self.main_layout.addWidget(scroll_area)

        # --- Mavzu (Theme) ---
        self.theme_combo = QComboBox()
        self.available_themes_list = available_themes
        if not self.available_themes_list:  # Если список не передан, используем значения по умолчанию
            # Эти имена должны совпадать с теми, что используются в main.py для функции apply_theme
            self.available_themes_list = [
                _DEFAULT_LIGHT_THEME_NAME if '_DEFAULT_LIGHT_THEME_NAME' in globals() else "System (Light)",
                _DEFAULT_DARK_THEME_NAME if '_DEFAULT_DARK_THEME_NAME' in globals() else "Dark"]

        self.theme_combo.addItems(self.available_themes_list)
        self.form_layout.addRow(QLabel("Interfeys mavzusi:"), self.theme_combo)

        # --- O'chirishni tasdiqlash ---
        self.confirm_delete_checkbox = QCheckBox("Komponentni o'chirishdan oldin tasdiq so'ralsinmi?")
        self.form_layout.addRow(self.confirm_delete_checkbox)

        # --- Standart Datasheet papkasi ---
        datasheet_dir_layout = QHBoxLayout()
        self.datasheet_dir_edit = QLineEdit()
        self.datasheet_dir_edit.setPlaceholderText("Papkani tanlang yoki yo'lni kiriting")
        datasheet_dir_button = QPushButton("...")
        datasheet_dir_button.setFixedWidth(30)
        datasheet_dir_button.clicked.connect(self.browse_datasheet_dir)
        datasheet_dir_layout.addWidget(self.datasheet_dir_edit)
        datasheet_dir_layout.addWidget(datasheet_dir_button)
        self.form_layout.addRow(QLabel("Standart Datasheet papkasi:"), datasheet_dir_layout)

        # --- Oxirgi import/export papkalari ---
        self.last_import_dir_label = QLabel(self.ui_settings.get("last_import_dir", "-"))
        self.form_layout.addRow(QLabel("Oxirgi import papkasi:"), self.last_import_dir_label)
        self.last_export_dir_label = QLabel(self.ui_settings.get("last_export_dir", "-"))
        self.form_layout.addRow(QLabel("Oxirgi eksport papkasi:"), self.last_export_dir_label)

        # --- Tugmalar ---
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.Apply)
        self.button_box.button(QDialogButtonBox.Ok).setText("OK (Saqlash)")
        self.button_box.button(QDialogButtonBox.Cancel).setText("Bekor qilish")
        self.button_box.button(QDialogButtonBox.Apply).setText("Qo'llash")

        self.button_box.accepted.connect(self.accept_settings)
        self.button_box.rejected.connect(self.reject)
        self.button_box.button(QDialogButtonBox.Apply).clicked.connect(self.apply_settings_action)
        self.main_layout.addWidget(self.button_box)

        self.load_settings_to_ui()

    def load_settings_to_ui(self):
        default_theme_name = self.available_themes_list[0] if self.available_themes_list else "System (Light)"
        current_theme = self.ui_settings.get("theme", default_theme_name)

        idx = self.theme_combo.findText(current_theme)
        if idx != -1:
            self.theme_combo.setCurrentIndex(idx)
        else:
            if self.theme_combo.count() > 0: self.theme_combo.setCurrentIndex(0)

        self.confirm_delete_checkbox.setChecked(self.ui_settings.get("confirm_delete", True))
        self.datasheet_dir_edit.setText(self.ui_settings.get("default_datasheet_dir", ""))
        self.last_import_dir_label.setText(self.ui_settings.get("last_import_dir", "-"))
        self.last_export_dir_label.setText(self.ui_settings.get("last_export_dir", "-"))

    def browse_datasheet_dir(self):
        current_dir = self.datasheet_dir_edit.text()
        if not current_dir or not os.path.isdir(current_dir): current_dir = os.path.expanduser("~")
        directory = QFileDialog.getExistingDirectory(self, "Standart Datasheet Papkasini Tanlang", current_dir)
        if directory: self.datasheet_dir_edit.setText(directory)

    def _save_current_ui_settings_to_app(self):
        APP_SETTINGS["theme"] = self.theme_combo.currentText()
        APP_SETTINGS["confirm_delete"] = self.confirm_delete_checkbox.isChecked()
        APP_SETTINGS["default_datasheet_dir"] = self.datasheet_dir_edit.text().strip()
        return save_settings(APP_SETTINGS)

    def apply_settings_action(self):
        old_theme_from_app_settings = APP_SETTINGS.get("theme")

        if self._save_current_ui_settings_to_app():
            print("Sozlamalar muvaffaqiyatli qo'llanildi.")
            new_theme_from_app_settings = APP_SETTINGS.get("theme")

            self.ui_settings = APP_SETTINGS.copy()

            if old_theme_from_app_settings != new_theme_from_app_settings:
                QMessageBox.information(self, "Mavzu o'zgarishi",
                                        "Interfeys mavzusi o'zgarishi uchun dasturni qayta ishga tushiring.")
                # Попытка применить QSS на лету
                if self.main_window_ref and hasattr(self.main_window_ref,
                                                    'apply_theme_from_main'):  # Используем новое имя метода
                    # Передаем имя темы, которое используется в main.py для логики apply_theme
                    self.main_window_ref.apply_theme_from_main(QApplication.instance(), new_theme_from_app_settings)
            return True
        else:
            QMessageBox.critical(self, "Xatolik", "Sozlamalarni saqlashda xatolik yuz berdi.")
            return False

    def accept_settings(self):
        if self.apply_settings_action():
            super().accept()

    def reject(self):
        print("Sozlamalar oynasi bekor qilindi.")
        super().reject()