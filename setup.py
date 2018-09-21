from setuptools import setup, find_packages

VERSION='0.1.0-alpha'

long_description='An opinionated fast tool that provisions kubernetes clusters atop libvirt'
packages=[
    'libvirt-installer',
]
install_requires=[
    'click',
]
def main():
    setup_info = dict(
        name='libvirt-installer',
        version=VERSION,
        author='Victor Palade',
        description='Libvirt/Kubernetes tools',
        long_description=long_description,
        license='Apache-2.0',
        packages=packages,
        install_requires=install_requires,
        zip_safe=False,
    )

    setup(**setup_info)

if __name__ == '__main__':
    main()
