# 🌐 Web Automation Checker

![Python](https://img.shields.io/badge/python-3.12+-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Automation](https://img.shields.io/badge/Automation-Web_Testing-BD93F9?style=for-the-badge&logo=playwright&logoColor=white)
![Uptime](https://img.shields.io/badge/Status-Monitoring-2ecc71?style=for-the-badge&logo=statuspage&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)

---

**Web Automation Checker** es una herramienta de automatización diseñada para verificar la disponibilidad, el rendimiento y el estado de diversos servicios web. Ideal para integrarse en pipelines de CI/CD o para monitorizar aplicaciones en producción de forma externa.

---

## 🛠️ Stack Tecnológico

| Herramienta | Función |
|---|---|
| **Python 3.12+** | Núcleo de la lógica de automatización. |
| **Automation Engine** | Gestión de navegación y validación de elementos DOM. |
| **HTTP Handlers** | Verificación de códigos de estado y tiempos de respuesta. |
| **Logging System** | Registro detallado de cada ejecución para auditoría. |

---

## 🚀 Funcionalidades Principales

| Categoría | Descripción |
|---|---|
| **Health Checks** | Validación automática de que el servicio está UP y respondiendo correctamente. |
| **Validación de UI** | Comprobación de que elementos críticos (botones, formularios) están presentes. |
| **Reporting** | Generación de logs con los resultados de cada test para facilitar el debug. |
| **Modo Headless** | Ejecución en segundo plano, ideal para servidores y entornos Linux sin GUI. |

---

## 📦 Instalación

Sigue estos pasos para poner en marcha el monitor:

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/Fontihate/web-automation-checker.git
   cd web-automation-checker
   ```

2. **Instala las dependencias necesarias:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 📖 Modo de Uso

Para ejecutar el checker sobre tus sitios configurados:

```bash
python main.py
```

> [!TIP]
> Puedes configurar los intervalos de chequeo y las URLs objetivo dentro de los archivos de configuración para adaptar la herramienta a tus necesidades.

---

## 📈 Roadmap de Desarrollo

- [ ] Notificaciones automáticas vía **Telegram** o **Slack** en caso de caída.
- [ ] Exportación de métricas a formato **Prometheus** para visualización en Grafana.
- [ ] Soporte para validación de certificados SSL y fechas de expiración.
- [ ] Implementación de capturas de pantalla automáticas cuando un test falla.

---

## 🤝 Contribuciones

¿Tienes alguna idea para mejorar la automatización? ¡Haz un Pull Request!

1. Haz un **Fork**.
2. Crea tu rama de mejora (`git checkout -b feature/MejoraWeb`).
3. Envía tus cambios.

---

Hecho con ⚡ por [Fontihate](https://github.com/Fontihate)
