from setuptools import find_packages, setup

package_name = 'hardware_interface_py'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='yangy',
    maintainer_email='yang-yy24@mails.tsinghua.edu.cn',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'camera = hardware_interface_py.camera:main',
            'buzzer = hardware_interface_py.buzzer:main',
            'i2c = hardware_interface_py.i2c:main',
        ],
    },
)
