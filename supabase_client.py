from supabase import create_client, Client

SUPABASE_URL = "https://jqmwzrkiutwifeswntzt.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpxbXd6cmtpdXR3aWZlc3dudHp0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDIzOTI3NzEsImV4cCI6MjA1Nzk2ODc3MX0.ykzCpmcgcIxS46__o8FYREWU06togj64AvRs7Ktb2_s"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def save_contact(name: str, email: str, company: str, position: str, phone: str, company_size: str, interests: str, message: str = ""):
    try:
        data = {
            "name": name,
            "email": email,
            "company": company,
            "position": position,
            "phone": phone,
            "company_size": company_size,
            "interests": interests,
            "message": message
        }
        response = supabase.table("contacts").insert(data).execute()
        return True, response
    except Exception as e:
        return False, str(e) 