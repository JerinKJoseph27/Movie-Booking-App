# Contributing to CinemaMax

First off, thank you for considering contributing to CinemaMax! It's people like you that make this project better.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the behavior
- **Expected behavior**
- **Actual behavior**
- **Screenshots** if applicable
- **Environment details** (OS, Python version, MySQL version)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear title and description**
- **Use case** - why is this enhancement needed?
- **Proposed solution**
- **Alternatives considered**

### Pull Requests

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Test thoroughly
5. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
6. Push to the branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

## Development Guidelines

### Python Code Style

- Follow [PEP 8](https://pep8.org/) style guide
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and small
- Use type hints where appropriate

### Code Example

```python
def validate_phone(phone: str) -> tuple[bool, str]:
    """
    Validate Indian phone numbers.
    
    Args:
        phone: Phone number string to validate
        
    Returns:
        Tuple of (is_valid, message_or_cleaned_number)
    """
    if not phone:
        return False, "Phone number is required"
    # ... rest of implementation
```

### HTML/CSS Guidelines

- Use semantic HTML5 elements
- Keep CSS organized and commented
- Ensure responsive design
- Test on multiple browsers
- Maintain consistent styling

### Database Changes

- Update `db_config.sql` if schema changes
- Document migration steps
- Ensure backward compatibility where possible
- Test with sample data

### Testing

- Test all functionality before submitting PR
- Include test cases for new features
- Verify error handling works correctly
- Check edge cases

## Project Structure

```
movie-booking/
├── app.py                 # Main Flask application
├── templates/             # HTML templates
├── static/               # Static assets
├── db_config.sql         # Database schema
└── README.md            # Documentation
```

## Questions?

Feel free to open an issue with the `question` label if you have any questions about contributing!

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all.

### Our Standards

- Be respectful and inclusive
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards others

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Public or private harassment
- Publishing others' private information

Thank you for contributing! 🎉
