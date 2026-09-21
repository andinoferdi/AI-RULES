param(
    [string]$ReleaseBaseUrl = $env:AI_RULES_RELEASE_BASE_URL,
    [string]$InstallDir = "$env:LOCALAPPDATA\AI-RULES\bin"
)
$ErrorActionPreference = "Stop"
if ([string]::IsNullOrWhiteSpace($ReleaseBaseUrl)) {
    throw "Set AI_RULES_RELEASE_BASE_URL to the release directory before bootstrapping."
}
$arch = if ([Environment]::Is64BitOperatingSystem) { "x64" } else { "x86" }
$asset = "ai-rules-windows-$arch.exe"
$target = Join-Path $InstallDir "ai-rules.exe"
$manifestUrl = "$ReleaseBaseUrl/release-manifest.json"
$checksumUrl = "$ReleaseBaseUrl/SHA256SUMS"
$temp = Join-Path ([IO.Path]::GetTempPath()) ("ai-rules-bootstrap-" + [guid]::NewGuid())
New-Item -ItemType Directory -Path $temp | Out-Null
try {
    Invoke-WebRequest -Uri "$ReleaseBaseUrl/$asset" -OutFile (Join-Path $temp $asset)
    Invoke-WebRequest -Uri $manifestUrl -OutFile (Join-Path $temp "release-manifest.json")
    Invoke-WebRequest -Uri $checksumUrl -OutFile (Join-Path $temp "SHA256SUMS")
    $expected = (Select-String -Path (Join-Path $temp "SHA256SUMS") -Pattern ([regex]::Escape($asset))).Line.Split()[0]
    $actual = (Get-FileHash -Algorithm SHA256 (Join-Path $temp $asset)).Hash.ToLowerInvariant()
    if ($actual -ne $expected.ToLowerInvariant()) { throw "checksum verification failed for $asset" }
    New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null
    Move-Item -Force (Join-Path $temp $asset) $target
    & $target setup @args
} finally {
    if (Test-Path -LiteralPath $temp) { Remove-Item -LiteralPath $temp -Recurse -Force }
}
