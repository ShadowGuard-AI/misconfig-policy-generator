import argparse
import logging
import json
import yaml
from yamllint import linter as yamllinter
from yamllint.config import YamlLintConfig
from json.decoder import JSONDecodeError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_argparse():
    """
    Set up the command line argument parser.
    """
    parser = argparse.ArgumentParser(
        description="misconfig-Policy-Generator: Generates security policies based on user-defined criteria."
    )
    parser.add_argument(
        '-i', '--input',
        required=True,
        help="Path to the configuration file (JSON or YAML)."
    )
    parser.add_argument(
        '-o', '--output',
        required=True,
        help="Path to save the generated security policy."
    )
    parser.add_argument(
        '-f', '--format',
        choices=['json', 'yaml'],
        required=True,
        help="Format of the output security policy (json/yaml)."
    )
    return parser

def validate_yaml(filepath):
    """
    Validate a YAML file for misconfigurations.
    """
    try:
        logger.info(f"Validating YAML file: {filepath}")
        with open(filepath, 'r') as file:
            yaml_content = file.read()
        config = YamlLintConfig('extends: default')
        lint_results = list(yamllinter.run(yaml_content, config))
        if lint_results:
            raise ValueError(f"YAML validation errors: {lint_results}")
        return yaml.safe_load(yaml_content)
    except Exception as e:
        logger.error(f"YAML validation failed: {e}")
        raise

def validate_json(filepath):
    """
    Validate a JSON file for misconfigurations.
    """
    try:
        logger.info(f"Validating JSON file: {filepath}")
        with open(filepath, 'r') as file:
            return json.load(file)
    except JSONDecodeError as e:
        logger.error(f"JSON validation failed: {e}")
        raise
    except Exception as e:
        logger.error(f"Error reading JSON file: {e}")
        raise

def generate_policy(data, format_type):
    """
    Generate a security policy based on the input data.
    """
    logger.info("Generating security policy...")
    policy = {
        "policy_name": "Generated Security Policy",
        "rules": [],
        "metadata": {
            "generated_by": "misconfig-Policy-Generator",
            "version": "1.0"
        }
    }
    for key, value in data.items():
        policy['rules'].append({
            "rule_name": f"Check {key}",
            "description": f"Ensure {key} is configured correctly.",
            "value": value
        })
    if format_type == 'json':
        return json.dumps(policy, indent=4)
    elif format_type == 'yaml':
        return yaml.dump(policy, default_flow_style=False)
    else:
        raise ValueError("Unsupported format type")

def main():
    """
    Main function to handle input, validation, and policy generation.
    """
    parser = setup_argparse()
    args = parser.parse_args()

    try:
        file_ext = args.input.split('.')[-1]
        if file_ext == 'yaml' or file_ext == 'yml':
            data = validate_yaml(args.input)
        elif file_ext == 'json':
            data = validate_json(args.input)
        else:
            raise ValueError("Unsupported input file format. Please provide a JSON or YAML file.")
        
        policy = generate_policy(data, args.format)
        
        with open(args.output, 'w') as output_file:
            output_file.write(policy)
        logger.info(f"Security policy successfully generated and saved to {args.output}")
    
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()