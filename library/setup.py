from setuptools import setup

setup(
   name='othello',
   version='1.0',
   description='A useful module',
   author='Man Foo',
   author_email='foomail@foo.example',
   packages=['othello'],  #same as name
   install_requires=["setuptools>=64.0.0", "wheel"], #external packages as dependencies
)