# ---------------------------------------------------------------
# file  : createCA.ps1
# author: (c) 2026 Jens Kallup - paule32
# note  : create root CA and one certificate per domain
# ---------------------------------------------------------------

$ErrorActionPreference = "Stop"

$caName = "MeineTestCA"
$certStore = "Cert:\CurrentUser\My"
$trustedRootStore = "Cert:\CurrentUser\Root"

# ---------------------------------------------------------------
# create or reuse root CA in CurrentUser\My
# IMPORTANT:
# The CA certificate must stay in CurrentUser\My because the private
# key is needed for signing. Do NOT Move-Item it away before signing.
# ---------------------------------------------------------------
$rootCert = Get-ChildItem $certStore |
    Where-Object { $_.Subject -eq "CN=$caName" -and $_.HasPrivateKey } |
    Sort-Object NotAfter -Descending |
    Select-Object -First 1

if (-not $rootCert) {
    $rootCert = New-SelfSignedCertificate `
        -Type Custom `
        -KeyUsage CertSign, CRLSign, DigitalSignature `
        -Subject "CN=$caName" `
        -KeyLength 2048 `
        -CertStoreLocation $certStore `
        -NotAfter (Get-Date).AddYears(5) `
        -KeyExportPolicy Exportable `
        -HashAlgorithm sha256

    Write-Host "Root CA created: $($rootCert.Thumbprint)"
} else {
    Write-Host "Root CA reused:  $($rootCert.Thumbprint)"
}

# ---------------------------------------------------------------
# trust root CA: copy public certificate to Trusted Root store
# ---------------------------------------------------------------
$trustedRoot = Get-ChildItem $trustedRootStore |
    Where-Object { $_.Thumbprint -eq $rootCert.Thumbprint } |
    Select-Object -First 1

if (-not $trustedRoot) {
    $tmpCaFile = Join-Path $env:TEMP "$caName.cer"
    Export-Certificate -Cert $rootCert -FilePath $tmpCaFile | Out-Null
    Import-Certificate -FilePath $tmpCaFile -CertStoreLocation $trustedRootStore | Out-Null
    Remove-Item $tmpCaFile -Force
    Write-Host "Root CA copied to Trusted Root store."
} else {
    Write-Host "Root CA already trusted."
}

# ---------------------------------------------------------------
# domains
# ---------------------------------------------------------------
$domains = @(
    "servera",
    "client1.servera",
    "client2.servera",
    "client3.servera",

    "serverb",
    "client1.serverb",
    "client2.serverb",
    "client3.serverb",

    "serverc",
    "client1.serverc",
    "client2.serverc",
    "client3.serverc"
)

# ---------------------------------------------------------------
# create/reuse one cert per domain
# ---------------------------------------------------------------
foreach ($domain in $domains) {
    $existing = Get-ChildItem $certStore |
        Where-Object { $_.Subject -eq "CN=$domain" -and $_.Issuer -eq "CN=$caName" } |
        Sort-Object NotAfter -Descending |
        Select-Object -First 1

    if ($existing) {
        Write-Host "Cert exists:  $domain  $($existing.Thumbprint)"
        continue
    }

    $cert = New-SelfSignedCertificate `
        -Type SSLServerAuthentication `
        -DnsName $domain `
        -CertStoreLocation $certStore `
        -Signer $rootCert `
        -NotAfter (Get-Date).AddYears(2) `
        -KeyExportPolicy Exportable `
        -HashAlgorithm sha256

    Write-Host "Cert created: $domain  $($cert.Thumbprint)"
}

Write-Host "Done."
