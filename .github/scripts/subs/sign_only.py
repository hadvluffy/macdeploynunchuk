import os
import subprocess

def qt_sign_only() -> bool:
    runner_workspace = os.environ.get('runner_workspace')
    app_name = os.environ.get('AppName')
    developer_ID = os.environ.get('DeveloperID')
    team_ID = os.environ.get('TeamID')
    keychain_password = os.environ.get('KeyChainPassword')
    apple_username = os.environ.get('AppleUserName')
    secret_2FA_password = os.environ.get('Secret_2FA_password')
    bundle_ID = os.environ.get('BundleID')
    print("app_name: " + app_name)
    print("developer_ID: " + developer_ID)
    print("team_ID: " + team_ID)
    print("keychain_password: " + keychain_password)
    print("apple_username: " + apple_username)
    print("secret_2FA_password: " + secret_2FA_password)
    print("bundle_ID: " + bundle_ID)

    print(runner_workspace)
    entitlementP=runner_workspace + "/nunchuck-qt/entitlements.plist"
    print(entitlementP)
    # Unlock keychain, incase it is locked. Needed for signing.
    os.system(f"security unlock-keychain -p {keychain_password} login.keychain")

    # Sign the app bundle using codesign
    print("Sign the app bundle using codesign: ")
    print("Sign all *.dylib: ")
    os.system(f"find {app_name}.app -name '*.dylib' | xargs -I $ codesign --force --verify --verbose --options=runtime --timestamp -s 'Developer ID Application: {developer_ID}' --entitlements {entitlementP} $")
    print("Sign all *.plugin: ")
    os.system(f"find {app_name}.app -name '*.plugin' | xargs -I $ codesign --force --verify --verbose --options=runtime --timestamp -s 'Developer ID Application: {developer_ID}' --entitlements {entitlementP} $")
    print("Sign Qt frameworks: ")
    os.system(f"find {app_name}.app -name 'Qt*' | xargs -I $ codesign --force --verify --verbose --options=runtime --timestamp -s 'Developer ID Application: {developer_ID}' --entitlements {entitlementP} $")
    print("Sign app: ")
    os.system(f"codesign --force --verify --verbose --options=runtime --timestamp -s 'Developer ID Application: {developer_ID}' --entitlements {entitlementP} {app_name}.app/Contents/MacOS/Nunchuk")
    print("Sign hwi: ")
    os.system(f"codesign --force --verify --verbose --options=runtime --timestamp -s 'Developer ID Application: {developer_ID}' --entitlements {entitlementP} {app_name}.app/Contents/MacOS/hwi")
    print("Sign verify: ")
    os.system(f"codesign -dvvv {app_name}.app")
    print("******* Verify Bundle using dpctl ***********")
    os.system(f"spctl -a -vvvv {app_name}.app")

qt_sign_only()
