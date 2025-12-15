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

1. **Navega a la raíz de tu proyecto Java**:
   ```bash
   cd /path/to/your/java/project
   ```

2. **Ejecuta el generador**:
   ```bash
   retrofit-generator
   ```

3. **Responde las preguntas**:
   - **API name** (PascalCase): Nombre de tu API (ej: `MapBox`, `UserProfile`)
   - **Endpoint path**: Ruta relativa del endpoint (ej: `api/v1/geocode`)
   - **Base URL**: URL base del servicio (ej: `https://api.mapbox.com/`)
   - **Service identifier**: Identificador único para la config YAML (ej: `mapbox-api`)
   - **Does this API require credentials?**: Responde `y` si la API necesita autenticación, `n` si no
   - **Credential field names**: Si la API requiere credenciales, especifica los nombres de los campos separados por comas (ej: `apiKey,xRequestId`)

4. **Completa los TODOs**:
   - El generador crea archivos Java con placeholders `/* TODO: Add fields */` que debes completar con los campos según la API
   - Si agregaste credenciales, actualiza los valores `TODO_ADD_VALUE` en el YAML con las credenciales reales

## Ejemplo de Uso

### Ejemplo 1: API sin credenciales

```bash
$ retrofit-generator

API name (PascalCase, e.g. MapBox, UserProfile): MapBox
Endpoint path (e.g. api/v1/geocode): api/v1/geocode
Base URL (e.g. https://api.mapbox.com/): https://api.mapbox.com/
YAML property identifier (e.g. mapbox-api): mapbox-api
Does this API require credentials? (y/n): n
Credential field names (comma-separated, e.g. apiKey,xRequestId):

🚀 Generating Retrofit client for: MapBox
   Base package: com.example.myapp
   Endpoint: api/v1/geocode

📝 Generating Java files...
✓ Created: src/main/java/com/example/myapp/client/dto/MapBoxRequestDto.java
✓ Created: src/main/java/com/example/myapp/client/dto/MapBoxResponseDto.java
...

⚙️  Updating configuration files...
✓ Added import to RestClientConfig.java
✓ Added bean to RestClientConfig.java
✓ Added bean to EndpointsConfig.java
✓ Added default http-client.timeout property
✓ Added default http-client.logging-level property
✓ Added default http-client.connect-timeout property
✓ Added configuration to application-local.yml

✅ Successfully generated MapBox Retrofit client!
```

**YAML generado:**
```yaml
http-client:
  timeout: 30
  logging-level: BODY
  connect-timeout: 10
  mapbox-api:
    base-url: https://api.mapbox.com/
    logging-level: ${http-client.logging-level}
    read-timeout: ${http-client.timeout}
    connect-timeout: ${http-client.connect-timeout}
```

### Ejemplo 2: API con credenciales

```bash
$ retrofit-generator

API name (PascalCase, e.g. MapBox, UserProfile): HerePartner
Endpoint path (e.g. api/v1/geocode): v1/geocode
Base URL (e.g. https://api.mapbox.com/): https://geocode.search.hereapi.com/
YAML property identifier (e.g. mapbox-api): here-partner
Does this API require credentials? (y/n): y
Credential field names (comma-separated, e.g. apiKey,xRequestId): apiKey,xRequestId

🚀 Generating Retrofit client for: HerePartner
...
✓ Added configuration to application-local.yml
✓ Added credentials section for here-partner

✅ Successfully generated HerePartner Retrofit client!
```

**YAML generado:**
```yaml
http-client:
  timeout: 30
  logging-level: BODY
  connect-timeout: 10
  here-partner:
    base-url: https://geocode.search.hereapi.com/
    logging-level: ${http-client.logging-level}
    read-timeout: ${http-client.timeout}
    connect-timeout: ${http-client.connect-timeout}

credentials:
  here-partner:
    apiKey: TODO_ADD_VALUE
    xRequestId: TODO_ADD_VALUE
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

- `__ApiName__`: Nombre en PascalCase (ej: `MapBox`)
- `__apiName__`: Nombre en camelCase (ej: `mapBox`)
- `__basePackage__`: Package base detectado (ej: `com.example.app`)
- `__endpointPath__`: Path del endpoint (ej: `api/v1/geocode`)
- `__baseUrl__`: URL base (ej: `https://api.mapbox.com/`)
- `__serviceIdentifier__`: Identificador del servicio (ej: `mapbox-api`)

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
