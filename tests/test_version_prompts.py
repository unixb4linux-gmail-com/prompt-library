import pytest
import os
import sys
from datetime import datetime

# Add the scripts directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))

from version_prompts import process_prompt_file

@pytest.fixture
def temp_prompt_file(tmp_path):
    def _create_file(content, filename="test_prompt.prompt.md"):
        file_path = tmp_path / filename
        file_path.write_text(content)
        return file_path
    return _create_file

def test_process_prompt_file_no_frontmatter(temp_prompt_file):
    content = "# My Prompt\nSome content."
    file_path = temp_prompt_file(content)
    
    success, message = process_prompt_file(str(file_path))
    assert success is True
    assert "Added new frontmatter with version 1.0.0" in message
    
    updated_content = file_path.read_text()
    assert "version: \"1.0.0\"" in updated_content
    assert "created_date:" in updated_content
    assert "last_updated:" in updated_content

def test_process_prompt_file_existing_frontmatter_no_version(temp_prompt_file):
    content = """
---
description: A test prompt
---

# My Prompt
Some content.
"""
    file_path = temp_prompt_file(content)
    
    success, message = process_prompt_file(str(file_path))
    assert success is True
    assert "Updated with version 1.0.0" in message
    
    updated_content = file_path.read_text()
    assert "version: \"1.0.0\"" in updated_content
    assert "description: A test prompt" in updated_content
    assert "created_date:" in updated_content
    assert "last_updated:" in updated_content

def test_process_prompt_file_existing_frontmatter_with_version(temp_prompt_file):
    content = """
---
version: \"1.1.0\"
created_date: \"2024-01-01\"
last_updated: \"2024-01-01\"
description: A test prompt
---

# My Prompt
Some content.
"""
    file_path = temp_prompt_file(content)
    
    success, message = process_prompt_file(str(file_path))
    assert success is True
    assert "Updated with version 1.1.0" in message
    
    updated_content = file_path.read_text()
    assert "version: \"1.1.0\"" in updated_content
    assert "description: A test prompt" in updated_content
    assert "created_date: \"2024-01-01\"" in updated_content
    assert f"last_updated: \"{datetime.now().strftime('%Y-%m-%d')}\"" in updated_content

def test_process_prompt_file_invalid_yaml(temp_prompt_file):
    content = """
---
version: \"1.1.0\"
  - invalid: yaml
---

# My Prompt
Some content.
"""
    file_path = temp_prompt_file(content)
    
    success, message = process_prompt_file(str(file_path))
    assert success is False
    assert "Failed to parse YAML frontmatter" in message
