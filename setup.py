import setuptools
import subprocess

getver =  subprocess.Popen("cdk version", shell=True, stdout=subprocess.PIPE).stdout
vernum =  getver.read()
parnum = vernum.decode().split(' ')

with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="distillery",
    version="0.0.1",

    description="An empty CDK Python app",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="author",

    package_dir={"": "distillery"},
    packages=setuptools.find_packages(where="distillery"),

    install_requires=[
        "aws-cdk.core=="+str(parnum[0]),
    ],

    python_requires=">=3.6",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",

        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",

        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",

        "Typing :: Typed",
    ],
)
