"""
Simple loader functions for quick access

These are convenience functions that create a ProfileManager internally
"""

from typing import List
from carm_data_models import CompanyProfile
from .manager import ProfileManager

# Global manager instance (lazy-loaded)
_manager = None


def _get_manager() -> ProfileManager:
    """Get or create global ProfileManager instance"""
    global _manager
    if _manager is None:
        _manager = ProfileManager()
    return _manager


def load_company_profile(profile_id: str) -> CompanyProfile:
    """
    Load a company profile (convenience function)
    
    Args:
        profile_id: Profile identifier
        
    Returns:
        CompanyProfile object
        
    Example:
        profile = load_company_profile("my-company")
        print(profile.company.name)
    """
    manager = _get_manager()
    return manager.load(profile_id)


def save_company_profile(profile_id: str, profile: CompanyProfile) -> None:
    """
    Save a company profile (convenience function)
    
    Args:
        profile_id: Profile identifier
        profile: CompanyProfile object
        
    Example:
        save_company_profile("my-company", profile)
    """
    manager = _get_manager()
    manager.save(profile_id, profile)


def list_company_profiles() -> List[str]:
    """
    List all company profile IDs (convenience function)
    
    Returns:
        List of profile IDs
        
    Example:
        profiles = list_company_profiles()
        # Returns: ["company-1", "company-2"]
    """
    manager = _get_manager()
    return manager.list()


def profile_exists(profile_id: str) -> bool:
    """
    Check if a profile exists (convenience function)
    
    Args:
        profile_id: Profile identifier
        
    Returns:
        True if exists
    """
    manager = _get_manager()
    return manager.exists(profile_id)
