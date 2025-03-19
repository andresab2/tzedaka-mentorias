import sqlite3


def list_contacts():
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute('SELECT * FROM contacts')
    contacts = c.fetchall()
    conn.close()
    return contacts


def print_contacts(contacts):
    if not contacts:
        print("No hay contactos guardados.")
        return

    print("Contactos guardados:")
    for contact in contacts:
        print(f"ID: {contact[0]}")
        print(f"Nombre: {contact[1]}")
        print(f"Email: {contact[2]}")
        print(f"Teléfono: {contact[3]}")
        print(f"Mensaje: {contact[4]}")
        print(f"Fecha: {contact[5]}")
        print("-" * 40)


if __name__ == '__main__':
    contacts = list_contacts()
    print_contacts(contacts) 