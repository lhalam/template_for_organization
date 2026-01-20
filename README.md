# Template for Organization

This repository contains Python scripts for creating an organization on GitHub and various templates for repositories.

## Features

- **Automated Organization Setup**: Python script to help set up GitHub organizations
- **Repository Templates**: Pre-configured templates for different project types:
  - **Basic**: Minimal repository structure with README and LICENSE
  - **Python**: Python project with best practices (src/, tests/, requirements.txt)
  - **Web**: Web application template with HTML, CSS, and JavaScript

## Prerequisites

- Python 3.8 or higher
- GitHub account with appropriate permissions
- GitHub Personal Access Token with `admin:org` and `repo` scopes

## Installation

1. Clone this repository:
```bash
git clone https://github.com/lhalam/template_for_organization.git
cd template_for_organization
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Create your configuration file:
```bash
cp config.example.yml config.yml
```

4. Edit `config.yml` and add your GitHub token and organization details.

## Configuration

Edit the `config.yml` file with your organization and repository settings:

```yaml
github:
  token: "your_github_personal_access_token"

organization:
  name: "your-org-name"
  display_name: "Your Organization"
  description: "Organization description"
  email: "admin@example.com"

repositories:
  - name: "repo-name"
    description: "Repository description"
    private: false
    template: "basic"  # Options: basic, python, web
```

### Getting a GitHub Token

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Click "Generate new token (classic)"
3. Select the following scopes:
   - `admin:org` (for organization management)
   - `repo` (for repository creation)
4. Generate and copy the token to your `config.yml`

## Usage

### Create Organization and Repositories

Run the script with your configuration:

```bash
python create_org.py
```

Or specify a custom config file:

```bash
python create_org.py --config my-config.yml
```

### Dry Run

To see what would be done without making actual changes:

```bash
python create_org.py --dry-run
```

### Custom Templates Directory

To use a custom templates directory:

```bash
python create_org.py --templates-dir /path/to/templates
```

## Templates

### Basic Template

A minimal repository template with:
- README.md
- LICENSE (MIT)

Perfect for simple projects or documentation repositories.

### Python Template

A Python project template with:
- `src/` - Source code directory
- `tests/` - Test directory
- `requirements.txt` - Python dependencies
- `.gitignore` - Python-specific gitignore
- `README.md` - Documentation
- `LICENSE` - MIT License

Follows Python best practices and PEP 8 guidelines.

### Web Template

A web application template with:
- `src/` - Source files (HTML, CSS, JavaScript)
- `public/` - Static assets
- `package.json` - Node.js package configuration
- `.gitignore` - Web project gitignore
- `README.md` - Documentation
- `LICENSE` - MIT License

Ready for modern web development.

## Project Structure

```
template_for_organization/
├── create_org.py           # Main script for organization creation
├── config.example.yml      # Example configuration file
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore rules
├── README.md              # This file
└── templates/             # Repository templates
    ├── basic/             # Basic template
    │   ├── README.md
    │   └── LICENSE
    ├── python/            # Python project template
    │   ├── src/
    │   │   └── main.py
    │   ├── tests/
    │   │   └── test_main.py
    │   ├── requirements.txt
    │   ├── .gitignore
    │   ├── README.md
    │   └── LICENSE
    └── web/               # Web application template
        ├── src/
        │   ├── index.html
        │   ├── styles.css
        │   └── app.js
        ├── public/
        ├── package.json
        ├── .gitignore
        ├── README.md
        └── LICENSE
```

## Important Notes

### Organization Creation

**Note**: Creating organizations via the GitHub API requires GitHub Enterprise. For regular GitHub accounts, you must create the organization manually:

1. Go to https://github.com/organizations/new
2. Create your organization
3. Then run this script to set up repositories

The script will detect if the organization exists and proceed with repository creation.

### Repository Templates

The template application feature in the script is currently a placeholder. Templates are provided as directory structures that can be used as reference when creating repositories.

For full template application, you would need to implement file upload logic using the GitHub API.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is provided as-is for educational and organizational purposes.

## Support

For issues or questions, please open an issue on GitHub.
