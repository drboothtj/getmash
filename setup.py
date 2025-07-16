from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    description = fh.read()

setup(
    name="getmash",
    version="0.0.3",
    author="Thomas J. Booth",
    author_email="thoboo@biosustain.dtu.dk",
    packages=find_packages(),
    description="a python package for assigning and evaluating mash clusters of genomic data",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/DrBoothTJ/getmash",
    license='GNU General Public License v3.0',
    python_requires='>=3.7',
    install_requires=[
    'pandas>=2.2.3',
    'scipy>=1.15.1',
    'scikit-learn>=1.6.1',
    'matplotlib>=3.10.0',
    'seaborn>=0.13.2',
    'pyvis==0.3.2'
    ],
    entry_points={'console_scripts': ["getmash=getmash.__main__:entrypoint"]}
)
