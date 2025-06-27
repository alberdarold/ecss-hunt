"""
Core Pydantic Schemas for the ECSS project.
This file centralizes base model definitions to prevent circular imports.
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

Core Pydantic Schemas for the ECSS project.
This file centralizes base model definitions to prevent circular imports.
"""
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / "config" / ".env")

import sys
# Add backend root to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from pydantic import BaseModel, Field
from morphik.rules import MetadataExtractionRule, NaturalLanguageRule
from typing import List

# This utility function is needed by other modules, so we define it here.
# In a real-world SDK, this would likely be part of the core library.
def dict_to_model(model_dict: dict, model_name: str = "DynamicModel"):
    """Dynamically creates a Pydantic model from a dictionary of Pydantic models."""
    return type(model_name, (BaseModel,), {'__annotations__': {k: v for k, v in model_dict.items()}}) 

import sys
# Add backend root to path

from pydantic import BaseModel, Field
from morphik.rules import MetadataExtractionRule, NaturalLanguageRule
from typing import List

# This utility function is needed by other modules, so we define it here.
# In a real-world SDK, this would likely be part of the core library.
def dict_to_model(model_dict: dict, model_name: str = "DynamicModel"):
    """Dynamically creates a Pydantic model from a dictionary of Pydantic models."""
    return type(model_name, (BaseModel,), {'__annotations__': {k: v for k, v in model_dict.items()}}) 