from http.server import HTTPServer, BaseHTTPRequestHandler
import socket
import json
from supabase_client import save_contact, supabase
import urllib.parse
import yagmail
import os

def send_email(contact):
    try:
        # Configuración del correo
        sender_email = os.environ.get("SENDER_EMAIL", "tzedakamentorias@gmail.com")
        sender_password = os.environ.get("SENDER_PASSWORD", "jwsf mkwk mxbh iknj")
        receiver_email = os.environ.get("RECEIVER_EMAIL", "andres@ab2capital.com")

        # Crear el contenido del correo
        email_content = f"""
        Se ha recibido un nuevo contacto:

        Nombre: {contact['name']}
        Email: {contact['email']}
        Empresa: {contact['company']}
        Cargo: {contact['position']}
        Teléfono: {contact['phone']}
        Tamaño de la Empresa: {contact['company_size']}
        Áreas de Interés: {contact['interests']}
        Mensaje: {contact.get('message', 'No se proporcionó mensaje')}
        """

        # Enviar el correo usando yagmail
        yag = yagmail.SMTP(sender_email, sender_password)
        yag.send(
            to=receiver_email,
            subject="Nuevo contacto recibido",
            contents=email_content
        )
        yag.close()

        print("\n=== Detalles del envío de correo ===")
        print(f"Correo enviado exitosamente")
        print(f"Para: {receiver_email}")
        print(f"Asunto: Nuevo contacto recibido")
        print("================================\n")
        print("✅ Correo enviado exitosamente.")
    except Exception as e:
        print("\n=== Error en el envío de correo ===")
        print("❌ Error al enviar el correo:", e)
        print("================================\n")

class RequestHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        if self.path == '/contact':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                print("\n=== Nuevo contacto recibido ===")
                print(f"Nombre: {data['name']}")
                print(f"Email: {data['email']}")
                print(f"Empresa: {data['company']}")
                print(f"Cargo: {data['position']}")
                print(f"Teléfono: {data['phone']}")
                print(f"Tamaño de la Empresa: {data['company_size']}")
                print(f"Áreas de Interés: {', '.join(data['interests'])}")
                print(f"Mensaje: {data.get('message', 'No se proporcionó mensaje')}")
                print("==============================\n")

                # Guardar en Supabase
                success, response = save_contact(
                    data['name'],
                    data['email'],
                    data['company'],
                    data['position'],
                    data['phone'],
                    data['company_size'],
                    data['interests'],
                    data.get('message', '')
                )

                if success:
                    print("✅ Contacto guardado en Supabase")
                    # Enviar correo
                    send_email(data)
                else:
                    print("❌ Error al guardar en Supabase:", response)

                # Enviar respuesta
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"message": "Contacto recibido correctamente"}).encode())
            except Exception as e:
                print("\n=== Error en el procesamiento ===")
                print("❌ Error:", e)
                print("==============================\n")
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        else:
            self.send_response(404)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(b"Not Found")

    def do_GET(self):
        if self.path == '/':
            try:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                with open('index.html', 'rb') as f:
                    self.wfile.write(f.read())
            except Exception as e:
                print(f"Error al servir index.html: {e}")
                self.send_response(500)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(b"Error interno del servidor")
        else:
            self.send_response(404)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(b"Not Found")

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def run_server():
    port = int(os.environ.get("PORT", 8000))
    server = HTTPServer(('0.0.0.0', port), RequestHandler)
    print(f"\nServidor iniciado en:")
    print(f"http://localhost:{port}")
    print(f"http://{get_local_ip()}:{port}")
    print("\nPresiona Ctrl+C para detener el servidor")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nDeteniendo el servidor...")
        server.server_close()

if __name__ == '__main__':
    run_server() 