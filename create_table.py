from supabase import create_client, Client
import sys

SUPABASE_URL = "https://jqmwzrkiutwifeswntzt.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpxbXd6cmtpdXR3aWZlc3dudHp0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDIzOTI3NzEsImV4cCI6MjA1Nzk2ODc3MX0.ykzCpmcgcIxS46__o8FYREWU06togj64AvRs7Ktb2_s"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def create_contacts_table():
    try:
        # Crear la tabla contacts con la estructura correcta
        response = supabase.table("contacts").select("*").limit(1).execute()
        print("La tabla contacts ya existe.")
        
        # Verificar si tiene todas las columnas necesarias
        data = {
            "name": "test",
            "email": "test@test.com",
            "phone": "1234567890",
            "message": "test message"
        }
        response = supabase.table("contacts").insert(data).execute()
        print("La estructura de la tabla es correcta.")
        
        # Eliminar el dato de prueba
        supabase.table("contacts").delete().eq("email", "test@test.com").execute()
        
    except Exception as e:
        print(f"Error: {str(e)}")
        print("\nPor favor, crea la tabla 'contacts' en Supabase con la siguiente estructura SQL:")
        print("""
CREATE TABLE contacts (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name text NOT NULL,
    email text NOT NULL,
    phone text,
    message text,
    created_at timestamp with time zone DEFAULT timezone('utc'::text, now()) NOT NULL
);
        """)
        sys.exit(1)

if __name__ == "__main__":
    create_contacts_table() 