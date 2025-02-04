from setuptools import setup, find_packages

setup(
    name='deep_lib',
    version='0.1.0',
    description='An open-source, modifiable Python library for deep learning',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    install_requires=[
        'numpy'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
