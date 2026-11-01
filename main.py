import argparse
import logging
import json
import sys
from pathlib import Path
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
        # The gate on YAML input is a style linter running its
        # default rules, so a document that parses perfectly is
        # rejected for a long line or a spacing fault, with the lint
        # complaints presented as validation errors. JSON input gets
        # no equivalent gate at all: it is parsed and accepted, style
        # unexamined, so the two formats face different bars.
        errors = [p for p in lint_results if getattr(p, 'level', 'error') == 'error']
        warnings = [p for p in lint_results if getattr(p, 'level', 'error') != 'error']
        for warning in warnings:
            logger.warning(f"YAML lint warning (not rejecting the input): {warning}")
        if errors:
            raise ValueError(f"YAML validation errors: {errors}")
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
    # Only the top level becomes rules. A nested section is
    # copied as one opaque value under its parent key's rule, so
    # the generated policy says nothing about the settings inside
    # it, however sensitive they are, beyond carrying their
    # values along.
    for key, value in data.items():
        policy['rules'].append({
            "rule_name": f"Check {key}",
            "description": f"Ensure {key} is configured correctly.",
            # Every value is copied into the policy word for word,
            # including any secret the config held. A password setting
            # becomes a rule whose value field is the password, written
            # to the output file in clear, so the generated policy needs
            # the same handling as the config it came from.
            "value": value
        })
    if format_type == 'json':
        return json.dumps(policy, indent=4)
    elif format_type == 'yaml':
        # The YAML form sorts the policy's keys, where the JSON form
        # above keeps the order the policy was built in. The same
        # generated policy therefore reads differently by format in
        # a way that has nothing to do with the input document.
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
        if Path(args.output).resolve() == Path(args.input).resolve():
            raise ValueError(
                "Output path is the input file; refusing to overwrite the input configuration. "
                "Choose a different output path."
            )

        # The format is whatever follows the last dot in the whole
        # path, taken case sensitively. A file named CONFIG.YAML is
        # refused as unsupported, and an extensionless file inside a
        # directory whose name ends in .yaml would be read as YAML
        # on the strength of its parent directory's name.
        file_ext = args.input.split('.')[-1]
        if file_ext == 'yaml' or file_ext == 'yml':
            data = validate_yaml(args.input)
        elif file_ext == 'json':
            data = validate_json(args.input)
        else:
            raise ValueError("Unsupported input file format. Please provide a JSON or YAML file.")

        if not isinstance(data, dict):
            raise ValueError("Input document must be a mapping of configuration keys to values; no policy was generated.")
        if not data:
            raise ValueError("Input document contains no keys; no policy was generated.")

        policy = generate_policy(data, args.format)
        
        with open(args.output, 'w') as output_file:
            output_file.write(policy)
        logger.info(f"Security policy successfully generated and saved to {args.output}")
    
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()