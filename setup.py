import setuptools

# The setup.py file was used from old versions of pip
# After PEP 518 (don't know which version)
# it was not used anymore.
# Basically, the pyproject.toml and setup.py must be kept in sync


with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cicconf",
    version="0.1.7",
    author="Carsten Wulff",
    author_email="carsten@wulff.no",
    description="Configuration and Revision tool ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wulffern/cicconf",
    packages=setuptools.find_packages(),
    python_requires='>=3.8',
    entry_points = {'console_scripts': [
        'cicconf = cicconf.entry:cli',
    ]},
    install_requires = 'matplotlib click GitPython'.split(),
    classifiers = [
        'Development Status :: 1 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        "License :: OSI Approved :: MIT License",
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Utilities',
        'Topic :: Scientific/Engineering',
    ],
)
