param(
    [ValidatePattern('^v[0-9][A-Za-z0-9.+-]*$')]
    [string]$Version = 'v0.13.4-zh.0.1.0-alpha.2'
)
$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path $PSScriptRoot -Parent
Push-Location $repoRoot
try {
    uv sync --frozen --python 3.11 --group build --group dev
    if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed' }
    uv run --no-sync pytest tests/test_chinese_localization.py -q
    if ($LASTEXITCODE -ne 0) { throw 'Chinese locale checks failed' }
    $versionText = "[DEFAULT]`nversion_number=$Version`nrelease_channel=stable`nupstream=KestrelFeather/clangen-zh`n"
    [IO.File]::WriteAllText((Join-Path $repoRoot 'version.ini'), $versionText, [Text.UTF8Encoding]::new($false))
    $previousPath = $env:PATH
    try {
        # Exclude unrelated Python/Qt/Conda DLLs from the build search path.
        $env:PATH = "$(Join-Path $repoRoot '.venv\Scripts');$env:SystemRoot\System32;$env:SystemRoot"
        & .venv/Scripts/python.exe -m PyInstaller --noconfirm --clean ClanGenChinese.spec
        if ($LASTEXITCODE -ne 0) { throw 'PyInstaller build failed' }
    } finally { $env:PATH = $previousPath }
    Copy-Item localization/PREVIEW.zh-CN.md dist/ClanGenChinese/试玩说明.md
    Copy-Item localization/TERMINOLOGY.zh-CN.md dist/ClanGenChinese/术语依据.md
    Copy-Item LICENSE.md dist/ClanGenChinese/LICENSE.md
    Write-Host 'Built dist/ClanGenChinese. Run the frozen smoke checks and review screenshots before publishing.'
} finally { Pop-Location }
