import os
import subprocess

def qt_notarytool_notarize() -> bool:
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

    cwd = os.getcwd() 
    print(cwd)
    workspace="/Users/haduong/gitLab"
    entitlementP="/Users/haduong/gitLab/nunchuck-qt/entitlements.plist"

    # Unlock keychain, incase it is locked. Needed for signing.
    os.system(f"security unlock-keychain -p {keychain_password} login.keychain")

    # Create a dmg of the app
    print("Create a dmg of the app: ")
    os.system(f"hdiutil create /tmp/tmp.dmg -ov -volname '{app_name}' -fs HFS+ -srcfolder '{app_name}.app'")
    os.system(f"hdiutil convert /tmp/tmp.dmg -format UDZO -o {app_name}.dmg")

    # Sign the dmg
    print("Sign the dmg: ")
    os.system(f"codesign -f --deep -v --options runtime -s 'Developer ID Application: {developer_ID}' {app_name}.dmg")
    
    # Create keychain profile:
    print("Create keychain profile: ")
    os.system(f"xcrun notarytool store-credentials 'notarytool-profile' --apple-id '{apple_username}' --team-id '{team_ID}' --password '{secret_2FA_password}'")

    notarytool_res = subprocess.check_output(f"xcrun notarytool submit {app_name}.dmg --keychain-profile 'notarytool-profile' --wait",stderr=subprocess.STDOUT,shell=True).decode("utf-8")
    print(notarytool_res)

    #os.system(f"xcrun notarytool log "86fa5ea2-ebd4-4027-b379-549d24926969" --keychain-profile "notarytool-profile"")

    os.system(f"xcrun stapler staple {app_name}.dmg")


qt_notarytool_notarize()
