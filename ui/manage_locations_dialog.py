# ElektronKomponentlarUchoti/ui/manage_locations_dialog.py
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QListWidget,
                             QPushButton, QMessageBox, QAbstractItemView, QLabel, QLineEdit)
from PyQt5.QtCore import Qt

try:
    from app_logic.db_manager import (get_all_storage_locations_names,
                                      add_storage_location_db,
                                      delete_storage_location_db)
except ImportError:
    print("XATOLIK: db_manager.py topilmadi yoki import qilishda muammo.")


    def get_all_storage_locations_names():
        return ["Xato: Joylar yuklanmadi"]


    def add_storage_location_db(name):
        print("DB XATOSI: Joy qo'shilmadi"); return False


    def delete_storage_location_db(name):
        print("DB XATOSI: Joy o'chirilmadi"); return False


class ManageLocationsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Saqlash Joylarini Boshqarish")
        self.setMinimumWidth(400)
        self.setModal(True)

        self.main_layout = QVBoxLayout(self)

        add_layout = QHBoxLayout()
        add_layout.addWidget(QLabel("Yangi joy nomi:"))
        self.new_location_input = QLineEdit()
        self.new_location_input.setPlaceholderText("Masalan, Polka Z9")
        add_layout.addWidget(self.new_location_input)
        self.add_new_button = QPushButton("Qo'shish")
        self.add_new_button.clicked.connect(self.add_new_location_from_input)
        add_layout.addWidget(self.add_new_button)
        self.main_layout.addLayout(add_layout)

        self.locations_list_widget = QListWidget()
        self.locations_list_widget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.populate_list()
        self.main_layout.addWidget(self.locations_list_widget)

        buttons_layout = QHBoxLayout()
        self.delete_button = QPushButton("Tanlanganni o'chirish")
        self.delete_button.clicked.connect(self.delete_selected_location)
        buttons_layout.addWidget(self.delete_button)

        self.close_button = QPushButton("Yopish")
        self.close_button.clicked.connect(self.accept)
        buttons_layout.addWidget(self.close_button)

        self.main_layout.addLayout(buttons_layout)

    def populate_list(self):
        self.locations_list_widget.clear()
        self.locations_list_widget.addItems(get_all_storage_locations_names())  # DB dan olish

    def add_new_location_from_input(self):
        new_location_text = self.new_location_input.text().strip()
        if not new_location_text:
            QMessageBox.warning(self, "Bo'sh nom", "Saqlash joyi nomi bo'sh bo'lishi mumkin emas.")
            return

        # Kichik-katta harflarni hisobga olmagan holda tekshirish (DB UNIQUE bu bilan ishlaydi)
        # Lekin foydalanuvchiga xabar berish uchun o'zimiz ham tekshiramiz
        existing_locations_lower = [loc.lower() for loc in get_all_storage_locations_names()]
        if new_location_text.lower() in existing_locations_lower:
            QMessageBox.information(self, "Mavjud", f"'{new_location_text}' saqlash joyi allaqachon mavjud.")
            self.new_location_input.clear()
            return

        if add_storage_location_db(new_location_text):  # DB ga qo'shish
            self.populate_list()
            self.new_location_input.clear()
            items = self.locations_list_widget.findItems(new_location_text, Qt.MatchExactly)
            if items: self.locations_list_widget.setCurrentItem(items[0])
        else:
            QMessageBox.warning(self, "Xatolik",
                                f"'{new_location_text}' saqlash joyini bazaga qo'shib bo'lmadi. Ehtimol, allaqachon mavjud.")

    def delete_selected_location(self):
        selected_items = self.locations_list_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Tanlanmagan", "O'chirish uchun avval saqlash joyini tanlang.")
            return

        location_to_delete = selected_items[0].text()

        reply = QMessageBox.question(self, "Tasdiqlash",
                                     f"Haqiqatdan ham '{location_to_delete}' saqlash joyini o'chirmoqchimisiz?\n"
                                     f"Agar bu joy biror komponentda ishlatilayotgan bo'lsa, o'chirilmaydi.",
                                     # Foydalanuvchiga eslatma
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            if delete_storage_location_db(location_to_delete):  # DB dan o'chirish
                self.populate_list()
            else:
                QMessageBox.warning(self, "Xatolik",
                                    f"'{location_to_delete}' saqlash joyini o'chirib bo'lmadi.\n"
                                    "Ehtimol, bu joy biror komponentda ishlatilmoqda yoki bazada topilmadi.")


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    # from app_logic.db_manager import create_tables # Test uchun
    # create_tables()

    app = QApplication(sys.argv)
    # Test uchun joy qo'shish
    # add_storage_location_db("Test Joy DB 1")
    # add_storage_location_db("Test Joy DB 2")
    dialog = ManageLocationsDialog()
    dialog.exec_()
    # print("Dialogdan keyingi saqlash joylari (bazadan):", get_all_storage_locations_names())