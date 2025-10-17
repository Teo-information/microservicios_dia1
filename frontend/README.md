# 🌐 Frontend

Aplicación web frontend desarrollada con React para el ecosistema de microservicios.

## 📋 Tabla de Contenidos

- [Descripción](#-descripción)
- [Tecnologías](#-tecnologías)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Instalación y Configuración](#-instalación-y-configuración)
- [Ejecución](#-ejecución)
- [Estructura de Componentes](#-estructura-de-componentes)
- [Rutas y Navegación](#-rutas-y-navegación)
- [Integración con APIs](#-integración-con-apis)
- [Variables de Entorno](#-variables-de-entorno)
- [Testing](#-testing)
- [Desarrollo](#-desarrollo)
- [Troubleshooting](#-troubleshooting)

## 🎯 Descripción

El **Frontend** es responsable de:

- **Interfaz de usuario** moderna y responsiva
- **Autenticación** y gestión de sesiones
- **Gestión de contenido** (artículos, comentarios)
- **Dashboard administrativo**
- **Perfil de usuario**
- **Búsqueda y filtrado** de contenido
- **Notificaciones** en tiempo real
- **PWA** (Progressive Web App)

## 🛠️ Tecnologías

- **React 18** (Framework principal)
- **TypeScript** (Tipado estático)
- **Vite** (Build tool)
- **React Router** (Ruteo)
- **Axios** (Cliente HTTP)
- **Tailwind CSS** (Styling)
- **React Query** (Estado del servidor)
- **Zustand** (Estado global)
- **React Hook Form** (Formularios)
- **React Toastify** (Notificaciones)

## 📁 Estructura del Proyecto

```
frontend/
├── 📄 package.json         # Dependencias y scripts
├── 📄 package-lock.json    # Lock de dependencias
├── 📄 vite.config.ts       # Configuración de Vite
├── 📄 tailwind.config.js   # Configuración de Tailwind
├── 📄 tsconfig.json        # Configuración de TypeScript
├── 📄 index.html           # HTML principal
├── 📁 src/                 # Código fuente
│   ├── 📄 main.tsx         # Punto de entrada
│   ├── 📄 App.tsx          # Componente principal
│   ├── 📁 components/      # Componentes reutilizables
│   │   ├── 📁 ui/          # Componentes base
│   │   ├── 📁 forms/       # Componentes de formularios
│   │   ├── 📁 layout/      # Componentes de layout
│   │   └── 📁 common/      # Componentes comunes
│   ├── 📁 pages/           # Páginas de la aplicación
│   │   ├── 📄 Home.tsx
│   │   ├── 📄 Login.tsx
│   │   ├── 📄 Register.tsx
│   │   ├── 📄 Dashboard.tsx
│   │   ├── 📄 Articles.tsx
│   │   └── 📄 Profile.tsx
│   ├── 📁 hooks/           # Custom hooks
│   │   ├── 📄 useAuth.ts
│   │   ├── 📄 useApi.ts
│   │   └── 📄 useLocalStorage.ts
│   ├── 📁 services/        # Servicios API
│   │   ├── 📄 api.ts
│   │   ├── 📄 auth.ts
│   │   ├── 📄 articles.ts
│   │   └── 📄 users.ts
│   ├── 📁 store/           # Estado global
│   │   ├── 📄 authStore.ts
│   │   └── 📄 uiStore.ts
│   ├── 📁 utils/           # Utilidades
│   │   ├── 📄 constants.ts
│   │   ├── 📄 helpers.ts
│   │   └── 📄 validation.ts
│   ├── 📁 types/           # Tipos TypeScript
│   │   ├── 📄 auth.ts
│   │   ├── 📄 article.ts
│   │   └── 📄 api.ts
│   └── 📁 assets/          # Recursos estáticos
│       ├── 📁 images/
│       ├── 📁 icons/
│       └── 📁 styles/
├── 📁 public/              # Archivos públicos
│   ├── 📄 favicon.ico
│   ├── 📄 manifest.json
│   └── 📄 robots.txt
├── 📁 tests/               # Tests
│   ├── 📁 components/
│   ├── 📁 pages/
│   └── 📄 setup.ts
└── 📄 README.md            # Este archivo
```

## 🚀 Instalación y Configuración

### Requisitos Previos
- **Node.js** 18+ y npm
- **Docker** y Docker Compose (opcional)
- Servicios backend funcionando

### Configuración con Docker
```bash
# Desde la raíz del proyecto
cd microservicios

# Levantar el frontend
docker-compose up -d frontend

# Verificar que esté funcionando
docker-compose ps frontend
```

### Configuración Local (Desarrollo)
```bash
# Navegar al directorio frontend
cd frontend

# Instalar dependencias
npm install

# Configurar variables de entorno
cp .env.example .env.local
```

### Configurar Variables de Entorno
```bash
# .env.local
VITE_API_BASE_URL=http://localhost:3000
VITE_AUTH_SERVICE_URL=http://localhost:8000
VITE_BLOG_SERVICE_URL=http://localhost:8001
VITE_EMAIL_SERVICE_URL=http://localhost:8002
VITE_APP_TITLE=Microservicios Lab
VITE_APP_VERSION=1.0.0
```

## 🏃‍♂️ Ejecución

### Con Docker (Recomendado)
```bash
# Levantar solo el frontend
docker-compose up -d frontend

# Ver logs
docker-compose logs -f frontend

# Ejecutar tests
docker exec frontend npm test

# Entrar al contenedor
docker exec -it frontend bash
```

### Localmente
```bash
# Activar entorno
cd frontend

# Modo desarrollo
npm run dev

# Modo producción
npm run build
npm run preview

# La aplicación estará disponible en http://localhost:5173
```

### Scripts Disponibles
```bash
npm run dev          # Servidor de desarrollo
npm run build        # Build de producción
npm run preview      # Preview del build
npm run test         # Ejecutar tests
npm run test:coverage # Tests con cobertura
npm run lint         # Linter
npm run lint:fix     # Arreglar problemas de lint
npm run type-check   # Verificar tipos TypeScript
```

## 🧩 Estructura de Componentes

### Componentes Base (UI)
```typescript
// src/components/ui/Button.tsx
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  onClick?: () => void;
  children: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  disabled = false,
  onClick,
  children
}) => {
  return (
    <button
      className={`btn btn-${variant} btn-${size}`}
      disabled={disabled}
      onClick={onClick}
    >
      {children}
    </button>
  );
};
```

### Componentes de Formularios
```typescript
// src/components/forms/LoginForm.tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { loginSchema } from '../../utils/validation';

export const LoginForm: React.FC = () => {
  const { register, handleSubmit, formState: { errors } } = useForm({
    resolver: zodResolver(loginSchema)
  });

  const onSubmit = async (data: LoginFormData) => {
    // Lógica de login
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {/* Campos del formulario */}
    </form>
  );
};
```

### Layout Components
```typescript
// src/components/layout/Header.tsx
export const Header: React.FC = () => {
  const { user, logout } = useAuth();

  return (
    <header className="bg-white shadow-sm">
      <nav className="container mx-auto px-4 py-2">
        <div className="flex justify-between items-center">
          <Link to="/" className="text-xl font-bold">
            Microservicios Lab
          </Link>
          {user ? (
            <UserMenu user={user} onLogout={logout} />
          ) : (
            <AuthButtons />
          )}
        </div>
      </nav>
    </header>
  );
};
```

## 🛣️ Rutas y Navegación

### Configuración de Rutas
```typescript
// src/App.tsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ProtectedRoute } from './components/ProtectedRoute';

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        <Header />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            {/* Rutas públicas */}
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/articles" element={<Articles />} />
            <Route path="/articles/:id" element={<ArticleDetail />} />
            
            {/* Rutas protegidas */}
            <Route path="/dashboard" element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            } />
            <Route path="/profile" element={
              <ProtectedRoute>
                <Profile />
              </ProtectedRoute>
            } />
            <Route path="/admin" element={
              <ProtectedRoute role="admin">
                <AdminPanel />
              </ProtectedRoute>
            } />
            
            {/* 404 */}
            <Route path="*" element={<NotFound />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </BrowserRouter>
  );
}
```

### Navegación Protegida
```typescript
// src/components/ProtectedRoute.tsx
interface ProtectedRouteProps {
  children: React.ReactNode;
  role?: string;
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ 
  children, 
  role 
}) => {
  const { user, isLoading } = useAuth();

  if (isLoading) {
    return <LoadingSpinner />;
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (role && user.role !== role) {
    return <Navigate to="/unauthorized" replace />;
  }

  return <>{children}</>;
};
```

## 🔌 Integración con APIs

### Configuración de Axios
```typescript
// src/services/api.ts
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 10000,
});

// Interceptor para agregar token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor para manejar errores
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expirado, redirigir a login
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
```

### Servicios de API
```typescript
// src/services/auth.ts
import api from './api';

export const authService = {
  async login(credentials: LoginCredentials) {
    const response = await api.post('/auth/login', credentials);
    return response.data;
  },

  async register(userData: RegisterData) {
    const response = await api.post('/auth/register', userData);
    return response.data;
  },

  async logout() {
    const response = await api.post('/auth/logout');
    return response.data;
  },

  async getProfile() {
    const response = await api.get('/users/me');
    return response.data;
  }
};

// src/services/articles.ts
export const articlesService = {
  async getArticles(params?: ArticlesParams) {
    const response = await api.get('/articles', { params });
    return response.data;
  },

  async getArticle(id: string) {
    const response = await api.get(`/articles/${id}`);
    return response.data;
  },

  async createArticle(article: CreateArticleData) {
    const response = await api.post('/articles', article);
    return response.data;
  }
};
```

### Custom Hooks
```typescript
// src/hooks/useAuth.ts
export const useAuth = () => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const login = async (credentials: LoginCredentials) => {
    try {
      const response = await authService.login(credentials);
      localStorage.setItem('access_token', response.access_token);
      setUser(response.user);
      return response;
    } catch (error) {
      throw error;
    }
  };

  const logout = async () => {
    try {
      await authService.logout();
    } finally {
      localStorage.removeItem('access_token');
      setUser(null);
    }
  };

  useEffect(() => {
    const initAuth = async () => {
      const token = localStorage.getItem('access_token');
      if (token) {
        try {
          const user = await authService.getProfile();
          setUser(user);
        } catch (error) {
          localStorage.removeItem('access_token');
        }
      }
      setIsLoading(false);
    };

    initAuth();
  }, []);

  return { user, isLoading, login, logout };
};

// src/hooks/useApi.ts
export const useApi = <T>(
  endpoint: string,
  options?: UseQueryOptions<T>
) => {
  return useQuery<T>(
    endpoint,
    () => api.get(endpoint).then(res => res.data),
    options
  );
};
```

## ⚙️ Variables de Entorno

```env
# URLs de los servicios
VITE_API_BASE_URL=http://localhost:3000
VITE_AUTH_SERVICE_URL=http://localhost:8000
VITE_BLOG_SERVICE_URL=http://localhost:8001
VITE_EMAIL_SERVICE_URL=http://localhost:8002

# Configuración de la app
VITE_APP_TITLE=Microservicios Lab
VITE_APP_VERSION=1.0.0
VITE_APP_DESCRIPTION=Laboratorio de microservicios

# Configuración de desarrollo
VITE_DEBUG=true
VITE_LOG_LEVEL=debug

# Configuración de analytics (opcional)
VITE_GOOGLE_ANALYTICS_ID=GA-XXXXXXXXX
```

## 🧪 Testing

### Configuración de Tests
```typescript
// tests/setup.ts
import { render } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const createTestQueryClient = () => new QueryClient({
  defaultOptions: {
    queries: { retry: false },
    mutations: { retry: false },
  },
});

export const renderWithProviders = (ui: React.ReactElement) => {
  const testQueryClient = createTestQueryClient();
  
  return render(
    <QueryClientProvider client={testQueryClient}>
      <BrowserRouter>
        {ui}
      </BrowserRouter>
    </QueryClientProvider>
  );
};
```

### Ejemplo de Test
```typescript
// tests/components/LoginForm.test.tsx
import { renderWithProviders } from '../setup';
import { LoginForm } from '../../src/components/forms/LoginForm';
import { screen, fireEvent, waitFor } from '@testing-library/react';

describe('LoginForm', () => {
  it('should submit form with valid data', async () => {
    renderWithProviders(<LoginForm />);
    
    const usernameInput = screen.getByLabelText(/username/i);
    const passwordInput = screen.getByLabelText(/password/i);
    const submitButton = screen.getByRole('button', { name: /login/i });
    
    fireEvent.change(usernameInput, { target: { value: 'testuser' } });
    fireEvent.change(passwordInput, { target: { value: 'password123' } });
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText(/login successful/i)).toBeInTheDocument();
    });
  });
});
```

### Ejecutar Tests
```bash
# Todos los tests
npm test

# Tests con watch mode
npm run test:watch

# Tests con cobertura
npm run test:coverage

# Tests específicos
npm test -- LoginForm
```

## 💻 Desarrollo

### Flujo de Desarrollo
1. **Crear nueva rama**:
   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```

2. **Desarrollar funcionalidad**:
   ```bash
   npm run dev
   ```

3. **Ejecutar tests**:
   ```bash
   npm test
   ```

4. **Linting**:
   ```bash
   npm run lint:fix
   ```

5. **Build**:
   ```bash
   npm run build
   ```

### Agregar Nuevos Componentes
1. **Crear archivo** en `src/components/`
2. **Exportar** en `src/components/index.ts`
3. **Agregar tipos** en `src/types/`
4. **Crear tests** en `tests/components/`

### Estructura de Código
```typescript
// src/components/ArticleCard.tsx
interface ArticleCardProps {
  article: Article;
  onEdit?: (article: Article) => void;
  onDelete?: (id: string) => void;
}

export const ArticleCard: React.FC<ArticleCardProps> = ({
  article,
  onEdit,
  onDelete
}) => {
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-xl font-semibold mb-2">{article.title}</h3>
      <p className="text-gray-600 mb-4">{article.excerpt}</p>
      <div className="flex justify-between items-center">
        <span className="text-sm text-gray-500">
          {formatDate(article.created_at)}
        </span>
        <div className="space-x-2">
          {onEdit && (
            <Button size="sm" onClick={() => onEdit(article)}>
              Editar
            </Button>
          )}
          {onDelete && (
            <Button 
              size="sm" 
              variant="danger" 
              onClick={() => onDelete(article.id)}
            >
              Eliminar
            </Button>
          )}
        </div>
      </div>
    </div>
  );
};
```

## 🚨 Troubleshooting

### Problemas Comunes

#### "Module not found"
```bash
# Limpiar node_modules y reinstalar
rm -rf node_modules package-lock.json
npm install

# Verificar que el archivo existe
ls -la src/components/
```

#### "API connection failed"
```bash
# Verificar variables de entorno
cat .env.local

# Verificar que los servicios estén corriendo
docker-compose ps

# Test manual de la API
curl http://localhost:8000/health
```

#### "Build failed"
```bash
# Verificar errores de TypeScript
npm run type-check

# Verificar errores de linting
npm run lint

# Limpiar build
rm -rf dist
npm run build
```

#### "Tests failing"
```bash
# Ejecutar tests con más detalle
npm test -- --verbose

# Limpiar cache de tests
npm test -- --clearCache

# Ejecutar tests específicos
npm test -- --testNamePattern="LoginForm"
```

### Comandos de Diagnóstico
```bash
# Ver logs del servicio
docker-compose logs -f frontend

# Ver estado del contenedor
docker-compose ps frontend

# Entrar al contenedor
docker exec -it frontend bash

# Ver variables de entorno
docker exec frontend env

# Verificar build
docker exec frontend npm run build
```

### Logs Útiles
```bash
# Logs en tiempo real
docker-compose logs -f frontend

# Logs con timestamp
docker-compose logs -t frontend

# Últimas 100 líneas
docker-compose logs --tail=100 frontend
```

## 📚 Recursos Adicionales

- [React Documentation](https://react.dev/)
- [TypeScript Documentation](https://www.typescriptlang.org/)
- [Vite Documentation](https://vitejs.dev/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)
- [React Router Documentation](https://reactrouter.com/)

## 🔄 Próximos Pasos

- [ ] Implementar PWA (Service Worker)
- [ ] Agregar tests E2E con Playwright
- [ ] Implementar internacionalización (i18n)
- [ ] Agregar dark mode
- [ ] Implementar notificaciones push
- [ ] Agregar analytics y métricas

---

**¡El Frontend está listo para tu aplicación! 🌐**