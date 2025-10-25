"""
Base Storage Interface

PSEUDO CODE:
------------
1. Define abstract base class for storage backends
2. All storage implementations must implement these methods
3. Ensures consistent API regardless of backend
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from carm_data_models import CompanyProfile


class BaseStorage(ABC):
    """
    Abstract base class for storage backends
    
    All storage implementations (local, Azure, database) must implement these methods.
    This ensures a consistent API regardless of where data is stored.
    """

    @abstractmethod
    def load(self, profile_id: str) -> CompanyProfile:
        """
        Load a company profile
        
        Args:
            profile_id: Unique profile identifier
            
        Returns:
            CompanyProfile object
            
        Raises:
            FileNotFoundError: If profile doesn't exist
        """
        pass

    @abstractmethod
    def save(self, profile_id: str, profile: CompanyProfile) -> None:
        """
        Save a company profile
        
        Args:
            profile_id: Unique profile identifier
            profile: CompanyProfile object to save
        """
        pass

    @abstractmethod
    def delete(self, profile_id: str) -> None:
        """
        Delete a company profile
        
        Args:
            profile_id: Unique profile identifier
            
        Raises:
            FileNotFoundError: If profile doesn't exist
        """
        pass

    @abstractmethod
    def exists(self, profile_id: str) -> bool:
        """
        Check if a profile exists
        
        Args:
            profile_id: Unique profile identifier
            
        Returns:
            True if profile exists, False otherwise
        """
        pass

    @abstractmethod
    def list(self) -> List[str]:
        """
        List all profile IDs
        
        Returns:
            List of profile ID strings
        """
        pass

    def load_dict(self, profile_id: str) -> Dict[str, Any]:
        """
        Load profile as dictionary (helper method)
        
        Args:
            profile_id: Unique profile identifier
            
        Returns:
            Profile data as dictionary
        """
        profile = self.load(profile_id)
        return profile.model_dump()

    def save_dict(self, profile_id: str, data: Dict[str, Any]) -> None:
        """
        Save profile from dictionary (helper method)
        
        Args:
            profile_id: Unique profile identifier
            data: Profile data as dictionary
        """
        profile = CompanyProfile.model_validate(data)
        self.save(profile_id, profile)
