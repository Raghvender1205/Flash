from setuptools import find_packages, setup

with open('README.md') as f:
    long_description = f.read()

if  __name__ == '__main__':
    setup(
        name='flash',
        description='Flash: A Fast and Simple PyTorch based Trainer',
        long_description=long_description,
        author='Raghvender',
        packages=find_packages(),
        include_package_data=True,
        platforms=['linux', 'unix'],
        python_requires='>=3.6'
    )