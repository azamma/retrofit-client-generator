#!/usr/bin/env python3
"""
Intelligent Java Retrofit API Client Generator

Generates a complete Retrofit API client using external template files.
Run from the root of your Java project.
"""

import os
import re
import sys
import shutil
from pathlib import Path
from typing import Dict

try:
    import click
    from ruamel.yaml import YAML
except ImportError:
    print("Error: Required dependencies not installed.")
    print("Please run: pip install click ruamel.yaml")
    sys.exit(1)


class RetrofitClientGenerator:
    """Generates Retrofit API client from template files."""

    def __init__(
        self,
        api_name: str,
        endpoint_path: str,
        base_url: str,
        service_identifier: str,
        project_root: Path,
        template_dir: Path,
        credentials: list = None
    ):
        self.api_name_pascal = api_name
        self.api_name_camel = self._to_camel_case(api_name)
        self.endpoint_path = endpoint_path
        self.base_url = base_url
        self.service_identifier = service_identifier
        self.project_root = project_root
        self.template_dir = template_dir
        self.credentials = credentials

        self.base_package = self._infer_base_package()
        self.base_package_path = self.base_package.replace('.', '/')
        self.src_path = project_root / 'src' / 'main' / 'java' / self.base_package_path

        # Replacement map for all placeholders
        self.replacements = {
            '__ApiName__': self.api_name_pascal,
            '__apiName__': self.api_name_camel,
            '__basePackage__': self.base_package,
            '__endpointPath__': self.endpoint_path,
            '__baseUrl__': self.base_url,
            '__serviceIdentifier__': self.service_identifier,
        }

    @staticmethod
    def _to_camel_case(pascal_case: str) -> str:
        """Convert PascalCase to camelCase."""
        if not pascal_case:
            return pascal_case
        return pascal_case[0].lower() + pascal_case[1:]

    @staticmethod
    def _to_kebab_case(pascal_case: str) -> str:
        """Convert PascalCase to kebab-case."""
        import re
        # Insert hyphen before uppercase letters (except the first one)
        kebab = re.sub(r'(?<!^)(?=[A-Z])', '-', pascal_case)
        return kebab.lower()

    def _infer_base_package(self) -> str:
        """Infer base package by finding the package containing a 'client' directory."""
        src_java = self.project_root / 'src' / 'main' / 'java'

        if not src_java.exists():
            raise FileNotFoundError(f"Could not find src/main/java in {self.project_root}")

        for root, dirs, _ in os.walk(src_java):
            if 'client' in dirs:
                relative_path = Path(root).relative_to(src_java)
                package = str(relative_path).replace(os.sep, '.')
                click.echo(f"✓ Detected base package: {package}")
                return package

        raise FileNotFoundError("Could not find a package containing 'client' directory")

    def _apply_replacements(self, content: str) -> str:
        """Apply all placeholder replacements to content."""
        for placeholder, value in self.replacements.items():
            content = content.replace(placeholder, value)
        return content

    def _process_template_file(self, template_path: Path, output_path: Path):
        """Process a single template file and write to output."""
        if output_path.exists():
            click.echo(f"⚠️  {output_path.relative_to(self.project_root)} already exists, skipping...")
            return

        # Read template
        content = template_path.read_text()

        # Apply replacements
        content = self._apply_replacements(content)

        # Create output directory
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Write output
        output_path.write_text(content)
        click.echo(f"✓ Created: {output_path.relative_to(self.project_root)}")

    def _process_template_directory(self, template_subdir: Path, output_base: Path):
        """Recursively process all template files in a directory."""
        for template_file in template_subdir.rglob('*.java'):
            # Get relative path from template subdir
            rel_path = template_file.relative_to(template_subdir)

            # Apply replacements to filename
            output_filename = self._apply_replacements(str(rel_path))

            # Determine output path
            output_path = output_base / output_filename

            # Process the file
            self._process_template_file(template_file, output_path)

    def generate_all(self):
        """Generate all files and configurations."""
        click.echo(f"\n🚀 Generating Retrofit client for: {self.api_name_pascal}")
        click.echo(f"   Base package: {self.base_package}")
        click.echo(f"   Endpoint: {self.endpoint_path}\n")

        # Process all template directories
        self._generate_java_files()
        self._modify_config_files()

        click.echo(f"\n✅ Successfully generated {self.api_name_pascal} Retrofit client!")

    def _generate_java_files(self):
        """Generate all Java files from templates."""
        click.echo("📝 Generating Java files...")

        # Process client templates
        client_templates = self.template_dir / 'client'
        if client_templates.exists():
            self._process_template_directory(client_templates, self.src_path / 'client')

        # Process domain templates
        domain_templates = self.template_dir / 'domain'
        if domain_templates.exists():
            self._process_template_directory(domain_templates, self.src_path / 'domain')

    def _modify_config_files(self):
        """Modify configuration files with snippets."""
        click.echo("\n⚙️  Updating configuration files...")

        self._add_to_rest_client_config()
        self._add_to_endpoints_config()
        self._add_to_application_yaml()

    def _add_to_rest_client_config(self):
        """Add import and bean to RestClientConfig.java."""
        config_path = self.src_path / 'config' / 'RestClientConfig.java'

        if not config_path.exists():
            click.echo(f"⚠️  RestClientConfig.java not found at default location, searching...")
            config_path = self._find_file_recursive('RestClientConfig.java', self.project_root)
            if not config_path:
                click.echo(f"⚠️  RestClientConfig.java not found in project")
                return

        content = config_path.read_text()

        # Add import
        import_snippet = (self.template_dir / 'config_snippets' / 'RestClientConfig.import.java').read_text()
        import_statement = self._apply_replacements(import_snippet).strip()

        if import_statement not in content:
            # Find last import and add after it
            import_pattern = re.compile(r'^import .+;$', re.MULTILINE)
            imports = list(import_pattern.finditer(content))
            if imports:
                last_import = imports[-1]
                insert_pos = last_import.end()
                content = content[:insert_pos] + f"\n{import_statement}" + content[insert_pos:]
                click.echo(f"✓ Added import to RestClientConfig.java")

        # Add bean
        bean_snippet = (self.template_dir / 'config_snippets' / 'RestClientConfig.bean.java').read_text()
        bean_code = self._apply_replacements(bean_snippet)

        if f"{self.api_name_camel}Api()" not in content:
            # Find last method and add bean before final closing brace
            class_match = re.search(r'(  \}\n)(\}\s*$)', content)
            if class_match:
                insert_pos = class_match.start(1) + len(class_match.group(1))
                content = content[:insert_pos] + bean_code + "\n" + content[insert_pos:]
                click.echo(f"✓ Added bean to RestClientConfig.java")

        config_path.write_text(content)

    def _add_to_endpoints_config(self):
        """Add bean to EndpointsConfig.java."""
        config_path = self.src_path / 'config' / 'endpoints' / 'EndpointsConfig.java'

        if not config_path.exists():
            click.echo(f"⚠️  EndpointsConfig.java not found at default location, searching...")
            config_path = self._find_file_recursive('EndpointsConfig.java', self.project_root)
            if not config_path:
                click.echo(f"⚠️  EndpointsConfig.java not found in project")
                return

        content = config_path.read_text()

        # Add bean
        bean_snippet = (self.template_dir / 'config_snippets' / 'EndpointsConfig.bean.java').read_text()
        bean_code = self._apply_replacements(bean_snippet)

        if f"{self.api_name_camel}Endpoint()" not in content:
            class_match = re.search(r'(  \}\n)(\}\s*$)', content)
            if class_match:
                insert_pos = class_match.start(1) + len(class_match.group(1))
                content = content[:insert_pos] + bean_code + "\n" + content[insert_pos:]
                click.echo(f"✓ Added bean to EndpointsConfig.java")

        config_path.write_text(content)

    def _find_file_recursive(self, filename: str, search_path: Path) -> Path:
        """Recursively search for a file in the project."""
        for root, dirs, files in os.walk(search_path):
            if filename in files:
                found_path = Path(root) / filename
                click.echo(f"✓ Found {filename} at {found_path.relative_to(self.project_root)}")
                return found_path
        return None

    def _add_to_application_yaml(self):
        """Add configuration block to application-local.yml."""
        yaml_path = self.project_root / 'src' / 'main' / 'resources' / 'application-local.yml'

        if not yaml_path.exists():
            click.echo(f"⚠️  application-local.yml not found at default location, searching...")
            yaml_path = self._find_file_recursive('application-local.yml', self.project_root)
            if not yaml_path:
                click.echo(f"⚠️  application-local.yml not found in project")
                return

        yaml = YAML()
        yaml.preserve_quotes = True
        yaml.default_flow_style = False

        with open(yaml_path, 'r') as f:
            data = yaml.load(f)

        if data is None:
            data = {}

        # Ensure http-client key exists
        if 'http-client' not in data:
            data['http-client'] = {}

        # Ensure global properties exist
        if 'timeout' not in data['http-client']:
            data['http-client']['timeout'] = 30
            click.echo(f"✓ Added default http-client.timeout property")

        if 'logging-level' not in data['http-client']:
            data['http-client']['logging-level'] = 'BODY'
            click.echo(f"✓ Added default http-client.logging-level property")

        if 'connect-timeout' not in data['http-client']:
            data['http-client']['connect-timeout'] = 10
            click.echo(f"✓ Added default http-client.connect-timeout property")

        # Check if service already configured
        if self.service_identifier in data['http-client']:
            click.echo(f"⚠️  Configuration for {self.service_identifier} already exists in YAML")
            return

        # Add service configuration
        data['http-client'][self.service_identifier] = {
            'base-url': self.base_url,
            'logging-level': '${http-client.logging-level}',
            'read-timeout': '${http-client.timeout}',
            'connect-timeout': '${http-client.connect-timeout}'
        }

        # Add credentials section if needed
        if self.credentials:
            if 'credentials' not in data:
                data['credentials'] = {}

            # Check if credentials for this service already exist
            if self.service_identifier in data['credentials']:
                click.echo(f"⚠️  Credentials for {self.service_identifier} already exist in YAML")
            else:
                credentials_dict = {}
                for field in self.credentials:
                    credentials_dict[field] = 'TODO_ADD_VALUE'

                data['credentials'][self.service_identifier] = credentials_dict
                click.echo(f"✓ Added credentials section for {self.service_identifier}")

        with open(yaml_path, 'w') as f:
            yaml.dump(data, f)

        click.echo(f"✓ Added configuration to application-local.yml")


def _generate_service_identifier(api_name: str) -> str:
    """Generate kebab-case service identifier from PascalCase API name."""
    import re
    kebab = re.sub(r'(?<!^)(?=[A-Z])', '-', api_name)
    return f"{kebab.lower()}-api"


@click.command()
def main():
    """
    Generate a complete Retrofit API client for Java/Spring Boot projects.

    This tool reads templates from the 'templates/' directory and generates
    DTOs, mappers, client interfaces, and configuration files.

    Run this script from the root of your Java project.
    """
    try:
        # Determine paths
        script_dir = Path(__file__).parent
        template_dir = script_dir / 'templates'
        project_root = Path.cwd()

        # Validate template directory exists
        if not template_dir.exists():
            click.echo(f"❌ Error: Template directory not found at {template_dir}", err=True)
            click.echo("Make sure you're running this script from the retrofit-generator directory.", err=True)
            sys.exit(1)

        # Prompt for API name
        api_name = click.prompt('API name (PascalCase, e.g. UserService, PaymentGateway)', type=str)

        # Prompt for endpoint path
        endpoint_path = click.prompt('Endpoint path (e.g. api/v1/users)', type=str)

        # Prompt for base URL
        base_url = click.prompt('Base URL (e.g. https://api.example.com/)', type=str)

        # Generate default service identifier
        default_identifier = _generate_service_identifier(api_name)
        click.echo(f"\n💡 Generated YAML property identifier: {default_identifier}")
        change_identifier = click.prompt('Do you want to change it? (y/n)',
                                        type=click.Choice(['y', 'n'], case_sensitive=False),
                                        default='n')

        if change_identifier.lower() == 'y':
            service_identifier = click.prompt('YAML property identifier', type=str)
        else:
            service_identifier = default_identifier
            click.echo(f"✓ Using: {service_identifier}\n")

        # Prompt for credentials
        has_credentials = click.prompt('Does this API require credentials? (y/n)',
                                      type=click.Choice(['y', 'n'], case_sensitive=False),
                                      default='n')

        credentials = None
        if has_credentials.lower() == 'y':
            credential_fields = click.prompt('Credential field names (comma-separated, e.g. apiKey,token)',
                                           type=str,
                                           default='')
            if credential_fields:
                credentials = [field.strip() for field in credential_fields.split(',') if field.strip()]
            else:
                click.echo("⚠️  No credential fields provided, skipping credentials section")

        # Generate client
        generator = RetrofitClientGenerator(
            api_name=api_name,
            endpoint_path=endpoint_path,
            base_url=base_url,
            service_identifier=service_identifier,
            project_root=project_root,
            template_dir=template_dir,
            credentials=credentials
        )
        generator.generate_all()

    except Exception as e:
        click.echo(f"\n❌ Error: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
