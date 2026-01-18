# 🤖 Music Database Checker & Automator

Herramienta de automatización basada en **Selenium** diseñada para verificar la existencia de álbumes en una base de datos web y preparar lotes de subida para álbumes faltantes.

### 🛠️ Tecnologías utilizadas
- **Python / Selenium WebDriver:** Automatización del navegador Chrome.
- **ChromeDriverManager:** Gestión de drivers.
- **OS & CSV:** Gestión de archivos locales.

### ⚙️ Características principales
- **Autologin:** Sistema automatizado de inicio de sesión en plataforma web.
- **Lógica de búsqueda inteligente:** Detecta variaciones de nombres (Self-titled, Split albums) para evitar duplicados.
- **Actualización masiva:** Capacidad de actualizar géneros y metadatos de forma masiva en archivos CSV locales tras la verificación web.
- **Interactividad:** Menú por consola para elegir archivos de datos dinámicamente.

### ⚠️ Nota de seguridad
Este script utiliza variables de entorno para la gestión de credenciales, asegurando que los datos sensibles no queden expuestos en el código fuente.
