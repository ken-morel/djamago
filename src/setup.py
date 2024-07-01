from pathlib import Path

from setuptools import setup, find_packages

from djamago import __version__

project_dir = Path(__file__).parent

try:
    long_description = (project_dir / "README.md").read_text()
except FileNotFoundError:
    try:
        long_description = Path("README.md").read_text()
    except FileNotFoundError:
        try:
            long_description = Path("/src/README.md").read_text()
        except FileNotFoundError:
            long_description = (project_dir.parent / "README.md").read_text()


extra_test = (
    "pytest",
    "pytest-cov",
    "pyoload",
)

extra_dev = (
    *extra_test,
)

extra_ci = (
    # *extra_flake8,
    *extra_test,
    "coveralls",
)

deps = ("pyoload",)

setup(
    name="djamago",
    version=__version__,
    packages=find_packages(exclude=["tests", "tests.*", "pyoload"]),
    project_urls={
        "Documentation": "https://djamago.readthedocs.io/",
        "Funding": "https://ko-fi.com/kenmorel",
        "Source": "https://github.com/ken-morel/djamago/",
        "Tracker": "https://github.com/ken-morel/djamago/issues",
    },
    url="https://github.com/ken-morel/djamago",
    license="MIT",
    author="ken-morel",
    author_email="engonken8@gmail.com",
    maintainer="ken-morel",
    maintainer_email="engonken8@gmail.com",
    description="Creating a simple chatbot, made easy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=deps,
    build_requires=deps,
    extras_require={
        "dev": extra_dev,
        "ci": extra_ci,
    },
    classifiers=[
        # See https://pypi.org/classifiers/
        "Intended Audience :: Developers",
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        "Development Status :: 3 - Alpha",
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        # "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Natural Language :: English",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
