import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="h_price_database",
    version="0.0.1",
    author="Cyril Welschen",
    author_email="cj.welschen@gmail.com",
    description="Construct, feed and handle database with prices.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cyrilwelschen/h_price_database",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)