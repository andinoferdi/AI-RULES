# Install or update skripsi-skill locally across Codex, Claude Code, OpenCode, and Antigravity.
# Canonical copy: $HOME\.agents\skills\skripsi-skill
# Junctions: $HOME\.claude\skills, $HOME\.config\opencode\skills, $HOME\.gemini\config\skills, $HOME\.gemini\antigravity-cli\skills

$ErrorActionPreference = "Stop"

$CanonicalPath = Join-Path $HOME ".agents\skills\skripsi-skill"
$RepoUrl = "https://github.com/andinoferdi/AI-RULES.git"
$Branch = "skripsi-skill"

# 1. Canonical setup / update
if (Test-Path $CanonicalPath) {
    Write-Host "Updating existing canonical skripsi-skill at $CanonicalPath..."
    git -C $CanonicalPath fetch origin $Branch
    git -C $CanonicalPath checkout $Branch
    git -C $CanonicalPath pull --ff-only origin $Branch
} else {
    Write-Host "Cloning canonical skripsi-skill to $CanonicalPath..."
    New-Item -ItemType Directory -Force (Split-Path $CanonicalPath) | Out-Null
    git clone --single-branch --branch $Branch $RepoUrl $CanonicalPath
}

# 2. Junction targets
$JunctionTargets = @(
    (Join-Path $HOME ".claude\skills\skripsi-skill"),
    (Join-Path $HOME ".config\opencode\skills\skripsi-skill"),
    (Join-Path $HOME ".gemini\config\skills\skripsi-skill"),
    (Join-Path $HOME ".gemini\antigravity-cli\skills\skripsi-skill")
)

foreach ($Target in $JunctionTargets) {
    $ParentDir = Split-Path $Target
    New-Item -ItemType Directory -Force $ParentDir | Out-Null
    if (-not (Test-Path $Target)) {
        Write-Host "Creating junction at $Target -> $CanonicalPath"
        New-Item -ItemType Junction -Path $Target -Target $CanonicalPath | Out-Null
    } else {
        Write-Host "Junction already exists at $Target"
    }
}

Write-Host "`nskripsi-skill successfully installed/updated for:"
Write-Host "  - Codex:           $CanonicalPath"
Write-Host "  - Claude Code:     $HOME\.claude\skills\skripsi-skill"
Write-Host "  - OpenCode:        $HOME\.config\opencode\skills\skripsi-skill"
Write-Host "  - Antigravity:     $HOME\.gemini\config\skills\skripsi-skill"
