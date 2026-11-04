#!/usr/bin/env python3
"""Source-only .NET application inventory; does not evaluate MSBuild or run builds."""
import argparse
import datetime as dt
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

SCHEMA_VERSION = 1
SKIP_DIRS = frozenset({'.git', '.vs', '.idea', '.vscode', 'bin', 'obj', 'node_modules', 'packages', 'TestResults', '__pycache__'})
PROJECT_SUFFIXES = frozenset({'.csproj', '.vbproj', '.fsproj', '.vcxproj', '.shproj', '.sqlproj', '.wixproj'})
CONFIG_NAMES = frozenset({'global.json', '.editorconfig', 'nuget.config', 'directory.build.props',
    'directory.build.targets', 'directory.build.rsp', 'directory.solution.props',
    'directory.solution.targets', 'directory.packages.props', 'packages.lock.json',
    'app.config', 'web.config', '.gitattributes'})
MAX_XML_BYTES = 8 * 1024 * 1024
SECRET_NAME = re.compile(r"password|secret|credential|connection.?string|access.?token|api.?key|private.?key", re.I)


def local(tag):
    return tag.rsplit('}', 1)[-1]


def git(root, *args):
    try:
        proc = subprocess.run(['git', '-C', str(root), *args], text=True,
                              stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                              timeout=10, check=False)
        return proc.stdout.strip() if proc.returncode == 0 else None
    except (OSError, subprocess.TimeoutExpired):
        return None


def walk(root):
    for parent, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not (Path(parent) / d).is_symlink())
        for name in sorted(files):
            full = Path(parent) / name
            if full.is_symlink() or not full.is_file():
                continue
            yield full, full.relative_to(root).as_posix()


def parse_xml(path):
    if path.stat().st_size > MAX_XML_BYTES:
        raise ValueError('XML too large for source inventory')
    return ET.parse(path).getroot()


def redact(name, value):
    return "<redacted>" if SECRET_NAME.search(name) else value


def attributes(element):
    return {local(k): redact(local(k), v) for k, v in sorted(element.attrib.items())}


def scoped_conditions(element, parents):
    conditions = []
    current = element
    while current in parents:
        if current.get('Condition'):
            conditions.append({'element': local(current.tag), 'expression': current.get('Condition')})
        current = parents[current]
    if current.get('Condition'):
        conditions.append({'element': local(current.tag), 'expression': current.get('Condition')})
    return list(reversed(conditions))


def inventory_project(path, rel):
    root = parse_xml(path)
    parents = {child: node for node in root.iter() for child in node}
    result = {'path': rel, 'type': path.suffix.lower().lstrip('.'),
              'sdk_declarations': [], 'properties': [], 'imports': [],
              'project_references': [], 'package_references': [],
              'assembly_references': [], 'com_references': [], 'other_dependency_items': []}
    if 'Sdk' in root.attrib:
        result['sdk_declarations'].append({'source': 'Project@Sdk', 'value': root.attrib['Sdk']})
    for element in root.iter():
        kind = local(element.tag)
        if kind == 'Sdk':
            result['sdk_declarations'].append({'source': 'Sdk element', **attributes(element)})
        elif kind == 'Import':
            result['imports'].append(attributes(element))
        elif kind == 'PropertyGroup':
            group_cond = element.get('Condition')
            for child in element:
                if len(child):
                    # Nested XML properties are retained as XML, not interpreted as simple values.
                    value = '<nested XML value omitted; inspect source>'
                else:
                    value = (child.text or '').strip()
                result['properties'].append({'name': local(child.tag), 'declared_value': redact(local(child.tag), value),
                    'group_condition': group_cond, 'condition': child.get('Condition'),
                    'conditions_in_scope': scoped_conditions(child, parents)})
        elif kind == 'ItemGroup':
            group_cond = element.get('Condition')
            for child in element:
                entry = {'item': local(child.tag), **attributes(child), 'group_condition': group_cond,
                         'conditions_in_scope': scoped_conditions(child, parents)}
                meta = {local(c.tag): {'value': redact(local(c.tag), (c.text or '').strip()),
                                      'condition': c.get('Condition')}
                        for c in child if len(c) == 0}
                if meta:
                    entry['metadata'] = meta
                cat = entry['item']
                if cat == 'ProjectReference':
                    result['project_references'].append(entry)
                elif cat in {'PackageReference', 'PackageVersion', 'GlobalPackageReference'}:
                    result['package_references'].append(entry)
                elif cat in {'Reference', 'FrameworkReference'}:
                    result['assembly_references'].append(entry)
                elif cat in {'COMReference', 'COMFileReference'}:
                    result['com_references'].append(entry)
                elif cat in {'NativeReference', 'Library', 'Link', 'Content', 'None'} and (
                        cat != 'None' or str(entry.get('Include', '')).lower().endswith(('.dll', '.lib'))):
                    result['other_dependency_items'].append(entry)
    return result


def inventory_packages_config(path, rel):
    root = parse_xml(path)
    return {'path': rel, 'directory': str(Path(rel).parent).replace('\\', '/'),
            'entries': [attributes(child) for child in root.iter() if local(child.tag) == 'package']}


def inventory_nuspec(path, rel):
    root = parse_xml(path)
    parents = {child: node for node in root.iter() for child in node}
    deps = []
    for el in root.iter():
        if local(el.tag) == 'dependency':
            group = parents.get(el)
            tfm = group.get('targetFramework') if group is not None and local(group.tag) == 'group' else None
            deps.append({**attributes(el), 'target_framework_group': tfm})
    return {'path': rel, 'dependencies': deps}


def generate(source):
    source = Path(source).resolve(strict=True)
    if not source.is_dir():
        raise ValueError('source must be a directory')
    tree = list(walk(source))
    result = {'schema_version': SCHEMA_VERSION, 'kind': 'declared-source-inventory',
        'generated_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
        'source': {'root': str(source), 'commit': git(source, 'rev-parse', 'HEAD'),
                   'branch': git(source, 'branch', '--show-current'),
                   'dirty_paths': (git(source, 'status', '--porcelain', '--untracked-files=normal') or '').splitlines()},
        'environment': {'os': platform.platform(), 'python': platform.python_version()},
        'solutions': [], 'projects': [], 'packages_config': [], 'nuspec': [],
        'central_package_versions': [],
        'configuration_files': [], 'errors': [],
        'limitations': ['Source declarations only, not evaluated MSBuild properties or executed behavior.',
                        'PackageReference and packages.config do not by themselves establish historical direct/transitive origin.',
                        'Configured NuGet feeds do not establish the source of actual downloaded packages.',
                        'Runtime service dependencies, dynamic assembly/native loading and COM activation are not assessed.',
                        'Imported files and MSBuild property expressions are not evaluated; nested XML values are omitted.',
                        'Generated/imported/machine-wide files are not completely inventoried.']}
    for full, rel in tree:
        lname = full.name.lower()
        try:
            if full.suffix.lower() in PROJECT_SUFFIXES:
                result['projects'].append(inventory_project(full, rel))
            elif full.suffix.lower() in ('.sln', '.slnx') or lname.endswith('.slnf'):
                result['solutions'].append({'path': rel, 'format': full.suffix.lower().lstrip('.')})
            elif lname == 'packages.config':
                result['packages_config'].append(inventory_packages_config(full, rel))
            elif full.suffix.lower() == '.nuspec':
                result['nuspec'].append(inventory_nuspec(full, rel))
            elif lname in CONFIG_NAMES or lname.endswith(('.props', '.targets')):
                result['configuration_files'].append({'path': rel})
                if lname == 'directory.packages.props':
                    xml_root = parse_xml(full)
                    for item in xml_root.iter():
                        if local(item.tag) in {'PackageVersion', 'GlobalPackageReference'}:
                            result['central_package_versions'].append(
                                {'path': rel, 'item': local(item.tag), **attributes(item),
                                 'conditions_in_scope': scoped_conditions(item,
                                    {child: node for node in xml_root.iter() for child in node})})
        except (OSError, ET.ParseError, ValueError) as ex:
            result['errors'].append({'path': rel, 'problem': type(ex).__name__, 'detail': str(ex)[:240]})
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True, help='Application checkout root (read-only)')
    parser.add_argument('--output', type=Path, required=True, help='JSON inventory path')
    parser.add_argument('--expect-commit', help='Required immutable baseline SHA; mismatch exits nonzero')
    args = parser.parse_args(argv)
    try:
        source_root = args.source.resolve(strict=True)
        target = args.output.resolve()
        if target == source_root or target.is_relative_to(source_root):
            raise ValueError('output must be outside the application checkout')
        report = generate(source_root)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n', encoding='utf-8')
        if args.expect_commit and report['source']['commit'] != args.expect_commit:
            print('ERROR: checkout commit does not match the expected baseline SHA', file=sys.stderr)
            return 2
        if report['errors']:
            print('ERROR: inventory is partial; inspect errors in the JSON', file=sys.stderr)
            return 2
        print(f"Inventory: {len(report['projects'])} projects; {len(report['packages_config'])} packages.config files; {target}")
        return 0
    except (OSError, ValueError) as ex:
        print(f'ERROR: {ex}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
