"""
Local File Storage Backend

PSEUDO CODE:
------------
1. Store profiles as JSON files in local directory
2. Use for development (no setup needed)
3. Simple file read/write operations
4. Good for local dev and testing
"""

import json
from pathlib import Path
from typing import List
from .base import BaseStorage
from carm_data_models import CompanyProfile


class LocalFileStorage(BaseStorage):
    """
    Local file system storage backend
    
    PSEUDO CODE:
    1. Store profiles as JSON files in specified directory
    2. Profile ID maps to filename: {profile_id}.json
    3. Create directory if it doesn't exist
    4. Read/write JSON files
    
    Perfect for:
    - Local development
    - Testing
    - Small deployments
    - Backup storage
    """

    def __init__(self, profiles_dir: str = "./profiles"):
        """
        Initialize local file storage
        
        Args:
            profiles_dir: Directory to store profile JSON files
        """
        self.profiles_dir = Path(profiles_dir)
        self.profiles_dir.mkdir(parents=True, exist_ok=True)

    def _get_file_path(self, profile_id: str) -> Path:
        """
        Get file path for a profile
        
        Args:
            profile_id: Profile identifier
            
        Returns:
            Path to JSON file
        """
        return self.profiles_dir / f"{profile_id}.json"

    def load(self, profile_id: str) -> CompanyProfile:
        """
        Load profile from JSON file
        
        PSEUDO CODE:
        1. Build file path from profile_id
        2. Check if file exists
        3. Read JSON file
        4. Parse into CompanyProfile object
        5. Return validated object
        """
        file_path = self._get_file_path(profile_id)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Profile '{profile_id}' not found at {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Validate and return CompanyProfile object
        return CompanyProfile.model_validate(data)

    def save(self, profile_id: str, profile: CompanyProfile) -> None:
        """
        Save profile to JSON file
        
        PSEUDO CODE:
        1. Convert CompanyProfile to dictionary
        2. Build file path
        3. Write to JSON file (pretty-printed)
        4. Ensure directory exists
        """
        file_path = self._get_file_path(profile_id)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Use Pydantic's JSON serialization to handle types like HttpUrl, datetime, etc.
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(profile.model_dump_json(indent=2))

    def delete(self, profile_id: str) -> None:
        """
        Delete profile JSON file
        
        Args:
            profile_id: Profile identifier
        """
        file_path = self._get_file_path(profile_id)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Profile '{profile_id}' not found")
        
        file_path.unlink()

    def exists(self, profile_id: str) -> bool:
        """
        Check if profile file exists
        
        Args:
            profile_id: Profile identifier
            
        Returns:
            True if file exists
        """
        return self._get_file_path(profile_id).exists()

    def list(self) -> List[str]:
        """
        List all profile IDs
        
        PSEUDO CODE:
        1. Scan profiles directory
        2. Find all .json files
        3. Extract profile IDs from filenames
        4. Return sorted list
        """
        if not self.profiles_dir.exists():
            return []
        
        profile_ids = []
        for file_path in self.profiles_dir.glob("*.json"):
            # Remove .json extension to get profile ID
            profile_id = file_path.stem
            profile_ids.append(profile_id)
        
        return sorted(profile_ids)
