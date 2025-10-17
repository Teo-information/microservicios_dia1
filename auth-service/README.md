# 🔐 Auth Service

Servicio de autenticación y autorización para el ecosistema de microservicios.

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

El **Auth Service** es responsable de:

- **Autenticación de usuarios** (login/logout)
- **Autorización** (verificación de permisos)
- **Gestión de sesiones** (JWT tokens)
- **Registro de usuarios**
- **Recuperación de contraseñas**
- **Validación de tokens**

## 🛠️ Tecnologías

- **Python 3.12**
- **FastAPI** (Framework web)
- **PostgreSQL** (Base de datos)
- **Redis** (Cache de sesiones)
- **JWT** (JSON Web Tokens)
- **Bcrypt** (Hash de contraseñas)
- **SQLAlchemy** (ORM)
- **Pydantic** (Validación de datos)

## 📁 Estructura del Servicio

```
auth-service/
├── 📄 Dockerfile           # Configuración del contenedor
├── 📄 requirements.txt     # Dependencias Python
├── 📄 test_connection.py   # Script de prueba de conectividad
├── 📄 app.py              # Aplicación principal FastAPI
├── 📄 models.py           # Modelos de base de datos
├── 📄 schemas.py          # Esquemas Pydantic
├── 📄 auth.py             # Lógica de autenticación
├── 📄 database.py         # Configuración de base de datos
├── 📄 config.py           # Configuración del servicio
├── 📁 tests/              # Tests unitarios
│   ├── 📄 test_auth.py
│   ├── 📄 test_users.py
│   └── 📄 conftest.py
└── 📄 README.md           # Este archivo
```

## 🚀 Instalación y Configuración

### Requisitos Previos
- Docker y Docker Compose
- PostgreSQL 15+
- Redis 7+

### Configuración con Docker
```bash
# Desde la raíz del proyecto
cd microservicios

# Levantar el auth-service
docker-compose up -d auth-service

# Verificar que esté funcionando
docker-compose ps auth-service
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
```

## 🏃‍♂️ Ejecución

### Con Docker (Recomendado)
```bash
# Levantar solo el auth-service
docker-compose up -d auth-service

# Ver logs
docker-compose logs -f auth-service

# Ejecutar tests
docker exec auth_service python -m pytest

# Entrar al contenedor
docker exec -it auth_service bash
```

### Localmente
```bash
# Activar entorno virtual
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows

# Ejecutar la aplicación
python app.py

# La API estará disponible en http://localhost:8000
```

### Verificar Conectividad
```bash
# Test de conexión a PostgreSQL y Redis
docker exec auth_service python /app/test_connection.py

# Test de la API
curl http://localhost:8000/health
```

## 🔗 API Endpoints

### Autenticación
```http
POST /auth/register
Content-Type: application/json

{
  "username": "usuario",
  "email": "usuario@example.com",
  "password": "password123"
}
```

```http
POST /auth/login
Content-Type: application/json

{
  "username": "usuario",
  "password": "password123"
}
```

```http
POST /auth/logout
Authorization: Bearer <token>
```

```http
POST /auth/refresh
Authorization: Bearer <refresh_token>
```

### Gestión de Usuarios
```http
GET /users/me
Authorization: Bearer <token>
```

```http
PUT /users/me
Authorization: Bearer <token>
Content-Type: application/json

{
  "email": "nuevo@email.com"
}
```

```http
POST /auth/forgot-password
Content-Type: application/json

{
  "email": "usuario@example.com"
}
```

### Health Check
```http
GET /health
```

## 🗄️ Base de Datos

### Esquema de Usuarios
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    token_hash VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Conexión a la Base de Datos
```bash
# Conectar directamente a PostgreSQL
docker exec -it db_postgres psql -U devuser -d main_db

# Ejecutar queries
\dt  # Ver tablas
SELECT * FROM users;  # Ver usuarios
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

# JWT
JWT_SECRET_KEY=tu-secret-key-super-segura
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Aplicación
AUTH_SERVICE_PORT=8000
DEBUG=True
```

## 🧪 Testing

### Ejecutar Tests
```bash
# Todos los tests
docker exec auth_service python -m pytest

# Tests específicos
docker exec auth_service python -m pytest tests/test_auth.py

# Con cobertura
docker exec auth_service python -m pytest --cov=app tests/
```

### Tests Disponibles
- **test_auth.py**: Tests de autenticación
- **test_users.py**: Tests de gestión de usuarios
- **test_connection.py**: Tests de conectividad

### Ejemplo de Test
```python
def test_user_registration():
    response = client.post("/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"
```

## 💻 Desarrollo

### Flujo de Desarrollo
1. **Modificar código** en `auth-service/`
2. **Reconstruir contenedor**:
   ```bash
   docker-compose up --build -d auth-service
   ```
3. **Ejecutar tests**:
   ```bash
   docker exec auth_service python -m pytest
   ```
4. **Ver logs**:
   ```bash
   docker-compose logs -f auth-service
   ```

### Agregar Nuevas Funcionalidades
1. **Modelo**: Agregar en `models.py`
2. **Schema**: Definir en `schemas.py`
3. **Endpoint**: Implementar en `app.py`
4. **Test**: Crear en `tests/`

### Estructura de Código
```python
# app.py - Endpoint principal
@app.post("/auth/login")
async def login(credentials: LoginSchema):
    user = authenticate_user(credentials.username, credentials.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# auth.py - Lógica de autenticación
def authenticate_user(username: str, password: str):
    user = get_user_by_username(username)
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user
```

## 🚨 Troubleshooting

### Problemas Comunes

#### "Connection refused to PostgreSQL"
```bash
# Verificar que PostgreSQL esté corriendo
docker-compose ps postgres

# Ver logs de PostgreSQL
docker-compose logs postgres

# Reiniciar servicios
docker-compose restart postgres auth-service
```

#### "Redis connection failed"
```bash
# Verificar Redis
docker-compose logs redis

# Test Redis
docker exec cache_redis redis-cli ping
```

#### "JWT token invalid"
```bash
# Verificar JWT_SECRET_KEY
docker exec auth_service env | grep JWT

# Regenerar tokens
# Eliminar sesiones en Redis
docker exec cache_redis redis-cli FLUSHDB
```

#### "Database schema not found"
```bash
# Verificar tablas
docker exec db_postgres psql -U devuser -d main_db -c "\dt"

# Ejecutar migraciones (si existen)
docker exec auth_service python -m alembic upgrade head
```

### Comandos de Diagnóstico
```bash
# Ver logs del servicio
docker-compose logs -f auth-service

# Ver estado del contenedor
docker-compose ps auth-service

# Entrar al contenedor
docker exec -it auth_service bash

# Ver variables de entorno
docker exec auth_service env

# Test de conectividad
docker exec auth_service python /app/test_connection.py
```

### Logs Útiles
```bash
# Logs en tiempo real
docker-compose logs -f auth-service

# Logs con timestamp
docker-compose logs -t auth-service

# Últimas 100 líneas
docker-compose logs --tail=100 auth-service
```

## 📚 Recursos Adicionales

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [JWT.io](https://jwt.io/) - Para debuggear tokens
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

## 🔄 Próximos Pasos

- [ ] Implementar 2FA (Two-Factor Authentication)
- [ ] Agregar OAuth2 (Google, GitHub)
- [ ] Implementar rate limiting
- [ ] Agregar auditoría de logs
- [ ] Implementar roles y permisos avanzados

---

**¡El Auth Service está listo para autenticar tu aplicación! 🔐**