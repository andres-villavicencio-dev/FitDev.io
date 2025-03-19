# FitDev.io

## Virtual Software Development Organization Generator

FitDev.io is a comprehensive Python application that generates a virtual software development organization consisting of specialized AI agents covering the entire software development lifecycle. The system includes agent roles across executive, development, quality, and specialized categories, with a built-in virtual compensation mechanism.

### Project Status

This project is in active development. Current implementation includes:

- Complete organization structure with agent management and critic evaluation
- Executive agents (CEO, CTO, Product Owner)
- Development agents (Frontend, Backend, Full Stack, DevOps)
- Quality agents (QA Engineer, Security Specialist, Technical Writer)
- Specialized agents (Knowledge Management, Trend Scout, UX Simulator, API Specialist, Tech Debt Manager)
- Task management and assignment system
- Performance evaluation through critic agents
- Compensation calculation based on performance metrics
- LLM integration for intelligent agent responses
- Web browsing capabilities for research and information gathering
- Agent memory for persistence across tasks

### Getting Started

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/macOS: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements-fitdev.txt`
5. Copy `.env.example` to `.env` and configure your environment variables:
   - Set `ENABLE_LLM=true` to enable LLM capabilities
   - Set `ENABLE_BROWSER=true` to enable web browsing
   - Configure your preferred LLM provider (OpenAI or Ollama)
6. Run the application: `python run_fitdev.py --cycles 5`

#### LLM Integration

The system supports integration with different LLM providers:

1. **OpenAI**: Set `OPENAI_API_KEY` in your `.env` file
2. **Ollama**: Install Ollama locally and have it running on the default port

#### Testing LLM Integration

To test the LLM and browser capabilities:

```
python test_llm_integration.py
```
   
### Testing

Run the test script to verify functionality:
```
python test_fitdev.py
```

This will run a simple test with a few sample tasks to ensure the organization components are working correctly.

### Agent Roles

The system implements multiple agent roles covering the entire software development lifecycle:

#### Executive Roles
- CEO/Project Manager: Sets overall direction and manages resources
- CTO/Technical Architect: Makes technology decisions and oversees architecture
- Product Owner: Defines requirements and maximizes value

#### Development Roles
- Frontend Developer: Implements user interfaces and client-side functionality
- Backend Developer: Develops server-side logic, databases, and APIs
- Full Stack Developer: Works on both frontend and backend systems
- DevOps Engineer: Manages infrastructure and deployment processes

#### Quality & Support Roles
- QA Engineer: Designs test plans and validates software quality
- Security Specialist: Performs security audits and implements best practices
- Technical Writer: Creates documentation for internal and external use

#### Specialized Roles
- Knowledge Management Specialist: Organizes organizational knowledge
- Trend Scout & Innovation Researcher: Monitors emerging technologies
- User Experience Simulator: Simulates user interactions to identify usability issues
- API Specialist: Manages integrations and ensures data flow between components
- Technical Debt Manager: Identifies and prioritizes technical debt

### Compensation System

The virtual compensation system tracks agent performance and allocates rewards based on:
- Role-based base rates
- Performance metrics specific to each role
- Value contribution to organizational goals

### License

This project is licensed under the MIT License - see the LICENSE file for details.