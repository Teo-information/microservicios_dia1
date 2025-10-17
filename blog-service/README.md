# 📝 Blog Service

Servicio de gestión de contenido para artículos, posts y categorías del blog.

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

El **Blog Service** es responsable de:

- **Gestión de artículos** (CRUD completo)
- **Categorías y tags** de contenido
- **Sistema de comentarios**
- **Búsqueda y filtrado** de contenido
- **Gestión de autores**
- **Estados de publicación** (borrador, publicado, archivado)
- **SEO metadata** (meta tags, slugs)

## 🛠️ Tecnologías

- **Python 3.12**
- **FastAPI** (Framework web)
- **PostgreSQL** (Base de datos)
- **Redis** (Cache de contenido)
- **SQLAlchemy** (ORM)
- **Pydantic** (Validación de datos)
- **Elasticsearch** (Búsqueda avanzada - opcional)
- **Markdown** (Formato de contenido)

## 📁 Estructura del Servicio

```
blog-service/
├── 📄 Dockerfile           # Configuración del contenedor
├── 📄 requirements.txt     # Dependencias Python
├── 📄 app.py              # Aplicación principal FastAPI
├── 📄 models.py           # Modelos de base de datos
├── 📄 schemas.py          # Esquemas Pydantic
├── 📄 crud.py             # Operaciones CRUD
├── 📄 search.py           # Lógica de búsqueda
├── 📄 database.py         # Configuración de base de datos
├── 📄 config.py           # Configuración del servicio
├── 📁 tests/              # Tests unitarios
│   ├── 📄 test_articles.py
│   ├── 📄 test_categories.py
│   └── 📄 conftest.py
├── 📁 migrations/         # Migraciones de base de datos
└── 📄 README.md           # Este archivo
```

## 🚀 Instalación y Configuración

### Requisitos Previos
- Docker y Docker Compose
- PostgreSQL 15+
- Redis 7+
- Auth Service (para autenticación)

### Configuración con Docker
```bash
# Desde la raíz del proyecto
cd microservicios

# Levantar el blog-service
docker-compose up -d blog-service

# Verificar que esté funcionando
docker-compose ps blog-service
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
export AUTH_SERVICE_URL=http://localhost:8000
```

## 🏃‍♂️ Ejecución

### Con Docker (Recomendado)
```bash
# Levantar solo el blog-service
docker-compose up -d blog-service

# Ver logs
docker-compose logs -f blog-service

# Ejecutar tests
docker exec blog_service python -m pytest

# Entrar al contenedor
docker exec -it blog_service bash
```

### Localmente
```bash
# Activar entorno virtual
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows

# Ejecutar la aplicación
python app.py

# La API estará disponible en http://localhost:8001
```

### Verificar Conectividad
```bash
# Test de la API
curl http://localhost:8001/health

# Test de conectividad con Auth Service
curl http://localhost:8001/auth/verify
```

## 🔗 API Endpoints

### Artículos
```http
GET /articles
# Query params: ?page=1&limit=10&category=tech&search=python

GET /articles/{article_id}

POST /articles
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Mi Primer Artículo",
  "content": "# Contenido en Markdown",
  "category_id": 1,
  "tags": ["python", "tutorial"],
  "status": "published",
  "meta_description": "Descripción SEO"
}

PUT /articles/{article_id}
Authorization: Bearer <token>

DELETE /articles/{article_id}
Authorization: Bearer <token>
```

### Categorías
```http
GET /categories

POST /categories
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Tecnología",
  "description": "Artículos sobre tecnología",
  "slug": "tecnologia"
}

PUT /categories/{category_id}
Authorization: Bearer <token>

DELETE /categories/{category_id}
Authorization: Bearer <token>
```

### Comentarios
```http
GET /articles/{article_id}/comments

POST /articles/{article_id}/comments
Content-Type: application/json

{
  "author_name": "Juan Pérez",
  "author_email": "juan@example.com",
  "content": "Excelente artículo!"
}

DELETE /comments/{comment_id}
Authorization: Bearer <token>
```

### Búsqueda
```http
GET /search?q=python&category=tech&author=admin

GET /articles/popular
GET /articles/recent
GET /articles/featured
```

### Health Check
```http
GET /health
```

## 🗄️ Base de Datos

### Esquema de Artículos
```sql
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    slug VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    content TEXT NOT NULL,
    excerpt TEXT,
    author_id INTEGER NOT NULL,
    category_id INTEGER REFERENCES categories(id),
    status VARCHAR(20) DEFAULT 'draft', -- draft, published, archived
    featured BOOLEAN DEFAULT FALSE,
    meta_description VARCHAR(255),
    meta_keywords VARCHAR(255),
    published_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    slug VARCHAR(50) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE article_tags (
    article_id INTEGER REFERENCES articles(id),
    tag_id INTEGER REFERENCES tags(id),
    PRIMARY KEY (article_id, tag_id)
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    article_id INTEGER REFERENCES articles(id),
    author_name VARCHAR(100) NOT NULL,
    author_email VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    is_approved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Conexión a la Base de Datos
```bash
# Conectar directamente a PostgreSQL
docker exec -it db_postgres psql -U devuser -d main_db

# Ejecutar queries
\dt  # Ver tablas
SELECT * FROM articles;  # Ver artículos
SELECT * FROM categories;  # Ver categorías
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

# Auth Service
AUTH_SERVICE_URL=http://auth-service:8000

# Aplicación
BLOG_SERVICE_PORT=8001
DEBUG=True

# Cache
CACHE_TTL=3600  # 1 hora en segundos

# Búsqueda (opcional)
ELASTICSEARCH_URL=http://elasticsearch:9200
```

## 🧪 Testing

### Ejecutar Tests
```bash
# Todos los tests
docker exec blog_service python -m pytest

# Tests específicos
docker exec blog_service python -m pytest tests/test_articles.py

# Con cobertura
docker exec blog_service python -m pytest --cov=app tests/
```

### Tests Disponibles
- **test_articles.py**: Tests de CRUD de artículos
- **test_categories.py**: Tests de categorías
- **test_comments.py**: Tests de comentarios
- **test_search.py**: Tests de búsqueda

### Ejemplo de Test
```python
def test_create_article():
    article_data = {
        "title": "Test Article",
        "content": "# Test Content",
        "category_id": 1
    }
    response = client.post("/articles", json=article_data, headers=auth_headers)
    assert response.status_code == 201
    assert response.json()["title"] == "Test Article"
```

## 💻 Desarrollo

### Flujo de Desarrollo
1. **Modificar código** en `blog-service/`
2. **Reconstruir contenedor**:
   ```bash
   docker-compose up --build -d blog-service
   ```
3. **Ejecutar tests**:
   ```bash
   docker exec blog_service python -m pytest
   ```
4. **Ver logs**:
   ```bash
   docker-compose logs -f blog-service
   ```

### Agregar Nuevas Funcionalidades
1. **Modelo**: Agregar en `models.py`
2. **Schema**: Definir en `schemas.py`
3. **CRUD**: Implementar en `crud.py`
4. **Endpoint**: Agregar en `app.py`
5. **Test**: Crear en `tests/`

### Estructura de Código
```python
# app.py - Endpoint principal
@app.get("/articles/{article_id}")
async def get_article(article_id: int, db: Session = Depends(get_db)):
    article = crud.get_article(db, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

# crud.py - Operaciones CRUD
def get_article(db: Session, article_id: int):
    return db.query(Article).filter(Article.id == article_id).first()

def create_article(db: Session, article: ArticleCreate, author_id: int):
    db_article = Article(**article.dict(), author_id=author_id)
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article
```

### Migraciones de Base de Datos
```bash
# Crear migración
docker exec blog_service python -m alembic revision --autogenerate -m "Add new table"

# Aplicar migraciones
docker exec blog_service python -m alembic upgrade head

# Ver historial de migraciones
docker exec blog_service python -m alembic history
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
docker-compose restart postgres blog-service
```

#### "Auth Service connection failed"
```bash
# Verificar Auth Service
docker-compose ps auth-service

# Test conectividad
docker exec blog_service curl http://auth-service:8000/health

# Ver logs
docker-compose logs auth-service
```

#### "Redis cache not working"
```bash
# Verificar Redis
docker-compose logs redis

# Test Redis
docker exec cache_redis redis-cli ping

# Limpiar cache
docker exec cache_redis redis-cli FLUSHDB
```

#### "Article not found"
```bash
# Verificar datos en base de datos
docker exec db_postgres psql -U devuser -d main_db -c "SELECT * FROM articles;"

# Verificar slug único
docker exec db_postgres psql -U devuser -d main_db -c "SELECT slug FROM articles WHERE slug = 'mi-articulo';"
```

### Comandos de Diagnóstico
```bash
# Ver logs del servicio
docker-compose logs -f blog-service

# Ver estado del contenedor
docker-compose ps blog-service

# Entrar al contenedor
docker exec -it blog_service bash

# Ver variables de entorno
docker exec blog_service env

# Test de conectividad
docker exec blog_service curl http://auth-service:8000/health
```

### Logs Útiles
```bash
# Logs en tiempo real
docker-compose logs -f blog-service

# Logs con timestamp
docker-compose logs -t blog-service

# Últimas 100 líneas
docker-compose logs --tail=100 blog-service
```

## 📚 Recursos Adicionales

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Markdown Guide](https://www.markdownguide.org/)
- [Elasticsearch Documentation](https://www.elastic.co/guide/)

## 🔄 Próximos Pasos

- [ ] Implementar sistema de likes/dislikes
- [ ] Agregar sistema de seguimiento de autores
- [ ] Implementar notificaciones de comentarios
- [ ] Agregar analytics de artículos
- [ ] Implementar sistema de versionado
- [ ] Agregar importación/exportación de contenido

---

**¡El Blog Service está listo para gestionar tu contenido! 📝**