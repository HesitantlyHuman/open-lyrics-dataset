from setuptools import setup, find_packages

if __name__ == '__main__':
    setup(
        name = 'open-lyrics-dataset',
        version = '0.0.8',
        package_dir = {'openlyrics' : 'src/openlyrics'},
        package_data = {
            '' : ['*.json']
        },
        include_package_data = True,
        packages = find_packages(
            where = 'src'
        )
    )