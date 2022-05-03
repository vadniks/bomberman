import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bomberman",
    version="0.0.1",
    authors="Erupb,vadniks,rodyapal",
    description="A bombergame game on Python with documentation and other technologies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vadniks/bomberman",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)

