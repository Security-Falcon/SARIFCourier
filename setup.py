from setuptools import setup, find_packages

setup(
    name="SARIF2MD",
    version="1.0.0",
    description="A tool to convert SARIF security reports to well formatted Markdown.",
    license='Apache-2.0 license',
    author='Abdullah Shahen',
    author_email='contact.abdullah.shahen@proton.me',

    url="https://github.com/Abdullah-Shahen/SARIF2MD",  # Replace with your repository URL
    install_requires=[
        "jsonschema",
        "markdown",
        "colorama",
        "termcolor",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Apache-2.0 license",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "samd=app.app:main",
        ],
    },
)
