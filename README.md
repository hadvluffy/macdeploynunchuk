# Mac Deploy Nunchuk

![github](https://github.com/bakaoh/macdeploynunchuk/workflows/mac/badge.svg) [![travis-ci](https://travis-ci.com/bakaoh/macdeploynunchuk.svg?branch=main)](https://travis-ci.com/bakaoh/macdeploynunchuk)


Done! Deleted 0 workflow runs.
PS D:\Workspace\macdeploynunchuk> gh auth login
? Where do you use GitHub? GitHub.com
? What is your preferred protocol for Git operations on this host? HTTPS
? Authenticate Git with your GitHub credentials? Yes
? How would you like to authenticate GitHub CLI? Login with a web browser

! First copy your one-time code: E88F-8DFE
Press Enter to open https://github.com/login/device in your browser... 
✓ Authentication complete.
- gh config set -h github.com git_protocol https
✓ Configured git protocol
✓ Logged in as hadvluffy
PS D:\Workspace\macdeploynunchuk> .\delete_workflow_runs.ps1 -Owner "hadvluffy" -Repo "macdeploynunchuk" -Workflow "nunchuk-macos[x86].yml"