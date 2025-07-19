# Create organized backend directory structure
Write-Host "🗂️ Creating organized backend structure..."

$directories = @(
    "production",
    "experimental", 
    "utils",
    "utils/cleanup",
    "utils/testing", 
    "utils/fixes",
    "deployment",
    "logs",
    "legacy"
)

foreach ($dir in $directories) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "✅ Created: $dir"
    } else {
        Write-Host "⏭️ Already exists: $dir"
    }
}

Write-Host "🎉 Directory structure created!" 