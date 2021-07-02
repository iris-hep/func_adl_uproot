import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='func_adl_uproot',
                 version='1.3',
                 description=('Functional Analysis Description Language'
                              + ' uproot backend for accessing flat ROOT ntuples'),
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 packages=setuptools.find_packages(exclude=['tests']),
                 python_requires=('>=3.6, <3.10'),
                 install_requires=['awkward>=1.2',
                                   'func_adl',
                                   'numpy',
                                   'qastle>=0.10',
                                   'uproot>=4'],
                 extras_require={'test': ['flake8', 'pytest', 'pytest-cov']},
                 author='Mason Proffitt',
                 author_email='masonlp@uw.edu',
                 url='https://github.com/iris-hep/func_adl_uproot')
