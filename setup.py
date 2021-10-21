import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hepi",
    setup_requires=['setuptools-git-versioning'],
    author="APN",
    author_email="APN-Pucky@no-reply.github.com",
    description="hepi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/APN-Pucky/hepi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "setuptools-git",
        "uncertainties",
        "numpy",
        "matplotlib",
        "scipy",
        "sympy",
        "smpl",
        "pyslha"
        # "requests",
        # "tqdm",
        # "pandas",
    ],
    version_config={
        "template": "{tag}",
        "dev_template": "{tag}.{ccount}",
        "dirty_template": "{tag}.{ccount}+dirty",
        "starting_version": "0.0.0",
        "version_callback": None,
        "version_file": None,
        "count_commits_from_version_file": False
    },
    include_package_data=True,
    python_requires='>=3.6',
)
