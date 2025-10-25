"""
carm-company-profile: Auto-switching local/cloud storage for company profiles
"""

from .manager import ProfileManager
from .loader import (
    load_company_profile,
    save_company_profile,
    list_company_profiles,
    profile_exists,
)
from .storage import (
    BaseStorage,
    LocalFileStorage,
    AzureBlobStorage,
    AZURE_AVAILABLE,
)

__version__ = "0.1.0"

__all__ = [
    # Manager
    "ProfileManager",
    # Simple functions
    "load_company_profile",
    "save_company_profile",
    "list_company_profiles",
    "profile_exists",
    # Storage backends
    "BaseStorage",
    "LocalFileStorage",
    "AzureBlobStorage",
    "AZURE_AVAILABLE",
]
