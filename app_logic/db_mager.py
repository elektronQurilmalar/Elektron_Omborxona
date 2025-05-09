# ElektronKomponentlarUchoti/app_logic/db_manager.py
import sqlite3
import os

try:
    # Эту переменную теперь будем использовать для начального заполнения
    from utils.component_packages import COMPONENT_PACKAGES as INITIAL_COMPONENT_PACKAGES_DEFINITIONS
except ImportError:
    print("OGOHLANTIRISH: Standart paketlar ro'yxati (utils/component_packages.py) topilmadi.")
    # Определяем запасной вариант, если файл не найден
    INITIAL_COMPONENT_PACKAGES_DEFINITIONS = {
        "Passiv": ["0805 (SMD)", "Axial (Through-Hole Rezistor)", "Boshqa (Passiv)"],
        "Diod": ["SOD-123", "DO-41", "Boshqa (Diod)"],
        "Boshqa Komponentlar": ["Noma'lum", "Boshqa"]
    }

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, "database")
DB_NAME = "components_inventory.db"
DB_PATH = os.path.join(DB_DIR, DB_NAME)

os.makedirs(DB_DIR, exist_ok=True)


def get_db_connection():
    conn = None;
    try:
        conn = sqlite3.connect(DB_PATH);
        conn.row_factory = sqlite3.Row;
        conn.execute(
            "PRAGMA foreign_keys = ON;");
        return conn
    except sqlite3.Error as e:
        print(f"DB Connection Error: {e}");
        return None


def close_db_connection(conn):
    if conn: conn.close()


def create_tables():
    conn = get_db_connection();
    if conn is None: return False
    tables_created_or_exist = False
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS components (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category_id INTEGER,
                part_number TEXT,
                value TEXT,
                package_type_id INTEGER,
                quantity INTEGER DEFAULT 0,
                min_quantity INTEGER DEFAULT 0,
                location_id INTEGER,
                description TEXT,
                datasheet_path TEXT, 
                project TEXT,
                reminder_date TEXT, 
                reminder_text TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE (name, part_number, value, package_type_id), 
                FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE SET NULL,
                FOREIGN KEY (package_type_id) REFERENCES package_types (id) ON DELETE SET NULL,
                FOREIGN KEY (location_id) REFERENCES storage_locations (id) ON DELETE SET NULL
            )
        """)
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS categories (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE)")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS package_types (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE)")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS storage_locations (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE)")

        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS update_components_updated_at
            AFTER UPDATE ON components
            FOR EACH ROW
            BEGIN
                UPDATE components SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
            END;
        """)
        conn.commit();
        print("Tables created or already exist.");
        tables_created_or_exist = True
        populate_initial_reference_data(conn)
    except sqlite3.Error as e:
        print(f"Table creation error: {e}")
    finally:
        close_db_connection(conn)
    return tables_created_or_exist


def populate_initial_reference_data(conn):  # <<<< ИЗМЕНЕНИЯ ЗДЕСЬ
    if conn is None: return
    try:
        cursor = conn.cursor()
        # Используем INITIAL_COMPONENT_PACKAGES_DEFINITIONS для начальных данных
        initial_categories = list(INITIAL_COMPONENT_PACKAGES_DEFINITIONS.keys())

        all_packages_from_definitions = set()
        for cat_name, pkg_list in INITIAL_COMPONENT_PACKAGES_DEFINITIONS.items():
            for pkg_name in pkg_list:
                all_packages_from_definitions.add(pkg_name)
        # Добавляем общий "Boshqa", если его нет, на случай если он не указан ни для одной категории
        if "Boshqa" not in all_packages_from_definitions:
            all_packages_from_definitions.add("Boshqa")

        inserted_categories_count = 0
        for category_name in initial_categories:
            try:
                cursor.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (category_name,))
                if cursor.rowcount > 0:
                    inserted_categories_count += 1
            except sqlite3.Error as e_inner:
                print(f"Error inserting category '{category_name}': {e_inner}")

        inserted_packages_count = 0
        for package_name in sorted(list(all_packages_from_definitions)):  # Сортируем для консистентности
            try:
                cursor.execute("INSERT OR IGNORE INTO package_types (name) VALUES (?)", (package_name,))
                if cursor.rowcount > 0:
                    inserted_packages_count += 1
            except sqlite3.Error as e_inner:
                print(f"Error inserting package type '{package_name}': {e_inner}")

        if inserted_categories_count > 0 or inserted_packages_count > 0:
            print(
                f"Populated initial data: {inserted_categories_count} categories, {inserted_packages_count} package types.")
            conn.commit()
    except Exception as e:  # Более общее исключение для отладки
        print(f"Error populating initial reference data: {e}")


def get_or_create_id(table_name, name, conn):
    if not name or not name.strip() or not table_name or conn is None: return None
    row_id = None
    last_id = -1
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT id FROM {table_name} WHERE LOWER(name) = LOWER(?)", (name.strip(),))
        row = cursor.fetchone()
        if row:
            row_id = row['id']
        else:
            cursor.execute(f"INSERT INTO {table_name} (name) VALUES (?)", (name.strip(),))
            last_id = cursor.lastrowid
            row_id = last_id
            # print(f"New entry: '{name.strip()}' (ID: {row_id}) in '{table_name}'") # Закомментировано для уменьшения вывода
    except sqlite3.IntegrityError:
        try:
            cursor.execute(f"SELECT id FROM {table_name} WHERE LOWER(name) = LOWER(?)", (name.strip(),))
            row = cursor.fetchone()
            if row: row_id = row['id']
        except sqlite3.Error as e_inner:
            print(f"Error re-fetching ID for '{name.strip()}' after IntegrityError: {e_inner}")
    except sqlite3.Error as e:
        print(f"Error in get_or_create_id for '{name.strip()}' in '{table_name}': {e}")

    return row_id if row_id is not None else (last_id if last_id > 0 else None)


def get_or_create_category_id(name, conn): return get_or_create_id("categories", name, conn)


def get_or_create_package_type_id(name, conn): return get_or_create_id("package_types", name, conn)


def get_or_create_location_id(name, conn): return get_or_create_id("storage_locations", name, conn)


def add_component(data):
    conn = get_db_connection();
    if conn is None: return None; new_id = None
    try:
        category_id = get_or_create_category_id(data.get('category'), conn)
        package_type_id = get_or_create_package_type_id(data.get('package_type'), conn)
        location_id = get_or_create_location_id(data.get('location'), conn)

        sql = """
            INSERT INTO components (
                name, category_id, part_number, value, package_type_id, 
                quantity, min_quantity, location_id, description, 
                datasheet_path, project, reminder_date, reminder_text
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor = conn.cursor();
        cursor.execute(sql, (
            data.get('name'), category_id, data.get('part_number'), data.get('value'), package_type_id,
            data.get('quantity', 0), data.get('min_quantity', 0), location_id, data.get('description'),
            data.get('datasheet_path'), data.get('project'), data.get('reminder_date'),
            data.get('reminder_text')
        ));
        new_id = cursor.lastrowid;
        conn.commit()
    except sqlite3.IntegrityError as e:
        print(f"Component add integrity error (возможно, дубликат): {e}. Data: {data}")
    except sqlite3.Error as e:
        print(f"Component add error: {e}")
    finally:
        close_db_connection(conn)
    return new_id


def get_all_components(filters=None):
    conn = get_db_connection();
    if conn is None: return []
    try:
        base_sql = """
            SELECT comp.id, comp.name, cat.name as category_name, comp.part_number, comp.value, 
                   pkg.name as package_type_name, comp.quantity, comp.min_quantity, 
                   loc.name as location_name, comp.project, comp.description, comp.datasheet_path, 
                   comp.reminder_date, comp.reminder_text, comp.created_at, comp.updated_at 
            FROM components comp 
            LEFT JOIN categories cat ON comp.category_id = cat.id 
            LEFT JOIN package_types pkg ON comp.package_type_id = pkg.id 
            LEFT JOIN storage_locations loc ON comp.location_id = loc.id
        """
        where_clauses = [];
        params = []

        if filters:
            if filters.get('search_text') and not (
                    filters.get('adv_name') or filters.get('adv_part_number') or filters.get('adv_value')):
                st = f"%{filters['search_text']}%";
                search_fields_clause = """
                    (LOWER(comp.name) LIKE LOWER(?) OR LOWER(comp.part_number) LIKE LOWER(?) OR 
                     LOWER(comp.value) LIKE LOWER(?) OR LOWER(comp.description) LIKE LOWER(?) OR 
                     LOWER(cat.name) LIKE LOWER(?) OR LOWER(pkg.name) LIKE LOWER(?) OR 
                     LOWER(loc.name) LIKE LOWER(?) OR LOWER(comp.project) LIKE LOWER(?))
                """
                where_clauses.append(search_fields_clause);
                params.extend([st] * 8)

            if filters.get('category_name') and filters['category_name'] != "Barcha kategoriyalar":
                where_clauses.append("cat.name = ?");
                params.append(filters['category_name'])
            if filters.get('project_name') and filters['project_name'] != "Barcha loyihalar":
                if filters['project_name'] == '':
                    where_clauses.append("(comp.project IS NULL OR comp.project = '')")
                else:
                    where_clauses.append("comp.project = ?");
                    params.append(filters['project_name'])

            if filters.get('low_stock_only'):
                where_clauses.append("(comp.min_quantity > 0 AND comp.quantity <= comp.min_quantity)")

            if filters.get('adv_name'):
                where_clauses.append("LOWER(comp.name) LIKE LOWER(?)")
                params.append(f"%{filters['adv_name']}%")
            if filters.get('adv_part_number'):
                where_clauses.append("LOWER(comp.part_number) LIKE LOWER(?)")
                params.append(f"%{filters['adv_part_number']}%")
            if filters.get('adv_value'):
                where_clauses.append("LOWER(comp.value) LIKE LOWER(?)")
                params.append(f"%{filters['adv_value']}%")

            if 'quantity_min' in filters and filters['quantity_min'] != -1:  # Учитываем -1 как "не важно"
                where_clauses.append("comp.quantity >= ?")
                params.append(filters['quantity_min'])
            if 'quantity_max' in filters and filters['quantity_max'] != -1:
                where_clauses.append("comp.quantity <= ?")
                params.append(filters['quantity_max'])

        if where_clauses: base_sql += " WHERE " + " AND ".join(where_clauses)
        base_sql += " ORDER BY comp.name ASC"

        cursor = conn.cursor();
        cursor.execute(base_sql, tuple(params));
        components = cursor.fetchall()
        return [dict(row) for row in components]
    except sqlite3.Error as e:
        print(f"Error fetching components: {e}");
        return []
    finally:
        close_db_connection(conn)


def get_component_by_id(component_id):
    conn = get_db_connection();
    if conn is None: return None
    try:
        sql = """
            SELECT comp.*, cat.name as category_name, pkg.name as package_type_name, loc.name as location_name 
            FROM components comp 
            LEFT JOIN categories cat ON comp.category_id = cat.id 
            LEFT JOIN package_types pkg ON comp.package_type_id = pkg.id 
            LEFT JOIN storage_locations loc ON comp.location_id = loc.id 
            WHERE comp.id = ?
        """
        cursor = conn.cursor();
        cursor.execute(sql, (component_id,));
        component = cursor.fetchone()
        return dict(component) if component else None
    except sqlite3.Error as e:
        print(f"Error fetching component by ID {component_id}: {e}");
        return None
    finally:
        close_db_connection(conn)


def update_component(component_id, data):
    conn = get_db_connection();
    if conn is None: return False; success = False
    try:
        category_id = get_or_create_category_id(data.get('category'), conn)
        package_type_id = get_or_create_package_type_id(data.get('package_type'), conn)
        location_id = get_or_create_location_id(data.get('location'), conn)
        sql = """
            UPDATE components SET 
                name = ?, category_id = ?, part_number = ?, value = ?, package_type_id = ?, 
                quantity = ?, min_quantity = ?, location_id = ?, description = ?, 
                datasheet_path = ?, project = ?, reminder_date = ?, reminder_text = ?
            WHERE id = ?
        """
        cursor = conn.cursor();
        cursor.execute(sql, (
            data.get('name'), category_id, data.get('part_number'), data.get('value'), package_type_id,
            data.get('quantity'), data.get('min_quantity'), location_id, data.get('description'),
            data.get('datasheet_path'), data.get('project'), data.get('reminder_date'),
            data.get('reminder_text'), component_id
        ));
        conn.commit();
        success = cursor.rowcount > 0
    except sqlite3.IntegrityError as e:
        print(f"Component update integrity error (возможно, дубликат после изменения): {e}. Data: {data}")
    except sqlite3.Error as e:
        print(f"Component update error: {e}")
    finally:
        close_db_connection(conn)
    return success


def delete_component(component_id):
    conn = get_db_connection();
    if conn is None: return False; success = False
    try:
        sql = "DELETE FROM components WHERE id = ?";
        cursor = conn.cursor();
        cursor.execute(sql, (component_id,));
        conn.commit();
        success = cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Component delete error: {e}")
    finally:
        close_db_connection(conn)
    return success


def get_distinct_project_names():
    conn = get_db_connection();
    if conn is None: return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT project FROM components WHERE project IS NOT NULL ORDER BY project ASC")
        projects = [row['project'] for row in cursor.fetchall()]
        return projects

    except sqlite3.Error as e:
        print(f"Error fetching distinct project names: {e}");
        return []
    finally:
        close_db_connection(conn)


def get_all_categories_names():
    conn = get_db_connection();
    if conn is None: return []
    try:
        cursor = conn.cursor();
        cursor.execute("SELECT name FROM categories ORDER BY name ASC");
        return [row['name'] for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"Error fetching category names: {e}");
        return []
    finally:
        close_db_connection(conn)


def get_all_package_types_names():  # <<<< ИЗМЕНЕНИЯ ЗДЕСЬ
    conn = get_db_connection();
    if conn is None: return []
    try:
        cursor = conn.cursor();
        cursor.execute("SELECT name FROM package_types ORDER BY name ASC");
        package_names = [row['name'] for row in cursor.fetchall()]
        # Убедимся, что "Boshqa" всегда присутствует, если есть хоть какие-то пакеты
        if package_names and "Boshqa" not in package_names:
            # Проверяем, нет ли уже специфичного "Boshqa (Kategoriya)"
            has_specific_boshqa = any(name.startswith("Boshqa (") and name.endswith(")") for name in package_names)
            if not has_specific_boshqa:
                package_names.append("Boshqa")
                package_names.sort()  # Пересортируем
        elif not package_names:  # Если база пуста, добавляем "Boshqa"
            package_names.append("Boshqa")

        return package_names
    except sqlite3.Error as e:
        print(f"Error fetching package type names: {e}");
        return []
    finally:
        close_db_connection(conn)


def get_all_storage_locations_names():
    conn = get_db_connection();
    if conn is None: return []
    try:
        cursor = conn.cursor();
        cursor.execute("SELECT name FROM storage_locations ORDER BY name ASC");
        return [row['name'] for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"Error fetching storage location names: {e}");
        return []
    finally:
        close_db_connection(conn)


def add_category_db(name):
    conn = get_db_connection()
    if conn is None or not name or not name.strip(): return False
    try:
        get_or_create_category_id(name, conn)
        # conn.commit() # get_or_create_id уже коммитит, если создает
        return True
    except sqlite3.Error as e:
        print(f"Category add DB error for '{name}': {e}")
        return False
    finally:
        close_db_connection(conn)


def delete_category_db(name):
    conn = get_db_connection();
    if conn is None: return False; success = False
    try:
        cursor = conn.cursor();
        cursor.execute(
            "SELECT COUNT(*) as count FROM components c JOIN categories cat ON c.category_id = cat.id WHERE LOWER(cat.name) = LOWER(?)",
            (name,))
        if cursor.fetchone()['count'] > 0:
            print(f"Cannot delete category '{name}' as it is in use.");
            return False

        cursor.execute("DELETE FROM categories WHERE LOWER(name) = LOWER(?)", (name,));
        conn.commit();
        success = cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Category delete DB error for '{name}': {e}")
    finally:
        close_db_connection(conn)
    return success


def add_storage_location_db(name):
    conn = get_db_connection()
    if conn is None or not name or not name.strip(): return False
    try:
        get_or_create_location_id(name, conn)
        # conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Location add DB error for '{name}': {e}")
        return False
    finally:
        close_db_connection(conn)


def delete_storage_location_db(name):
    conn = get_db_connection();
    if conn is None: return False; success = False
    try:
        cursor = conn.cursor();
        cursor.execute(
            "SELECT COUNT(*) as count FROM components c JOIN storage_locations sl ON c.location_id = sl.id WHERE LOWER(sl.name) = LOWER(?)",
            (name,))
        if cursor.fetchone()['count'] > 0:
            print(f"Cannot delete location '{name}' as it is in use.");
            return False

        cursor.execute("DELETE FROM storage_locations WHERE LOWER(name) = LOWER(?)", (name,));
        conn.commit();
        success = cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Location delete DB error for '{name}': {e}")
    finally:
        close_db_connection(conn)
    return success


if __name__ == '__main__':
    if create_tables():
        print("DB and tables are ready for testing.")
        print("Categories from DB:", get_all_categories_names())
        print("Package types from DB:", get_all_package_types_names())
        print("Projects from DB:", get_distinct_project_names())
    else:
        print("Failed to initialize database and tables.")
