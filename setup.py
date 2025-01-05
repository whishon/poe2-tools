from setuptools import setup, find_packages

setup(
    name="poe2-tools",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "keyboard>=0.13.5",
        "pyperclip>=1.8.2",
        "pyautogui>=0.9.53"
    ],
    entry_points={
        'console_scripts': [
            'poe2-tools=poe2_tools.main:main',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A Path of Exile utility tool for item analysis and quick commands",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/poe2-tools",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
