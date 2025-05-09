# ElektronKomponentlarUchoti/utils/component_data_lists.py

# Vaqtinchalik saqlash joylari (dastur qayta ishga tushganda yo'qoladi)
# Keyinchalik bu ma'lumotlar bazasidan olinadi
STORAGE_LOCATIONS = [
    "Quti A1", "Quti A2", "Quti A3",
    "Quti B1", "Quti B2",
    "Polka 1A", "Polka 1B",
    "Stol usti",
    "Loyihalar uchun quti"
]

def get_storage_locations():
    # Takrorlanmas va saralangan holatda qaytarish uchun set va sorted dan foydalanamiz
    return sorted(list(set(STORAGE_LOCATIONS)))

def add_storage_location(location):
    # Bo'sh yoki faqat probellardan iborat bo'lsa, qo'shmaymiz
    stripped_location = location.strip() if location else ""
    if stripped_location and stripped_location not in STORAGE_LOCATIONS:
        STORAGE_LOCATIONS.append(stripped_location)
        # print(f"Yangi saqlash joyi qo'shildi (vaqtincha): {stripped_location}") # Konsolga xabar (ixtiyoriy)
        return True
    return False

def remove_storage_location(location):
    stripped_location = location.strip() if location else ""
    if stripped_location in STORAGE_LOCATIONS:
        STORAGE_LOCATIONS.remove(stripped_location)
        # print(f"Saqlash joyi o'chirildi (vaqtincha): {stripped_location}") # Konsolga xabar (ixtiyoriy)
        return True
    return False