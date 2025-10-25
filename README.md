# carm-company-profile

Company profile management with automatic local/cloud storage switching.

## Purpose

Store and manage company profiles with **smart storage** that automatically uses:
- **Local JSON files** in development (no setup needed)
- **Azure Blob Storage** in production (just add secrets)

## Features

- 🔄 **Auto-switching storage** - Local dev, Azure prod
- 💾 **Multiple storage backends** - File, Azure Blob, Database
- ✅ **Type-safe** - Uses carm-data-models for validation
- 🚀 **Zero-config dev** - Just clone and run
- ☁️ **Easy production** - Add Azure secrets, done
- 🔒 **Secure** - Secrets only in production .env

## Installation

```bash
# Base package
pip install git+https://github.com/JustinCarm001/carm-company-profile.git

# With Azure support
pip install git+https://github.com/JustinCarm001/carm-company-profile.git[azure]
```

## Quick Start

### Development (Local Files - No Setup Needed!)

```python
from carm_company_profile import load_company_profile, save_company_profile

# Just works! Uses local ./profiles/ directory
profile = load_company_profile("my-company")

# Update and save
profile.company.name = "Updated Name"
save_company_profile("my-company", profile)
```

### Production (Azure Blob - Add Secrets Only!)

```bash
# Add to .env
ENVIRONMENT=production
AZURE_STORAGE_CONNECTION_STRING=your-connection-string
AZURE_STORAGE_CONTAINER_NAME=company-profiles
```

```python
# SAME CODE - automatically uses Azure!
profile = load_company_profile("my-company")
```

## Storage Backends

### Auto-Detection (Recommended)

Package automatically chooses storage:

1. **Check environment** - Is ENVIRONMENT=production?
2. **Check Azure secrets** - Do Azure env vars exist?
3. **Use Azure if both true**, otherwise use local files

### Manual Selection

```python
from carm_company_profile import ProfileManager
from carm_company_profile.storage import LocalFileStorage, AzureBlobStorage

# Force local storage
manager = ProfileManager(storage=LocalFileStorage("./profiles"))

# Force Azure storage
manager = ProfileManager(storage=AzureBlobStorage(
    connection_string="...",
    container_name="profiles"
))
```

## API Reference

### Load Profile

```python
from carm_company_profile import load_company_profile

# Load by profile ID
profile = load_company_profile("carm-visuals")
# Returns: CompanyProfile object

# Access fields
print(profile.company.name)        # "Carm Visuals"
print(profile.mission)             # "Your mission..."
print(profile.services_detailed)   # [...]
```

### Save Profile

```python
from carm_company_profile import save_company_profile
from carm_data_models import Company, CompanyProfile

# Create new profile
company = Company(name="My Company", website="https://mycompany.com")
profile = CompanyProfile(
    company=company,
    mission="Our mission",
    services_detailed=[...]
)

# Save it
save_company_profile("my-company", profile)
```

### List Profiles

```python
from carm_company_profile import list_company_profiles

# Get all profile IDs
profiles = list_company_profiles()
# Returns: ["carm-visuals", "company-2", "company-3"]
```

### Profile Manager (Advanced)

```python
from carm_company_profile import ProfileManager

manager = ProfileManager()

# Load
profile = manager.load("my-company")

# Save
manager.save("my-company", profile)

# Delete
manager.delete("my-company")

# List
all_profiles = manager.list()

# Check if exists
exists = manager.exists("my-company")
```

## Environment Variables

### Development (Optional)

```bash
# Uses local files by default
PROFILES_DIR=./profiles  # Optional: custom location
```

### Production (Required for Azure)

```bash
# Auto-switches to Azure when these exist
ENVIRONMENT=production
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;...
AZURE_STORAGE_CONTAINER_NAME=company-profiles

# Optional
AZURE_STORAGE_TIMEOUT_SECONDS=30
```

## Migration Helper

Sync local profiles to Azure:

```python
from carm_company_profile import sync_local_to_azure

# One-time migration from local to Azure
sync_local_to_azure(
    local_dir="./profiles",
    connection_string="...",
    container_name="company-profiles"
)
```

## Django Integration

```python
# In your Django views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from carm_company_profile import load_company_profile, save_company_profile

@api_view(['GET'])
def get_company_profile(request):
    """Get user's company profile"""
    profile_id = request.user.company_id
    profile = load_company_profile(profile_id)
    return Response(profile.model_dump())

@api_view(['POST'])
def update_company_profile(request):
    """Update user's company profile"""
    profile_id = request.user.company_id
    save_company_profile(profile_id, request.data)
    return Response({"status": "saved"})
```

## Profile Structure

Profiles are stored as JSON with this structure:

```json
{
  "company": {
    "name": "Carm Visuals",
    "website": "https://carmvisuals.com",
    "industry": "Design & Marketing",
    "description": "Professional design services"
  },
  "tagline": "Bringing your vision to life",
  "mission": "To help businesses succeed through design",
  "values": ["Quality", "Innovation", "Client-First"],
  "services_detailed": [
    {
      "name": "Web Design",
      "description": "Custom websites",
      "features": ["Responsive", "SEO-optimized"],
      "pricing_range": "$2,000 - $10,000"
    }
  ],
  "unique_selling_points": [
    "10+ years experience",
    "100% satisfaction guarantee"
  ],
  "team_members": [
    {
      "name": "Justin",
      "role": "Founder",
      "bio": "Passionate designer"
    }
  ]
}
```

## Development

```bash
# Install in editable mode
cd packages/carm-company-profile
pip install -e ".[dev,azure]"

# Run tests
pytest

# Format code
black src/
isort src/
```

## Project Structure

```
carm-company-profile/
├── src/carm_company_profile/
│   ├── __init__.py
│   ├── manager.py           # ProfileManager class
│   ├── loader.py            # Simple load/save functions
│   ├── migration.py         # Sync local ↔ Azure
│   ├── storage/
│   │   ├── __init__.py
│   │   ├── base.py          # Base storage interface
│   │   ├── local_storage.py # Local file storage
│   │   └── azure_storage.py # Azure Blob storage
├── profiles/                # Local profiles (dev)
│   ├── carm-visuals.json
│   └── example.json
├── tests/
├── pyproject.toml
└── README.md
```
