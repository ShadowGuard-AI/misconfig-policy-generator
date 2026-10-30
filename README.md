![Banner](banner.png)

# misconfig-Policy-Generator

### Overview

The misconfig-Policy-Generator tool automates the generation of security policies based on user-defined criteria, ensuring consistency and compliance. It focuses on detecting misconfigurations in configuration files or infrastructure definitions.

### Installation

1. Install the required dependencies:
   - `yamllint` (Python package, imported by main.py to validate YAML input)
   - `PyYAML`
2. Clone this repository:
   - `git clone https://github.com/ShadowStrikeHQ/misconfig-Policy-Generator.git`
3. Navigate to the cloned directory:
   - `cd misconfig-Policy-Generator`

### Usage

```
python main.py -i INPUT -o OUTPUT -f {json,yaml}
```

- `-h`, `--help`: Display help message and exit
- `-i`, `--input`: Path to the configuration file (JSON or YAML). Required.
- `-o`, `--output`: Path to save the generated security policy. Required.
- `-f`, `--format`: Format of the output security policy (`json` or `yaml`). Required.

#### Input File

The input file is a JSON or YAML file whose top level is a mapping of configuration keys to values. YAML input is validated with yamllint before it is parsed; JSON input is parsed directly. The generated policy contains one rule per top-level key, named `Check <key>`, with the description `Ensure <key> is configured correctly.` and that key's value, plus generated-by metadata.

For example, with an input file containing:

```json
{"ssh_enabled": true, "port": 22}
```

running:

```
python main.py -i config.json -o policy.json -f json
```

writes a JSON policy whose rules list contains one entry for `ssh_enabled` and one for `port`.

### Security Warnings

This tool performs security scans, so it is crucial to take appropriate security measures to prevent unauthorized access or misuse.

### License

This tool is licensed under the GNU General Public License v3.0 ("GPLv3") to CY83R-3X71NC710N.
