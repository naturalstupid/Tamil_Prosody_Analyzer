param(
    [string]$Version = "",
    [Parameter(Mandatory = $true)][string]$Message
)

# YaappaRiSeyali release helper: update setup.py, one commit, one annotated tag, one push.

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$SetupFile = "setup.py"
$HistoryFile = "_release_history.txt"
$TagPrefix = "v"
$MinMessageLength = 10
$BannedMessages = @(
    'new version','new release','bug fixes','minor changes','misc changes','work in progress',
    'no comment','none','n/a','test','testing','update','updated','fix','fixes','wip'
)

function Stop-Release([string]$Reason) {
    Write-Host ""
    Write-Host "RELEASE REJECTED: $Reason" -ForegroundColor Red
    Write-Host "Nothing was changed: no version/history edit, no commit, no tag." -ForegroundColor Red
    exit 1
}

function Invoke-GitCapture([string[]]$GitArgs) {
    $old = $ErrorActionPreference; $ErrorActionPreference = "Continue"
    try { $out = & git @GitArgs 2>$null; $code = $LASTEXITCODE }
    finally { $ErrorActionPreference = $old }
    return [pscustomobject]@{ Code = $code; Output = @($out) }
}

function Invoke-Git([string[]]$GitArgs, [string]$FailureMessage) {
    $old = $ErrorActionPreference; $ErrorActionPreference = "Continue"
    try { & git @GitArgs; $code = $LASTEXITCODE }
    finally { $ErrorActionPreference = $old }
    if ($code -ne 0) { throw $FailureMessage }
}

function Get-ChangedFiles {
    $r = Invoke-GitCapture @('-c','core.quotepath=false','status','--porcelain=v1','--untracked-files=all')
    if ($r.Code -ne 0) { Stop-Release "Unable to read Git status." }
    $files = @()
    foreach ($line in $r.Output) {
        $text = [string]$line
        if ($text.Trim().Length -eq 0 -or $text.Length -lt 4) { continue }
        $path = $text.Substring(3).Trim().Trim('"')
        if ($path -match ' -> ') { $path = ($path -split ' -> ')[-1] }
        if ($path) { $files += $path.Replace('\','/') }
    }
    return @($files | Sort-Object -Unique)
}

function Plain-Version([string]$Value) {
    return ($Value.Trim() -replace '^[vV]','')
}

function Get-CurrentVersion {
    $setupPath = Join-Path $PSScriptRoot $SetupFile
    if (-not (Test-Path -LiteralPath $setupPath -PathType Leaf)) {
        Stop-Release "$SetupFile was not found."
    }
    $content = [System.IO.File]::ReadAllText($setupPath, (New-Object System.Text.UTF8Encoding($false)))
    $m = [regex]::Match($content, 'version\s*=\s*["'']([^"''\r\n]+)["'']')
    if (-not $m.Success) {
        Stop-Release "Could not find version=... in $SetupFile."
    }
    return (Plain-Version $m.Groups[1].Value)
}

function Set-SetupVersion([string]$NewVer) {
    $setupPath = Join-Path $PSScriptRoot $SetupFile
    $content = [System.IO.File]::ReadAllText($setupPath, (New-Object System.Text.UTF8Encoding($false)))
    $pattern = '(version\s*=\s*["''])([^"''\r\n]+)(["''])'
    if (-not [regex]::IsMatch($content, $pattern)) {
        throw "Could not update version in $SetupFile."
    }
    $updated = [regex]::Replace($content, $pattern, "`${1}$NewVer`${3}", 1)
    [System.IO.File]::WriteAllText($setupPath, $updated, (New-Object System.Text.UTF8Encoding($false)))
}

function Get-NextVersion([string]$Current) {
    if ($Current -notmatch '^\d+(\.\d+)*$') { return "" }
    $p = $Current.Split('.')
    $p[-1] = [string]([int64]$p[-1] + 1)
    return ($p -join '.')
}

function Read-NewVersion([string]$Current) {
    $suggested = Get-NextVersion $Current
    $shown = if ($Current) { $Current } else { '(unknown)' }
    Write-Host ""
    Write-Host "Current YaappaRiSeyali version: $shown" -ForegroundColor Cyan
    $prompt = if ($suggested) { "New version [Enter = $suggested]" } else { "New version (e.g. 1.7.8)" }
    $answer = Read-Host $prompt
    if ([string]::IsNullOrWhiteSpace($answer)) { $answer = $suggested }
    return (Plain-Version $answer)
}

function Test-Version([string]$Value) {
    if ($Value -notmatch '^\d+(\.\d+){1,3}$') {
        Stop-Release "Version '$Value' is invalid. Use numbers separated by dots, for example 1.7.8"
    }
}

function Test-TagUnused([string]$Tag) {
    $local = Invoke-GitCapture @('tag','-l',$Tag)
    if (($local.Output -join '').Trim()) { Stop-Release "Tag '$Tag' already exists locally." }
    $remote = Invoke-GitCapture @('ls-remote','--tags','origin',"refs/tags/$Tag")
    if ($remote.Code -ne 0) { Stop-Release "Unable to check tags on origin." }
    if (($remote.Output -join '').Trim()) { Stop-Release "Tag '$Tag' already exists on origin." }
}

function Write-Utf8NoBom([string]$Path,[string]$Text) {
    [System.IO.File]::WriteAllText((Join-Path $PSScriptRoot $Path), $Text, (New-Object System.Text.UTF8Encoding($false)))
}

function Add-History([string]$Ver,[string]$Msg) {
    $entry = "V$Ver - $Msg"
    $old = @()
    if (Test-Path -LiteralPath $HistoryFile) {
        $old = @(Get-Content -LiteralPath $HistoryFile -Encoding UTF8 | Where-Object { $_ -ne "V$Ver" -and $_ -notlike "V$Ver - *" })
    }
    Write-Utf8NoBom $HistoryFile ((@($entry) + $old) -join "`r`n")
}

# ---------------- validation: edit nothing above this line ----------------
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { Stop-Release "git was not found." }
if ((Invoke-GitCapture @('rev-parse','--is-inside-work-tree')).Code -ne 0) { Stop-Release "Not inside a Git repository." }
if ((Invoke-GitCapture @('remote','get-url','origin')).Code -ne 0) { Stop-Release "Git remote 'origin' is not configured." }

$Message = ($Message -replace '\s+',' ').Trim()
if ($Message.Length -lt $MinMessageLength) { Stop-Release "Release comment must be at least $MinMessageLength characters." }
if (($Message -replace '[^\p{L}]','').Length -lt 5) { Stop-Release "Release comment must contain words." }
if ($BannedMessages -contains $Message.TrimEnd('.','!').ToLowerInvariant()) { Stop-Release "Describe what changed; '$Message' is too generic." }

$branchResult = Invoke-GitCapture @('branch','--show-current')
$Branch = (($branchResult.Output -join '').Trim())
if ($branchResult.Code -ne 0 -or -not $Branch) { Stop-Release "Detached HEAD or unknown branch." }

$ChangedFiles = @(Get-ChangedFiles)
if ($ChangedFiles.Count -eq 0) { Stop-Release "There are no changed files to release." }
Write-Host ""; Write-Host "Changed files:" -ForegroundColor Cyan
$ChangedFiles | ForEach-Object { Write-Host "  $_" }

$Version = Plain-Version $Version
if (-not $Version) { $Version = Read-NewVersion (Get-CurrentVersion) }
Test-Version $Version
$Tag = "$TagPrefix$Version"
Test-TagUnused $Tag

$remoteBranch = Invoke-GitCapture @('ls-remote','--exit-code','--heads','origin',$Branch)
if ($remoteBranch.Code -eq 0) {
    if ((Invoke-GitCapture @('fetch','--quiet','origin',$Branch)).Code -ne 0) { Stop-Release "Could not fetch origin/$Branch." }
    $behind = Invoke-GitCapture @('rev-list','--count',"HEAD..origin/$Branch")
    if ($behind.Code -ne 0 -or (($behind.Output -join '').Trim()) -ne '0') { Stop-Release "Local branch is behind origin/$Branch. Pull first." }
}

Write-Host ""
Write-Host "Release plan" -ForegroundColor Cyan
Write-Host "  Version: V$Version"
Write-Host "  Branch:  $Branch"
Write-Host "  Message: $Message"

$backups = @{}
foreach ($f in @($SetupFile, $HistoryFile)) {
    if (Test-Path -LiteralPath $f) { $backups[$f] = [System.IO.File]::ReadAllBytes((Join-Path $PSScriptRoot $f)) }
    else { $backups[$f] = $null }
}
$CommitCreated = $false
$TagCreated = $false

try {
    Set-SetupVersion $Version
    Add-History $Version $Message

    Invoke-Git @('add','-A') 'git add failed'
    $staged = @((Invoke-GitCapture @('-c','core.quotepath=false','diff','--cached','--name-only')).Output)
    if ($staged.Count -eq 0) { throw 'No files were staged for release.' }

    Write-Host ""; Write-Host "Staged for release:" -ForegroundColor Cyan
    $staged | ForEach-Object { Write-Host "  $_" }

    $msgFile = [System.IO.Path]::GetTempFileName()
    try {
        [System.IO.File]::WriteAllText($msgFile, "V$Version $Message`n", (New-Object System.Text.UTF8Encoding($false)))
        Invoke-Git @('commit','-F',$msgFile) 'git commit failed'
        $CommitCreated = $true
        [System.IO.File]::WriteAllText($msgFile, "V$Version $Message`n", (New-Object System.Text.UTF8Encoding($false)))
        Invoke-Git @('tag','-a',$Tag,'-F',$msgFile) "git tag '$Tag' failed"
        $TagCreated = $true
    }
    finally { Remove-Item $msgFile -ErrorAction SilentlyContinue }

    Write-Host ""; Write-Host "Pushing branch '$Branch'..." -ForegroundColor Cyan
    Invoke-Git @('push','origin',$Branch) "Commit exists locally, but push of '$Branch' failed."
    Write-Host "Pushing tag '$Tag'..." -ForegroundColor Cyan
    Invoke-Git @('push','origin',$Tag) "Branch pushed, but tag '$Tag' failed to push."

    Write-Host ""; Write-Host "RELEASE COMPLETED: $Tag on $Branch" -ForegroundColor Green
    & git log --oneline -1
}
catch {
    Write-Host ""; Write-Host "RELEASE FAILED: $($_.Exception.Message)" -ForegroundColor Red
    if (-not $CommitCreated) {
        Invoke-GitCapture @('reset','-q') | Out-Null
        foreach ($f in $backups.Keys) {
            if ($null -eq $backups[$f]) { if (Test-Path $f) { Remove-Item $f -Force } }
            else { [System.IO.File]::WriteAllBytes((Join-Path $PSScriptRoot $f), $backups[$f]) }
        }
        Write-Host "Version/history edits were undone." -ForegroundColor Yellow
    }
    else {
        Write-Host "A local release commit exists. Check: git status ; git log --oneline -3" -ForegroundColor Yellow
        Write-Host "To finish manually: git push origin $Branch" -ForegroundColor Yellow
        if ($TagCreated) { Write-Host "Then: git push origin $Tag" -ForegroundColor Yellow }
    }
    exit 1
}