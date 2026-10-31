param(
    [ValidatePattern('^v[0-9][A-Za-z0-9.+-]*$')]
    [string]$Version = 'v0.13.4-zh.0.1.0-alpha.4',
    [switch]$UseExistingEnvironment
)
$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path $PSScriptRoot -Parent
Push-Location $repoRoot
try {
    if (-not $UseExistingEnvironment) {
        uv sync --frozen --python 3.11 --group build --group dev
        if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed' }
    }
    # Existing-environment mode is for the already provisioned locked build venv.
    & .venv/Scripts/python.exe -m pytest tests/test_chinese_localization.py tests/test_name_localization.py tests/test_chinese_profile_health.py tests/test_chinese_management.py tests/test_chinese_clan_admin.py tests/test_lang.py tests/test_pronouns.py -q -p no:cacheprovider --basetemp ".localization-work/pytest-build-$PID"
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
    foreach ($doc in @('NAME-AFFIXES', 'PROFILE-HEALTH', 'MANAGEMENT', 'CLAN-ADMIN')) {
        Copy-Item "localization/$doc.zh-CN.md" "dist/ClanGenChinese/$doc.zh-CN.md"
    }
    Copy-Item LICENSE.md dist/ClanGenChinese/LICENSE.md
    Write-Host 'Built dist/ClanGenChinese. Run the frozen smoke checks and review screenshots before publishing.'
} finally { Pop-Location }
