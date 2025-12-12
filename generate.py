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
        template_dir: Path
    ):
        self.api_name_pascal = api_name
        self.api_name_camel = self._to_camel_case(api_name)
        self.endpoint_path = endpoint_path
        self.base_url = base_url
        self.service_identifier = service_identifier
        self.project_root = project_root
        self.template_dir = template_dir

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
            click.echo(f"⚠️  RestClientConfig.java not found at {config_path}")
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
            click.echo(f"⚠️  EndpointsConfig.java not found at {config_path}")
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

    def _add_to_application_yaml(self):
        """Add configuration block to application-local.yml."""
        yaml_path = self.project_root / 'src' / 'main' / 'resources' / 'application-local.yml'

        if not yaml_path.exists():
            click.echo(f"⚠️  application-local.yml not found at {yaml_path}")
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

        # Check if service already configured
        if self.service_identifier in data['http-client']:
            click.echo(f"⚠️  Configuration for {self.service_identifier} already exists in YAML")
            return

        # Add service configuration
        data['http-client'][self.service_identifier] = {
            'baseUrl': self.base_url,
            'loggingLevel': 'BODY',
            'readTimeout': 30,
            'connectTimeout': 30
        }

        with open(yaml_path, 'w') as f:
            yaml.dump(data, f)

        click.echo(f"✓ Added configuration to application-local.yml")


@click.command()
@click.option('--api-name', prompt='API name (PascalCase)',
              help='Name of the API in PascalCase (e.g., UserProfile, MapBox)')
@click.option('--endpoint-path', prompt='Endpoint path',
              help='Relative URL path (e.g., api/v1/geocode)')
@click.option('--base-url', prompt='Base URL',
              help='Base URL for the endpoint (e.g., https://api.mapbox.com/)')
@click.option('--service-identifier', prompt='Service identifier',
              help='Unique service identifier (e.g., mapbox-api)')
def main(api_name: str, endpoint_path: str, base_url: str, service_identifier: str):
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

        # Generate client
        generator = RetrofitClientGenerator(
            api_name=api_name,
            endpoint_path=endpoint_path,
            base_url=base_url,
            service_identifier=service_identifier,
            project_root=project_root,
            template_dir=template_dir
        )
        generator.generate_all()

    except Exception as e:
        click.echo(f"\n❌ Error: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
