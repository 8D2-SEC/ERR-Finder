import requests
from bs4 import BeautifulSoup
import re
import os

def read_vuln_file(file_name):
    urls = []
    try:
        with open(file_name, 'r') as file:
            urls = [line.strip() for line in file.readlines() if line.strip()]
    except Exception as e:
        print(f"[error] No se pudo leer el archivo {file_name}: {e}")
    return urls

def find_emails(url):
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')

        emails = set(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", soup.text))
        
        if emails:
            return emails
        return None
    except Exception as e:
        print(f"[error] No se pudo hacer scraping en {url}: {e}")
        return None

def generate_message(vulnerability, site):
    messages = {
        'csrf': f"Hola, hemos detectado una vulnerabilidad en {site}: falta de protección CSRF. Esto puede permitir ataques como el robo de cuentas o la modificación de datos. Recomendamos implementar protección CSRF lo antes posible.",
        'xss': f"¡Alerta! Se ha detectado una posible vulnerabilidad XSS en {site}. Esto puede permitir la ejecución de scripts maliciosos. Es crucial aplicar filtros de entrada y salida para mitigar este riesgo.",
        'clickjacking': f"Hola, {site} parece tener una configuración débil contra Clickjacking. Los atacantes podrían incrustarlo en un iframe. Recomendamos asegurar los encabezados X-Frame-Options.",
        'html': f"¡Atención! Se ha detectado una vulnerabilidad de inyección HTML en {site}. Esto puede permitir la ejecución de código HTML no deseado. Recomendamos filtrar adecuadamente las entradas de los usuarios.",
    }
    return messages.get(vulnerability, "¡Atención! Hemos detectado una vulnerabilidad crítica en tu sitio.")

def save_to_file(email, vulnerability):
    try:
        with open('emails.mes', 'a') as file:
            file.write(f"correo:{email}:{vulnerability}\n")
    except Exception as e:
        print(f"[error] No se pudo guardar el correo en emails.mes: {e}")

def main():
    vulnerabilities = {
        'csrf': 'csrf_vuln.txt',
        'xss': 'xss_vuln.txt',
        'clickjacking': 'clickjacking_vuln.txt',
        'html': 'html_injection_vuln.txt',
    }

    for vuln, file_name in vulnerabilities.items():
        if os.path.exists(file_name):
            print(f"Procesando {file_name}...")
            urls = read_vuln_file(file_name)
            for url in urls:
                print(f"    [*] Buscando correos en {url}...")
                emails = find_emails(url)
                if emails:
                    for email in emails:
                        save_to_file(email, vuln)
                    print(f"    [*] Correos encontrados en {url} ({vuln})")
                else:
                    print(f"    [!] No se encontraron correos en {url}")
        else:
            print(f"[error] No se encontró el archivo {file_name}")

if __name__ == '__main__':
    main()
