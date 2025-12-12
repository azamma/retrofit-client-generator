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

4. **Completa los TODOs**:
   El generador crea los archivos con placeholders `/* TODO: Add fields */`.
   Debes agregar manualmente los campos de los records según la API.

## Ejemplo de Uso

```bash
$ retrofit-generator

API name (PascalCase): MapBox
Endpoint path: api/v1/geocode
Base URL: https://api.mapbox.com/
Service identifier: mapbox-api

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
✓ Added configuration to application-local.yml

✅ Successfully generated MapBox Retrofit client!
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

Tu proyecto debe tener la siguiente estructura estándar:

```
your-java-project/
├── src/
│   └── main/
│       ├── java/
│       │   └── com/example/yourapp/
│       │       ├── client/          # ← El generador busca este directorio
│       │       └── config/
│       │           ├── RestClientConfig.java
│       │           └── endpoints/
│       │               └── EndpointsConfig.java
│       └── resources/
│           └── application-local.yml
```

## Notas

- El script detecta automáticamente el **base package** buscando un directorio llamado `client` dentro de `src/main/java/`
- Si un archivo ya existe, el generador lo saltea con una advertencia
- Los archivos de configuración existentes son modificados (se agregan imports/beans/YAML)

## Dependencias

- Python 3.7+
- `click`: CLI interactivo
- `ruamel.yaml`: Manipulación de YAML preservando formato

## Autor

Generado con Claude Code
