# --- Imports
from setuptools import setup, find_packages;

# --- Setup
setup(
    name="gmcli",
    version="0.0.0",
    description="CLI to interact with the Gaijin Market.",
    url="https://github.com/JowiAoun/Gaijin-Market-CLI",
    author="Jowi Aoun",
    packages=find_packages(),
    install_requires=['click'],
    entry_points='''
    [console_scripts]
    gmcli=main:main
    ''',
)