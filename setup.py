from setuptools import setup

setup(
    name='Yacta',
    entry_points={
        'console_scripts': [
            'todo = todo:main',
            't = todo:main',
            'yacta = todo:main',
            'y = todo:main'
        ]
    }
)