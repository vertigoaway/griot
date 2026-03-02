from setuptools import setup, find_packages
setup(
    name="griot",
    version="0.1.1",
    author="verti",
    author_email="verti@piss.industries",
    description='Text tokenization library',
    url='https://github.com/vertigoaway/griot',
    license="MIT",
    license_files=['LICENSE'],
    packages=find_packages(),
    install_requires=[
        "setuptools==59.6.0",
    ],
)
