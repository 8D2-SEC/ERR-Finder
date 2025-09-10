import requests
import json
import smtplib
from email.message import EmailMessage


GEMINI_API_KEY = "jeje aca cambiar a la api key" # hoy no scrapers de apis 
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

GMAIL_USER = "correo@gmail.com"
GMAIL_APP_PASSWORD = "xxxxx"  # No tu contraseña normal. Usa una contraseña de aplicación.

def limpiar_mensaje(texto):
    frases_ban = ["aquí tienes", "este es tu correo", "claro que sí"]
    lineas = texto.split('\n')
    return '\n'.join([l for l in lineas if all(b not in l.lower() for b in frases_ban)])

def redactar_con_gemini(correo, vulnerabilidad):
    prompt = (
        f"Eres mi asistente de la empresa 8D2-SEC mi nombre es Dylan y tienes que Redacta un correo profesional dirigido al equipo de {correo} informando que su sitio web presenta El correo debe estar listo para ser enviado, sin campos vacíos, sin placeholders como [tu nombre] o [rellenar aquí]."
        f"una vulnerabilidad de tipo {vulnerabilidad} ademas se detallado y tienes que ofrecer los servicios de consultoria de 8D2-SEC. Sé claro, directo y amable. No agregues frases como 'aquí tienes tu redacción' y No incluyas ninguna frase de explicación adicional, solo el contenido del correo directamente. repito SIN PLACEHOLDERs ya que es mensaje directo con el cliente."
    )   #aca me doy cuenta revisando el scritp meses depsues para subirlo a github me doy cuenta que soy bobo ese prompt tan largo para eso hubiera sido un guion pre hecho y ya jeejeje
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    res = requests.post(GEMINI_URL, headers=headers, data=json.dumps(payload))
    if res.status_code == 200:
        text = res.json()['candidates'][0]['content']['parts'][0]['text']
        return limpiar_mensaje(text.strip())
    else:
        return f"[Error al redactar con Gemini]: {res.status_code} {res.text}"

def enviar_correo(destinatario, asunto, cuerpo):
    msg = EmailMessage()
    msg['Subject'] = asunto
    msg['From'] = GMAIL_USER
    msg['To'] = destinatario
    msg.set_content(cuerpo)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            smtp.send_message(msg)
            print(f"✅ Correo enviado a {destinatario}")
    except Exception as e:
        print(f"❌ Error enviando correo a {destinatario}: {e}")

def main():
    with open('emails.mes', 'r') as f:
        lineas = [line.strip() for line in f if line.strip()]

    for linea in lineas:
        if linea.startswith("correo:"):
            try:
                _, correo, vuln = linea.split(':')
                print(f"\n📬 Procesando {correo} por {vuln}")
                cuerpo = redactar_con_gemini(correo, vuln)
                enviar_correo(correo, f"Reporte de vulnerabilidad en su sitio web ({vuln})", cuerpo)
            except Exception as e:
                print(f"❌ Error procesando línea: {linea} → {e}")

if __name__ == "__main__":
    main()
