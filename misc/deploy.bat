rmdir /s /q ..\fpgatools.egg-info
rmdir /s /q ..\dist

cd ..
python setup.py sdist
twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
