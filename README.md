# Retrofit API Client Generator

Generador inteligente de clientes Retrofit para proyectos Java/Spring Boot.

## Características

- 🚀 Genera un cliente Retrofit completo con una sola ejecución
- 📝 Templates externos fáciles de modificar
- 🔍 Detecta automáticamente el package base del proyecto
- ⚙️ Actualiza archivos de configuración existentes
- ✨ Sigue las convenciones de Spring Boot y MapStruct

## Estructura Generada

El generador crea:

- **DTOs** (Request/Response)
- **Domain Objects** (Request/Response)
- **MapStruct Mappers** (Request/Response)
- **Client Interface** (contrato del cliente)
- **Retrofit API Interface** (anotaciones HTTP)
- **Client Implementation** (lógica del cliente)
- **Configuración Spring** (beans en RestClientConfig y EndpointsConfig)
- **Configuración YAML** (application-local.yml)

## Instalación

### Opción 1: Instalación con pip (Recomendado)

Instala el paquete localmente:

```bash
cd /path/to/retrofit-generator
pip install -e .
```

O si querés instalarlo sin modo editable:

```bash
pip install .
```

Esto instala el comando `retrofit-generator` globalmente en tu sistema.

### Opción 2: Instalación desde el código fuente

1. Clona este repositorio
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecuta directamente: `python -m retrofit_generator.cli`

## Uso

### Modo Interactivo (Recomendado)

1. **Navega a la raíz de tu proyecto Java**:
   ```bash
   cd /path/to/your/java/project
   ```

2. **Ejecuta el generador**:
   ```bash
   retrofit-generator
   ```

3. **Responde las preguntas**:
   - **API name** (PascalCase): Nombre de tu API (ej: `UserService`, `PaymentGateway`)
   - **Endpoint path**: Ruta relativa del endpoint (ej: `api/v1/users`)
   - **Base URL**: URL base del servicio (ej: `https://api.example.com/`)
   - **Service identifier**: Se genera automáticamente en kebab-case con sufijo `-api` (ej: `UserService` → `user-service-api`). Puedes cambiarlo si lo necesitas.
   - **Does this API require credentials?**: Responde `y` si la API necesita autenticación, `n` si no
   - **Credential field names**: Si la API requiere credenciales, especifica los nombres de los campos separados por comas (ej: `apiKey,token`)

4. **Completa los TODOs**:
   - El generador crea archivos Java con placeholders `/* TODO: Add fields */` que debes completar con los campos según la API
   - Si agregaste credenciales, actualiza los valores `TODO_ADD_VALUE` en el YAML con las credenciales reales

### Modo No-Interactivo (Línea de Comandos)

Puedes ejecutar el generador en una sola línea pasando todos los parámetros:

```bash
# Sintaxis básica
retrofit-generator --api-name=<NombreAPI> --endpoint-path=<ruta> --base-url=<url>

# API sin credenciales
retrofit-generator --api-name=UserService --endpoint-path=api/v1/users --base-url=https://api.example.com/

# API con credenciales
retrofit-generator --api-name=PaymentGateway --endpoint-path=v1/payments --base-url=https://pay.example.com/ --credentials=apiKey,secretKey

# Con service identifier personalizado
retrofit-generator --api-name=BigDataCloud --endpoint-path=data/reverse-geocode --base-url=https://api-bdc.net/ --service-identifier=bdc-geo-api
```

**Parámetros disponibles:**
- `--api-name`: Nombre de la API en PascalCase (requerido)
- `--endpoint-path`: Ruta del endpoint (requerido)
- `--base-url`: URL base del servicio (requerido)
- `--service-identifier`: Identificador YAML (opcional, se auto-genera si no se proporciona)
- `--credentials`: Lista de campos de credenciales separados por comas (opcional)

**Ver ayuda:**
```bash
retrofit-generator --help
```

## Ejemplos de Uso

### Ejemplo 1: Modo Interactivo - API sin credenciales

```bash
$ retrofit-generator

API name (PascalCase, e.g. UserService, PaymentGateway): UserService
Endpoint path (e.g. api/v1/users): api/v1/users
Base URL (e.g. https://api.example.com/): https://api.example.com/

💡 Generated YAML property identifier: user-service-api
Do you want to change it? (y/n) [n]: n
✓ Using: user-service-api

Does this API require credentials? (y/n) [n]: n

🚀 Generating Retrofit client for: UserService
   Base package: com.example.myapp
   Endpoint: api/v1/users

📝 Generating Java files...
✓ Created: src/main/java/com/example/myapp/client/dto/UserServiceRequestDto.java
✓ Created: src/main/java/com/example/myapp/client/dto/UserServiceResponseDto.java
...

⚙️  Updating configuration files...
✓ Added import to RestClientConfig.java
✓ Added bean to RestClientConfig.java
✓ Added bean to EndpointsConfig.java
✓ Added default http-client.timeout property
✓ Added default http-client.logging-level property
✓ Added default http-client.connect-timeout property
✓ Added configuration to application-local.yml

✅ Successfully generated UserService Retrofit client!
```

**YAML generado:**
```yaml
http-client:
  timeout: 30
  logging-level: BODY
  connect-timeout: 10
  user-service-api:
    base-url: https://api.example.com/
    logging-level: ${http-client.logging-level}
    read-timeout: ${http-client.timeout}
    connect-timeout: ${http-client.connect-timeout}
```

### Ejemplo 2: Modo Interactivo - API con credenciales

```bash
$ retrofit-generator

API name (PascalCase, e.g. UserService, PaymentGateway): PaymentGateway
Endpoint path (e.g. api/v1/users): v1/payments
Base URL (e.g. https://api.example.com/): https://payments.example.com/

💡 Generated YAML property identifier: payment-gateway-api
Do you want to change it? (y/n) [n]: n
✓ Using: payment-gateway-api

Does this API require credentials? (y/n) [n]: y
Credential field names (comma-separated, e.g. apiKey,token): apiKey,secretKey

🚀 Generating Retrofit client for: PaymentGateway
...
✓ Added configuration to application-local.yml
✓ Added credentials section for payment-gateway-api

✅ Successfully generated PaymentGateway Retrofit client!
```

**YAML generado:**
```yaml
http-client:
  timeout: 30
  logging-level: BODY
  connect-timeout: 10
  payment-gateway-api:
    base-url: https://payments.example.com/
    logging-level: ${http-client.logging-level}
    read-timeout: ${http-client.timeout}
    connect-timeout: ${http-client.connect-timeout}

credentials:
  payment-gateway-api:
    apiKey: TODO_ADD_VALUE
    secretKey: TODO_ADD_VALUE
```

### Ejemplo 3: Modo No-Interactivo - Una sola línea

```bash
$ cd /path/to/java-project
$ retrofit-generator --api-name=BigDataCloud --endpoint-path=data/reverse-geocode --base-url=https://api-bdc.net/

✓ Generated service identifier: big-data-cloud-api

🚀 Generating Retrofit client for: BigDataCloud
   Base package: com.example.myapp
   Endpoint: data/reverse-geocode

📝 Generating Java files...
✓ Created: src/main/java/com/example/myapp/client/dto/BigDataCloudRequestDto.java
✓ Created: src/main/java/com/example/myapp/client/dto/BigDataCloudResponseDto.java
...

⚙️  Updating configuration files...
✓ Added import to RestClientConfig.java
✓ Added bean to RestClientConfig.java
✓ Added bean to EndpointsConfig.java
✓ Added default http-client.timeout property
✓ Added default http-client.logging-level property
✓ Added default http-client.connect-timeout property
✓ Added configuration to application-local.yml

✅ Successfully generated BigDataCloud Retrofit client!
```

**YAML generado:**
```yaml
http-client:
  timeout: 30
  logging-level: BODY
  connect-timeout: 10
  big-data-cloud-api:
    base-url: https://api-bdc.net/
    logging-level: ${http-client.logging-level}
    read-timeout: ${http-client.timeout}
    connect-timeout: ${http-client.connect-timeout}
```

### Ejemplo 4: Modo No-Interactivo - Con credenciales

```bash
$ retrofit-generator --api-name=AuthService --endpoint-path=oauth/v2/token --base-url=https://auth.example.com/ --credentials=clientId,clientSecret

✓ Generated service identifier: auth-service-api
✓ Using credentials: clientId, clientSecret

🚀 Generating Retrofit client for: AuthService
...
✓ Added credentials section for auth-service-api

✅ Successfully generated AuthService Retrofit client!
```

**YAML generado:**
```yaml
http-client:
  timeout: 30
  logging-level: BODY
  connect-timeout: 10
  auth-service-api:
    base-url: https://auth.example.com/
    logging-level: ${http-client.logging-level}
    read-timeout: ${http-client.timeout}
    connect-timeout: ${http-client.connect-timeout}

credentials:
  auth-service-api:
    clientId: TODO_ADD_VALUE
    clientSecret: TODO_ADD_VALUE
```

## Personalización de Templates

### En modo desarrollo

Si instalaste con `pip install -e .`, los templates están en `retrofit_generator/templates/` y puedes modificarlos directamente.

### En instalación normal

Los templates se instalan con el paquete. Para personalizarlos, necesitarás:
1. Clonar/descargar el código fuente
2. Modificar los templates en `retrofit_generator/templates/`
3. Reinstalar con `pip install -e .`

Todos los templates usan placeholders que puedes modificar según tus necesidades.

### Placeholders disponibles:

- `__ApiName__`: Nombre en PascalCase (ej: `UserService`)
- `__apiName__`: Nombre en camelCase (ej: `userService`)
- `__basePackage__`: Package base detectado (ej: `com.example.app`)
- `__endpointPath__`: Path del endpoint (ej: `api/v1/users`)
- `__baseUrl__`: URL base (ej: `https://api.example.com/`)
- `__serviceIdentifier__`: Identificador del servicio (ej: `user-service-api`)

### Estructura de templates:

```
templates/
├── client/
│   ├── dto/
│   │   ├── __ApiName__RequestDto.java
│   │   └── __ApiName__ResponseDto.java
│   ├── mapper/
│   │   ├── __ApiName__RequestClientMapper.java
│   │   └── __ApiName__ResponseClientMapper.java
│   └── rest/
│       ├── __ApiName__Client.java
│       ├── api/
│       │   └── __ApiName__Api.java
│       └── impl/
│           └── __ApiName__ClientImpl.java
├── domain/
│   └── external_request/
│       ├── __ApiName__Request.java
│       └── __ApiName__Response.java
└── config_snippets/
    ├── RestClientConfig.import.java
    ├── RestClientConfig.bean.java
    ├── EndpointsConfig.bean.java
    └── application.yml
```

## Requisitos del Proyecto Java

Tu proyecto debe tener la siguiente estructura (o el generador buscará recursivamente):

```
your-java-project/
├── src/
│   └── main/
│       ├── java/
│       │   └── com/example/yourapp/
│       │       ├── client/          # ← REQUERIDO: El generador busca este directorio
│       │       └── config/
│       │           ├── RestClientConfig.java      # ← Buscado recursivamente si no está aquí
│       │           └── endpoints/
│       │               └── EndpointsConfig.java   # ← Buscado recursivamente si no está aquí
│       └── resources/
│           └── application-local.yml              # ← Buscado recursivamente si no está aquí
```

**Nota:** El directorio `client` **debe existir** para la detección del base package. Los demás archivos se buscan recursivamente si no están en la ubicación estándar.

## Características Avanzadas

### Búsqueda Recursiva de Archivos
Si los archivos de configuración no están en las ubicaciones estándar, el generador los busca recursivamente en todo el proyecto.

### Properties YAML con Placeholders
Las configuraciones usan **kebab-case** y referencian propiedades globales:
- `base-url`: URL específica del servicio
- `logging-level`: Referencia a `${http-client.logging-level}`
- `read-timeout`: Referencia a `${http-client.timeout}`
- `connect-timeout`: Referencia a `${http-client.connect-timeout}`

### Creación Automática de Properties Globales
Si las properties globales de `http-client` no existen, se crean automáticamente con valores por defecto.

### Gestión de Credenciales
Opcionalmente agrega una sección `credentials` con campos personalizables para APIs que requieren autenticación.

## Notas

- El script detecta automáticamente el **base package** buscando un directorio llamado `client` dentro de `src/main/java/`
- Si un archivo ya existe, el generador lo saltea con una advertencia
- Los archivos de configuración existentes son modificados (se agregan imports/beans/YAML)
- Si las configuraciones del servicio ya existen, no se sobrescriben
- Los valores de credenciales deben actualizarse manualmente desde `TODO_ADD_VALUE`

## Dependencias

- Python 3.7+
- `click`: CLI interactivo
- `ruamel.yaml`: Manipulación de YAML preservando formato

## Autor

Generado con Claude Code
