
# ERR-Finder

Conjunto de scripts desarrollados para **detectar vulnerabilidades comunes en aplicaciones web** y generar reportes básicos. El objetivo es automatizar parte del proceso de auditoría de seguridad de forma educativa.

⚠️ **Aviso:** Este proyecto es únicamente con fines **educativos y de investigación en seguridad**. No debe utilizarse contra sistemas sin autorización explícita. ademas que subi este script para engordar mi portafolio 

---

## 📂 Scripts incluidos

### `scan.py`

Escanea sitios web en busca de vulnerabilidades básicas:

* **CSRF** (falta de tokens en formularios)
* **Clickjacking** (cabeceras ausentes/débiles)
* **XSS** reflejado
* **Inyección HTML**

Genera archivos de salida con las URLs vulnerables (`csrf_vuln.txt`, `xss_vuln.txt`, etc.).

---

### `scancorreo.py`

* Lee los reportes de vulnerabilidades.
* Extrae posibles correos de contacto desde las páginas afectadas.
* Guarda los resultados en `emails.mes` para notificación posterior.

---

### `emails.py`

* Usa la API de **Gemini** para redactar correos profesionales.
* Integra con Gmail para enviar los reportes a los contactos encontrados.
* Filtra frases automáticas para que los mensajes suenen más humanos.

---

### `runall.py`

Script orquestador que ejecuta todo el flujo en orden:

1. Escaneo de vulnerabilidades.
2. Extracción de correos.
3. Generación y envío de correos.

---

## 🚀 Uso básico

```bash
# 1. Colocar las URLs en targets.txt
# 2. Ejecutar el orquestador
python runall.py
```

Archivos generados:

* `csrf_vuln.txt`, `xss_vuln.txt`, `clickjacking_vuln.txt`, `html_injection_vuln.txt`
* `emails.mes` con los contactos recopilados

---

## 🔧 Requisitos

* Python 3.8+
* Librerías: `requests`, `beautifulsoup4`

Instalación rápida:

```bash
pip install -r requirements.txt
```

---

## 👨‍💻 Autor

Proyecto desarrollado por **8D2-SEC** (Dylan).
Más info: [https://8d2sec.pro](https://8d2sec.pro) 
