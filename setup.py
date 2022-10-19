from setuptools import find_packages, setup

__package_name__ = "twitter-api-data-stack"
__version__ = "0.0.1"
__repository_url__ = "https://github.com/NicholasBaraldi/twitter-api-data-stack"

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name=__package_name__,
    description="",
    keywords="api twitter data",
    version=__version__,
    url=__repository_url__,
    packages=find_packages(
        exclude=(
            "docs",
            "tests",
            "tests.*",
            "venv",
            "pipenv",
            "env",
            "examples",
            "htmlcov",
            ".pytest_cache",
        )
    ),
    license="MIT",
    author="",
    install_requires=requirements,
    python_requires=">=3.8, <4",
)
