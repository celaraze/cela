from setuptools import setup, find_packages

setup(
    name='cela',
    version='0.0.2-alpha',
    packages=find_packages(),
    description='A command client for CELA.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='celaraze',
    author_email='celaraze@qq.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    keywords='cela,asset,management,client',
    install_requires=['pyyaml', 'pymysql'],
    entry_points={
        'console_scripts': [
            'cela=client.main:main',
        ],
    },
)
