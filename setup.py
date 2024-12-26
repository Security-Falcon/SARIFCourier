from setuptools import setup, find_packages

setup(
    name="sarif-2-md",
    version="1.0.0",
    description="A tool to convert SARIF security reports to Markdown format.",
    version='0.1.0',
    license='MIT License',
    author='Abdullah Shahen',
    author_email='contact.abdullah.shahen@proton.me',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    url="https://github.com/your-repo/sarif-to-md-converter",  # Replace with your repository URL
    packages=find_packages(),
    install_requires=[
        "jsonschema",
        "markdown",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "sarif2md=main:main",
        ],
    },
)
