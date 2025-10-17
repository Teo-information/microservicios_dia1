# 🏗️ Microservicios Lab - Proyecto de Laboratorio

Este es un proyecto de laboratorio para aprender arquitectura de microservicios usando Docker, PostgreSQL, Redis y Python.

## 📋 Tabla de Contenidos

- [Descripción del Proyecto](#-descripción-del-proyecto)
- [Arquitectura](#-arquitectura)
- [Servicios Incluidos](#-servicios-incluidos)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación y Configuración](#-instalación-y-configuración)
- [Ejecución del Proyecto](#-ejecución-del-proyecto)
- [Comandos Útiles](#-comandos-útiles)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Desarrollo](#-desarrollo)
- [Troubleshooting](#-troubleshooting)

## 🎯 Descripción del Proyecto

Este proyecto implementa una arquitectura de microservicios básica con los siguientes componentes:

- **Auth Service**: Servicio de autenticación y autorización
- **Blog Service**: Servicio para gestión de artículos/blog
- **Email Service**: Servicio para envío de emails
- **Frontend**: Interfaz de usuario web
- **Reverse Proxy**: Proxy inverso para enrutamiento

## 🏛️ Arquitectura

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Frontend  │    │ Blog Service│    │Email Service│
│   (React)   │    │  (Python)   │    │  (Python)   │
└─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │
       └───────────────────┼───────────────────┘
                           │
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│Reverse Proxy│────│ Auth Service│────│ PostgreSQL  │
│   (Nginx)   │    │  (Python)   │    │  Database   │
└─────────────┘    └─────────────┘    └─────────────┘
                           │
                   ┌─────────────┐
                   │    Redis    │
                   │   (Cache)   │
                   └─────────────┘
```

## 🔧 Servicios Incluidos

### Servicios de Aplicación
- **auth-service**: Autenticación JWT, gestión de usuarios
- **blog-service**: CRUD de artículos, categorías
- **email-service**: Envío de emails transaccionales
- **frontend**: Interfaz React con routing

### Servicios de Infraestructura
- **postgres**: Base de datos principal
- **redis**: Cache y sesiones
- **reverse-proxy**: Enrutamiento y load balancing

## 📋 Requisitos Previos

### Software Necesario
- **Docker Desktop** (versión 4.0+)
- **Git** (para clonar el repositorio)
- **Terminal/PowerShell** (Windows) o **Terminal** (Linux/Mac)

### Verificar Instalación
```bash
docker --version
docker-compose --version
git --version
```

## 🚀 Instalación y Configuración

### 1. Clonar el Repositorio
```bash
git clone <url-del-repositorio>
cd microservicios
```

### 2. Verificar Estructura del Proyecto
```bash
ls -la
```

Deberías ver:
```
microservicios/
├── auth-service/
├── blog-service/
├── email-service/
├── frontend/
├── reverse-proxy/
├── docker-compose.yml
├── .gitignore
└── README.md
```

## 🏃‍♂️ Ejecución del Proyecto

### Opción 1: Levantar Todo el Stack
```bash
# Levantar todos los servicios
docker-compose up -d

# Verificar que todos estén funcionando
docker-compose ps
```

### Opción 2: Levantar Servicios Individuales
```bash
# Solo base de datos y cache
docker-compose up -d postgres redis

# Solo auth-service
docker-compose up -d auth-service

# Solo blog-service
docker-compose up -d blog-service
```

### Verificar Estado de los Servicios
```bash
# Ver todos los contenedores
docker-compose ps

# Ver logs en tiempo real
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs auth-service
```

## 🧪 Pruebas de Conectividad

### Test de Conexión del Auth Service
```bash
docker exec auth_service python /app/test_connection.py
```

**Resultado esperado:**
```
Iniciando pruebas de conexión...
✅ PostgreSQL OK → PostgreSQL 15.14...
✅ Redis OK → ping=True
🎉 Todo listo: conexiones OK.
```

### Verificar Servicios Individuales
```bash
# Test PostgreSQL
docker exec db_postgres psql -U devuser -d main_db -c "SELECT version();"

# Test Redis
docker exec cache_redis redis-cli ping

# Test Auth Service
docker exec auth_service python -c "import psycopg2; import redis; print('Dependencias OK')"
```

## 🛠️ Comandos Útiles

### Gestión de Contenedores
```bash
# Levantar servicios
docker-compose up -d

# Detener servicios
docker-compose down

# Detener y eliminar volúmenes
docker-compose down -v

# Reconstruir contenedores
docker-compose up --build -d

# Ver logs
docker-compose logs -f [servicio]

# Ejecutar comando en contenedor
docker exec -it [nombre_contenedor] [comando]
```

### Desarrollo
```bash
# Entrar al contenedor del auth-service
docker exec -it auth_service bash

# Instalar nuevas dependencias
docker exec auth_service pip install [paquete]

# Ejecutar tests
docker exec auth_service python -m pytest

# Ver logs en tiempo real
docker-compose logs -f auth-service
```

### Base de Datos
```bash
# Conectar a PostgreSQL
docker exec -it db_postgres psql -U devuser -d main_db

# Backup de la base de datos
docker exec db_postgres pg_dump -U devuser main_db > backup.sql

# Restaurar backup
docker exec -i db_postgres psql -U devuser main_db < backup.sql
```

## 📁 Estructura del Proyecto

```
microservicios/
├── 📁 auth-service/          # Servicio de autenticación
│   ├── 📄 Dockerfile        # Configuración del contenedor
│   ├── 📄 requirements.txt  # Dependencias Python
│   ├── 📄 test_connection.py # Script de prueba
│   └── 📄 README.md         # Documentación del servicio
├── 📁 blog-service/          # Servicio de blog
│   └── 📄 README.md
├── 📁 email-service/         # Servicio de email
│   └── 📄 README.md
├── 📁 frontend/              # Aplicación web
│   └── 📄 README.md
├── 📁 reverse-proxy/         # Proxy inverso
│   └── 📄 README.md
├── 📄 docker-compose.yml     # Orquestación de servicios
├── 📄 .gitignore            # Archivos ignorados por Git
└── 📄 README.md             # Este archivo
```

## 💻 Desarrollo

### Flujo de Desarrollo
1. **Modificar código** en el servicio correspondiente
2. **Reconstruir contenedor** si es necesario:
   ```bash
   docker-compose up --build -d [servicio]
   ```
3. **Probar cambios** usando los scripts de test
4. **Ver logs** para debugging:
   ```bash
   docker-compose logs -f [servicio]
   ```

### Variables de Entorno
Los servicios usan las siguientes variables (con valores por defecto):

```env
# Base de Datos
POSTGRES_USER=devuser
POSTGRES_PASSWORD=devpass
POSTGRES_DB=main_db
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# Auth Service
AUTH_SERVICE_PORT=8000
```

### Agregar Nuevos Servicios
1. Crear carpeta del servicio
2. Agregar `Dockerfile` y `requirements.txt`
3. Actualizar `docker-compose.yml`
4. Agregar documentación en `README.md`

## 🚨 Troubleshooting

### Problemas Comunes

#### "docker-compose: command not found"
```bash
# Usar la sintaxis nueva (sin guión)
docker compose up -d
```

#### "Port already in use"
```bash
# Ver qué proceso usa el puerto
netstat -ano | findstr :5432

# Cambiar puertos en docker-compose.yml
ports:
  - "5433:5432"  # Puerto externo diferente
```

#### "Container keeps restarting"
```bash
# Ver logs para identificar el problema
docker-compose logs [servicio]

# Verificar configuración
docker-compose config
```

#### "Database connection failed"
```bash
# Verificar que PostgreSQL esté listo
docker-compose logs postgres

# Esperar unos segundos y reintentar
docker-compose restart auth-service
```

### Comandos de Diagnóstico
```bash
# Ver estado de todos los contenedores
docker-compose ps

# Ver uso de recursos
docker stats

# Ver redes Docker
docker network ls

# Ver volúmenes
docker volume ls

# Limpiar contenedores parados
docker system prune
```

## 📚 Documentación Adicional

- [Auth Service](./auth-service/README.md)
- [Blog Service](./blog-service/README.md)
- [Email Service](./email-service/README.md)
- [Frontend](./frontend/README.md)
- [Reverse Proxy](./reverse-proxy/README.md)

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es para fines educativos y de laboratorio.

---

## 🆘 Soporte

Si tienes problemas:

1. Revisa la sección [Troubleshooting](#-troubleshooting)
2. Verifica los logs: `docker-compose logs -f`
3. Consulta la documentación específica de cada servicio
4. Abre un issue en el repositorio

**¡Happy coding! 🚀**