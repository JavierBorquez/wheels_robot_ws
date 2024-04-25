from setuptools import find_packages, setup

package_name = 'wheels_ctrl'

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
    maintainer='javier',
    maintainer_email='javier@todo.todo',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'hello_world = wheels_ctrl.hello_world:main',
            'basic_pub = wheels_ctrl.basic_pub:main',
            'gamepad_pub = wheels_ctrl.gamepad_pub:main',
        ],
    },
)
