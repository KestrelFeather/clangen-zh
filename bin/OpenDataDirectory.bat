@echo off
if defined CLANGEN_ZH_DATA_DIR (
    start "" "%CLANGEN_ZH_DATA_DIR%"
) else (
    start "" "%LocalAppData%\KestrelFeather\ClanGenChinese"
)
