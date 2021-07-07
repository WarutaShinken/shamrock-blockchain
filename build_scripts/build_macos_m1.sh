#!/bin/bash

set -euo pipefail

pip install setuptools_scm
# The environment variable SHAMROCK_INSTALLER_VERSION needs to be defined.
# If the env variable NOTARIZE and the username and password variables are
# set, this will attempt to Notarize the signed DMG.
SHAMROCK_INSTALLER_VERSION=$(python installer-version.py)

if [ ! "$SHAMROCK_INSTALLER_VERSION" ]; then
	echo "WARNING: No environment variable SHAMROCK_INSTALLER_VERSION set. Using 0.0.0."
	SHAMROCK_INSTALLER_VERSION="0.0.0"
fi
echo "Shamrock Installer Version is: $SHAMROCK_INSTALLER_VERSION"

echo "Installing npm and electron packagers"
npm install electron-installer-dmg -g
npm install electron-packager -g
npm install electron/electron-osx-sign -g
npm install notarize-cli -g

echo "Create dist/"
sudo rm -rf dist
mkdir dist

echo "Install pyinstaller and build bootloaders for M1"
#pip install pyinstaller==4.3
# Once there is a 4.4, we can clone that tag and build that
# M1 support isn't in a tag yet.
# Alternatively, if the m1 bootloaders are distributed with pip in the future, can just use those
git clone https://github.com/pyinstaller/pyinstaller.git
cd pyinstaller/bootloader
python ./waf all
pip install ..
cd ../..

echo "Create executables with pyinstaller"
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

echo "npm build"
npm install
npm audit fix
npm run build
LAST_EXIT_CODE=$?
if [ "$LAST_EXIT_CODE" -ne 0 ]; then
	echo >&2 "npm run build failed!"
	exit $LAST_EXIT_CODE
fi

electron-packager . Shamrock --asar.unpack="**/daemon/**" --platform=darwin \
--icon=src/assets/img/Shamrock.icns --overwrite --app-bundle-id=net.shamrock.blockchain \
--appVersion=$SHAMROCK_INSTALLER_VERSION
LAST_EXIT_CODE=$?
if [ "$LAST_EXIT_CODE" -ne 0 ]; then
	echo >&2 "electron-packager failed!"
	exit $LAST_EXIT_CODE
fi

if [ "$NOTARIZE" ]; then
  electron-osx-sign Shamrock-darwin-arm64/Shamrock.app --platform=darwin \
  --hardened-runtime=true --provisioning-profile=shamrockblockchain.provisionprofile \
  --entitlements=entitlements.mac.plist --entitlements-inherit=entitlements.mac.plist \
  --no-gatekeeper-assess
fi
LAST_EXIT_CODE=$?
if [ "$LAST_EXIT_CODE" -ne 0 ]; then
	echo >&2 "electron-osx-sign failed!"
	exit $LAST_EXIT_CODE
fi

mv Shamrock-darwin-arm64 ../build_scripts/dist/
cd ../build_scripts || exit

DMG_NAME="Shamrock-$SHAMROCK_INSTALLER_VERSION-arm64.dmg"
echo "Create $DMG_NAME"
mkdir final_installer
electron-installer-dmg dist/Shamrock-darwin-arm64/Shamrock.app Shamrock-$SHAMROCK_INSTALLER_VERSION-arm64 \
--overwrite --out final_installer
LAST_EXIT_CODE=$?
if [ "$LAST_EXIT_CODE" -ne 0 ]; then
	echo >&2 "electron-installer-dmg failed!"
	exit $LAST_EXIT_CODE
fi

ls -lh final_installer

if [ "$NOTARIZE" ]; then
	echo "Notarize $DMG_NAME on ci"
	cd final_installer || exit
  notarize-cli --file=$DMG_NAME --bundle-id net.shamrock.blockchain \
	--username "$APPLE_NOTARIZE_USERNAME" --password "$APPLE_NOTARIZE_PASSWORD"
  echo "Notarization step complete"
else
	echo "Not on ci or no secrets so skipping Notarize"
fi

# Notes on how to manually notarize
#
# Ask for username and password. password should be an app specific password.
# Generate app specific password https://support.apple.com/en-us/HT204397
# xcrun altool --notarize-app -f Shamrock-0.1.X.dmg --primary-bundle-id net.shamrock.blockchain -u username -p password
# xcrun altool --notarize-app; -should return REQUEST-ID, use it in next command
#
# Wait until following command return a success message".
# watch -n 20 'xcrun altool --notarization-info  {REQUEST-ID} -u username -p password'.
# It can take a while, run it every few minutes.
#
# Once that is successful, execute the following command":
# xcrun stapler staple Shamrock-0.1.X.dmg
#
# Validate DMG:
# xcrun stapler validate Shamrock-0.1.X.dmg
