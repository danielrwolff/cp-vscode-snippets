from __future__ import print_function

import argparse
import sys
import xml.etree.ElementTree as ET
import json
import yaml
from os import listdir
from os.path import isfile, join, isdir

def warn(msg, *args) :
  print(msg % args, file=sys.stderr)

def fail(msg, *args) :
  warn(msg, *args)
  exit()

def get_files_in_dir(directory) : 
  filenames = [f for f in listdir(directory) if isfile(join(directory, f))]
  filedata = {}

  for filename in filenames :
    with open(join(directory, filename), "r") as f:
      filedata[filename] = f.read()

  return filedata

def parse_config(filename):
  with open(filename, 'r') as stream:
    config = yaml.safe_load(stream)

  schemas = {}
  for schema in config:
    if 'Name' not in schema: fail("Schema '%s' does not specify a template name.", schema)
    template_name = schema.get('Name')
    template_disp = schema.get('Display', template_name)
    template_desc = schema.get('Description', template_name)
    template_pref = schema.get('Prefix', 'cpp')
    template_deps = set(schema.get('Dependencies', []))
    schemas[template_name] = {
      "name": template_name,
      "display-name": template_disp,
      "description": template_desc,
      "prefix": template_pref,
      "dependencies": template_deps,
      "raw_schema": schema
    }

  for template_name, schema in schemas.items():
    valid_dependencies = []
    for dependency_name in schema['dependencies']:
      if dependency_name in schemas.keys(): valid_dependencies.append(dependency_name)
      else: warn("Schema '%s' depends on a template that could not be found: '%s'.", template_name, dependency_name)
    schema['dependencies'] = valid_dependencies
  return schemas


def parse_schema(name, data) :
  schema = ET.fromstring(data)

  template_data = schema.find("template")
  if template_data is None : fail("Schema '%s' does not contain a 'template' element", name)
  elif template_data.attrib.get("name") is None : fail("Schema '%s' did not specify a template name", name)

  template_name = template_data.attrib.get("name").strip()
  template_disp = (template_data.attrib.get("display-name") or template_name).strip()
  template_desc = (template_data.text or template_name).strip()
  template_pref = (template_data.attrib.get("prefix") or "cpp").strip()
  template_deps = []

  dependencies = schema.find("dependencies")
  if dependencies is not None :
    for dependency in dependencies.iter("dependency") :
      dependency_name = dependency.attrib.get("template-name")
      if dependency_name is None : fail("Schema '%s' has a depency with no 'template-name' attribute.", name)
      if dependency_name in templates : template_deps.append(dependency_name)
      else : warn("Schema '%s' depends on a template that could not be found: '%s'", name, dependency_name)

  return {
    "name": template_name,
    "display-name": template_disp,
    "description": template_desc,
    "prefix": template_pref,
    "dependencies": template_deps,
    "raw_schema": schema
  }


def topological_sort(schemas, schema, seen, result) :
  schema_name = schema["name"]
  seen.add(schema_name)

  for dependency in schema["dependencies"] :
    if dependency in seen : continue
    topological_sort(schemas, schemas[dependency], seen, result)
  
  result.append(schema_name)
  

def resolve_dependencies(schemas, schema) :
  seen = set()
  result = []
  topological_sort(schemas, schema, seen, result)
  return result


if __name__ == "__main__" :
  parser = argparse.ArgumentParser()
  parser.add_argument('--templates_dir', '-td', type=str, default='templates', help='path to the templates directory')
  parser.add_argument('--schemas_dir', '-sd', type=str, default='schemas', help='path to the schemas directory')
  parser.add_argument('--config_file', '-cf', type=str, help='path to the configuration file (this overrides schemas_dir)')
  parser.add_argument('--output_dir', '-od', type=str, default='/mnt/c/Users/Daniel/AppData/Roaming/Code/User/snippets', help='path to the output directory')
  parser.add_argument('--output_filename', '-of', type=str, default='cp.code-snippets', help='name of the output snippets file')
  args = parser.parse_args()

  templates = get_files_in_dir(args.templates_dir)
  schemas = {}
  out_json = {}

  if args.config_file:
    schemas = parse_config(args.config_file)
  else:
    raw_schemas = get_files_in_dir(args.schemas_dir)
    for schema_name, data in raw_schemas.items() :
      schema = parse_schema(schema_name, data)
      schemas[schema["name"]] = schema

  for template_name, template_data in templates.items() :
    schema = schemas[template_name]
    ordered_dependencies = resolve_dependencies(schemas, schema)

    out_body = "\n\n".join([templates[template] for template in ordered_dependencies])

    out_json[schema["display-name"]] = {
      "scope": schema["prefix"],
      "prefix": "%s_%s" % (schema["prefix"], template_name),
      "body": out_body,
      "description": schema["description"]
    }

  with open(join(args.output_dir, args.output_filename), 'w') as output :
    output.write(json.dumps(out_json))
