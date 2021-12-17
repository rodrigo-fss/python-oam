from setuptools import setup


setup(
    name='oam',
    version='0.1',
    description='OAM',
    author=['Rodrigo Faria', 'Tiago Colli'],
    author_email='rodrigo.f.ss@uol.com.br',
    license='MIT',
    install_requires=[
      'pandas', 'seaborn'
    ],
    packages=['oam'],
    zip_safe=False
)
