from setuptools import setup


with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="openvpn_py", 
    version="0.1",
    packages=["openvpn_py"],
    package_dir={"openvpn_py": "."},
    install_requires=requirements,
)