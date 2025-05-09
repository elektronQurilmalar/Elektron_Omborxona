# ElektronKomponentlarUchoti/ui_logic/table_manager.py
import os
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor


class TableManager:
    def __init__(self, table_widget, headers_db_keys, display_headers):
        self.table_widget = table_widget
        self.headers_db_keys = headers_db_keys
        self.display_headers = display_headers
        # --- Изменяем цвет для подсветки ---
        # Старый цвет: self.low_stock_color = QColor(255, 255, 180) # Светло-желтый

        # Вариант 1: Приглушенный красноватый/розоватый (хорошо виден на темном)
        self.low_stock_color = QColor(180, 100, 100, 150)  # R, G, B, Alpha (полупрозрачный)
        # Вариант 2: Приглушенный оранжевый
        # self.low_stock_color = QColor(200, 130, 80, 150)
        # Вариант 3: Светло-серый, чуть отличающийся от основного фона текста,
        # чтобы не сильно выделялся, но был заметен (менее "тревожный")
        # self.low_stock_color = QColor(80, 80, 80) # Для фона ячейки, если текст светлый
        # self.low_stock_text_color = QColor(255, 120, 120) # Или меняем цвет текста на красный

    def _parse_value(self, value_str):
        """Qiymat matnini son va birlikka ajratishga harakat qiladi (soddalashtirilgan)."""
        if value_str is None: return None, None
        value_str = str(value_str).strip().lower()
        num_part = ""
        unit_part = ""
        for char in value_str:
            if char.isdigit() or char == '.':
                num_part += char
            else:
                unit_part += char
        try:
            return float(num_part) if num_part else None, unit_part.strip()
        except ValueError:
            return None, value_str

    def load_and_display_data(self, filters=None):
        from app_logic.db_manager import get_all_components

        db_filters = filters.copy() if filters else {}
        # value_min_str = db_filters.pop('value_min_str', None) # Эти фильтры по значению сейчас не используются
        # value_max_str = db_filters.pop('value_max_str', None)

        components_from_db = get_all_components(db_filters)

        # --- Python-сторонняя фильтрация по значению (если понадобится в будущем) ---
        # filtered_components = []
        # if value_min_str or value_max_str:
        #     val_min_num, _ = self._parse_value(value_min_str)
        #     val_max_num, _ = self._parse_value(value_max_str)
        #     # ... (логика фильтрации) ...
        #     final_components_to_display = filtered_components
        # else:
        #     final_components_to_display = components_from_db
        final_components_to_display = components_from_db  # Пока без дополнительной фильтрации здесь

        self.populate_table(final_components_to_display)
        return len(final_components_to_display)

    def populate_table(self, components_list_of_dicts):
        self.table_widget.setSortingEnabled(False)
        self.table_widget.setRowCount(0)
        self.table_widget.setColumnCount(len(self.display_headers))
        self.table_widget.setHorizontalHeaderLabels(self.display_headers)
        header = self.table_widget.horizontalHeader()

        # Получаем индексы колонок один раз
        try:
            qty_col_idx = self.headers_db_keys.index("quantity")
        except ValueError:
            qty_col_idx = -1

        try:
            desc_col_idx = self.headers_db_keys.index("description")
        except ValueError:
            desc_col_idx = -1

        try:
            reminder_text_col_idx = self.headers_db_keys.index("reminder_text")
        except ValueError:
            reminder_text_col_idx = -1

        try:
            datasheet_col_idx = self.headers_db_keys.index("datasheet_path")
        except ValueError:
            datasheet_col_idx = -1

        for i, key in enumerate(self.headers_db_keys):
            if i == desc_col_idx or i == reminder_text_col_idx:
                header.setSectionResizeMode(i, QHeaderView.Stretch)
            elif i == datasheet_col_idx:
                header.setSectionResizeMode(i, QHeaderView.Interactive);
                self.table_widget.setColumnWidth(i, 120)
            elif key in ["id", "quantity", "min_quantity", "reminder_date"]:
                header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
            else:  # name, category, part_number, value, package_type, location, project
                default_width = 110
                if key == "name":
                    default_width = 150
                elif key == "part_number":
                    default_width = 130
                elif key == "project":
                    default_width = 100
                header.setSectionResizeMode(i, QHeaderView.Interactive);
                self.table_widget.setColumnWidth(i, default_width)

        for row_idx, component_dict in enumerate(components_list_of_dicts):
            self.table_widget.insertRow(row_idx);
            is_low_stock = False;
            min_qty_val = 0
            try:
                current_qty = int(component_dict.get("quantity", 0)) if component_dict.get(
                    "quantity") is not None else 0
                min_qty_val = int(component_dict.get("min_quantity", 0)) if component_dict.get(
                    "min_quantity") is not None else 0
                if min_qty_val > 0 and current_qty <= min_qty_val:
                    is_low_stock = True
            except (ValueError, TypeError):
                pass  # Оставляем is_low_stock = False, если данные некорректны

            for col_idx, db_key in enumerate(self.headers_db_keys):
                cell_data = component_dict.get(db_key, "");
                item = QTableWidgetItem()

                # Установка данных и выравнивание
                if db_key in ["id", "quantity", "min_quantity"]:
                    try:
                        val = int(cell_data) if cell_data is not None and str(cell_data).strip() != "" else 0
                        item.setData(Qt.DisplayRole, val)
                        item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    except (ValueError, TypeError):
                        item.setText(str(cell_data) if cell_data is not None else "")
                        item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                elif db_key == "datasheet_path" and cell_data:
                    # Для datasheet в ячейке показываем только имя первого файла/ссылки, если их несколько
                    first_path = str(cell_data).split(';')[0].strip()
                    item.setText(os.path.basename(first_path) if first_path else "")
                    item.setToolTip(str(cell_data))  # Полный список в tooltip
                    item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                else:
                    item.setText(str(cell_data) if cell_data is not None else "")
                    item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)

                # Применение цвета для строк с низким запасом
                if is_low_stock:
                    item.setBackground(self.low_stock_color)
                    # Можно также изменить цвет текста для лучшей читаемости на новом фоне
                    # item.setForeground(QColor("white")) # Если фон темный

                if is_low_stock and col_idx == qty_col_idx:  # Tooltip только для колонки "Miqdori"
                    item.setToolTip(f"Minimal miqdor ({min_qty_val}) dan kam yoki teng!")

                self.table_widget.setItem(row_idx, col_idx, item)

        self.table_widget.setSortingEnabled(True)