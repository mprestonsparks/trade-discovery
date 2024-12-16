# Task status update script
param(
    [Parameter(Mandatory=$true)]
    [int]$TaskId,
    
    [Parameter(Mandatory=$true)]
    [ValidateSet('ready', 'in-progress', 'review', 'blocked', 'completed')]
    [string]$NewStatus,
    
    [Parameter(Mandatory=$true)]
    [string]$Details
)

Import-Module powershell-yaml

# Load and parse DEVELOPMENT_STATUS.yaml
$yamlPath = ".project/status/DEVELOPMENT_STATUS.yaml"
$content = Get-Content $yamlPath -Raw
$status = ConvertFrom-Yaml $content

# Update task status
$taskFound = $false
$task = $null
foreach ($t in $status.next_available_tasks) {
    if ($t.id -eq $TaskId) {
        $task = $t
        $task.status = $NewStatus
        $taskFound = $true
        break
    }
}

if (-not $taskFound) {
    Write-Error "Task $TaskId not found"
    exit 1
}

# Add activity log entry
$timestamp = Get-Date -Format "o"
$logEntry = @{
    task_id = $TaskId
    action = "Updated task $TaskId to $NewStatus"
    details = $Details
    timestamp = $timestamp
}

if (-not $status.ai_activity_log) {
    $status.ai_activity_log = @()
}
$status.ai_activity_log += $logEntry

# Save updated YAML
$updatedYaml = ConvertTo-Yaml $status
Set-Content -Path $yamlPath -Value $updatedYaml

# Update GitHub issue label if issue exists
if ($task.github_issue) {
    gh issue edit $task.github_issue --add-label $NewStatus
    Write-Host "https://github.com/mprestonsparks/trade-discovery/issues/$($task.github_issue)"
} else {
    Write-Host "Note: No GitHub issue associated with task $TaskId"
}

Write-Host "Task $TaskId updated to status: $NewStatus"
