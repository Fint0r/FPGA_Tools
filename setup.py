from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'Operating System :: POSIX :: Linux',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='fpgatools',
    version='1.2.0',
    author='József Fintor',
    author_email='fintor976@gmail.com',
    description='University project to support FPGA development.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Fint0r/FPGA_Tools',
    license='MIT',
    classifiers=classifiers,
    keywords=['fpga', 'development', 'xdc', 'testbench', 'generator', 'tb'],
    packages=find_packages(),
    install_requires=['PyQt5']
)
