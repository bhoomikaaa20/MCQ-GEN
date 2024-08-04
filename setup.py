from setuptools import find_packages,setup

setup(
    name='mcqgen',
    version='0.0.1',
    author='Bhoomi',
    author_email='bhoomikaaa20@gmail.com',
    install_requires=['openai','langchain','streamlit','pyPDF2','python-dotenv'],
    packages=find_packages()
)