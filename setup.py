from distutils.core import setup

setup(
    name='monni',
    version='',
    packages=['monni', 'monni.ui', 'monni.ui.lists', 'monni.ui.server', 'monni.ui.favorites', 'monni.games',
              'monni.games.teeworlds', 'monni.games.urbanterror'],
    url='',
    license='',
    author='',
    author_email='',
    description='',
    entry_points = {
        'console_scripts': ['monni=monni.__init__:main'],
    }
)
