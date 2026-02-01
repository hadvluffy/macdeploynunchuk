# PowerShell script to delete GitHub Actions workflow runs
# Requires: GitHub CLI (gh) to be installed and authenticated
# Usage: .\delete_workflow_runs.ps1 -Owner "owner" -Repo "repo" [-Workflow "workflow.yml"]
#
# Examples:
#   .\delete_workflow_runs.ps1 -Owner "hadvluffy" -Repo "macdeploynunchuk"
#   .\delete_workflow_runs.ps1 -Owner "hadvluffy" -Repo "macdeploynunchuk" -Workflow "nunchuk-macos[x86].yml"

param(
    [Parameter(Mandatory = $true)]
    [string]$Owner,
    
    [Parameter(Mandatory = $true)]
    [string]$Repo,
    
    [Parameter(Mandatory = $false)]
    [string]$Workflow
)

# Refresh PATH to ensure gh is available
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

if ($Workflow) {
    Write-Host "Deleting workflow runs for $Owner/$Repo (workflow: $Workflow)..." -ForegroundColor Yellow
    $apiUrl = "repos/$Owner/$Repo/actions/workflows/$Workflow/runs?per_page=100"
} else {
    Write-Host "Deleting all workflow runs for $Owner/$Repo..." -ForegroundColor Yellow
    $apiUrl = "repos/$Owner/$Repo/actions/runs?per_page=100"
}

$deletedCount = 0

do {
    Write-Host "Fetching workflow runs..." -ForegroundColor Cyan
    
    $response = gh api $apiUrl 2>$null | ConvertFrom-Json
    
    if ($null -eq $response -or $response.total_count -eq 0) {
        Write-Host "No workflow runs found." -ForegroundColor Gray
        break
    }
    
    $runs = $response.workflow_runs
    
    if ($null -eq $runs -or $runs.Count -eq 0) {
        break
    }
    
    foreach ($run in $runs) {
        $runId = $run.id
        if ($runId) {
            Write-Host "Deleting workflow run: $runId" -ForegroundColor Gray
            gh api -X DELETE "repos/$Owner/$Repo/actions/runs/$runId" 2>$null
            $deletedCount++
        }
    }
    
    # Small delay to avoid rate limiting
    Start-Sleep -Milliseconds 100
    
} while ($true)

Write-Host "`nDone! Deleted $deletedCount workflow runs." -ForegroundColor Green
