from setuptools import find_packages, setup

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# Read version from lim_procurement/__init__.py
version = "0.0.1"
with open("lim_procurement/__init__.py") as f:
	for line in f:
		if line.startswith("__version__"):
			version = line.split("=")[1].strip().strip('"').strip("'")
			break

setup(
	name="lim_procurement",
	version=version,
	description="LIM-specific extensions of ERPNext: Custom Fields, Custom DocTypes, hooks, and whitelisted REST methods.",
	author="Lagos International Market",
	author_email="ibrahimolayemi09@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires,
)
