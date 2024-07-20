import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import pandas as pd

# Leer el DataFrame desde el archivo CSV
df = pd.read_csv('data.csv')
def create_email(row):
    date_str = row['fecha']
    state = row['estado']
    nombre_proveedor = row['nombre_proveedor']
    codigo_pedido = row['codigo_pedido']

    date_format = "%Y-%m-%d"
    date_obj = datetime.strptime(date_str, date_format)
    current_date = datetime.now()
    
    if date_obj < current_date or state in ["retraso", "retrasoExtremo"]:
        email_subject = "Notificación de retraso en entrega"
        email_body = f"""
        Estimado proveedor {nombre_proveedor},

        Hemos notado un retraso significativo en la entrega de suministros de la Universidad Nacional de Ingeniería con el código de pedido {codigo_pedido}.

        Por favor, tome las acciones necesarias para resolver este retraso lo antes posible.

        Atentamente,
        Equipo de Monitorización
        """
        
        return email_subject, email_body
    
    return None, None

def send_email(smtp_server, smtp_port, sender_email, sender_password, recipient_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Configuración del servidor SMTP y las credenciales
smtp_server = "smtp.gmail.com"
smtp_port = 587
sender_email = "your_email@gmail.com"
sender_password = "your_app_password"  # Use the app password generated in the steps above

# Envío de emails basados en el DataFrame
for index, row in df.iterrows():
    subject, body = create_email(row)
    if subject and body:
        recipient_email = row['email_proveedor']
        send_email(smtp_server, smtp_port, sender_email, sender_password, recipient_email, subject, body)
    else:
        print(f"No action required for {row['nombre_proveedor']}.")
