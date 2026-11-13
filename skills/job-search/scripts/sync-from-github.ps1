<#
  sync-from-github.ps1 -- keep a local job-search skill in step with its GitHub repo.
  Author: Jibril Sulaiman (with Claude Code)

  What it does, once per run:
    1. Fetches the repo's default branch.
    2. If GitHub has new commits, fast-forwards the local clone (skips, and logs why,
       when the clone has uncommitted edits or has diverged).
    3. Compares the repo's skills/job-search folder with the installed skill folder.
       If anything differs, backs the installed folder up, then copies the repo's
       version over it.
  Every run appends one or more lines to the log file.

  Run it by hand:
    powershell -ExecutionPolicy Bypass -File .\sync-from-github.ps1 -RepoDir C:\path\to\clone

  Schedule it daily (Windows Task Scheduler, runs as you, only while you're signed in):
    $a = New-ScheduledTaskAction -Execute "powershell.exe" -Argument '-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File "C:\path\to\clone\skills\job-search\scripts\sync-from-github.ps1" -RepoDir "C:\path\to\clone"'
    $t = New-ScheduledTaskTrigger -Daily -At 9am
    $s = New-ScheduledTaskSettingsSet -StartWhenAvailable
    Register-ScheduledTask -TaskName "Job search skill - daily GitHub sync" -Action $a -Trigger $t -Settings $s
#>
param(
  [Parameter(Mandatory = $true)][string]$RepoDir,
  [string]$SkillDir = (Join-Path $HOME ".claude\skills\job-search"),
  [string]$LogFile = (Join-Path $HOME ".claude\skills\job-search-sync.log"),
  [string]$BackupRoot = (Join-Path $HOME ".claude\skill-backups")
)

$ErrorActionPreference = "Stop"
function Log($msg) {
  $line = "{0}  {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), $msg
  Add-Content -Path $LogFile -Value $line -Encoding utf8
  Write-Output $line
}
function Invoke-Git([string[]]$GitArgs) {
  # Windows PowerShell turns git's stderr into errors under "Stop"; judge by exit code instead
  $ErrorActionPreference = "Continue"
  $out = & git.exe -C $RepoDir @GitArgs 2>&1 | ForEach-Object { "$_" }
  if ($LASTEXITCODE -ne 0) { throw "git $($GitArgs -join ' ') failed: $($out -join ' ')" }
  return ($out -join "`n")
}
function FolderHashes($dir) {
  $map = @{}
  if (-not (Test-Path $dir)) { return $map }
  Get-ChildItem -Path $dir -Recurse -File | ForEach-Object {
    $rel = $_.FullName.Substring($dir.Length).TrimStart('\', '/')
    # Compare text with line endings normalised, so CRLF/LF checkouts don't count as changes
    $text = [IO.File]::ReadAllText($_.FullName) -replace "`r`n", "`n"
    $bytes = [Text.Encoding]::UTF8.GetBytes($text)
    $sha = [Security.Cryptography.SHA256]::Create()
    $map[$rel] = [BitConverter]::ToString($sha.ComputeHash($bytes))
  }
  return $map
}

try {
  if (-not (Test-Path (Join-Path $RepoDir ".git"))) { throw "Not a git clone: $RepoDir" }

  # 1. Fetch
  $branch = (Invoke-Git @("rev-parse", "--abbrev-ref", "HEAD")).Trim()
  Invoke-Git @("fetch", "--quiet", "origin", $branch) | Out-Null
  $local = (Invoke-Git @("rev-parse", "HEAD")).Trim()
  $remote = (Invoke-Git @("rev-parse", "origin/$branch")).Trim()

  # 2. Fast-forward when GitHub is ahead
  if ($local -ne $remote) {
    $dirty = Invoke-Git @("status", "--porcelain")
    $base = (Invoke-Git @("merge-base", "HEAD", "origin/$branch")).Trim()
    if ($dirty) {
      Log "GitHub has new commits, but the clone has uncommitted changes; not pulling. Commit or discard them, then rerun."
    } elseif ($base -ne $local) {
      Log "The clone has local commits GitHub doesn't have; not pulling. Push or reset them, then rerun."
    } else {
      Invoke-Git @("merge", "--ff-only", "--quiet", "origin/$branch") | Out-Null
      Log ("Pulled {0}..{1} from GitHub." -f $local.Substring(0, 7), $remote.Substring(0, 7))
    }
  }

  # 3. Update the installed skill when the repo's copy differs
  $src = Join-Path $RepoDir "skills\job-search"
  if (-not (Test-Path (Join-Path $src "SKILL.md"))) { throw "No SKILL.md in $src" }
  $a = FolderHashes $src
  $b = FolderHashes $SkillDir
  $changed = @($a.Keys | Where-Object { $b[$_] -ne $a[$_] }) + @($b.Keys | Where-Object { -not $a.ContainsKey($_) })
  if ($changed.Count -eq 0) {
    Log "No changes. Installed skill matches GitHub ($($remote.Substring(0, 7)))."
  } else {
    if (Test-Path $SkillDir) {
      $stamp = Get-Date -Format "yyyyMMdd-HHmmss"
      New-Item -ItemType Directory -Force -Path $BackupRoot | Out-Null
      Copy-Item -Recurse -Path $SkillDir -Destination (Join-Path $BackupRoot "job-search-$stamp")
      Remove-Item -Recurse -Force -Path $SkillDir
    }
    Copy-Item -Recurse -Path $src -Destination $SkillDir
    Log ("Updated the installed skill from GitHub ({0}). Changed: {1}" -f $remote.Substring(0, 7), ($changed -join ", "))
  }
} catch {
  Log "ERROR: $($_.Exception.Message)"
  exit 1
}
