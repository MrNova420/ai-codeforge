# Contributing to AI CodeForge

Thank you for considering contributing to AI CodeForge! This document provides guidelines and instructions for contributing.

## 🌟 Ways to Contribute

- **Bug Reports**: Found a bug? Open an issue with detailed reproduction steps
- **Feature Requests**: Have an idea? Share it in the discussions or issues
- **Code Contributions**: Submit pull requests with improvements
- **Documentation**: Help improve or translate documentation
- **Testing**: Write tests, report issues, improve test coverage
- **Examples**: Share examples of what you've built

## 🚀 Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/ai-codeforge.git
cd ai-codeforge
```

### 2. Set Up Development Environment

```bash
# Run the setup script
./setup_proper.py

# Install development dependencies
pip install -r requirements.txt
pip install pytest pytest-asyncio pytest-mock black flake8

# Run tests to ensure everything works
pytest
```

### 3. Create a Branch

```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Or a bugfix branch
git checkout -b fix/issue-number-description
```

## 📝 Development Guidelines

### Code Style

- **Follow PEP 8**: Use `black` for formatting, `flake8` for linting
- **Type Hints**: Use type hints for function parameters and returns
- **Docstrings**: Include docstrings for classes and functions
- **Comments**: Add comments for complex logic

```python
def example_function(param: str, count: int = 5) -> List[str]:
    """
    Brief description of what the function does.
    
    Args:
        param: Description of param
        count: Description of count (default: 5)
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When something goes wrong
    """
    # Implementation here
    pass
```

### Project Structure

```
ai-codeforge/
├── agents/              # Specialized agent implementations
├── ai_dev_team/         # Core team module
├── codebase/            # Code analysis tools
├── docs/                # Documentation
├── examples/            # Example projects
├── memory/              # Memory and vector store
├── tools/               # Tool system
├── tests/               # Test suite
├── *.py                 # Core system files
└── *.md                 # Agent definitions & docs
```

### Commit Messages

Use clear, descriptive commit messages:

```
feat: Add new web scraping tool
fix: Resolve memory leak in agent manager
docs: Update installation guide
test: Add tests for collaboration engine
refactor: Simplify tool registry logic
```

Prefixes:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Test additions or changes
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `chore`: Maintenance tasks

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_tools.py

# Run with coverage
pytest --cov=. --cov-report=html
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files `test_*.py`
- Use descriptive test function names
- Include docstrings explaining what is tested

```python
def test_tool_registry_adds_tool():
    """Test that tools can be registered successfully."""
    registry = ToolRegistry()
    tool = MockTool("test_tool")
    
    registry.register_tool(tool)
    
    assert "test_tool" in registry.list_tools()
    assert registry.get_tool("test_tool") == tool
```

## 🔍 Code Review Process

1. **Self-Review**: Review your own code before submitting
2. **Tests**: Ensure all tests pass
3. **Documentation**: Update relevant documentation
4. **Pull Request**: Submit PR with clear description
5. **Address Feedback**: Respond to review comments

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring
- [ ] Performance improvement

## Testing
- [ ] All existing tests pass
- [ ] New tests added (if applicable)
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Documentation updated
- [ ] No new warnings or errors
- [ ] Commit messages are clear
```

## 🎯 Priority Areas

Areas where contributions are especially welcome:

### High Priority
- **Test Coverage**: Expand test suite
- **Performance**: Optimize slow operations
- **Documentation**: Improve clarity and examples
- **Bug Fixes**: Fix reported issues

### Medium Priority
- **New Agents**: Add specialized agents
- **New Tools**: Add useful tools
- **Integrations**: IDE plugins, CI/CD
- **UI**: Web dashboard, better CLI

### Future/Experimental
- **Cloud Deployment**: Deploy to cloud platforms
- **Plugin System**: Extensible architecture
- **Analytics**: Usage analytics and insights
- **Mobile**: Mobile app or interface

## 🐛 Reporting Issues

### Before Reporting

1. **Search existing issues**: Check if already reported
2. **Reproduce**: Confirm the issue is reproducible
3. **Environment**: Note your system details

### Issue Template

```markdown
## Description
Clear description of the issue

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., Ubuntu 22.04]
- Python: [e.g., 3.11]
- AI CodeForge Version: [e.g., 0.1.0]
- Model: [e.g., codellama:7b]

## Additional Context
Any other relevant information, logs, screenshots
```

## 💡 Feature Requests

We love new ideas! When suggesting features:

1. **Use Case**: Explain the problem it solves
2. **Implementation**: Suggest how it might work
3. **Alternatives**: Any alternative approaches
4. **Examples**: Real-world examples or mockups

## 📚 Documentation

### Improving Documentation

- Fix typos and grammar
- Add missing information
- Improve clarity and organization
- Add examples and tutorials
- Translate to other languages

### Documentation Standards

- Use Markdown format
- Include code examples
- Add screenshots where helpful
- Keep it concise and scannable
- Test all code examples

## 🤝 Community Guidelines

### Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Give constructive feedback
- Focus on the work, not the person
- Assume good intentions

### Getting Help

- **Issues**: For bugs and feature requests
- **Discussions**: For questions and ideas
- **Discord/Slack**: For real-time chat (coming soon)

## 🎓 Learning Resources

New to the project? Start here:

1. Read the [README](README.md)
2. Follow the [Tutorial](docs/TUTORIAL.md)
3. Review [Project Structure](PROJECT_STRUCTURE.md)
4. Read the [Implementation Roadmap](MASTER_IMPLEMENTATION_ROADMAP.md)
5. Check [existing issues](https://github.com/MrNova420/ai-codeforge/issues)

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors will be recognized in:
- README.md contributors section
- CHANGELOG.md for significant contributions
- Special thanks in release notes

## 📞 Contact

- **Issues**: GitHub Issues
- **Email**: [Maintainer email if available]
- **Twitter**: [If available]

---

**Thank you for contributing to AI CodeForge!** 🚀

Every contribution, no matter how small, helps make this project better for everyone.
