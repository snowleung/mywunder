from setuptools import setup, find_packages

try:
    desc_file = open("README.rst")
    description = desc_file.read()
    desc_file.close()
except:
    description = ""

setup(
    name="mywunder",
    version="0.1.1",
    author="snowleung",
    author_email="snowleung@gmail.com",
    url="https://github.com/snowleung/mywunder",
    license="MIT",
    description="an extension of wunder list",
    long_description=description,
    classifiers=['Development Status :: 0.1 - Beta',
                'License :: OSI Approved :: MIT License',
                'Intended Audience :: Developers',
                'Natural Language :: English',
                'Programming Language :: Python',
                'Programming Language :: Python :: 2.7',
                'Programming Language :: Python :: Implementation :: PyPy',
                'Topic :: Utilities',
                'Topic :: Documentation',
                'Environment :: Console'],
    packages=find_packages(exclude=("tests",)),
    install_requires=["wunderpy"],
    entry_points={'console_scripts': ['mywunder = mywunder.mywunder_main:main']}
)
