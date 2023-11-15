import setuptools

with open('README.md','r',encoding='utf-8') as f:
    long_description=f.read()

setuptools.setup(
    name='FDSMLP',
    version='1.0.3',
    author='Micheal',
    description='可以打印单纯形表的LP求解器！',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/xuanfengzu/FDSMLP',
    packages=setuptools.find_packages(),
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: BSD License",
    "Operating System :: OS Independent",
    ]
)