from setuptools import setup

setup(
    name='todo',
    entry_points={
        'console_scripts': [
            'todo = todo:main',
            't = todo:main'
        ]
    }
)