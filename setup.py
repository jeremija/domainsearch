import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='magnet',
    version='1.0.0',
    author='Jerko Steiner',
    author_email='jerko.steiner@gmail.com',
    description=(
        'Search for available domains using wildcards'
    ),
    install_requires=[],
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jeremija/domainsearch',
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)