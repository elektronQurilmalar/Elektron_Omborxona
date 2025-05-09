# ElektronKomponentlarUchoti/ui/advanced_search_dialog.py
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QLineEdit,
                             QPushButton, QDialogButtonBox, QLabel, QSpinBox,
                             QDateEdit, QComboBox, QCheckBox, QGroupBox)
from PyQt5.QtCore import QDate, Qt  # Добавлен Qt


class AdvancedSearchDialog(QDialog):
    def __init__(self, parent=None):  # parent - это MainWindow
        super().__init__(parent)
        self.setWindowTitle("Kengaytirilgan qidiruv")
        self.setMinimumWidth(450)
        self.layout = QVBoxLayout(self)
        self.form_layout = QFormLayout()
        self.main_window_ref = parent  # Сохраняем ссылку для доступа к данным, если нужно

        # Поля для поиска
        self.name_search = QLineEdit()
        self.part_number_search = QLineEdit()

        self.category_search_combo = QComboBox()
        self.project_search_combo = QComboBox()
        self.value_search = QLineEdit()
        self.value_search.setPlaceholderText("Masalan: 10k, 100nF, LM358")

        qty_group = QGroupBox("Miqdori")
        qty_layout = QFormLayout(qty_group)
        self.quantity_min_spin = QSpinBox()
        self.quantity_min_spin.setRange(-1, 999999)  # -1 для "не важно"
        self.quantity_min_spin.setSpecialValueText("Min.")  # Текст для -1
        self.quantity_min_spin.setValue(-1)  # По умолчанию

        self.quantity_max_spin = QSpinBox()
        self.quantity_max_spin.setRange(-1, 999999)
        self.quantity_max_spin.setSpecialValueText("Maks.")
        self.quantity_max_spin.setValue(-1)

        qty_layout.addRow(" минимал:", self.quantity_min_spin)
        qty_layout.addRow(" максимал:", self.quantity_max_spin)

        self.low_stock_only_check = QCheckBox("Faqat kam qolganlar")
        if self.main_window_ref:  # Устанавливаем начальное состояние из главного окна
            self.low_stock_only_check.setChecked(self.main_window_ref.low_stock_checkbox.isChecked())

        # Добавление полей в форму
        self.form_layout.addRow("Nomi (o'z ichiga oladi):", self.name_search)
        self.form_layout.addRow("Qism raqami (o'z ichiga oladi):", self.part_number_search)
        self.form_layout.addRow("Kategoriya:", self.category_search_combo)
        self.form_layout.addRow("Loyiha:", self.project_search_combo)
        self.form_layout.addRow("Qiymati (o'z ichiga oladi):", self.value_search)
        self.layout.addLayout(self.form_layout)
        self.layout.addWidget(qty_group)
        self.layout.addWidget(self.low_stock_only_check)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.Reset)
        self.button_box.button(QDialogButtonBox.Ok).setText("Qidirish")
        self.button_box.button(QDialogButtonBox.Cancel).setText("Bekor qilish")
        self.button_box.button(QDialogButtonBox.Reset).setText("Tozalash")

        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.button_box.button(QDialogButtonBox.Reset).clicked.connect(self.reset_filters)
        self.layout.addWidget(self.button_box)

        self._load_combobox_data()

    def _load_combobox_data(self):
        self.category_search_combo.addItem("Har qanday kategoriya", None)
        self.project_search_combo.addItem("Har qanday loyiha", None)
        self.project_search_combo.addItem("Loyihasiz", "")  # Для поиска компонентов без проекта

        if self.main_window_ref:  # Используем ссылку на главное окно
            try:
                # Данные берем из комбобоксов главного окна, чтобы были консистентны
                for i in range(self.main_window_ref.category_filter_combo.count()):
                    text = self.main_window_ref.category_filter_combo.itemText(i)
                    if text != "Barcha kategoriyalar":  # Пропускаем общий пункт
                        self.category_search_combo.addItem(text, text)

                for i in range(self.main_window_ref.project_filter_combo.count()):
                    text = self.main_window_ref.project_filter_combo.itemText(i)
                    if text != "Barcha loyihalar":  # Пропускаем общий пункт
                        # Если в основном комбо есть "Без проекта", то он будет добавлен
                        self.project_search_combo.addItem(text, text if text != "Loyihasiz" else "")


            except Exception as e:  # Более общее исключение
                print(f"Kengaytirilgan qidiruv uchun ro'yxatlarni yuklashda xatolik: {e}")

    def reset_filters(self):
        self.name_search.clear()
        self.part_number_search.clear()
        self.value_search.clear()
        self.category_search_combo.setCurrentIndex(0)  # "Har qanday kategoriya"
        self.project_search_combo.setCurrentIndex(0)  # "Har qanday loyiha"
        self.quantity_min_spin.setValue(-1)
        self.quantity_max_spin.setValue(-1)
        if self.main_window_ref:
            self.low_stock_only_check.setChecked(self.main_window_ref.low_stock_checkbox.isChecked())
        else:
            self.low_stock_only_check.setChecked(False)

    def get_filters(self):
        filters = {}
        # Флаг, указывающий, был ли установлен хотя бы один фильтр
        has_active_filter = False

        if self.name_search.text().strip():
            filters['adv_name'] = self.name_search.text().strip()  # .lower() будет в db_manager
            has_active_filter = True
        if self.part_number_search.text().strip():
            filters['adv_part_number'] = self.part_number_search.text().strip()
            has_active_filter = True

        cat_data = self.category_search_combo.currentData()  # currentData() возвращает второй аргумент addItem
        if cat_data is not None:  # Если выбрана конкретная категория (не "Har qanday...")
            filters['category_name'] = cat_data
            has_active_filter = True

        proj_data = self.project_search_combo.currentData()
        if proj_data is not None:  # Если выбран конкретный проект или "Loyihasiz"
            filters['project_name'] = proj_data
            has_active_filter = True

        if self.value_search.text().strip():
            filters['adv_value'] = self.value_search.text().strip()
            has_active_filter = True

        if self.quantity_min_spin.value() != -1:
            filters['quantity_min'] = self.quantity_min_spin.value()
            has_active_filter = True

        if self.quantity_max_spin.value() != -1:
            filters['quantity_max'] = self.quantity_max_spin.value()
            has_active_filter = True

        # Фильтр low_stock_only: если он отличается от того, что в главном окне, или если он True
        main_low_stock_checked = self.main_window_ref.low_stock_checkbox.isChecked() if self.main_window_ref else False
        if self.low_stock_only_check.isChecked() or (self.low_stock_only_check.isChecked() != main_low_stock_checked):
            filters['low_stock_only'] = self.low_stock_only_check.isChecked()
            has_active_filter = True

        # Если ни один фильтр не активен, возвращаем пустой словарь,
        # чтобы главный обработчик знал, что нужно просто обновить с основными фильтрами
        return filters if has_active_filter else {}