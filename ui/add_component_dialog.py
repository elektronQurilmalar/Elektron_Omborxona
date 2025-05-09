# ElektronKomponentlarUchoti/ui/add_component_dialog.py
import os
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QLineEdit,
                             QPushButton, QDialogButtonBox, QTextEdit, QSpinBox, QLabel,
                             QComboBox, QHBoxLayout, QFileDialog, QMessageBox, QSpacerItem, QSizePolicy,
                             QDateEdit)
from PyQt5.QtCore import Qt, QStandardPaths, QDate, QTimer

try:
    from app_logic.db_manager import (get_all_categories_names, get_all_package_types_names,
                                      get_all_storage_locations_names, get_component_by_id)
except ImportError:
    print("XATOLIK: db_manager.py import qilinmadi (add_component_dialog.py).")


    def get_all_categories_names():
        return ["DB Xato: Kat."]


    def get_all_package_types_names():
        return ["DB Xato: Pkg."]


    def get_all_storage_locations_names():
        return ["DB Xato: Joy."]


    def get_component_by_id(id):
        return None

try:
    from utils.component_packages import get_packages_for_type
except ImportError:
    print("OGOHLANTIRISH: utils/component_packages.py topilmadi.")
    get_packages_for_type = lambda cat: get_all_package_types_names()


class AddComponentDialog(QDialog):
    def __init__(self, parent=None, component_id_to_edit=None):
        super().__init__(parent)

        self.component_id_to_edit = component_id_to_edit
        self.existing_data = None
        self.close_on_error = False

        if self.component_id_to_edit:
            self.setWindowTitle("Komponentni Tahrirlash")
            try:
                self.existing_data = get_component_by_id(self.component_id_to_edit)
                if not self.existing_data:
                    QMessageBox.critical(self, "Xatolik", f"ID={self.component_id_to_edit} bilan komponent topilmadi.")
                    self.close_on_error = True
                    return
            except Exception as e:
                print(f"Komponentni olishda xatolik: {e}")
                QMessageBox.critical(self, "Xatolik", f"Komponent ma'lumotlarini yuklashda xatolik: {e}")
                self.close_on_error = True
                return
        else:
            self.setWindowTitle("Yangi Komponent Qo'shish")

        self.setMinimumWidth(500)
        self.setModal(True)

        self.layout = QVBoxLayout(self)
        self.form_layout = QFormLayout()

        self.name_input = QLineEdit()
        self.type_input = QComboBox()
        self.type_input.setEditable(True)
        self.type_input.setInsertPolicy(QComboBox.NoInsert)

        self.part_number_input = QLineEdit()
        self.value_input = QLineEdit()

        self.package_input = QComboBox()
        self.package_input.setEditable(True)
        self.package_input.setInsertPolicy(QComboBox.NoInsert)

        self.quantity_input = QSpinBox();
        self.quantity_input.setRange(0, 999999);
        self.quantity_input.setMinimumWidth(100)
        self.min_quantity_input = QSpinBox();
        self.min_quantity_input.setRange(0, 99999);
        self.min_quantity_input.setMinimumWidth(100)

        self.location_input = QComboBox();
        self.location_input.setEditable(True);
        self.location_input.setInsertPolicy(QComboBox.NoInsert)
        self.project_input = QLineEdit()
        self.description_input = QTextEdit();
        self.description_input.setFixedHeight(60)

        self.datasheet_input = QLineEdit();
        self.datasheet_input.setPlaceholderText("Fayl yo'li yoki URL (bir nechta ';')")
        browse_datasheet_button = QPushButton("Fayl tanlash...")
        datasheet_layout_wrapper = QHBoxLayout();
        datasheet_layout_wrapper.addWidget(self.datasheet_input);
        datasheet_layout_wrapper.addWidget(browse_datasheet_button)

        self.reminder_date_edit = QDateEdit(calendarPopup=True)  # <<<< ИЗМЕНЕНИЯ ЗДЕСЬ
        self.reminder_date_edit.setSpecialValueText(" ")
        self.reminder_date_edit.setDate(QDate.currentDate())  # По умолчанию сегодняшняя дата
        self.reminder_date_edit.setMinimumDate(QDate.currentDate())  # Минимум - сегодняшняя дата
        self.reminder_date_edit.setMinimumWidth(120)

        self.reminder_text_input = QLineEdit();
        self.reminder_text_input.setPlaceholderText("Nima haqida eslatma?")

        self.form_layout.addRow(QLabel("Nomi*:"), self.name_input)
        self.form_layout.addRow(QLabel("Kategoriya:"), self.type_input)
        self.form_layout.addRow(QLabel("Qism Raqami:"), self.part_number_input)
        self.form_layout.addRow(QLabel("Qiymati:"), self.value_input)
        self.form_layout.addRow(QLabel("Korpus turi:"), self.package_input)

        quantity_layout = QHBoxLayout();
        quantity_layout.addWidget(QLabel("Miqdori:"));
        quantity_layout.addWidget(self.quantity_input);
        quantity_layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Expanding, QSizePolicy.Minimum));
        quantity_layout.addWidget(QLabel("Min. miqdor:"));
        quantity_layout.addWidget(self.min_quantity_input);
        self.form_layout.addRow(quantity_layout)

        self.form_layout.addRow(QLabel("Saqlash Joyi:"), self.location_input)
        self.form_layout.addRow(QLabel("Loyiha:"), self.project_input)
        self.form_layout.addRow(QLabel("Tavsif:"), self.description_input)
        self.form_layout.addRow(QLabel("Datasheet (yo'l/URL):"), datasheet_layout_wrapper)

        reminder_layout = QHBoxLayout();
        reminder_layout.addWidget(QLabel("Eslatma sanasi:"));
        reminder_layout.addWidget(self.reminder_date_edit);
        reminder_layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Expanding));
        reminder_layout.addWidget(QLabel("Eslatma matni:"));
        reminder_layout.addWidget(self.reminder_text_input, 1);
        self.form_layout.addRow(reminder_layout)
        self.layout.addLayout(self.form_layout)

        self.button_box = QDialogButtonBox();
        self.save_button = self.button_box.addButton("Saqlash", QDialogButtonBox.AcceptRole);
        self.cancel_button = self.button_box.addButton("Bekor qilish", QDialogButtonBox.RejectRole);
        self.layout.addWidget(self.button_box)

        browse_datasheet_button.clicked.connect(self.browse_datasheet_file)
        self.button_box.accepted.connect(self.validate_and_accept)
        self.button_box.rejected.connect(self.reject)
        self.name_input.textChanged.connect(self.toggle_save_button_state)

        self.load_combobox_data()

        if self.existing_data:
            self.load_data_into_fields(self.existing_data)
        else:
            if self.type_input.count() > 0:
                self.type_input.setCurrentIndex(0)
                self.update_package_combo_based_on_category(self.type_input.itemText(0))
            else:
                self.update_package_combo_based_on_category(None)

        self.type_input.currentTextChanged.connect(self.update_package_combo_based_on_category)
        self.toggle_save_button_state()

    def load_combobox_data(self):
        self.type_input.blockSignals(True)
        self.package_input.blockSignals(True)
        self.location_input.blockSignals(True)

        self.type_input.clear()
        self.type_input.addItems(get_all_categories_names())

        self.package_input.clear()
        all_pkgs = get_all_package_types_names()
        if all_pkgs: self.package_input.addItems(all_pkgs)
        if self.package_input.count() > 0: self.package_input.setCurrentIndex(-1)

        self.location_input.clear()
        self.location_input.addItems(get_all_storage_locations_names())
        if self.location_input.count() > 0: self.location_input.setCurrentIndex(-1)

        self.type_input.blockSignals(False)
        self.package_input.blockSignals(False)
        self.location_input.blockSignals(False)

    def update_package_combo_based_on_category(self, category_name):
        self.package_input.blockSignals(True)
        current_package_text = self.package_input.currentText()
        self.package_input.clear()

        packages_to_load = []
        if category_name and category_name.strip():
            packages_to_load = get_packages_for_type(category_name)
        else:
            packages_to_load = get_all_package_types_names()

        if not packages_to_load:
            packages_to_load = ["Boshqa"]

        self.package_input.addItems(packages_to_load)

        idx = self.package_input.findText(current_package_text, Qt.MatchFixedString | Qt.MatchCaseSensitive)
        if idx != -1:
            self.package_input.setCurrentIndex(idx)
        elif self.package_input.count() > 0:
            self.package_input.setCurrentIndex(0)

        self.package_input.blockSignals(False)

    def toggle_save_button_state(self):
        if hasattr(self, 'save_button') and self.save_button:
            self.save_button.setEnabled(bool(self.name_input.text().strip()))

    def browse_datasheet_file(self):
        try:
            from utils.config_manager import get_setting
            default_dir_setting = get_setting("default_datasheet_dir", "")
            start_dir = default_dir_setting if default_dir_setting and os.path.isdir(default_dir_setting) \
                else QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation)
        except ImportError:
            start_dir = QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation)

        current_paths_str = self.datasheet_input.text().strip()

        file_path, _ = QFileDialog.getOpenFileName(self, "Datasheet faylini tanlang", start_dir,
                                                   "PDF fayllari (*.pdf);;Barcha fayllar (*)")
        if file_path:
            if current_paths_str:
                self.datasheet_input.setText(current_paths_str + ";" + file_path)
            else:
                self.datasheet_input.setText(file_path)

    def _set_combobox_text_carefully(self, combobox, text_value):
        combobox.blockSignals(True)
        if text_value is None: text_value = ""

        idx = combobox.findText(text_value, Qt.MatchFixedString | Qt.MatchCaseSensitive)

        if idx != -1:
            combobox.setCurrentIndex(idx)
        elif combobox.isEditable():
            combobox.setCurrentText(text_value)
        elif combobox.count() > 0:
            combobox.setCurrentIndex(-1)
        else:
            combobox.setCurrentText("")

        combobox.blockSignals(False)

    def load_data_into_fields(self, data_dict):
        try:
            self.name_input.setText(data_dict.get('name', ''))
            self.part_number_input.setText(data_dict.get('part_number', ''))
            self.value_input.setText(data_dict.get('value', ''))
            self.quantity_input.setValue(int(data_dict.get('quantity', 0) or 0))
            self.min_quantity_input.setValue(int(data_dict.get('min_quantity', 0) or 0))
            self.project_input.setText(data_dict.get('project', ''))
            self.description_input.setPlainText(data_dict.get('description', ''))
            self.datasheet_input.setText(data_dict.get('datasheet_path', ''))

            reminder_date_str = data_dict.get('reminder_date')
            if reminder_date_str:
                reminder_qdate = QDate.fromString(reminder_date_str, "yyyy-MM-dd")
                # Устанавливаем дату, даже если она прошлая, но минимум календаря не даст выбрать прошлую
                self.reminder_date_edit.setDate(reminder_qdate if reminder_qdate.isValid() else QDate.currentDate())
            else:
                self.reminder_date_edit.setDate(QDate.currentDate())  # По умолчанию сегодня

            self.reminder_text_input.setText(data_dict.get('reminder_text', ''))

            category_to_set = data_dict.get('category_name', '')
            self._set_combobox_text_carefully(self.type_input, category_to_set)
            # Важно: после установки категории, пакеты должны обновиться.
            # Если сигнал currentTextChanged подключен *после* load_data_into_fields,
            # нужно вызвать обновление пакетов вручную или через QTimer.
            # В текущей логике __init__ сигнал подключается до вызова load_data_into_fields (если existing_data),
            # поэтому автоматическое обновление должно сработать.
            # QTimer.singleShot(0, lambda: self.update_package_combo_based_on_category(category_to_set)) # Для отложенного обновления, если нужно

            package_to_set = data_dict.get('package_type_name', '')
            # Для установки пакета может потребоваться небольшая задержка, чтобы список успел обновиться
            # Это особенно актуально, если update_package_combo_based_on_category сама по себе сложная
            QTimer.singleShot(10, lambda: self._set_combobox_text_carefully(self.package_input, package_to_set))

            self._set_combobox_text_carefully(self.location_input, data_dict.get('location_name', ''))

        except Exception as e:
            print(f"Error loading data into fields: {e}")
            QMessageBox.critical(self, "Xatolik", f"Dialog maydonlariga ma'lumotlarni yuklashda xatolik:\n{e}")
            self.close_on_error = True

    def get_data_from_fields(self):
        reminder_date = self.reminder_date_edit.date()
        reminder_date_str = None
        # Если дата не "пустая" (т.е. не просто пробел) и валидна
        if self.reminder_date_edit.text().strip() and reminder_date.isValid():
            reminder_date_str = reminder_date.toString("yyyy-MM-dd")

        data = {
            "name": self.name_input.text().strip(),
            "category": self.type_input.currentText().strip(),
            "part_number": self.part_number_input.text().strip(),
            "value": self.value_input.text().strip(),
            "package_type": self.package_input.currentText().strip(),
            "quantity": self.quantity_input.value(),
            "min_quantity": self.min_quantity_input.value(),
            "location": self.location_input.currentText().strip(),
            "project": self.project_input.text().strip(),
            "description": self.description_input.toPlainText().strip(),
            "datasheet_path": self.datasheet_input.text().strip(),
            "reminder_date": reminder_date_str,
            "reminder_text": self.reminder_text_input.text().strip()
        }
        return data

    def validate_and_accept(self):
        component_data = self.get_data_from_fields()
        if not component_data['name']:
            QMessageBox.warning(self, "Xatolik", "Komponent nomi kiritilishi shart!")
            self.name_input.setFocus()
            return

        if not component_data['category']:
            QMessageBox.warning(self, "Xatolik", "Kategoriya tanlanishi shart!")
            self.type_input.setFocus()
            return

        # Пакет может быть "Boshqa", но не должен быть пустым, если он редактируемый
        if self.package_input.isEditable() and not component_data['package_type']:
            # Если он не редактируемый и пустой - это ошибка выбора из списка
            QMessageBox.warning(self, "Xatolik", "Korpus turi tanlanishi yoki kiritilishi shart!")
            self.package_input.setFocus()
            return
        elif not self.package_input.isEditable() and self.package_input.currentIndex() == -1 and self.package_input.count() > 0:
            QMessageBox.warning(self, "Xatolik", "Korpus turi tanlanishi shart!")
            self.package_input.setFocus()
            return

        super().accept()

    def check_initialization_error(self):
        return self.close_on_error