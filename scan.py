import requests
from bs4 import BeautifulSoup
import argparse
import sys

def check_clickjacking(url):
    try:
        if not url.startswith(('http://','https://')):
            url = 'http://' + url
        response = requests.get(url, timeout=10)
        headers = response.headers
        xfo = headers.get('X-Frame-Options')
        csp = headers.get('Content-Security-Policy')
        vulnerable = False
        if not xfo:
            vulnerable = True
        else:
            if xfo.lower() not in ['deny','sameorigin']:
                vulnerable = True
        if csp:
            if 'frame-ancestors' in csp.lower():
                fa = ''
                parts = csp.split(';')
                for part in parts:
                    if 'frame-ancestors' in part:
                        fa = part.strip()
                        break
                if fa and ('none' not in fa and 'self' not in fa and '*' in fa):
                    vulnerable = True
        return vulnerable, headers
    except Exception as e:
        print(f"    [error] No se pudo comprobar clickjacking en {url}: {e}")
        return False, {}

def check_csrf(url):
    try:
        if not url.startswith(('http://','https://')):
            url = 'http://' + url
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        forms = soup.find_all('form')
        if not forms:
            return False
        found_token = False
        for form in forms:
            hidden_inputs = form.find_all('input', {'type': 'hidden'})
            for hidden in hidden_inputs:
                name = hidden.get('name') or ''
                if 'csrf' in name.lower() or 'token' in name.lower():
                    found_token = True
                    break
            if found_token:
                break
        return not found_token
    except Exception as e:
        print(f"    [error] No se pudo comprobar CSRF en {url}: {e}")
        return False

def check_xss_and_html(url):
    results = {'xss': False, 'html': False}
    try:
        if not url.startswith(('http://','https://')):
            url = 'http://' + url
        xss_payload = "<script>alert('XSS')</script>"
        html_payload = "<b>test</b>"
        if '?' in url:
            xss_url = url + '&q=' + xss_payload
            html_url = url + '&q=' + html_payload
        else:
            xss_url = url + '?q=' + xss_payload
            html_url = url + '?q=' + html_payload
        res_xss = requests.get(xss_url, timeout=10)
        if xss_payload in res_xss.text:
            results['xss'] = True
        res_html = requests.get(html_url, timeout=10)
        if html_payload in res_html.text:
            results['html'] = True
        return results
    except Exception as e:
        print(f"    [error] No se pudo comprobar XSS/HTML en {url}: {e}")
        return results

def main():
    parser = argparse.ArgumentParser(
        description='Escaneo básico de vulnerabilidades web (CSRF, XSS, HTML, Clickjacking)')
    parser.add_argument('-f','--file', type=str, required=True,
                        help='Archivo con lista de URLs (una por línea)')
    args = parser.parse_args()
    try:
        with open(args.file, 'r') as f:
            targets = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"No se pudo leer el archivo {args.file}: {e}")
        sys.exit(1)

    reports = {
        'xss': 'xss_vuln.txt',
        'html': 'html_injection_vuln.txt',
        'csrf': 'csrf_vuln.txt',
        'clickjacking': 'clickjacking_vuln.txt'
    }
    for rep in reports.values():
        open(rep, 'w').close()

    for url in targets:
        print(f"Escaneando {url} ...")
        csrf_vuln = check_csrf(url)
        if csrf_vuln:
            print(f"    [!] CSRF tokens ausentes en formularios. Posible vulnerabilidad CSRF.")
            with open(reports['csrf'], 'a') as fc:
                fc.write(url + '\n')
        click_vuln, headers = check_clickjacking(url)
        if click_vuln:
            print(f"    [!] Encabezados de protección contra clickjacking ausentes o débiles.")
            with open(reports['clickjacking'], 'a') as fl:
                fl.write(url + '\n')
        xss_results = check_xss_and_html(url)
        if xss_results.get('xss'):
            print(f"    [!] Posible XSS reflejado detectado usando payload script.")
            with open(reports['xss'], 'a') as fx:
                fx.write(url + '\n')
        if xss_results.get('html'):
            print(f"    [!] Posible inyección HTML detectada usando payload de etiqueta.")
            with open(reports['html'], 'a') as fh:
                fh.write(url + '\n')

if __name__ == '__main__':
    main()
