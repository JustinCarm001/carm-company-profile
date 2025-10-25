"""
Profile Manager with Auto Storage Detection

PSEUDO CODE:
------------
1. Detect environment (dev vs prod)
2. Check for Azure secrets
3. Auto-select storage backend
4. Provide unified API for all operations
"""

import os
from typing import Optional, List
from carm_data_models import CompanyProfile
from .storage import BaseStorage, LocalFileStorage, AzureBlobStorage, AZURE_AVAILABLE


def _auto_detect_storage() -> BaseStorage:
    """
    Automatically detect and initialize the appropriate storage backend
    
    PSEUDO CODE:
    1. Check if ENVIRONMENT=production
    2. Check if Azure secrets exist
    3. If both true, use Azure Blob Storage
    4. Otherwise, use Local File Storage
    
    Returns:
        Initialized storage backend
    """
    environment = os.getenv("ENVIRONMENT", "development").lower()
    
    # Check for Azure credentials
    azure_connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    azure_container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME", "company-profiles")
    
    # Use Azure if in production AND secrets exist
    if environment == "production" and azure_connection_string and AZURE_AVAILABLE:
        print(f"🔵 Using Azure Blob Storage (container: {azure_container_name})")
        timeout = int(os.getenv("AZURE_STORAGE_TIMEOUT_SECONDS", "30"))
        return AzureBlobStorage(
            connection_string=azure_connection_string,
            container_name=azure_container_name,
            timeout_seconds=timeout
        )
    
    # Default to local file storage
    profiles_dir = os.getenv("PROFILES_DIR", "./profiles")
    print(f"📁 Using Local File Storage (directory: {profiles_dir})")
    return LocalFileStorage(profiles_dir=profiles_dir)


class ProfileManager:
    """
    Company Profile Manager
    
    PSEUDO CODE:
    1. Initialize with storage backend (or auto-detect)
    2. Provide methods for CRUD operations
    3. Handle errors gracefully
    4. Validate all data using CompanyProfile model
    
    This is the main class you'll use to manage company profiles.
    It automatically selects the right storage backend based on environment.
    """

    def __init__(self, storage: Optional[BaseStorage] = None):
        """
        Initialize Profile Manager
        
        Args:
            storage: Storage backend (if None, auto-detects)
            
        Example:
            # Auto-detect (recommended)
            manager = ProfileManager()
            
            # Manual selection
            from carm_company_profile.storage import LocalFileStorage
            manager = ProfileManager(storage=LocalFileStorage("./profiles"))
        """
        self.storage = storage or _auto_detect_storage()

    def load(self, profile_id: str) -> CompanyProfile:
        """
        Load a company profile
        
        Args:
            profile_id: Unique profile identifier
            
        Returns:
            CompanyProfile object
            
        Raises:
            FileNotFoundError: If profile doesn't exist
            
        Example:
            profile = manager.load("my-company")
            print(profile.company.name)
        """
        return self.storage.load(profile_id)

    def save(self, profile_id: str, profile: CompanyProfile) -> None:
        """
        Save a company profile
        
        Args:
            profile_id: Unique profile identifier
            profile: CompanyProfile object
            
        Example:
            manager.save("my-company", profile)
        """
        self.storage.save(profile_id, profile)

    def delete(self, profile_id: str) -> None:
        """
        Delete a company profile
        
        Args:
            profile_id: Unique profile identifier
            
        Raises:
            FileNotFoundError: If profile doesn't exist
        """
        self.storage.delete(profile_id)

    def exists(self, profile_id: str) -> bool:
        """
        Check if a profile exists
        
        Args:
            profile_id: Unique profile identifier
            
        Returns:
            True if profile exists
        """
        return self.storage.exists(profile_id)

    def list(self) -> List[str]:
        """
        List all profile IDs
        
        Returns:
            List of profile ID strings
            
        Example:
            profiles = manager.list()
            # Returns: ["company-1", "company-2", "my-company"]
        """
        return self.storage.list()

    def create(self, profile_id: str, profile_data: dict) -> CompanyProfile:
        """
        Create a new company profile
        
        Args:
            profile_id: Unique profile identifier
            profile_data: Profile data as dictionary
            
        Returns:
            Created CompanyProfile object
            
        Raises:
            ValueError: If profile already exists
            
        Example:
            profile = manager.create("new-company", {
                "company": {
                    "name": "New Company",
                    "website": "https://newcompany.com"
                },
                "mission": "Our mission..."
            })
        """
        if self.exists(profile_id):
            raise ValueError(f"Profile '{profile_id}' already exists")
        
        # Validate data
        profile = CompanyProfile.model_validate(profile_data)
        
        # Save it
        self.save(profile_id, profile)
        
        return profile

    def update(self, profile_id: str, updates: dict) -> CompanyProfile:
        """
        Update an existing profile
        
        Args:
            profile_id: Unique profile identifier
            updates: Fields to update
            
        Returns:
            Updated CompanyProfile object
            
        Raises:
            FileNotFoundError: If profile doesn't exist
            
        Example:
            profile = manager.update("my-company", {
                "mission": "Updated mission statement"
            })
        """
        # Load existing profile
        profile = self.load(profile_id)
        
        # Convert to dict, update, and re-validate
        profile_dict = profile.model_dump()
        profile_dict.update(updates)
        updated_profile = CompanyProfile.model_validate(profile_dict)
        
        # Save updated profile
        self.save(profile_id, updated_profile)
        
        return updated_profile
