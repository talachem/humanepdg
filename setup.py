import setuptools

with open("README.md", "r") as fh:
    description = fh.read()

setuptools.setup(
    name="humanepdg",
    version="0.1",
    author="Johannes Bilk",
    author_email="johannes.bilk@physik.uni-giessen.de",
    description="A simple packages converting human readable particle names to pdg gibberish and back again",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://gitlab.ub.uni-giessen.de/gc2052/fromroot",
    packages=setuptools.find_packages(),
    package_data={'': ['data/*.json']},
    license='MIT',
    python_requires='>=3.9',
    install_requires=[
        "numpy>=1.21.0",
        "uproot>=4.0.11",
        "importlib_resources>=6.1.0"
    ],
    keywords=['python', 'pdg', 'root'],
    classifiers= [
        "Development Status :: 0.1",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
