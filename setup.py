# --- Imports
from setuptools import setup, find_packages

# --- Setup
setup(
    name="gmcli",
    version="0.0.1",
    description="CLI to interact with the Gaijin Market.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/JowiAoun/Gaijin-Market-CLI",
    author="Jowi Aoun",
    packages=find_packages(),
    install_requires=['click', 'python-dotenv'],
    entry_points='''
    [console_scripts]
    gmcli=gmcli.main:main
    ''',
)
