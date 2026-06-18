$ROOT = "D:\Project_Lighthouse"

$OUTFILE = Join-Path $ROOT "project_inventory.txt"

if (Test-Path $OUTFILE) {
    Remove-Item $OUTFILE
}

"PROJECT INVENTORY SNAPSHOT" | Out-File $OUTFILE
"Generated: $(Get-Date)" | Out-File $OUTFILE -Append
"" | Out-File $OUTFILE -Append

"========================================" | Out-File $OUTFILE -Append
"FOLDER STRUCTURE" | Out-File $OUTFILE -Append
"========================================" | Out-File $OUTFILE -Append

tree $ROOT /F | Out-File $OUTFILE -Append

"" | Out-File $OUTFILE -Append
"========================================" | Out-File $OUTFILE -Append
"FILE INVENTORY" | Out-File $OUTFILE -Append
"========================================" | Out-File $OUTFILE -Append

Get-ChildItem $ROOT -Recurse -File |
Select-Object `
    FullName,
    Length,
    LastWriteTime |
Format-Table -AutoSize |
Out-String |
Out-File $OUTFILE -Append

Write-Host "Created:"
Write-Host $OUTFILE