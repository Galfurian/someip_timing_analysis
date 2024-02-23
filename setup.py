import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='SOME/IP Timing Analysis',
    version='1.0.0',
    author='Enrico Fraccaroli',
    author_email='enrico.fraccaroli@univr.it',
    description='SOME/IP timing analysis library',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Galfurian/someip_timing_analysis/',
    license='MIT',
    packages=['someip_timing_analysis'],
    install_requires=[],
    include_package_data=True
)
