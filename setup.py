import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='someip-timing-analysis',
    version='1.3.3',
    author='Enrico Fraccaroli',
    author_email='enrico.fraccaroli@univr.it',
    description='SOME/IP timing analysis library',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Galfurian/someip_timing_analysis/',
    license='MIT',
    packages=['someip_timing_analysis'],
    include_package_data=True
)
