from setuptools import setup, find_packages

VERSION='0.1.0'

long_description='''
An opinionated command line utility that provisions kubernetes clusters atop libvirt.
'''

packages=[
    'installer',
]

install_requires=[
    'click',
    'libvirt-python',
    'toml',
    'jinja2',
    'tabulate',
]

def main():
    setup_info = dict(
        name='libvirt-installer',
        version=VERSION,
        url="https://github.com/pi-victor/libvirt-installer",
        author='Victor Palade <victor@cloudflavor.io>',
        description='Libvirt wrapper for fast kubernetes bootstraps',
        long_description=long_description,
        license='Apache-2.0',
        packages=packages,
        install_requires=install_requires,
        zip_safe=False,
    )

    setup(**setup_info)

if __name__ == '__main__':
    main()
