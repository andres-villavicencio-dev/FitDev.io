# FitDev.io - Virtual Software Development Organization Generator

## Project Overview
FitDev.io is a comprehensive Python application that generates a virtual software development organization consisting of specialized AI agents covering the entire software development lifecycle. The system includes agent roles across executive, development, quality, and specialized categories, with a built-in virtual compensation mechanism.

## Features
- Specialized AI agents with well-defined roles and responsibilities
- Task management system for coordinating work between agents
- Browser capabilities for information retrieval
- Virtual compensation system with performance metrics

## Project Structure
```
fitdev/
├── agents/              # Agent implementations
│   ├── executive/       # Executive role agents
│   ├── development/     # Development role agents
│   ├── quality/         # Quality role agents
│   └── specialized/     # Specialized role agents
├── config/              # Configuration files
├── docs/                # Documentation
├── models/              # Data models and schemas
├── tests/               # Test suite
└── utils/               # Utility functions
```

## Getting Started

### Prerequisites
- Python 3.10 or higher
- Git

### Installation
1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/macOS: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements-fitdev.txt`
5. Copy `.env.example` to `.env` and configure your environment variables

### Running the Application
```bash
python fitdev/main.py
```

## Development
- Use `black` for code formatting
- Run tests with `pytest`
- Check type hints with `mypy`

## License
This project is licensed under the MIT License - see the LICENSE file for details.
