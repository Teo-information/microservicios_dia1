# 🔄 Reverse Proxy

Proxy inverso usando Nginx para enrutamiento, load balancing y gestión de tráfico en el ecosistema de microservicios.

## 📋 Tabla de Contenidos

- [Descripción](#-descripción)
- [Tecnologías](#-tecnologías)
- [Estructura del Servicio](#-estructura-del-servicio)
- [Instalación y Configuración](#-instalación-y-configuración)
- [Ejecución](#-ejecución)
- [Configuración de Rutas](#-configuración-de-rutas)
- [Load Balancing](#-load-balancing)
- [SSL/TLS](#-ssltls)
- [Variables de Entorno](#-variables-de-entorno)
- [Testing](#-testing)
- [Desarrollo](#-desarrollo)
- [Troubleshooting](#-troubleshooting)

## 🎯 Descripción

El **Reverse Proxy** es responsable de:

- **Enrutamiento de requests** a los microservicios apropiados
- **Load balancing** entre múltiples instancias
- **Terminación SSL/TLS**
- **Rate limiting** y protección DDoS
- **Caching** de respuestas estáticas
- **Compresión** de contenido
- **Headers de seguridad**
- **Logging** centralizado de requests

## 🛠️ Tecnologías

- **Nginx** (Servidor web y proxy)
- **OpenSSL** (Certificados SSL)
- **Lua** (Scripts personalizados)
- **Docker** (Contenedorización)

## 📁 Estructura del Servicio

```
reverse-proxy/
├── 📄 Dockerfile           # Configuración del contenedor
├── 📄 nginx.conf           # Configuración principal de Nginx
├── 📄 default.conf         # Configuración de sitios
├── 📁 ssl/                 # Certificados SSL
│   ├── 📄 server.crt       # Certificado del servidor
│   ├── 📄 server.key       # Clave privada
│   └── 📄 dhparam.pem      # Parámetros Diffie-Hellman
├── 📁 conf.d/              # Configuraciones adicionales
│   ├── 📄 rate-limit.conf  # Rate limiting
│   ├── 📄 security.conf    # Headers de seguridad
│   ├── 📄 gzip.conf        # Compresión
│   └── 📄 cache.conf       # Configuración de cache
├── 📁 lua/                 # Scripts Lua personalizados
│   ├── 📄 auth.lua         # Validación de JWT
│   └── 📄 routing.lua      # Lógica de enrutamiento
├── 📁 logs/                # Logs de Nginx
│   ├── 📄 access.log
│   └── 📄 error.log
├── 📁 static/              # Archivos estáticos
│   ├── 📁 css/
│   ├── 📁 js/
│   └── 📁 images/
└── 📄 README.md            # Este archivo
```

## 🚀 Instalación y Configuración

### Requisitos Previos
- Docker y Docker Compose
- Certificados SSL (opcional para desarrollo)
- Servicios backend funcionando

### Configuración con Docker
```bash
# Desde la raíz del proyecto
cd microservicios

# Levantar el reverse-proxy
docker-compose up -d reverse-proxy

# Verificar que esté funcionando
docker-compose ps reverse-proxy
```

### Configuración Local (Desarrollo)
```bash
# Instalar Nginx localmente
# Ubuntu/Debian:
sudo apt update && sudo apt install nginx

# macOS:
brew install nginx

# Windows:
# Usar Docker o WSL

# Copiar configuración
sudo cp nginx.conf /etc/nginx/nginx.conf
sudo cp default.conf /etc/nginx/sites-available/default
sudo nginx -t  # Verificar configuración
sudo systemctl restart nginx
```

## 🏃‍♂️ Ejecución

### Con Docker (Recomendado)
```bash
# Levantar solo el reverse-proxy
docker-compose up -d reverse-proxy

# Ver logs
docker-compose logs -f reverse-proxy

# Entrar al contenedor
docker exec -it reverse_proxy bash

# Verificar configuración
docker exec reverse_proxy nginx -t

# Recargar configuración
docker exec reverse_proxy nginx -s reload
```

### Localmente
```bash
# Verificar configuración
sudo nginx -t

# Iniciar Nginx
sudo systemctl start nginx

# Reiniciar Nginx
sudo systemctl restart nginx

# Ver logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Verificar Funcionamiento
```bash
# Test de conectividad
curl -I http://localhost:80

# Test de rutas
curl http://localhost/api/auth/health
curl http://localhost/api/blog/health
curl http://localhost/api/email/health
```

## 🛣️ Configuración de Rutas

### Configuración Principal
```nginx
# nginx.conf
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
    use epoll;
    multi_accept on;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    
    # Logging
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';
    
    access_log /var/log/nginx/access.log main;
    
    # Basic settings
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;
    
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=auth:10m rate=5r/s;
    
    # Upstream servers
    upstream auth_service {
        server auth-service:8000;
        keepalive 32;
    }
    
    upstream blog_service {
        server blog-service:8001;
        keepalive 32;
    }
    
    upstream email_service {
        server email-service:8002;
        keepalive 32;
    }
    
    upstream frontend {
        server frontend:3000;
        keepalive 32;
    }
    
    # Include site configurations
    include /etc/nginx/conf.d/*.conf;
}
```

### Configuración de Sitio
```nginx
# default.conf
server {
    listen 80;
    server_name localhost;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    # Frontend (React app)
    location / {
        proxy_pass http://frontend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
    
    # Auth Service
    location /api/auth/ {
        limit_req zone=auth burst=20 nodelay;
        
        proxy_pass http://auth_service/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # CORS
        add_header Access-Control-Allow-Origin $http_origin always;
        add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS" always;
        add_header Access-Control-Allow-Headers "Authorization, Content-Type" always;
        
        if ($request_method = 'OPTIONS') {
            add_header Access-Control-Allow-Origin $http_origin;
            add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS";
            add_header Access-Control-Allow-Headers "Authorization, Content-Type";
            add_header Access-Control-Max-Age 1728000;
            add_header Content-Type 'text/plain; charset=utf-8';
            add_header Content-Length 0;
            return 204;
        }
    }
    
    # Blog Service
    location /api/blog/ {
        limit_req zone=api burst=50 nodelay;
        
        proxy_pass http://blog_service/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Cache static content
        location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
    
    # Email Service
    location /api/email/ {
        limit_req zone=api burst=10 nodelay;
        
        proxy_pass http://email_service/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Health check endpoint
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
    
    # Static files
    location /static/ {
        alias /var/www/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

## ⚖️ Load Balancing

### Configuración de Upstreams
```nginx
# Load balancing con múltiples instancias
upstream auth_service {
    # Round-robin (default)
    server auth-service-1:8000 weight=1;
    server auth-service-2:8000 weight=1;
    server auth-service-3:8000 weight=2;  # Mayor peso
    
    # Health checks
    keepalive 32;
}

upstream blog_service {
    # Least connections
    least_conn;
    server blog-service-1:8001;
    server blog-service-2:8001;
    server blog-service-3:8001;
    
    keepalive 32;
}

upstream email_service {
    # IP hash para sticky sessions
    ip_hash;
    server email-service-1:8002;
    server email-service-2:8002;
    
    keepalive 32;
}
```

### Health Checks
```nginx
# Configuración de health checks
upstream auth_service {
    server auth-service:8000 max_fails=3 fail_timeout=30s;
    keepalive 32;
}

# Endpoint de health check
location /health/auth {
    proxy_pass http://auth_service/health;
    proxy_set_header Host $host;
    access_log off;
}
```

## 🔒 SSL/TLS

### Configuración SSL
```nginx
# SSL configuration
server {
    listen 443 ssl http2;
    server_name localhost;
    
    # SSL certificates
    ssl_certificate /etc/nginx/ssl/server.crt;
    ssl_certificate_key /etc/nginx/ssl/server.key;
    
    # SSL settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # HSTS
    add_header Strict-Transport-Security "max-age=63072000" always;
    
    # Rest of configuration...
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name localhost;
    return 301 https://$server_name$request_uri;
}
```

### Generar Certificados para Desarrollo
```bash
# Crear directorio SSL
mkdir -p ssl

# Generar clave privada
openssl genrsa -out ssl/server.key 2048

# Generar certificado autofirmado
openssl req -new -x509 -key ssl/server.key -out ssl/server.crt -days 365 -subj "/CN=localhost"

# Generar parámetros Diffie-Hellman
openssl dhparam -out ssl/dhparam.pem 2048
```

## ⚙️ Variables de Entorno

```env
# Nginx Configuration
NGINX_WORKER_PROCESSES=auto
NGINX_WORKER_CONNECTIONS=1024
NGINX_KEEPALIVE_TIMEOUT=65

# Upstream Services
AUTH_SERVICE_URL=http://auth-service:8000
BLOG_SERVICE_URL=http://blog-service:8001
EMAIL_SERVICE_URL=http://email-service:8002
FRONTEND_URL=http://frontend:3000

# Rate Limiting
RATE_LIMIT_API=10r/s
RATE_LIMIT_AUTH=5r/s
RATE_LIMIT_BURST=50

# SSL Configuration
SSL_ENABLED=false
SSL_CERT_PATH=/etc/nginx/ssl/server.crt
SSL_KEY_PATH=/etc/nginx/ssl/server.key

# Logging
LOG_LEVEL=info
ACCESS_LOG_ENABLED=true
ERROR_LOG_ENABLED=true
```

## 🧪 Testing

### Tests de Configuración
```bash
# Verificar configuración de Nginx
docker exec reverse_proxy nginx -t

# Test de conectividad
curl -I http://localhost/

# Test de rutas
curl http://localhost/api/auth/health
curl http://localhost/api/blog/health
curl http://localhost/api/email/health

# Test de rate limiting
for i in {1..20}; do curl http://localhost/api/auth/health; done
```

### Tests de Load Balancing
```bash
# Test con múltiples requests
for i in {1..10}; do
  curl -s http://localhost/api/auth/health | grep "Server:"
done

# Test de health checks
curl http://localhost/health/auth
curl http://localhost/health/blog
curl http://localhost/health/email
```

### Tests de SSL (si está habilitado)
```bash
# Test SSL
curl -k https://localhost/

# Verificar certificado
openssl s_client -connect localhost:443 -servername localhost
```

## 💻 Desarrollo

### Flujo de Desarrollo
1. **Modificar configuración** en `reverse-proxy/`
2. **Verificar configuración**:
   ```bash
   docker exec reverse_proxy nginx -t
   ```
3. **Recargar configuración**:
   ```bash
   docker exec reverse_proxy nginx -s reload
   ```
4. **Probar cambios**:
   ```bash
   curl http://localhost/api/auth/health
   ```

### Agregar Nuevas Rutas
1. **Editar** `default.conf`
2. **Agregar upstream** si es necesario
3. **Verificar configuración**:
   ```bash
   docker exec reverse_proxy nginx -t
   ```
4. **Recargar**:
   ```bash
   docker exec reverse_proxy nginx -s reload
   ```

### Estructura de Configuración
```nginx
# Agregar nuevo servicio
upstream new_service {
    server new-service:8003;
    keepalive 32;
}

# Agregar nueva ruta
location /api/new/ {
    limit_req zone=api burst=30 nodelay;
    
    proxy_pass http://new_service/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

## 🚨 Troubleshooting

### Problemas Comunes

#### "502 Bad Gateway"
```bash
# Verificar que los servicios estén corriendo
docker-compose ps

# Ver logs de Nginx
docker-compose logs reverse-proxy

# Verificar conectividad a upstreams
docker exec reverse_proxy curl http://auth-service:8000/health
```

#### "504 Gateway Timeout"
```bash
# Verificar configuración de timeout
docker exec reverse_proxy grep -r "proxy_read_timeout" /etc/nginx/

# Aumentar timeout en configuración
proxy_read_timeout 60s;
proxy_connect_timeout 30s;
```

#### "Rate limit exceeded"
```bash
# Ver logs de rate limiting
docker-compose logs reverse-proxy | grep "limiting requests"

# Ajustar límites en configuración
limit_req zone=api burst=100 nodelay;
```

#### "SSL certificate error"
```bash
# Verificar certificados
docker exec reverse_proxy ls -la /etc/nginx/ssl/

# Verificar configuración SSL
docker exec reverse_proxy nginx -t

# Regenerar certificados si es necesario
```

### Comandos de Diagnóstico
```bash
# Ver logs del servicio
docker-compose logs -f reverse-proxy

# Ver estado del contenedor
docker-compose ps reverse-proxy

# Entrar al contenedor
docker exec -it reverse_proxy bash

# Ver configuración activa
docker exec reverse_proxy nginx -T

# Ver procesos Nginx
docker exec reverse_proxy ps aux | grep nginx

# Verificar conectividad
docker exec reverse_proxy curl -I http://auth-service:8000/health
```

### Logs Útiles
```bash
# Logs de acceso
docker exec reverse_proxy tail -f /var/log/nginx/access.log

# Logs de error
docker exec reverse_proxy tail -f /var/log/nginx/error.log

# Logs con filtros
docker exec reverse_proxy tail -f /var/log/nginx/access.log | grep "POST /api/auth"
```

### Herramientas de Diagnóstico
```bash
# Verificar configuración
nginx -t

# Ver configuración completa
nginx -T

# Ver estadísticas (si está habilitado)
curl http://localhost/nginx_status

# Ver métricas de upstreams
curl http://localhost/upstream_status
```

## 📚 Recursos Adicionales

- [Nginx Documentation](https://nginx.org/en/docs/)
- [Nginx Configuration Guide](https://nginx.org/en/docs/beginners_guide.html)
- [Load Balancing with Nginx](https://nginx.org/en/docs/http/load_balancing.html)
- [SSL/TLS Configuration](https://nginx.org/en/docs/http/configuring_https_servers.html)

## 🔄 Próximos Pasos

- [ ] Implementar autenticación JWT en el proxy
- [ ] Agregar métricas y monitoring
- [ ] Implementar circuit breaker
- [ ] Agregar cache de respuestas
- [ ] Implementar blue-green deployment
- [ ] Agregar WAF (Web Application Firewall)

---

**¡El Reverse Proxy está listo para enrutar tu tráfico! 🔄**