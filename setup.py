from setuptools import setup, find_packages

setup(
    name='AI-Agents',
    version='0.1',
    packages=find_packages(),
    install_requires=[  # List the external dependencies you need
        'requests',
        'beautifulsoup4',  # Example dependencies
        'pytest',
    ],
    entry_points={  # Optionally, specify the entry point if needed
        'console_scripts': [
            'your_command=your_module:main_function',
        ],
    },
)
