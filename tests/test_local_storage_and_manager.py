from pathlib import Path

from carm_data_models.company import Company, CompanyProfile
from carm_company_profile.storage.local_storage import LocalFileStorage
from carm_company_profile.manager import ProfileManager
from carm_company_profile.loader import load_company_profile, save_company_profile, list_company_profiles, profile_exists


def _sample_profile() -> CompanyProfile:
    return CompanyProfile(
        company=Company(name="Carm Visuals", website="https://carmvisuals.com"),
        tagline="Bringing your vision to life",
    )


def test_local_file_storage_crud(tmp_path: Path):
    storage = LocalFileStorage(profiles_dir=str(tmp_path))
    pid = "carm-visuals"
    profile = _sample_profile()

    assert storage.exists(pid) is False
    storage.save(pid, profile)
    assert storage.exists(pid) is True

    loaded = storage.load(pid)
    assert loaded.company.name == "Carm Visuals"

    items = storage.list()
    assert pid in items

    storage.delete(pid)
    assert storage.exists(pid) is False


def test_manager_create_update_list(tmp_path: Path, monkeypatch):
    # Force manager to use LocalFileStorage at tmp_path
    monkeypatch.setenv("PROFILES_DIR", str(tmp_path))
    monkeypatch.delenv("ENVIRONMENT", raising=False)

    mgr = ProfileManager()  # auto-detect to local
    pid = "my-company"
    created = mgr.create(pid, {"company": {"name": "My Co"}})
    assert created.company.name == "My Co"

    updated = mgr.update(pid, {"tagline": "Great"})
    assert updated.tagline == "Great"

    assert mgr.exists(pid) is True
    assert pid in mgr.list()

    mgr.delete(pid)
    assert mgr.exists(pid) is False


def test_loader_convenience_functions(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("PROFILES_DIR", str(tmp_path))
    pid = "carm-visuals"
    save_company_profile(pid, _sample_profile())
    assert profile_exists(pid) is True
    prof = load_company_profile(pid)
    assert prof.company.name == "Carm Visuals"
    ids = list_company_profiles()
    assert pid in ids

