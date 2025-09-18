import pytest
import os
import sys
from datetime import datetime

# Add the scripts directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))

from generate_index import extract_metadata

@pytest.fixture
def temp_markdown_file(tmp_path):
    content = """---
title: Test Title
description: Test Description
category: Test Category
---

# Another Title
Some content here.
"""
    file_path = tmp_path / "test_prompt.md"
    file_path.write_text(content)
    return file_path

def test_extract_metadata_with_frontmatter(temp_markdown_file):
    title, description, category = extract_metadata(str(temp_markdown_file))
    assert title == "Test Title"
    assert description == "Test Description"
    assert category == "Test Category"

def test_extract_metadata_without_frontmatter(tmp_path):
    content = """# Fallback Title
Some content here.
"""
    file_path = tmp_path / "test_prompt_no_fm.md"
    file_path.write_text(content)
    title, description, category = extract_metadata(str(file_path))
    assert title == "Fallback Title"
    assert description is None
    assert category is None

def test_extract_metadata_empty_title_in_frontmatter(tmp_path):
    content = """---
title: ""
description: Test Description
category: Test Category
---

# Fallback Title
Some content here.
"""
    file_path = tmp_path / "test_prompt_empty_fm_title.md"
    file_path.write_text(content)
    title, description, category = extract_metadata(str(file_path))
    assert title == "Fallback Title"
    assert description == "Test Description"
    assert category == "Test Category"

def test_extract_metadata_no_title_in_frontmatter_fallback_to_heading(tmp_path):
    content = """---
description: Test Description
category: Test Category
---

# Fallback Title
Some content here.
"""
    file_path = tmp_path / "test_prompt_no_fm_title.md"
    file_path.write_text(content)
    title, description, category = extract_metadata(str(file_path))
    assert title == "Fallback Title"
    assert description == "Test Description"
    assert category == "Test Category"

def test_extract_metadata_no_title_no_heading(tmp_path):
    content = """---
description: Test Description
category: Test Category
---

Some content here.
"""
    file_path = tmp_path / "test_prompt_no_title_no_heading.md"
    file_path.write_text(content)
    title, description, category = extract_metadata(str(file_path))
    assert title is None
    assert description == "Test Description"
    assert category == "Test Category"
