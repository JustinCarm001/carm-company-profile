"""
Storage package initialization
"""

from .base import BaseStorage
from .local_storage import LocalFileStorage

# Azure storage is optional (only import if available)
try:
    from .azure_storage import AzureBlobStorage
    AZURE_AVAILABLE = True
except ImportError:
    AzureBlobStorage = None
    AZURE_AVAILABLE = False

__all__ = [
    "BaseStorage",
    "LocalFileStorage",
    "AzureBlobStorage",
    "AZURE_AVAILABLE",
]
