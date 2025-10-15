from setuptools import setup, find_packages

setup(
    name="github-org-audit",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "PyGithub==2.1.1",
        "click==8.1.7",
        "pyyaml==6.0.1",
        "tabulate==0.9.0",
    ],
    entry_points={
        "console_scripts": [
            "github-org-audit=github_org_audit.cli:main",
        ],
    },
    python_requires=">=3.8",
)
