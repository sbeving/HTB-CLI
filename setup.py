from setuptools import setup, find_packages

setup(
    name="htb-cli",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests>=2.31.0",
        "click>=8.1.7",
        "colorama>=0.4.6",
        "tabulate>=0.9.0",
        "pyyaml>=6.0.1",
        "python-dotenv>=1.0.0",
        "rich>=13.7.0",
    ],
    entry_points={
        "console_scripts": [
            "htb-cli=htb_cli.main:cli",
        ],
    },
    author="Saleh Eddine Touil",
    author_email="saleh.touil@icloud.com",
    description="HackTheBox CLI utility for automation",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sbeving/HTB-CLI",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
