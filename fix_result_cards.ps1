# Fix all fraud detection pages
$pages = @(
    "brand_abuse.html",
    "click_fraud.html",
    "credit_card.html",
    "document_forgery.html",
    "fake_news.html",
    "fake_profile.html",
    "insurance_fraud.html",
    "loan_default.html",
    "phishing_url.html",
    "spam_email.html",
    "upi_fraud.html"
)

$fixedCount = 0

foreach ($page in $pages) {
    $path = "templates\$page"
    
    if (-not (Test-Path $path)) {
        Write-Host "⚠️  $page - File not found" -ForegroundColor Yellow
        continue
    }
    
    $content = Get-Content $path -Raw
    
    # Remove inline style if exists
    $newContent = $content -replace '<div class="result-card" id="resultCard" style="display: none;">', '<div class="result-card" id="resultCard">'
    
    # Add JavaScript to hide on page load if not already present
    if ($newContent -notmatch 'DOMContentLoaded.*resultCard') {
        $newContent = $newContent -replace '(<script>)', @'
$1
        // Ensure result card is hidden on page load
        document.addEventListener("DOMContentLoaded", function() {
            const resultCard = document.getElementById("resultCard");
            if (resultCard) {
                resultCard.style.display = "none";
            }
        });
        
'@
    }
    
    if ($newContent -ne $content) {
        $newContent | Set-Content $path -NoNewline
        Write-Host "✅ $page - Fixed" -ForegroundColor Green
        $fixedCount++
    } else {
        Write-Host "⏭️  $page - Already fixed" -ForegroundColor Cyan
    }
}

Write-Host "`n============================================================" -ForegroundColor White
Write-Host "🎉 Fixed $fixedCount out of $($pages.Count) files" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor White
