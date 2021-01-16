pipenv install
cd web
npm install
npm run build
cd ../

# pyinstallerビルド
git submodule update --init --recursive
cd pyinstaller/bootloader
pipenv run python ./waf all
cd ../
pipenv run python setup.py install
cd ../