$ROOT = "D:\Project_Lighthouse"

$OUTFILE = Join-Path $ROOT "project_source_dump.txt"

if (Test-Path $OUTFILE) {
    Remove-Item $OUTFILE
}

"PROJECT SOURCE DUMP" | Out-File $OUTFILE
"Generated: $(Get-Date)" | Out-File $OUTFILE -Append
"" | Out-File $OUTFILE -Append

$extensions = @(
    "*.py",
    "*.ipynb",
    "*.yaml",
    "*.yml",
    ".env"
)

Get-ChildItem `
    -Path $ROOT `
    -Recurse `
    -File |
Where-Object {

    $_.FullName -notmatch "\\\.venv\\" -and
    $_.FullName -notmatch "\\\.git\\" -and
    $_.FullName -notmatch "__pycache__" -and
    $_.FullName -notmatch "\\\.ipynb_checkpoints\\" -and
    (
        $_.Extension -in @(
            ".py",
            ".ipynb",
            ".yaml",
            ".yml"
        ) -or
        $_.Name -eq ".env"
    )
} |
ForEach-Object {

    "" | Out-File $OUTFILE -Append
    "============================================================" | Out-File $OUTFILE -Append
    "FILE: $($_.FullName)" | Out-File $OUTFILE -Append
    "============================================================" | Out-File $OUTFILE -Append
    "" | Out-File $OUTFILE -Append

    Get-Content $_.FullName |
    Out-File $OUTFILE -Append
}

Write-Host ""
Write-Host "Created:"
Write-Host $OUTFILE