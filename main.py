import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from matplotlib import pyplot as plt
import pandas as pd 
import os
from dotenv import load_dotenv
load_dotenv()
print(os.environ)

# Leer el DataFrame desde el archivo CSV
df = pd.read_excel('Seguimiento de Compras.xlsx')

def create_email(row):
    date_str = row['Fecha Esperada']
    state = row['Status']
    nombre_proveedor = row['Proveedor']
    codigo_pedido = row['Codigo de Pedido']

    date_format = "%Y-%m-%d"
    print(date_str)
    #date_obj = datetime.strptime(date_str, date_format)
    current_date = datetime.now()
    
    if date_str < current_date or state in ["retraso", "retrasoExtremo"]:
        print("alerta")
        email_subject = "Notificación de retraso en entrega"
        email_body = f"""
        Estimado proveedor {nombre_proveedor},

        Hemos notado un retraso significativo en la entrega de suministros de la Universidad Nacional de Ingeniería con el código de pedido {codigo_pedido}.

        Por favor, tome las acciones necesarias para resolver este retraso lo antes posible.

        Atentamente,
        Equipo de Compras
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
# for index, row in df.iterrows():
#     subject, body = create_email(row)
#     if subject and body:
#         recipient_email = row['Correo de Proveedor']
#         send_email(smtp_server, smtp_port, sender_email, sender_password, recipient_email, subject, body)
#     else:
#         print(f"No action required for {row['Proveedor']}.")

# muestra un grafico de pastel de los estados de los pedidos
estado_counts = df['Status'].value_counts()

# Crear el diagrama de pastel
plt.figure(figsize=(8, 8))
plt.pie(estado_counts, labels=estado_counts.index, autopct='%1.1f%%', startangle=140)
plt.title('Cantidad de pedidos por estado')
plt.show()
    