"""
Azure Blob Storage Backend

PSEUDO CODE:
------------
1. Store profiles as JSON blobs in Azure Storage
2. Use for production (cloud storage)
3. Auto-activate when Azure secrets present
4. Secure, scalable, and reliable
"""

import json
from typing import List, Optional
from .base import BaseStorage
from carm_data_models import CompanyProfile

# Azure imports are optional (only needed if using Azure)
try:
    from azure.storage.blob import BlobServiceClient, BlobClient
    from azure.core.exceptions import ResourceNotFoundError
    AZURE_AVAILABLE = True
except ImportError:
    AZURE_AVAILABLE = False


class AzureBlobStorage(BaseStorage):
    """
    Azure Blob Storage backend
    
    PSEUDO CODE:
    1. Store profiles as JSON blobs in Azure container
    2. Profile ID maps to blob name: {profile_id}.json
    3. Use Azure SDK for all operations
    4. Handle Azure-specific errors
    
    Perfect for:
    - Production deployments
    - Scalable storage
    - Multi-region access
    - Secure cloud storage
    
    Requires:
    - Azure Storage account
    - Connection string
    - Container name
    """

    def __init__(
        self,
        connection_string: str,
        container_name: str = "company-profiles",
        timeout_seconds: int = 30
    ):
        """
        Initialize Azure Blob Storage
        
        Args:
            connection_string: Azure Storage connection string
            container_name: Container to store profiles in
            timeout_seconds: Timeout for operations
            
        Raises:
            ImportError: If azure-storage-blob not installed
        """
        if not AZURE_AVAILABLE:
            raise ImportError(
                "Azure Storage SDK not installed. "
                "Install with: pip install carm-company-profile[azure]"
            )
        
        self.connection_string = connection_string
        self.container_name = container_name
        self.timeout_seconds = timeout_seconds
        
        # Initialize Azure client
        self.blob_service_client = BlobServiceClient.from_connection_string(
            connection_string,
            connection_timeout=timeout_seconds
        )
        
        # Ensure container exists
        self._ensure_container_exists()

    def _ensure_container_exists(self) -> None:
        """
        Create container if it doesn't exist
        
        PSEUDO CODE:
        1. Try to get container
        2. If doesn't exist, create it
        3. Set appropriate permissions
        """
        try:
            self.blob_service_client.get_container_client(self.container_name)
        except ResourceNotFoundError:
            self.blob_service_client.create_container(self.container_name)

    def _get_blob_name(self, profile_id: str) -> str:
        """
        Get blob name for a profile
        
        Args:
            profile_id: Profile identifier
            
        Returns:
            Blob name (e.g., "my-company.json")
        """
        return f"{profile_id}.json"

    def _get_blob_client(self, profile_id: str) -> 'BlobClient':
        """
        Get blob client for a profile
        
        Args:
            profile_id: Profile identifier
            
        Returns:
            BlobClient instance
        """
        blob_name = self._get_blob_name(profile_id)
        return self.blob_service_client.get_blob_client(
            container=self.container_name,
            blob=blob_name
        )

    def load(self, profile_id: str) -> CompanyProfile:
        """
        Load profile from Azure Blob
        
        PSEUDO CODE:
        1. Get blob client for profile
        2. Download blob content
        3. Parse JSON
        4. Validate into CompanyProfile
        5. Return object
        """
        blob_client = self._get_blob_client(profile_id)
        
        try:
            # Download blob content
            blob_data = blob_client.download_blob()
            content = blob_data.readall().decode('utf-8')
            
            # Parse JSON
            data = json.loads(content)
            
            # Validate and return
            return CompanyProfile.model_validate(data)
            
        except ResourceNotFoundError:
            raise FileNotFoundError(f"Profile '{profile_id}' not found in Azure Blob Storage")

    def save(self, profile_id: str, profile: CompanyProfile) -> None:
        """
        Save profile to Azure Blob
        
        PSEUDO CODE:
        1. Convert profile to JSON
        2. Get blob client
        3. Upload JSON to blob
        4. Overwrite if exists
        """
        blob_client = self._get_blob_client(profile_id)
        
        # Convert to JSON using Pydantic's serializer
        json_data = profile.model_dump_json(indent=2)
        
        # Upload to Azure (overwrite if exists)
        blob_client.upload_blob(
            json_data,
            overwrite=True,
            content_settings={'content_type': 'application/json'}
        )

    def delete(self, profile_id: str) -> None:
        """
        Delete profile from Azure Blob
        
        Args:
            profile_id: Profile identifier
        """
        blob_client = self._get_blob_client(profile_id)
        
        try:
            blob_client.delete_blob()
        except ResourceNotFoundError:
            raise FileNotFoundError(f"Profile '{profile_id}' not found")

    def exists(self, profile_id: str) -> bool:
        """
        Check if profile exists in Azure Blob
        
        Args:
            profile_id: Profile identifier
            
        Returns:
            True if blob exists
        """
        blob_client = self._get_blob_client(profile_id)
        return blob_client.exists()

    def list(self) -> List[str]:
        """
        List all profile IDs from Azure container
        
        PSEUDO CODE:
        1. Get container client
        2. List all blobs
        3. Filter .json files
        4. Extract profile IDs from blob names
        5. Return sorted list
        """
        container_client = self.blob_service_client.get_container_client(self.container_name)
        
        profile_ids = []
        for blob in container_client.list_blobs():
            if blob.name.endswith('.json'):
                # Remove .json extension to get profile ID
                profile_id = blob.name[:-5]
                profile_ids.append(profile_id)
        
        return sorted(profile_ids)
