from setuptools import setup, find_packages

setup(
    name="webezyio",
    install_requires=["pluggy>=0.3,<1.0","protobuf","grpcio","grpcio-tools"],
    packages=find_packages(),
)
