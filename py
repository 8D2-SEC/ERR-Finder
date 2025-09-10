#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
script: small_targets_daemon.py
descripcion: Misma lógica de small_targets_finder_ddg.py,
             pero corriendo en bucle infinito con pausas.
"""

import time
from urllib.parse import urlparse

# —— IMPORT dI ——
try:
    from duckduckgo_search import ddg
    def duck_search(query: str, max_results: int = 20):
        return ddg(query, region='wt-wt', safesearch='Moderate', max_results=max_results)
except ImportError:
    from duckduckgo_search import DDGS
    def duck_search(query: str, max_results: int = 20):
        return DDGS().text(query, max_results=max_results)

# ——— CONFIGURACIÓN ———
BUSINESS_TERMS = ['papeleria','tienda','cafe','mecanico','panaderia','peluqueria','restaurante']
EXCLUDE_KEYWORDS = ['google','amazon','facebook','twitter','linkedin','youtube','microsoft','apple','cloudflare','shopify','.gov','.edu','wordreference.com','zhihu.com','canada.ca']
OUTPUT_FILE = 'targets.txt'
PAUSE_QUERY = 1.0      
PAUSE_CYCLE = 5 * 1
def is_small_target(url: str) -> bool:
    domain = urlparse(url).netloc.lower()
    return not any(kw in domain for kw in EXCLUDE_KEYWORDS)

def scrape_ddg(dork: str, max_results: int = 20) -> list:
    raw = duck_search(dork, max_results=max_results)
    time.sleep(PAUSE_QUERY)
    links = []
    for item in raw:
        url = item.get('href') or item.get('url')
        if url:
            links.append(url)
    return links

def main():
    found = set()
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Arrancando ciclo de búsqueda...")
    for term in BUSINESS_TERMS:
        q = f"{term} inurl:login"
        print(f"  [+] Buscando «{q}»…")
        try:
            links = scrape_ddg(q)
            print(f"      → {len(links)} URLs obtenidas")
        except Exception as e:
            print(f"      ¡Error en «{term}»!: {e}")
            continue
        for url in links:
            if is_small_target(url):
                found.add(url)

    print(f"  [+] Total objetivos nuevos: {len(found)}. Guardando en {OUTPUT_FILE}…")
    with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:  
        for url in sorted(found):
            f.write(url + "\n")
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Ciclo completado. Durmiendo {PAUSE_CYCLE}s…\n")

if __name__ == '__main__':
    try:
            main()
            time.sleep(PAUSE_CYCLE)
    except KeyboardInterrupt:
        print("\n[!] Proceso interrumpido por el usuario. Hasta la próxima cacería 😎")
