#!/bin/bash

if [ ! "$1" ]; then
  echo "This script requires either amd64 of arm64 as an argument"
	exit 1
elif [ "$1" = "amd64" ]; then
	PLATFORM="$1"
	DIR_NAME="shamrock-blockchain-linux-x64"
else
	PLATFORM="$1"
	DIR_NAME="shamrock-blockchain-linux-arm64"
fi

pip install setuptools_scm
# The environment variable SHAMROCK_INSTALLER_VERSION needs to be defined
# If the env variable NOTARIZE and the username and password variables are
# set, this will attempt to Notarize the signed DMG
SHAMROCK_INSTALLER_VERSION=$(python installer-version.py)

if [ ! "$SHAMROCK_INSTALLER_VERSION" ]; then
	echo "WARNING: No environment variable SHAMROCK_INSTALLER_VERSION set. Using 0.0.0."
	SHAMROCK_INSTALLER_VERSION="0.0.0"
fi
echo "Shamrock Installer Version is: $SHAMROCK_INSTALLER_VERSION"

echo "Installing yarn and electron packagers"
yarn add electron-packager -g
yarn add electron-installer-debian -g

echo "Create dist/"
rm -rf dist
mkdir dist

echo "Create executables with pyinstaller"
pip install pyinstaller==4.2
SPEC_FILE=$(python -c 'import shamrock; print(shamrock.PYINSTALLER_SPEC_PATH)')
pyinstaller --log-level=INFO "$SPEC_FILE"
LAST_EXIT_CODE=$?
if [ "$LAST_EXIT_CODE" -ne 0 ]; then
	echo >&2 "pyinstaller failed!"
	exit $LAST_EXIT_CODE
fi

cp -r dist/daemon ../shamrock-blockchain-gui
cd .. || exit
cd shamrock-blockchain-gui || exit

echo "yarn build"
yarn
yarn audit fix
yarn run build
LAST_EXIT_CODE=$?
if [ "$LAST_EXIT_CODE" -ne 0 ]; then
	echo >&2 "yarn run build failed!"
	exit $LAST_EXIT_CODE
fi

electron-packager . shamrock-blockchain --asar.unpack="**/daemon/**" --platform=linux \
--icon=src/assets/img/Shamrock.icns --overwrite --app-bundle-id=net.shamrock.blockchain \
--appVersion=$SHAMROCK_INSTALLER_VERSION
LAST_EXIT_CODE=$?
if [ "$LAST_EXIT_CODE" -ne 0 ]; then
	echo >&2 "electron-packager failed!"
	exit $LAST_EXIT_CODE
fi

mv $DIR_NAME ../build_scripts/dist/
cd ../build_scripts || exit

echo "Create shamrock-$SHAMROCK_INSTALLER_VERSION.deb"
rm -rf final_installer
mkdir final_installer
electron-installer-debian --src dist/$DIR_NAME/ --dest final_installer/ \
--arch "$PLATFORM" --options.version $SHAMROCK_INSTALLER_VERSION
LAST_EXIT_CODE=$?
if [ "$LAST_EXIT_CODE" -ne 0 ]; then
	echo >&2 "electron-installer-debian failed!"
	exit $LAST_EXIT_CODE
fi

ls final_installer/
