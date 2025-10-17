# 📧 Email Service

Servicio de envío de emails transaccionales y notificaciones para el ecosistema de microservicios.

## 📋 Tabla de Contenidos

- [Descripción](#-descripción)
- [Tecnologías](#-tecnologías)
- [Estructura del Servicio](#-estructura-del-servicio)
- [Instalación y Configuración](#-instalación-y-configuración)
- [Ejecución](#-ejecución)
- [API Endpoints](#-api-endpoints)
- [Base de Datos](#-base-de-datos)
- [Variables de Entorno](#-variables-de-entorno)
- [Testing](#-testing)
- [Desarrollo](#-desarrollo)
- [Troubleshooting](#-troubleshooting)

## 🎯 Descripción

El **Email Service** es responsable de:

- **Envío de emails transaccionales** (registro, login, reset password)
- **Notificaciones automáticas** (nuevos comentarios, artículos)
- **Newsletters** y comunicaciones masivas
- **Templates de email** personalizables
- **Cola de emails** con retry automático
- **Tracking de emails** (abierto, clickeado)
- **Integración con proveedores** (SendGrid, Mailgun, SMTP)

## 🛠️ Tecnologías

- **Python 3.12**
- **FastAPI** (Framework web)
- **Celery** (Cola de tareas)
- **Redis** (Broker de mensajes)
- **PostgreSQL** (Logs y tracking)
- **Jinja2** (Templates de email)
- **SendGrid/Mailgun** (Proveedores de email)
- **SMTP** (Servidor de email)

## 📁 Estructura del Servicio

```
email-service/
├── 📄 Dockerfile           # Configuración del contenedor
├── 📄 requirements.txt     # Dependencias Python
├── 📄 app.py              # Aplicación principal FastAPI
├── 📄 worker.py           # Worker de Celery
├── 📄 models.py           # Modelos de base de datos
├── 📄 schemas.py          # Esquemas Pydantic
├── 📄 email_client.py     # Cliente de email
├── 📄 templates.py        # Generación de templates
├── 📄 tasks.py            # Tareas de Celery
├── 📄 database.py         # Configuración de base de datos
├── 📄 config.py           # Configuración del servicio
├── 📁 templates/          # Templates de email
│   ├── 📄 welcome.html
│   ├── 📄 password_reset.html
│   ├── 📄 new_comment.html
│   └── 📄 newsletter.html
├── 📁 tests/              # Tests unitarios
│   ├── 📄 test_email.py
│   ├── 📄 test_templates.py
│   └── 📄 conftest.py
└── 📄 README.md           # Este archivo
```

## 🚀 Instalación y Configuración

### Requisitos Previos
- Docker y Docker Compose
- PostgreSQL 15+
- Redis 7+
- Proveedor de email (SendGrid, Mailgun, o SMTP)

### Configuración con Docker
```bash
# Desde la raíz del proyecto
cd microservicios

# Levantar el email-service
docker-compose up -d email-service

# Verificar que esté funcionando
docker-compose ps email-service
```

### Configuración Local (Desarrollo)
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
export POSTGRES_HOST=localhost
export REDIS_HOST=localhost
export SMTP_HOST=smtp.gmail.com
export SMTP_PORT=587
```

## 🏃‍♂️ Ejecución

### Con Docker (Recomendado)
```bash
# Levantar solo el email-service
docker-compose up -d email-service

# Ver logs
docker-compose logs -f email-service

# Ejecutar tests
docker exec email_service python -m pytest

# Entrar al contenedor
docker exec -it email_service bash
```

### Localmente
```bash
# Activar entorno virtual
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows

# Ejecutar la aplicación
python app.py

# Ejecutar worker de Celery
celery -A worker worker --loglevel=info

# La API estará disponible en http://localhost:8002
```

### Verificar Conectividad
```bash
# Test de la API
curl http://localhost:8002/health

# Test de conectividad con Redis
docker exec email_service python -c "import redis; r = redis.Redis(); print(r.ping())"
```

## 🔗 API Endpoints

### Envío de Emails
```http
POST /email/send
Content-Type: application/json

{
  "to": "usuario@example.com",
  "subject": "Bienvenido!",
  "template": "welcome",
  "data": {
    "username": "usuario",
    "activation_link": "https://example.com/activate/123"
  }
}
```

```http
POST /email/send-bulk
Content-Type: application/json

{
  "recipients": ["user1@example.com", "user2@example.com"],
  "subject": "Newsletter Semanal",
  "template": "newsletter",
  "data": {
    "articles": [...],
    "unsubscribe_link": "https://example.com/unsubscribe"
  }
}
```

### Gestión de Templates
```http
GET /templates

POST /templates
Content-Type: application/json

{
  "name": "new_template",
  "subject": "Nuevo Template",
  "html_content": "<h1>Hola {{username}}!</h1>",
  "text_content": "Hola {{username}}!"
}

PUT /templates/{template_id}

DELETE /templates/{template_id}
```

### Cola de Emails
```http
GET /queue/status

POST /queue/retry
Content-Type: application/json

{
  "email_id": "123"
}

DELETE /queue/{email_id}
```

### Tracking
```http
GET /tracking/emails
# Query params: ?status=sent&date_from=2024-01-01

GET /tracking/emails/{email_id}

GET /tracking/emails/{email_id}/events
```

### Health Check
```http
GET /health
```

## 🗄️ Base de Datos

### Esquema de Emails
```sql
CREATE TABLE email_templates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    subject VARCHAR(255) NOT NULL,
    html_content TEXT NOT NULL,
    text_content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE emails (
    id SERIAL PRIMARY KEY,
    to_email VARCHAR(255) NOT NULL,
    subject VARCHAR(255) NOT NULL,
    template_id INTEGER REFERENCES email_templates(id),
    template_data JSONB,
    status VARCHAR(20) DEFAULT 'pending', -- pending, sent, failed, retry
    provider VARCHAR(50), -- sendgrid, mailgun, smtp
    provider_id VARCHAR(255), -- ID del proveedor
    sent_at TIMESTAMP,
    failed_at TIMESTAMP,
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE email_events (
    id SERIAL PRIMARY KEY,
    email_id INTEGER REFERENCES emails(id),
    event_type VARCHAR(50) NOT NULL, -- sent, delivered, opened, clicked, bounced
    event_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE email_queues (
    id SERIAL PRIMARY KEY,
    email_id INTEGER REFERENCES emails(id),
    priority INTEGER DEFAULT 0,
    scheduled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending'
);
```

### Conexión a la Base de Datos
```bash
# Conectar directamente a PostgreSQL
docker exec -it db_postgres psql -U devuser -d main_db

# Ejecutar queries
\dt  # Ver tablas
SELECT * FROM emails;  # Ver emails
SELECT * FROM email_events;  # Ver eventos
```

## ⚙️ Variables de Entorno

```env
# Base de Datos
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_USER=devuser
POSTGRES_PASSWORD=devpass
POSTGRES_DB=main_db

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# Email Provider - SendGrid
SENDGRID_API_KEY=tu-sendgrid-api-key
SENDGRID_FROM_EMAIL=noreply@example.com

# Email Provider - Mailgun
MAILGUN_API_KEY=tu-mailgun-api-key
MAILGUN_DOMAIN=example.com

# Email Provider - SMTP
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=tu-email@gmail.com
SMTP_PASSWORD=tu-app-password
SMTP_USE_TLS=True

# Aplicación
EMAIL_SERVICE_PORT=8002
DEBUG=True

# Celery
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

## 🧪 Testing

### Ejecutar Tests
```bash
# Todos los tests
docker exec email_service python -m pytest

# Tests específicos
docker exec email_service python -m pytest tests/test_email.py

# Con cobertura
docker exec email_service python -m pytest --cov=app tests/
```

### Tests Disponibles
- **test_email.py**: Tests de envío de emails
- **test_templates.py**: Tests de templates
- **test_tasks.py**: Tests de tareas de Celery

### Ejemplo de Test
```python
def test_send_welcome_email():
    email_data = {
        "to": "test@example.com",
        "template": "welcome",
        "data": {"username": "testuser"}
    }
    response = client.post("/email/send", json=email_data)
    assert response.status_code == 200
    assert response.json()["status"] == "queued"
```

## 💻 Desarrollo

### Flujo de Desarrollo
1. **Modificar código** en `email-service/`
2. **Reconstruir contenedor**:
   ```bash
   docker-compose up --build -d email-service
   ```
3. **Ejecutar tests**:
   ```bash
   docker exec email_service python -m pytest
   ```
4. **Ver logs**:
   ```bash
   docker-compose logs -f email-service
   ```

### Agregar Nuevos Templates
1. **Crear template HTML** en `templates/`
2. **Registrar template** en `templates.py`
3. **Crear endpoint** si es necesario
4. **Agregar test**

### Estructura de Código
```python
# app.py - Endpoint principal
@app.post("/email/send")
async def send_email(email_data: EmailRequest, db: Session = Depends(get_db)):
    # Validar template
    template = get_template(db, email_data.template)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    # Enviar a cola
    task = send_email_task.delay(email_data.dict())
    return {"task_id": task.id, "status": "queued"}

# tasks.py - Tarea de Celery
@celery_app.task(bind=True, max_retries=3)
def send_email_task(self, email_data):
    try:
        # Renderizar template
        html_content = render_template(email_data['template'], email_data['data'])
        
        # Enviar email
        result = email_client.send_email(
            to=email_data['to'],
            subject=email_data['subject'],
            html_content=html_content
        )
        
        # Guardar en base de datos
        save_email_record(email_data, result)
        
    except Exception as exc:
        # Retry automático
        raise self.retry(exc=exc, countdown=60)
```

### Templates de Email
```html
<!-- templates/welcome.html -->
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Bienvenido</title>
</head>
<body>
    <h1>¡Bienvenido {{username}}!</h1>
    <p>Gracias por registrarte en nuestra plataforma.</p>
    <a href="{{activation_link}}">Activar cuenta</a>
</body>
</html>
```

## 🚨 Troubleshooting

### Problemas Comunes

#### "SMTP connection failed"
```bash
# Verificar configuración SMTP
docker exec email_service env | grep SMTP

# Test SMTP manual
docker exec email_service python -c "
import smtplib
smtp = smtplib.SMTP('smtp.gmail.com', 587)
smtp.starttls()
print('SMTP connection OK')
"
```

#### "SendGrid API key invalid"
```bash
# Verificar API key
docker exec email_service env | grep SENDGRID

# Test SendGrid
docker exec email_service python -c "
from sendgrid import SendGridAPIClient
sg = SendGridAPIClient('tu-api-key')
print('SendGrid OK')
"
```

#### "Celery worker not processing"
```bash
# Verificar worker
docker-compose logs email-service | grep worker

# Reiniciar worker
docker-compose restart email-service

# Ver cola de Redis
docker exec cache_redis redis-cli LLEN celery
```

#### "Email template not found"
```bash
# Verificar templates en base de datos
docker exec db_postgres psql -U devuser -d main_db -c "SELECT * FROM email_templates;"

# Verificar archivos de template
docker exec email_service ls -la /app/templates/
```

### Comandos de Diagnóstico
```bash
# Ver logs del servicio
docker-compose logs -f email-service

# Ver estado del contenedor
docker-compose ps email-service

# Entrar al contenedor
docker exec -it email_service bash

# Ver variables de entorno
docker exec email_service env

# Ver estado de Celery
docker exec email_service celery -A worker inspect active
```

### Logs Útiles
```bash
# Logs en tiempo real
docker-compose logs -f email-service

# Logs de Celery
docker exec email_service celery -A worker events

# Ver cola de Redis
docker exec cache_redis redis-cli MONITOR
```

## 📚 Recursos Adicionales

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Celery Documentation](https://docs.celeryproject.org/)
- [SendGrid API Documentation](https://docs.sendgrid.com/)
- [Mailgun API Documentation](https://documentation.mailgun.com/)

## 🔄 Próximos Pasos

- [ ] Implementar tracking de emails (abierto, clickeado)
- [ ] Agregar sistema de bounces y unsubscribes
- [ ] Implementar A/B testing de emails
- [ ] Agregar analytics de engagement
- [ ] Implementar templates drag & drop
- [ ] Agregar integración con más proveedores

---

**¡El Email Service está listo para enviar tus comunicaciones! 📧**