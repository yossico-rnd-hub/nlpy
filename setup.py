import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nlpy",
    version="0.0.1",
    author="Yossi Cohen",
    author_email="yossi.cohen@live.com",
    description="nlp playground based on spacy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yossi-cohen/nlpy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
