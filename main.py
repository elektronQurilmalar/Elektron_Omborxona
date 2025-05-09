# ElektronKomponentlarUchoti/main.py
import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
                             QLineEdit, QHeaderView, QAbstractItemView, QLabel, QSpacerItem,
                             QSizePolicy, QGroupBox, QAction, QStatusBar, QMessageBox, QDialog,
                             QComboBox, QFileDialog, QMenu, QCheckBox, QDialogButtonBox, QListWidget,
                             QStyleFactory)
from PyQt5.QtCore import Qt, QUrl, QDate
from PyQt5.QtGui import QIcon, QDesktopServices, QColor, QPalette, QLinearGradient, QBrush # Добавлены для градиентов


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller создает временную папку и сохраняет путь в sys._MEIPASS
        base_path = sys._MEIPASS
    else:
        # Режим разработки: путь относительно основного скрипта
        # Предполагаем, что main.py находится в корне проекта,
        # а ресурсы в подпапке 'resources'
        base_path = os.path.abspath(os.path.dirname(sys.argv[0]))
        # Если main.py находится глубже, например, в src/, то base_path нужно скорректировать
        # base_path = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), "..")) # Пример: подняться на уровень выше

    # Убедимся, что base_path указывает на корень, где лежит папка resources
    # Это может потребовать корректировки, если структура проекта сложная

    path_to_resource = os.path.join(base_path, relative_path)
    # print(f"DEBUG: Trying to access resource at: {path_to_resource}") # Для отладки
    return path_to_resource

# --- UI va DB/Actions importlari ---
from ui.add_component_dialog import AddComponentDialog
from ui.manage_locations_dialog import ManageLocationsDialog
from ui_logic.table_manager import TableManager
from ui.settings_dialog import SettingsDialog

try:
    from app_logic.db_manager import (create_tables, get_all_components, delete_component,
                                      get_all_categories_names, add_component, update_component,
                                      get_distinct_project_names)
    from app_logic.actions import (delete_selected_components, search_selected_component_online,
                                   export_data_dialog, generate_label_for_selected,
                                   generate_order_list_action)
    from utils.config_manager import load_settings, save_settings
except ImportError as e:
    print(f"XATOLIK: Kerakli modullarni import qilishda muammo: {e}")
    QMessageBox.critical(None, "Kritik Xatolik", f"Dastur modullarini yuklashda xatolik:\n{e}\n\nDastur yopiladi.")
    sys.exit(1)

LIGHT_THEME_NAME = "Tizim (Yorqin)"
DARK_THEME_NAME = "Metall (Qorong'u)" # Новое название для темы

# --- Новый DARK_STYLE_SHEET для металлического вида ---
DARK_STYLE_SHEET = """
QWidget {
    background-color: #4a4a4a; /* Основной темный фон */
    color: #e0e0e0;           /* Светлый текст */
    border-color: #606060;
    font-family: "Segoe UI", Arial, sans-serif; /* Более современный шрифт */
}
QMainWindow {
    background-color: #404040; 
}
QMenuBar {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                      stop:0 #555555, stop:1 #484848);
    color: #e0e0e0;
    border-bottom: 1px solid #303030;
}
QMenuBar::item {
    background-color: transparent;
    padding: 4px 8px;
}
QMenuBar::item:selected {
    background-color: #6a6a6a;
}
QMenu {
    background-color: #484848;
    color: #e0e0e0;
    border: 1px solid #303030;
}
QMenu::item:selected {
    background-color: #6a6a6a;
}
QMenu::separator { 
    height: 1px;
    background-color: #606060;
    margin-left: 5px;
    margin-right: 5px;
}
QPushButton {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                      stop:0 #606060, stop:1 #505050);
    color: #e0e0e0;
    border: 1px solid #404040;
    border-radius: 4px; /* Скругленные углы */
    padding: 5px 10px;
    min-height: 18px; 
}
QPushButton:hover {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                      stop:0 #686868, stop:1 #585858);
    border-color: #505050;
}
QPushButton:pressed {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                      stop:0 #484848, stop:1 #585858);
}
QPushButton:disabled { 
    background-color: #404040;
    color: #808080;
    border-color: #353535;
}
QLineEdit, QTextEdit, QSpinBox, QComboBox {
    background-color: #3d3d3d;
    color: #e0e0e0;
    border: 1px solid #555555;
    border-radius: 3px;
    padding: 4px;
}
QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QComboBox:focus {
    border: 1px solid #0078d7; /* Подсветка при фокусе */
}
QLineEdit:disabled, QTextEdit:disabled, QSpinBox:disabled, QComboBox:disabled {
    background-color: #303030; 
    color: #707070;
}
QComboBox::drop-down {
    border: none;
    background-color: #505050;
    border-top-right-radius: 3px;
    border-bottom-right-radius: 3px;
    width: 20px;
}
QComboBox::down-arrow {
    image: url(resources/icons/down_arrow_light.png); /* Нужна светлая иконка для темного фона */
    width: 10px;
    height: 10px;
}
QTableWidget {
    background-color: #383838;
    color: #d8d8d8; /* Чуть ярче текст таблицы */
    gridline-color: #505050;
    alternate-background-color: #404040; /* Чередование строк */
    selection-background-color: #0066CC; 
    selection-color: #ffffff;
    border: 1px solid #555555;
}
QHeaderView::section {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                      stop:0 #585858, stop:1 #4d4d4d);
    color: #e0e0e0;
    padding: 5px;
    border: 1px solid #404040;
    border-bottom: 2px solid #383838; /* Нижняя граница для объема */
}
QGroupBox {
    border: 1px solid #555555;
    margin-top: 12px; 
    background-color: transparent; /* Прозрачный фон для групбокса, чтобы фон виджета был виден */
    border-radius: 4px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left; 
    padding: 0 5px 0 5px;
    left: 10px; 
    color: #e0e0e0;
    background-color: #4a4a4a; /* Фон для самого заголовка */
    border-radius: 3px;
}
QStatusBar {
    background-color: #383838;
    color: #d0d0d0;
    border-top: 1px solid #505050;
}
QScrollBar:vertical {
    border: 1px solid #555555;
    background: #3d3d3d;
    width: 16px;
    margin: 0px;
}
QScrollBar::handle:vertical {
    background: #606060;
    min-height: 25px;
    border-radius: 3px;
}
QScrollBar::handle:vertical:hover {
    background: #686868;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px; 
}
QScrollBar:horizontal {
    border: 1px solid #555555;
    background: #3d3d3d;
    height: 16px;
    margin: 0px;
}
QScrollBar::handle:horizontal {
    background: #606060;
    min-width: 25px;
    border-radius: 3px;
}
QScrollBar::handle:horizontal:hover {
    background: #686868;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px; 
}
QCheckBox {
    spacing: 5px; /* Расстояние между индикатором и текстом */
}
QCheckBox::indicator {
    width: 14px;
    height: 14px;
    border-radius: 3px;
}
QCheckBox::indicator:unchecked {
    background-color: #454545; 
    border: 1px solid #555555;
}
QCheckBox::indicator:unchecked:hover {
    border: 1px solid #656565;
}
QCheckBox::indicator:checked {
    background-color: #0078d7; 
    border: 1px solid #005ca8;
    /* image: url(resources/icons/checkmark_light.png); Нужна светлая галочка */
}
QCheckBox::indicator:checked:hover {
    background-color: #0088f7;
    border: 1px solid #006fc8;
}
QDateEdit {
    background-color: #3d3d3d;
    color: #e0e0e0;
    border: 1px solid #555555;
    border-radius: 3px;
}
QDateEdit::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 20px;
    border-left: 1px solid #555555;
    background-color: #505050;
    border-top-right-radius: 3px;
    border-bottom-right-radius: 3px;
}
QDateEdit::down-arrow {
    image: url(resources/icons/down_arrow_light.png);
}
QListWidget {
    background-color: #383838;
    color: #d8d8d8;
    border: 1px solid #555555;
    border-radius: 3px;
}
QListWidget::item {
    padding: 3px;
}
QListWidget::item:selected {
    background-color: #0066CC;
    color: #ffffff;
    border-radius: 2px; /* Скругление для выделенного элемента */
}
QDialog { /* Стиль для диалоговых окон */
    background-color: #454545;
}
QMessageBox { /* Для QMessageBox может потребоваться отдельная настройка через палитру или более специфичные QSS */
    background-color: #454545;
}
QMessageBox QLabel { /* Текст в QMessageBox */
    color: #e0e0e0;
}
QWidget {
    background-color: #4a4a4a; 
    color: #e0e0e0;            /* Этот цвет должен наследоваться QLabel, но для надежности добавим явный стиль */
    border-color: #606060;
    font-family: "Segoe UI", Arial, sans-serif; 
}
"""

# Иконка для стрелки выпадающего списка (down_arrow_light.png)
# Вам нужно будет создать этот файл (например, белый треугольник на прозрачном фоне)
# и поместить его в resources/icons/
# Пример простого SVG, который можно конвертировать в PNG (белый треугольник):
# <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 5"><path d="M0 0 L5 5 L10 0 Z" fill="white"/></svg>
# Аналогично для checkmark_light.png, если решите использовать кастомную галочку.

def apply_theme_globally(application, theme_name):
    if theme_name == DARK_THEME_NAME:
        application.setStyleSheet(DARK_STYLE_SHEET)
        # Дополнительно можно попробовать установить темную палитру,
        # чтобы стандартные диалоги (QFileDialog) тоже выглядели темнее.
        # Это может конфликтовать с QSS, нужно тестировать.
        # dark_palette = QPalette()
        # dark_palette.setColor(QPalette.Window, QColor(60, 60, 60))
        # dark_palette.setColor(QPalette.WindowText, Qt.white)
        # # ... и так далее для других ролей палитры ...
        # application.setPalette(dark_palette)
    else:
        application.setStyleSheet("")
        # Сброс палитры к стандартной системной
        application.setPalette(QApplication.style().standardPalette())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        try:
            self.settings = load_settings()
            if "theme" not in self.settings:
                self.settings["theme"] = LIGHT_THEME_NAME
        except Exception as e:
            print(f"XATOLIK: Sozlamalarni yuklashda muammo: {e}. Zapas sozlamalar ishlatiladi.")
            self.settings = {"theme": LIGHT_THEME_NAME, "confirm_delete": True, "default_datasheet_dir": ""}
            if not os.path.exists(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config",
                                               "settings.json")):
                save_settings(self.settings)

        if not create_tables():
            QMessageBox.critical(self, "Kritik Xatolik", "Ma'lumotlar bazasini yaratib bo'lmadi. Dastur yopiladi.")
            sys.exit(1)

        self.setWindowTitle("Elektron Omborxona")
        self.setGeometry(100, 100, 1450, 800)
        self.load_icons()
        self.init_ui()
        self.connect_signals()

        self.table_headers_db_keys = ["id", "name", "category_name", "part_number", "value", "package_type_name",
                                      "quantity", "min_quantity", "location_name", "project", "description",
                                      "datasheet_path", "reminder_date", "reminder_text"]
        self.table_display_headers = ["ID", "Nomi", "Kategoriya", "Qism Raqami", "Qiymati", "Korpus", "Miqdori",
                                      "Min.Miqdor", "Joylashuvi", "Loyiha", "Tavsif", "Datasheet", "Eslatma sanasi",
                                      "Eslatma"]

        self.table_manager = TableManager(self.table_widget, self.table_headers_db_keys, self.table_display_headers)
        self.refresh_all_data_and_filters()

    def load_icons(self):
        self.icons = {name: QIcon(self._get_icon_path(f"{name}.png"))
                      for name in ["plus", "pencil", "delete", "exit", "info",
                                   "settings", "export", "pdf", "refresh",
                                   "label", "www",
                                   "search_advanced", "order_list",
                                   "template"
                                   ]}

    def _get_icon_path(self, filename):
        # filename это 'plus.png', 'delete.png' и т.д.
        # relative_path должен быть 'resources/icons/plus.png'
        relative_icon_path = os.path.join("resources", "icons", filename)
        path = resource_path(relative_icon_path)
        # print(f"DEBUG: _get_icon_path for {filename} resolved to {path}") # Для отладки
        if os.path.exists(path):
            return path
        else:
            print(f"OGOHLANTIRISH: Ikona topilmadi - {path}") # Переведено
            return "" # Возвращаем пустую строку, QIcon() создаст пустую иконку

    def init_ui(self):
        central_widget = QWidget();
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget);
        top_filter_layout = QHBoxLayout()
        search_groupbox = QGroupBox("Qidiruv");
        search_layout_h = QHBoxLayout(search_groupbox)
        self.search_input = QLineEdit();
        self.search_input.setPlaceholderText("Nomi, qism raqami, loyiha...")
        search_layout_h.addWidget(self.search_input);
        top_filter_layout.addWidget(search_groupbox, 2)
        cat_filter_groupbox = QGroupBox("Kategoriya");
        cat_filter_layout_h = QHBoxLayout(cat_filter_groupbox)
        self.category_filter_combo = QComboBox();
        self.category_filter_combo.addItem("Barcha kategoriyalar")
        cat_filter_layout_h.addWidget(self.category_filter_combo);
        top_filter_layout.addWidget(cat_filter_groupbox, 1)
        proj_filter_groupbox = QGroupBox("Loyiha");
        proj_filter_layout_h = QHBoxLayout(proj_filter_groupbox)
        self.project_filter_combo = QComboBox();
        self.project_filter_combo.addItem("Barcha loyihalar")
        proj_filter_layout_h.addWidget(self.project_filter_combo);
        top_filter_layout.addWidget(proj_filter_groupbox, 1)
        self.low_stock_checkbox = QCheckBox("Faqat kam qolganlar");
        top_filter_layout.addWidget(self.low_stock_checkbox)
        top_filter_layout.addStretch(1);
        main_layout.addLayout(top_filter_layout)

        action_button_layout = QHBoxLayout();
        actions_groupbox = QGroupBox("Amallar");
        actions_layout_h = QHBoxLayout(actions_groupbox)
        self.refresh_button = QPushButton(self.icons.get("refresh", QIcon()), " Yangilash");
        actions_layout_h.addWidget(self.refresh_button)
        self.add_button = QPushButton(self.icons.get("plus", QIcon()), " Qo'shish");
        actions_layout_h.addWidget(self.add_button)
        self.edit_button = QPushButton(self.icons.get("pencil", QIcon()), " Tahrirlash");
        actions_layout_h.addWidget(self.edit_button)
        self.delete_button = QPushButton(self.icons.get("delete", QIcon()), " O'chirish");
        actions_layout_h.addWidget(self.delete_button)
        self.open_datasheet_button = QPushButton(self.icons.get("pdf", QIcon()), " Datasheet");
        self.open_datasheet_button.setEnabled(False);
        actions_layout_h.addWidget(self.open_datasheet_button)
        self.search_web_button = QPushButton(self.icons.get("www", QIcon()), " Web Qidiruv");
        self.search_web_button.setEnabled(False);
        actions_layout_h.addWidget(self.search_web_button)
        self.label_button = QPushButton(self.icons.get("label", QIcon()), " Etiketka");
        label_menu = QMenu(self);
        label_menu.addAction("Tanlangan uchun etiketka...", lambda: generate_label_for_selected(self));
        self.label_button.setMenu(label_menu);
        self.label_button.setEnabled(False);
        actions_layout_h.addWidget(self.label_button)

        self.advanced_search_button = QPushButton(self.icons.get("search_advanced", QIcon()), " Kengaytirilgan qidiruv")
        actions_layout_h.addWidget(self.advanced_search_button)

        self.generate_order_list_button = QPushButton(self.icons.get("order_list", QIcon()), " Buyurtma ro'yxati")
        actions_layout_h.addWidget(self.generate_order_list_button)

        actions_groupbox.setLayout(actions_layout_h);
        action_button_layout.addWidget(actions_groupbox);
        action_button_layout.addStretch(1);
        main_layout.addLayout(action_button_layout)

        self.table_widget = QTableWidget();
        self.table_widget.verticalHeader().setVisible(False);
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows);
        self.table_widget.setSelectionMode(QAbstractItemView.ExtendedSelection);
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers);
        self.table_widget.setSortingEnabled(True)
        main_layout.addWidget(self.table_widget)
        self.setup_menu_and_statusbar()

    def connect_signals(self):
        self.search_input.textChanged.connect(self.apply_filters_and_search)
        self.category_filter_combo.currentTextChanged.connect(self.apply_filters_and_search)
        self.project_filter_combo.currentTextChanged.connect(self.apply_filters_and_search)
        self.low_stock_checkbox.stateChanged.connect(self.apply_filters_and_search)
        self.refresh_button.clicked.connect(self.refresh_all_data_and_filters)
        self.add_button.clicked.connect(self.open_add_component_dialog)
        self.edit_button.clicked.connect(self.open_edit_component_dialog)
        self.delete_button.clicked.connect(lambda: delete_selected_components(self))
        self.open_datasheet_button.clicked.connect(self.open_selected_datasheet)
        self.search_web_button.clicked.connect(lambda: search_selected_component_online(self))
        self.table_widget.itemDoubleClicked.connect(self.handle_table_double_click)
        self.table_widget.selectionModel().selectionChanged.connect(self.update_action_button_states)

        self.advanced_search_button.clicked.connect(self.open_advanced_search_dialog)
        self.generate_order_list_button.clicked.connect(self.generate_order_list)

    def setup_menu_and_statusbar(self):
        menu_bar = self.menuBar();
        file_menu = menu_bar.addMenu("&Fayl")
        export_action = QAction(self.icons.get("export", QIcon()), "Eksport qilish...", self);
        export_action.triggered.connect(lambda: export_data_dialog(self));
        file_menu.addAction(export_action)

        extras_menu = file_menu.addMenu("Qo'shimcha imkoniyatlar");
        settings_action = QAction(self.icons.get("settings", QIcon()), "&Sozlamalar", self);
        settings_action.triggered.connect(self.open_settings_dialog);
        extras_menu.addAction(settings_action)

        manage_templates_action = QAction(self.icons.get("template", QIcon()), "Shablonlarni boshqarish", self)
        manage_templates_action.triggered.connect(self.open_manage_templates_dialog)
        extras_menu.addAction(manage_templates_action)

        file_menu.addSeparator();
        exit_action = QAction(self.icons.get("exit", QIcon()), "&Chiqish", self);
        exit_action.setShortcut("Ctrl+Q");
        exit_action.triggered.connect(self.close);
        file_menu.addAction(exit_action)

        warehouse_menu = menu_bar.addMenu("&Ombor");
        manage_locations_action = QAction("Saqlash joylarini boshqarish", self);  # Переведено
        manage_locations_action.triggered.connect(self.open_manage_locations_dialog);
        warehouse_menu.addAction(manage_locations_action)

        language_menu = menu_bar.addMenu("&Til");
        lang_uz_action = QAction("O'zbekcha", self);
        lang_uz_action.setCheckable(True);
        lang_uz_action.setChecked(True)
        lang_ru_action = QAction("Русский", self);
        lang_ru_action.setCheckable(True)  # Оставил для примера, можно удалить
        lang_en_action = QAction("English", self);
        lang_en_action.setCheckable(True)  # Оставил для примера, можно удалить
        language_menu.addAction(lang_uz_action);
        language_menu.addAction(lang_ru_action);
        language_menu.addAction(lang_en_action)

        help_menu = menu_bar.addMenu("&Yordam");
        about_action = QAction(self.icons.get("info", QIcon()), "Dastur &haqida", self);
        about_action.triggered.connect(self.show_about_dialog);
        help_menu.addAction(about_action)

        self.setStatusBar(QStatusBar(self));
        self.statusBar().showMessage("Tayyor")

    def refresh_all_data_and_filters(self):
        self.update_category_filter_combo()
        self.update_project_filter_combo()
        self.load_and_display_data_from_db(self.get_current_filters())

    def update_category_filter_combo(self):
        current_selection = self.category_filter_combo.currentText()
        self.category_filter_combo.blockSignals(True);
        self.category_filter_combo.clear();
        self.category_filter_combo.addItem("Barcha kategoriyalar")
        try:
            categories = get_all_categories_names();
            self.category_filter_combo.addItems(categories)
        except Exception as e:
            print(f"Kategoriya filtrini yangilashda xato: {e}");
            self.category_filter_combo.addItem("XATO")
        idx = self.category_filter_combo.findText(current_selection);
        if idx != -1:
            self.category_filter_combo.setCurrentIndex(idx)
        else:
            self.category_filter_combo.setCurrentIndex(0)
        self.category_filter_combo.blockSignals(False)

    def update_project_filter_combo(self):
        current_selection = self.project_filter_combo.currentText()
        self.project_filter_combo.blockSignals(True);
        self.project_filter_combo.clear();
        self.project_filter_combo.addItem("Barcha loyihalar")
        try:
            projects = get_distinct_project_names();
            self.project_filter_combo.addItems(projects)
        except Exception as e:
            print(f"Loyiha filtrini yangilashda xato: {e}");
            self.project_filter_combo.addItem("XATO")
        idx = self.project_filter_combo.findText(current_selection)
        if idx != -1:
            self.project_filter_combo.setCurrentIndex(idx)
        else:
            self.project_filter_combo.setCurrentIndex(0)
        self.project_filter_combo.blockSignals(False)

    def get_current_filters(self):
        filters = {'search_text': self.search_input.text().strip().lower(),
                   'category_name': self.category_filter_combo.currentText(),
                   'project_name': self.project_filter_combo.currentText(),
                   'low_stock_only': self.low_stock_checkbox.isChecked()}
        if filters['category_name'] == "Barcha kategoriyalar": filters['category_name'] = None
        if filters['project_name'] == "Barcha loyihalar": filters['project_name'] = None
        return filters

    def apply_filters_and_search(self):
        component_count = self.table_manager.load_and_display_data(self.get_current_filters())
        self.statusBar().showMessage(f"{component_count} ta komponent topildi.", 3000)

    def load_and_display_data_from_db(self, filters=None):
        if filters is None: filters = self.get_current_filters()
        component_count = self.table_manager.load_and_display_data(filters)
        self.statusBar().showMessage(f"{component_count} ta komponent topildi.", 3000)

    def _ask_user_to_select_datasheet(self, paths_string):
        paths = [p.strip() for p in paths_string.split(';') if p.strip()]
        if not paths:
            return None
        if len(paths) == 1:
            return paths[0]

        dialog = QDialog(self)
        dialog.setWindowTitle("Datasheet tanlash")  # Переведено
        layout = QVBoxLayout(dialog)
        label = QLabel("Bir nechta datasheet/havola topildi. Ochish uchun birini tanlang:")
        layout.addWidget(label)

        list_widget = QListWidget()
        for path_or_url_item in paths:
            display_text = os.path.basename(path_or_url_item) if os.path.exists(
                path_or_url_item) and not path_or_url_item.startswith(('http://', 'https://')) else path_or_url_item
            list_widget.addItem(display_text)
        list_widget.setCurrentRow(0)
        layout.addWidget(list_widget)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.button(QDialogButtonBox.Ok).setText("OK (Tanlash)")
        buttons.button(QDialogButtonBox.Cancel).setText("Bekor qilish")
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        if dialog.exec_() == QDialog.Accepted and list_widget.currentItem():
            selected_index = list_widget.currentRow()
            return paths[selected_index]
        return None

    def handle_table_double_click(self, item):
        if item:
            current_row = item.row()
            try:
                datasheet_col_idx = self.table_headers_db_keys.index("datasheet_path")
            except ValueError:
                datasheet_col_idx = -1

            if datasheet_col_idx != -1 and item.column() == datasheet_col_idx:
                datasheet_path_item = self.table_widget.item(current_row, datasheet_col_idx)
                if datasheet_path_item:
                    paths_string = datasheet_path_item.toolTip()
                    if not paths_string: paths_string = datasheet_path_item.text()

                    if paths_string:
                        path_to_open = self._ask_user_to_select_datasheet(paths_string)
                        if path_to_open:
                            self.open_datasheet(path_to_open)
                            return

            self.table_widget.selectRow(current_row)
            self.open_edit_component_dialog()

    def update_action_button_states(self):
        selected_rows = self.table_widget.selectionModel().selectedRows()
        has_selection = bool(selected_rows);
        enable_single_selection_actions = len(selected_rows) == 1
        self.edit_button.setEnabled(enable_single_selection_actions);
        self.delete_button.setEnabled(has_selection)
        self.label_button.setEnabled(has_selection);
        self.search_web_button.setEnabled(enable_single_selection_actions)
        enable_datasheet = False
        if enable_single_selection_actions:
            current_row = selected_rows[0].row()
            try:
                datasheet_col_idx = self.table_headers_db_keys.index("datasheet_path")
                if datasheet_col_idx != -1:
                    datasheet_item = self.table_widget.item(current_row, datasheet_col_idx)
                    if datasheet_item and (datasheet_item.toolTip() or datasheet_item.text()):
                        enable_datasheet = True
            except (ValueError, AttributeError, IndexError):
                pass
        self.open_datasheet_button.setEnabled(enable_datasheet)

    def open_selected_datasheet(self):
        selected_rows = self.table_widget.selectionModel().selectedRows()
        if len(selected_rows) != 1: return
        current_row = selected_rows[0].row()
        try:
            datasheet_col_idx = self.table_headers_db_keys.index("datasheet_path")
            datasheet_path_item = self.table_widget.item(current_row, datasheet_col_idx)
            if datasheet_path_item:
                paths_string = datasheet_path_item.toolTip();
                if not paths_string: paths_string = datasheet_path_item.text()

                if paths_string:
                    path_to_open = self._ask_user_to_select_datasheet(paths_string)
                    if path_to_open:
                        self.open_datasheet(path_to_open)
                        return
        except (ValueError, AttributeError) as e:
            print(f"Datasheet ochish uchun ma'lumot olishda xato: {e}")
        QMessageBox.information(self, "Datasheet yo'q",
                                "Tanlangan komponent uchun datasheet ko'rsatilmagan yoki fayl tanlanmadi.")

    def open_datasheet(self, path_or_url):
        if not path_or_url: return
        url_to_open = QUrl(path_or_url)
        if not url_to_open.scheme() and os.path.exists(path_or_url):
            url_to_open = QUrl.fromLocalFile(path_or_url)
        elif not url_to_open.scheme():
            if "." in path_or_url and not path_or_url.startswith(("/", "\\")):
                url_to_open = QUrl("http://" + path_or_url, QUrl.TolerantMode)
            else:
                QMessageBox.warning(self, "Xatolik",
                                    f"'{path_or_url}' fayli topilmadi yoki URL manzili noto'g'ri.");
                return

        if not QDesktopServices.openUrl(url_to_open):
            QMessageBox.warning(self, "Xatolik", f"'{path_or_url}' manzilini ochib bo'lmadi.")

    def open_add_component_dialog(self):
        dialog = AddComponentDialog(self)
        if dialog.check_initialization_error():
            print("XATOLIK: AddComponentDialog ni ochishda muammo.")
            return

        if dialog.exec_() == QDialog.Accepted:
            data_from_dialog = dialog.get_data_from_fields();
            new_component_id = add_component(data_from_dialog)
            if new_component_id:
                self.statusBar().showMessage(f"'{data_from_dialog['name']}' (ID: {new_component_id}) qo'shildi.",
                                             5000);
                self.refresh_all_data_and_filters()
            else:
                QMessageBox.critical(self, "Xatolik", f"'{data_from_dialog['name']}' komponentini qo'shishda xatolik.")
        else:
            self.statusBar().showMessage("Qo'shish bekor qilindi.", 3000)

    def open_edit_component_dialog(self):
        selected_rows = self.table_widget.selectionModel().selectedRows()
        if len(selected_rows) != 1:
            QMessageBox.warning(self, "Xatolik", "Tahrirlash uchun bitta komponent tanlang!")
            return

        current_row_display = selected_rows[0].row()
        component_id_to_edit = None
        try:
            id_item = self.table_widget.item(current_row_display, 0);
            if id_item is None: raise ValueError("ID katakchasi bo'sh (None).")
            component_id_to_edit = int(id_item.text())
        except (AttributeError, ValueError, TypeError) as e:
            print(f"XATOLIK: IDni olishda: {e}")
            QMessageBox.critical(self, "Xatolik", f"Tanlangan IDni o'qishda xato: {e}");
            return

        dialog = AddComponentDialog(self, component_id_to_edit=component_id_to_edit)
        if dialog.check_initialization_error():
            return

        if dialog.exec_() == QDialog.Accepted:
            updated_data = dialog.get_data_from_fields()
            if update_component(component_id_to_edit, updated_data):
                self.statusBar().showMessage(f"'{updated_data['name']}' (ID: {component_id_to_edit}) yangilandi.",
                                             5000);
                self.refresh_all_data_and_filters()
            else:
                QMessageBox.critical(self, "Xatolik", f"'{updated_data['name']}' komponentini yangilashda xatolik.")
        else:
            self.statusBar().showMessage("Tahrirlash bekor qilindi.", 3000)

    def show_about_dialog(self):
        QMessageBox.about(self, "Dastur haqida",
                          "<b>Elektron Omborxona</b><br>Versiya: 0.6.0<br>Yaratuvchi: Abdulloh<br>" + f"Python {sys.version_info.major}.{sys.version_info.minor}, PyQt5")

    def open_settings_dialog(self):
        old_theme = self.settings.get("theme")
        dialog = SettingsDialog(self, available_themes=[LIGHT_THEME_NAME, DARK_THEME_NAME])

        if dialog.exec_() == QDialog.Accepted:
            self.settings = load_settings()
            print("Sozlamalar saqlandi:", self.settings)
            new_theme = self.settings.get("theme")
            if old_theme != new_theme:
                QMessageBox.information(self, "Mavzu o'zgarishi",
                                        "Interfeys mavzusi o'zgarishi uchun dasturni qayta ishga tushiring.")
                apply_theme_globally(QApplication.instance(), new_theme)
        else:
            print("Sozlamalar bekor qilindi.")

    def open_manage_locations_dialog(self):
        dialog = ManageLocationsDialog(self);
        dialog.exec_();
        self.refresh_all_data_and_filters()

    def open_advanced_search_dialog(self):
        try:
            from ui.advanced_search_dialog import AdvancedSearchDialog
        except ImportError as e:
            QMessageBox.critical(self, "Import Xatosi",
                                 f"Kengaytirilgan qidiruv dialogini yuklab bo'lmadi: {e}")  # Переведено
            return

        dialog = AdvancedSearchDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            adv_filters = dialog.get_filters()
            if adv_filters:
                self.search_input.blockSignals(True)
                self.search_input.clear()
                self.search_input.blockSignals(False)

                if 'category_name' in adv_filters:
                    self.category_filter_combo.blockSignals(True)
                    idx = self.category_filter_combo.findText("Barcha kategoriyalar")
                    if idx != -1: self.category_filter_combo.setCurrentIndex(idx)
                    self.category_filter_combo.blockSignals(False)

                if 'project_name' in adv_filters:
                    self.project_filter_combo.blockSignals(True)
                    idx = self.project_filter_combo.findText("Barcha loyihalar")
                    if idx != -1: self.project_filter_combo.setCurrentIndex(idx)
                    self.project_filter_combo.blockSignals(False)

                if 'low_stock_only' in adv_filters:
                    self.low_stock_checkbox.blockSignals(True)
                    self.low_stock_checkbox.setChecked(adv_filters['low_stock_only'])
                    self.low_stock_checkbox.blockSignals(False)

                current_main_filters = self.get_current_filters()
                final_filters = {**current_main_filters, **adv_filters}

                if 'adv_name' in final_filters or 'adv_part_number' in final_filters or 'adv_value' in final_filters:
                    final_filters.pop('search_text', None)

                print("DEBUG: Kengaytirilgan filtrlar qo'llanildi:", final_filters)  # Переведено
                self.load_and_display_data_from_db(final_filters)
            else:
                self.refresh_all_data_and_filters()

    def generate_order_list(self):
        generate_order_list_action(self)

    def open_manage_templates_dialog(self):
        QMessageBox.information(self, "Ishlab chiqilmoqda", "Shablonlarni boshqarish ishlab chiqilmoqda.")  # Переведено

    def apply_theme_from_main(self, application_instance, theme_name):  # Этот метод теперь вызывается из SettingsDialog
        apply_theme_globally(application_instance, theme_name)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    initial_settings = load_settings()
    apply_theme_globally(app, initial_settings.get("theme", LIGHT_THEME_NAME))

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
