# FitDev.io - Virtual Software Development Organization Generator

## Project Overview
FitDev.io is a comprehensive Python application that generates a virtual software development organization consisting of specialized AI agents covering the entire software development lifecycle. The system includes agent roles across executive, development, quality, and specialized categories, with a built-in virtual compensation mechanism and reinforcement learning capabilities.

## Features
- Specialized AI agents with well-defined roles and responsibilities
- Task management system for coordinating work between agents
- Browser capabilities for information retrieval
- LLM integration for intelligent agent responses
- Virtual compensation system with performance metrics
- Reinforcement learning system with three approaches:
  - Parameter-based learning to adjust agent behavior parameters
  - Prompt engineering optimization for effective LLM interactions
  - Task strategy selection to learn efficient execution approaches

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
5. Create `.env` file with the following configuration options:

```
# LLM Configuration
ENABLE_LLM=true
DEFAULT_LLM_PROVIDER=ollama  # or openai
OPENAI_API_KEY=your_openai_api_key  # if using OpenAI
USE_OLLAMA=true  # if using Ollama
OLLAMA_API_BASE=http://localhost:11434
OLLAMA_MODEL=gemma3  # Supported models: gemma3, mistral-small

# Browser Configuration
ENABLE_BROWSER=true

# Reinforcement Learning Configuration
ENABLE_LEARNING=true
LEARNING_DATA_DIR=data/learning
```

### Running the Application
```bash
python fitdev/main.py
```

### Setting Up Ollama Models
Before running the application with Ollama, you need to pull the required models:

```bash
# Pull the required models
./create_llama3_model.sh
```

This script will pull the gemma3 and mistral-small models from Ollama, which are the only supported models in the current configuration.

## Development
- Use `black` for code formatting
- Run tests with `pytest`
- Check type hints with `mypy`

## Reinforcement Learning System

The reinforcement learning system in FitDev.io allows agents to learn from feedback provided through the compensation mechanism. As agents complete tasks and receive compensation, they adapt their behavior to maximize future rewards. The system includes three main learning approaches:

### 1. Parameter-Based Learning

Agents have adjustable parameters that control aspects of their behavior:
- Common parameters (for all agents): thoroughness, creativity, risk_taking
- Role-specific parameters:
  - Frontend: design_focus, accessibility_focus
  - Backend: performance_focus, security_focus, code_reusability
  - QA: test_coverage, edge_case_focus

These parameters are adjusted based on the compensation received after completing tasks, with higher compensation reinforcing successful parameter combinations.

### 2. Prompt Engineering Optimization

For agents using LLMs, this system learns which prompt templates yield the best results for different task types. The system maintains a collection of prompt templates and tracks which ones correlate with higher compensation, gradually favoring the most effective templates.

### 3. Task Strategy Selection

This system implements a Multi-Armed Bandit algorithm to select between different execution strategies for tasks. It balances exploration (trying different strategies) and exploitation (using strategies that have worked well in the past), gradually decreasing the exploration rate over time as it accumulates experience.

## Future Development Plans

- Apply reinforcement learning to more agent types beyond Frontend and Backend
- Enhance task execution with more realistic work outputs
- Implement more sophisticated collaboration mechanics between agents
- Create project templates for common software development scenarios
- Add visualization and reporting features for organization performance
- Implement external integrations with tools like Git and issue trackers
- Enhance the exploration/exploitation balance in RL algorithms

## License
This project is licensed under the MIT License - see the LICENSE file for details.
