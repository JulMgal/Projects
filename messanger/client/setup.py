from setuptools import setup, find_packages

setup(name="messanger_client",
      version="0.0.1",
      description="messanger_client",
      author="Yuliya Mgalobelova",
      author_email="jv-av@mail.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
