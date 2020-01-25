import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='func_adl_uproot',
                 version=0.4,
                 description=('Functional Analysis Description Language'
                              + ' uproot backend for accessing flat ROOT ntuples'),
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 packages=setuptools.find_packages(exclude=['tests']),
                 install_requires=['awkward', 'qastle', 'uproot'],
                 author='Mason Proffitt',
                 author_email='masonlp@uw.edu',
                 url='https://github.com/iris-hep/func_adl.uproot')
