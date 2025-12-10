"""
AI CodeForge Version Information
"""

__version__ = "1.0.0"
__version_info__ = (1, 0, 0)
__title__ = "AI CodeForge"
__description__ = "AAA Production-Grade AI Development Team with 23 Specialized Agents"
__author__ = "MrNova420"
__license__ = "MIT"
__url__ = "https://github.com/MrNova420/ai-codeforge"

# Release Information
RELEASE_NAME = "Enterprise Edition"
RELEASE_DATE = "2025-12-10"

# Feature Completeness
FEATURES_COMPLETE = {
    "core_agents": 23,
    "work_modes": 4,
    "enterprise_systems": 5,
    "interfaces": 2,  # CLI + Web
    "total_features": 100,
    "production_ready": True
}

def get_version():
    """Return version string."""
    return __version__

def get_version_info():
    """Return detailed version information."""
    return {
        "version": __version__,
        "title": __title__,
        "description": __description__,
        "release": RELEASE_NAME,
        "release_date": RELEASE_DATE,
        "url": __url__,
        "features": FEATURES_COMPLETE
    }

def print_version():
    """Print version information."""
    info = get_version_info()
    print(f"{info['title']} v{info['version']}")
    print(f"{info['description']}")
    print(f"\nRelease: {info['release']} ({info['release_date']})")
    print(f"URL: {info['url']}")
    print(f"\nFeatures:")
    for key, value in info['features'].items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    print_version()
