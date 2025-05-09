import os
import csv
import pandas as pd
import webbrowser
import urllib.parse
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, \
    QHBoxLayout, QDialogButtonBox, QLabel
from PyQt5.QtCore import Qt

from .db_manager import delete_component, get_all_components


def delete_selected_components(main_window_instance):
    table_widget = main_window_instance.table_widget
    selected_rows = table_widget.selectionModel().selectedRows()
    if not selected_rows:
        QMessageBox.warning(main_window_instance, "Xatolik", "O'chirish uchun komponent(lar) tanlang!")
        return

    ids_to_delete = []
    names_to_delete = []
    id_col_idx = main_window_instance.table_headers_db_keys.index('id')
    name_col_idx = main_window_instance.table_headers_db_keys.index('name')

    for model_index in selected_rows:
        row = model_index.row()
        try:
            id_item = table_widget.item(row, id_col_idx)
            name_item = table_widget.item(row, name_col_idx)
            if id_item and name_item:
                ids_to_delete.append(int(id_item.text()))
                names_to_delete.append(name_item.text())
            else:
                raise ValueError("ID yoki Nomi katakchasi bo'sh.")
        except (AttributeError, ValueError, TypeError) as e:
            QMessageBox.warning(main_window_instance, "Xatolik", f"{row + 1}-qatordagi ID/Nomni o'qib bo'lmadi: {e}");
            return

    if not ids_to_delete: return

    confirm_delete_setting = True
    if hasattr(main_window_instance, 'settings') and 'confirm_delete' in main_window_instance.settings:
        confirm_delete_setting = main_window_instance.settings['confirm_delete']

    reply = QMessageBox.Yes
    if confirm_delete_setting:
        reply = QMessageBox.question(main_window_instance, "Tasdiqlash",
                                     f"{len(ids_to_delete)} ta komponentni o'chirmoqchimisiz?\n({', '.join(names_to_delete[:5])}{'...' if len(names_to_delete) > 5 else ''})",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

    if reply == QMessageBox.Yes:
        deleted_count = 0;
        error_count = 0
        for comp_id in ids_to_delete:
            if delete_component(comp_id):
                deleted_count += 1
            else:
                error_count += 1
        main_window_instance.statusBar().showMessage(f"{deleted_count} ta o'chirildi, {error_count} ta xatolik.", 5000)
        main_window_instance.refresh_all_data_and_filters()
    else:
        main_window_instance.statusBar().showMessage("O'chirish bekor qilindi.", 3000)


def search_selected_component_online(main_window_instance):
    table_widget = main_window_instance.table_widget
    selected_rows = table_widget.selectionModel().selectedRows()
    if len(selected_rows) != 1:
        QMessageBox.warning(main_window_instance, "Tanlanmagan", "Qidirish uchun bitta komponent tanlang!")
        return

    current_row = selected_rows[0].row()
    search_terms = []
    try:
        name_idx = main_window_instance.table_headers_db_keys.index('name')
        part_num_idx = main_window_instance.table_headers_db_keys.index('part_number')
        value_idx = main_window_instance.table_headers_db_keys.index('value')
        package_idx = main_window_instance.table_headers_db_keys.index('package_type_name')

        name_item = table_widget.item(current_row, name_idx);
        part_num_item = table_widget.item(current_row, part_num_idx)
        value_item = table_widget.item(current_row, value_idx);
        package_item = table_widget.item(current_row, package_idx)

        part_num = part_num_item.text().strip() if part_num_item else "";
        name = name_item.text().strip() if name_item else ""
        value = value_item.text().strip() if value_item else "";
        package = package_item.text().strip() if package_item else ""

        if part_num:
            search_terms.append(part_num)
        elif name:
            search_terms.append(name)
        else:
            QMessageBox.warning(main_window_instance, "Ma'lumot yetarli emas",
                                "Komponent nomi yoki qism raqami yo'q.");
            return

        if value and value != '-': search_terms.append(value)
        if package and package.lower() != 'boshqa' and package.lower() != 'n/a': search_terms.append(package)

    except (AttributeError, ValueError, IndexError, TypeError) as e:
        QMessageBox.critical(main_window_instance, "Xatolik", f"Qidiruv uchun ma'lumot olishda xato: {e}");
        return

    if search_terms:
        full_search_query = " ".join(search_terms);
        query = urllib.parse.quote_plus(full_search_query)
        url = f"https://www.google.com/search?q={query}"
        print(f"Opening browser for search: {url}")
        try:
            webbrowser.open(url);
            main_window_instance.statusBar().showMessage(
                f"'{full_search_query}' uchun qidirilmoqda...", 3000)
        except Exception as e_web:
            QMessageBox.critical(main_window_instance, "Xatolik", f"Brauzerni ochishda xatolik: {e_web}")


def export_data_dialog(main_window_instance):
    all_db_components = get_all_components()
    if not all_db_components:
        QMessageBox.warning(main_window_instance, "Eksport xatosi", "Eksport uchun ma'lumotlar bazada mavjud emas.")
        return
    export_db_keys = main_window_instance.table_headers_db_keys
    headers_for_export = main_window_instance.table_display_headers
    data_to_export = []
    for comp_dict in all_db_components:
        row_data = []
        for key in export_db_keys:
            row_data.append(comp_dict.get(key, ""))
        data_to_export.append(row_data)

    options = QFileDialog.Options()
    last_export_dir = main_window_instance.settings.get("last_export_dir", os.path.expanduser("~"))
    file_path, selected_filter = QFileDialog.getSaveFileName(
        main_window_instance, "Ma'lumotlarni eksport qilish",
        os.path.join(last_export_dir, "komponentlar_hisoboti"),
        "Excel fayllari (*.xlsx);;CSV fayllari (*.csv)", options=options)

    if file_path:
        main_window_instance.settings["last_export_dir"] = os.path.dirname(file_path)
        from utils.config_manager import save_settings
        save_settings(main_window_instance.settings)

        default_excel_ext = ".xlsx";
        default_csv_ext = ".csv"
        try:
            if selected_filter == "Excel fayllari (*.xlsx)":
                if not file_path.lower().endswith(default_excel_ext): file_path += default_excel_ext
                _export_to_excel(main_window_instance, file_path, data_to_export, headers_for_export)
            elif selected_filter == "CSV fayllari (*.csv)":
                if not file_path.lower().endswith(default_csv_ext): file_path += default_csv_ext
                _export_to_csv(main_window_instance, file_path, data_to_export, headers_for_export)
            else:
                if file_path.lower().endswith(default_excel_ext):
                    _export_to_excel(main_window_instance, file_path, data_to_export, headers_for_export)
                elif file_path.lower().endswith(default_csv_ext):
                    _export_to_csv(main_window_instance, file_path, data_to_export, headers_for_export)
                else:
                    file_path += default_excel_ext;
                    _export_to_excel(main_window_instance, file_path, data_to_export,
                                     headers_for_export)
        except Exception as e:
            QMessageBox.critical(main_window_instance, "Eksport xatosi", f"Eksport qilishda kutilmagan xatolik:\n{e}")


def _export_to_excel(main_window_instance, file_path, data, headers):
    try:
        df = pd.DataFrame(data, columns=headers)
        df.to_excel(file_path, index=False, engine='openpyxl')
        main_window_instance.statusBar().showMessage(f"'{os.path.basename(file_path)}' ga eksport qilindi.", 5000)
        QMessageBox.information(main_window_instance, "Eksport", f"'{file_path}' ga saqlandi.")
    except Exception as e:
        QMessageBox.critical(main_window_instance, "Excel Eksport Xatosi", f"Xatolik:\n{e}")


def _export_to_csv(main_window_instance, file_path, data, headers):
    try:
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=';');
            writer.writerow(headers);
            writer.writerows(data)
        main_window_instance.statusBar().showMessage(f"'{os.path.basename(file_path)}' ga eksport qilindi.", 5000)
        QMessageBox.information(main_window_instance, "Eksport", f"'{file_path}' ga saqlandi.")
    except Exception as e:
        QMessageBox.critical(main_window_instance, "CSV Eksport Xatosi", f"Xatolik:\n{e}")


def generate_label_for_selected(main_window_instance):
    table_widget = main_window_instance.table_widget
    selected_rows_indices = table_widget.selectionModel().selectedRows()
    if not selected_rows_indices:
        QMessageBox.warning(main_window_instance, "Tanlanmagan", "Etiketka uchun komponent tanlang.");
        return

    label_texts = [];
    for model_index in selected_rows_indices:
        row = model_index.row();
        label_text = "";
        comp_data = {}
        try:
            for i, key in enumerate(main_window_instance.table_headers_db_keys):
                item = table_widget.item(row, i);
                if key == "datasheet_path" and item:
                    comp_data[key] = item.toolTip() if item.toolTip() else item.text()
                else:
                    comp_data[key] = item.text() if item else ""

            label_text = f"** {comp_data.get('name', 'N/A')} **\n";
            if comp_data.get('part_number'): label_text += f"PN: {comp_data['part_number']}\n"
            if comp_data.get('value'): label_text += f"Qiymat: {comp_data['value']}\n"
            if comp_data.get('package_type_name'): label_text += f"Korpus: {comp_data['package_type_name']}\n"
            if comp_data.get('location_name'): label_text += f"Joy: {comp_data['location_name']}\n"
            label_text += f"ID: {comp_data.get('id', 'N/A')}";
            label_texts.append(label_text)
        except Exception as e:
            print(f"Etiketka ma'lumoti xatosi (qator {row}): {e}");
            continue

    if label_texts:
        full_label_content = "\n\n---\n\n".join(label_texts);
        msg_box = QMessageBox(main_window_instance);
        msg_box.setWindowTitle("Generatsiya qilingan Etiketkalar")
        msg_box.setText("Quyidagi etiketka(lar) generatsiya qilindi:");
        msg_box.setDetailedText(full_label_content)
        msg_box.setTextInteractionFlags(Qt.TextSelectableByMouse)
        msg_box.setIcon(QMessageBox.Information);
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Save)
        button_save = msg_box.button(QMessageBox.Save);
        button_save.setText("Faylga saqlash...")
        ret = msg_box.exec_();
        if ret == QMessageBox.Save:
            _save_labels_to_file(main_window_instance, full_label_content)


def _save_labels_to_file(main_window_instance, content):
    options = QFileDialog.Options();
    last_export_dir = main_window_instance.settings.get("last_export_dir", os.path.expanduser("~"))
    file_path, _ = QFileDialog.getSaveFileName(main_window_instance, "Etiketkalarni faylga saqlash",
                                               os.path.join(last_export_dir, "etiketkalar.txt"),
                                               "Matnli fayllar (*.txt);;Barcha fayllar (*)", options=options)
    if file_path:
        main_window_instance.settings["last_export_dir"] = os.path.dirname(file_path)
        from utils.config_manager import save_settings
        save_settings(main_window_instance.settings)
        try:
            if not file_path.lower().endswith(".txt"): file_path += ".txt"
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            QMessageBox.information(main_window_instance, "Muvaffaqiyatli", f"Etiketkalar '{file_path}' ga saqlandi.")
        except Exception as e:
            QMessageBox.critical(main_window_instance, "Xatolik", f"Faylga saqlashda xatolik:\n{e}")


class GenerateOrderListDialog(QDialog):  # <<<< ИЗМЕНЕНИЯ ЗДЕСЬ (для пункта 2)
    def __init__(self, parent=None, low_stock_components=None, bom_needed_components=None):
        super().__init__(parent)
        self.setWindowTitle("Buyurtma uchun ro'yxat")
        self.setMinimumSize(850, 500)  # Увеличил для новых колонок
        self.main_window = parent
        layout = QVBoxLayout(self)

        self.table_widget = QTableWidget()
        # Обновляем заголовки таблицы
        self.table_widget.setColumnCount(8)
        self.table_widget.setHorizontalHeaderLabels([
            "Nomi", "Qism Raqami", "Kategoriya", "Qiymati", "Korpus",  # Добавлены "Qiymati", "Korpus"
            "Omborda", "Min. Miqdor", "Buyurtma qilish kerak"
        ])
        layout.addWidget(self.table_widget)

        self.populate_table(low_stock_components, bom_needed_components)

        button_box = QDialogButtonBox(QDialogButtonBox.Close | QDialogButtonBox.Save)
        button_box.button(QDialogButtonBox.Close).setText("Yopish")
        button_box.rejected.connect(self.reject)

        button_export = button_box.button(QDialogButtonBox.Save)
        button_export.setText("CSV ga eksport")
        button_export.clicked.connect(self.export_to_csv)
        layout.addWidget(button_box)

    def populate_table(self, low_stock_components, bom_needed_components):  # <<<< ИЗМЕНЕНИЯ ЗДЕСЬ
        self.table_widget.setSortingEnabled(False)
        self.table_widget.setRowCount(0)

        components_to_order = {}

        if low_stock_components:
            for comp in low_stock_components:
                comp_id = comp.get('id')
                if comp_id not in components_to_order:
                    components_to_order[comp_id] = comp.copy()
                    components_to_order[comp_id]['needed_for_stock'] = max(0, int(comp.get('min_quantity', 0)) - int(
                        comp.get('quantity', 0)))
                else:
                    components_to_order[comp_id]['needed_for_stock'] = max(
                        components_to_order[comp_id].get('needed_for_stock', 0),
                        max(0, int(comp.get('min_quantity', 0)) - int(comp.get('quantity', 0)))
                    )

        for comp_id, comp_data in components_to_order.items():
            to_order_val = comp_data.get('needed_for_stock', 0)
            if to_order_val <= 0: continue

            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)

            self.table_widget.setItem(row_position, 0, QTableWidgetItem(comp_data.get('name')))
            self.table_widget.setItem(row_position, 1, QTableWidgetItem(comp_data.get('part_number')))
            self.table_widget.setItem(row_position, 2, QTableWidgetItem(comp_data.get('category_name')))
            self.table_widget.setItem(row_position, 3, QTableWidgetItem(comp_data.get('value')))  # Номинал
            self.table_widget.setItem(row_position, 4, QTableWidgetItem(comp_data.get('package_type_name')))  # Корпус

            qty_item = QTableWidgetItem()
            qty_item.setData(Qt.DisplayRole, int(comp_data.get('quantity', 0)))
            self.table_widget.setItem(row_position, 5, qty_item)  # Индекс сдвинулся

            min_qty_item = QTableWidgetItem()
            min_qty_item.setData(Qt.DisplayRole, int(comp_data.get('min_quantity', 0)))
            self.table_widget.setItem(row_position, 6, min_qty_item)  # Индекс сдвинулся

            needed_item = QTableWidgetItem()
            needed_item.setData(Qt.DisplayRole, to_order_val)
            self.table_widget.setItem(row_position, 7, needed_item)  # Индекс сдвинулся

        self.table_widget.resizeColumnsToContents()
        self.table_widget.setSortingEnabled(True)

    def get_order_data_for_export(self):  # <<<< ИЗМЕНЕНИЯ ЗДЕСЬ
        data = []
        headers = [self.table_widget.horizontalHeaderItem(i).text() for i in range(self.table_widget.columnCount())]

        for row in range(self.table_widget.rowCount()):
            row_data = {}
            # Собираем данные в соответствии с заголовками для DictWriter
            # Индексы должны соответствовать порядку в self.table_widget.setHorizontalHeaderLabels
            row_data[headers[0]] = self.table_widget.item(row, 0).text()  # Nomi
            row_data[headers[1]] = self.table_widget.item(row, 1).text()  # Qism Raqami
            row_data[headers[2]] = self.table_widget.item(row, 2).text()  # Kategoriya
            row_data[headers[3]] = self.table_widget.item(row, 3).text()  # Qiymati
            row_data[headers[4]] = self.table_widget.item(row, 4).text()  # Korpus
            row_data[headers[5]] = self.table_widget.item(row, 5).text()  # Omborda
            row_data[headers[6]] = self.table_widget.item(row, 6).text()  # Min. Miqdor
            row_data[headers[7]] = self.table_widget.item(row, 7).text()  # Buyurtma qilish kerak

            if int(row_data[headers[7]]) > 0:  # Проверяем по колонке "Buyurtma qilish kerak"
                data.append(row_data)
        return data, headers

    def export_to_csv(self):
        order_data, headers = self.get_order_data_for_export()
        if not order_data:
            QMessageBox.information(self, "Ma'lumot yo'q",
                                    "Buyurtma ro'yxatiga eksport qilish uchun komponentlar yo'q.")
            return

        options = QFileDialog.Options()
        last_export_dir = self.main_window.settings.get("last_export_dir", os.path.expanduser("~"))
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Buyurtma ro'yxatini eksport qilish", os.path.join(last_export_dir, "buyurtma_royxati.csv"),
            "CSV-fayllar (*.csv)", options=options)

        if file_path:
            self.main_window.settings["last_export_dir"] = os.path.dirname(file_path)
            from utils.config_manager import save_settings
            save_settings(self.main_window.settings)

            try:
                if not file_path.lower().endswith(".csv"): file_path += ".csv"
                with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                    if order_data:
                        writer = csv.DictWriter(csvfile, fieldnames=headers, delimiter=';')
                        writer.writeheader()
                        writer.writerows(order_data)
                QMessageBox.information(self, "Eksport", f"Buyurtma ro'yxati '{file_path}' ga saqlandi.")
            except Exception as e:
                QMessageBox.critical(self, "Eksport xatosi", f"Ro'yxatni eksport qilib bo'lmadi: {e}")


def generate_order_list_action(main_window_instance):
    all_components = get_all_components()
    if not all_components:
        QMessageBox.information(main_window_instance, "Ma'lumot yo'q", "Bazadagi komponentlar yo'q.")
        return

    low_stock_components = [
        comp for comp in all_components
        if comp.get('min_quantity', 0) > 0 and comp.get('quantity', 0) < comp.get('min_quantity', 0)
    ]

    if not low_stock_components:
        QMessageBox.information(main_window_instance, "Hammasi joyida",
                                "Buyurtma talab qiladigan komponentlar yo'q (minimal miqdordan kam).")
        return

    dialog = GenerateOrderListDialog(main_window_instance, low_stock_components=low_stock_components)
    dialog.exec_()
