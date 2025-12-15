# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python CLI tool that generates complete Retrofit API clients for Java/Spring Boot projects. It uses a template-based approach with placeholder replacement to generate DTOs, mappers, client interfaces, implementations, and configuration updates.

## Development Commands

### Installation for Development
```bash
# Install in editable mode (changes to code/templates take effect immediately)
pip install -e .

# Install dependencies only
pip install -r requirements.txt
```

### Running the Tool

**If installed via pip:**
```bash
retrofit-generator
```

**Running directly without installation:**
```bash
# From repository root
python -m retrofit_generator.cli

# Or using the standalone script
python generate.py
```

### Testing the Generator
Navigate to a Java/Spring Boot project and run the generator:
```bash
cd /path/to/java-project
retrofit-generator
```

The tool expects the Java project to have:
- `src/main/java/*/client/` directory (for package detection)
- `src/main/java/*/config/RestClientConfig.java`
- `src/main/java/*/config/endpoints/EndpointsConfig.java`
- `src/main/resources/application-local.yml`

## Architecture

### Two Versions of the Code

1. **`generate.py`**: Standalone script for direct execution
2. **`retrofit_generator/cli.py`**: Packaged version installed via pip

Both implement the same `RetrofitClientGenerator` class. The packaged version handles template directory resolution for installed packages using `importlib.resources`.

### Template System

Templates are located in `retrofit_generator/templates/` with the following structure:

```
templates/
├── client/
│   ├── dto/              # Data Transfer Objects
│   ├── mapper/           # MapStruct mappers
│   └── rest/            # Client interfaces and implementations
│       ├── api/         # Retrofit API interface (HTTP annotations)
│       └── impl/        # Client implementation
├── domain/
│   └── external_request/ # Domain objects
└── config_snippets/     # Code snippets for configuration file updates
```

### Placeholder Replacement

All templates use placeholders that get replaced during generation:

- `__ApiName__`: PascalCase API name (e.g., `MapBox`)
- `__apiName__`: camelCase API name (e.g., `mapBox`)
- `__basePackage__`: Auto-detected base package (e.g., `com.example.app`)
- `__endpointPath__`: Endpoint path (e.g., `api/v1/geocode`)
- `__baseUrl__`: Base URL (e.g., `https://api.mapbox.com/`)
- `__serviceIdentifier__`: YAML config identifier (e.g., `mapbox-api`)

Placeholders appear in both file **names** and **content**.

### File Generation vs. File Modification

**Generated (new files):**
- All Java classes from templates (DTOs, mappers, clients, etc.)
- Skips if file already exists with a warning

**Modified (existing files):**
- `RestClientConfig.java`: Adds import and @Bean method
- `EndpointsConfig.java`: Adds @Bean method
- `application-local.yml`: Adds service configuration block

Modifications use regex patterns to find insertion points (e.g., after last import, after last bean).

### Package Detection

The tool auto-detects the base package by:
1. Walking `src/main/java/`
2. Finding the first directory named `client`
3. Using its parent path as the base package

Example: If it finds `src/main/java/com/example/myapp/client/`, the base package is `com.example.myapp`.

## Important Patterns

### Template Processing Flow

1. Read template file
2. Apply placeholder replacements to content
3. Apply placeholder replacements to filename
4. Write to target location in Java project

### Configuration File Updates

- **RestClientConfig**: Inserts import after last import, bean after last @Bean method
- **EndpointsConfig**: Inserts bean after last @Bean method
- **YAML**: Uses `ruamel.yaml` to preserve formatting while adding entries

### Error Handling

- Checks for template directory existence
- Validates Java project structure (`src/main/java`, `client` directory)
- Warns if configuration files don't exist
- Warns if generated files or config entries already exist

## Key Dependencies

- **click**: Interactive CLI prompts and commands
- **ruamel.yaml**: YAML manipulation while preserving formatting/comments
- **importlib-resources**: Template directory resolution for Python < 3.9

## Modifying Templates

Templates can be edited directly in `retrofit_generator/templates/`. If installed with `pip install -e .`, changes take effect immediately. Otherwise, reinstall the package.

All templates are plain text files with placeholders. The generator doesn't parse Java syntax—it does simple string replacement.

## Common Gotchas

- The tool must be run from the **root of the Java project**, not from this repository
- Base package detection requires a `client` directory to exist
- Generated Java files include `/* TODO: Add fields */` comments that must be filled manually
- Configuration file modifications assume specific code patterns (imports section, @Bean methods, closing braces)
