# misconfig-Policy-Generator

### Overview

The misconfig-Policy-Generator tool automates the generation of security policies based on user-defined criteria, ensuring consistency and compliance. It focuses on detecting misconfigurations in configuration files or infrastructure definitions.

### Installation

1. Install the required dependencies:
   - `yamllint`
   - `jsonlint`
2. Clone this repository:
   - `git clone https://github.com/ShadowStrikeHQ/misconfig-Policy-Generator.git`
3. Navigate to the cloned directory:
   - `cd misconfig-Policy-Generator`

### Usage

```
python main.py [OPTIONS]
```

#### General Usage

- `-h`, `--help`: Display help message and exit
- `-c`, `--config`: Path to a configuration file in YAML format

#### Configuration File Options

The configuration file should be in YAML format and specify the following parameters:

- `policies`: A list of dictionaries, each representing a security policy. Each policy should have the following keys:
  - `name`: The name of the policy
  - `criteria`: A dictionary of criteria to check for misconfigurations. The keys are the names of the criteria, and the values are the expected values.

For example:

```yaml
policies:
  - name: Check for missing SSH keys
    criteria:
      - ssh_key_path: /etc/ssh/ssh_host_rsa_key
```

### Security Warnings

This tool performs security scans, so it is crucial to take appropriate security measures to prevent unauthorized access or misuse.

### License

This tool is licensed under the GNU General Public License v3.0 ("GPLv3") to CY83R-3X71NC710N.
