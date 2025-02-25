# Sonar SDK

A Python SDK for interacting with Perplexity AI's Sonar models.

## Features

- Simple interface for sending prompts to Perplexity AI's Sonar models
- Support for all Sonar model variants (Sonar, Sonar Pro, Sonar Reasoning, etc.)
- Rich text formatting of responses using the `rich` library
- Automatic saving of responses to files (optional)
- Easy configuration via environment variables

## Installation


Set up your Perplexity API key:
   - Create a `.env` file in the project root
   - Add your API key: `PLEX_API_KEY=your_api_key_here`

## Usage

### Basic Usage

1. Edit the `prompt.txt` file with your query.
2. Run the main script:
   ```
   uv run sonar.py
   ```


You can customize the request by modifying the `SonarRequest` object:

```python
from sonar_request import SonarRequest, SonarModels
from sonar import send_request
from display_response import display_response
from pathlib import Path

# Create a custom request
request = SonarRequest(
    prompt_path=Path("custom_prompt.txt"),
    model=SonarModels.SONAR_REASONING_PRO,
    system_prompt="You are a helpful AI assistant specialized in scientific research.",
    save_response=True
)

# Send the request and display the response
response = send_request(request)
display_response(response, save_to_file=request.save_response)
```

