import setuptools

with open('README.md','r',encoding='utf-8') as f:
    long_discription=f.read()

setuptools.setup(
    name='FDSMLP',
    version='1.0.0',
    author='Micheal',
    author_email='853974517@qq.com',
    description='这个库写着玩滴！可以做运筹作业',
    long_description=long_discription,
    long_description_content_type="text/markdown",
    url='',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python ::3",
        "License :: OSI Approved ::MIT Licence",
        "Operating System :: Os Independent"
    ]
)