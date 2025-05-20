from setuptools import setup, find_packages

setup(
    name="SARIFCourier",
    version="1.0.0",
    description="Delivering security insights to your developers.",
    license='Apache-2.0 license',
    author='Abdullah Schahin',
    author_email='contact.abdullah.shahen@proton.me',

    url="https://github.com/Abdullah-Schahin/SARIF2MD",  # Replace with your repository URL
    install_requires=[
        "jsonschema",
        "markdown",
        "colorama",
        "termcolor",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "sc=main:main",
        ],
    },

)
