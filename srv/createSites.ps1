# ---------------------------------------------------------------
# file  : createSites.ps1
# author: (c) 2026 Jens Kallup - paule32
# note  : create IIS sites
# ---------------------------------------------------------------
Import-Module WebAdministration

# ---------------------------------------------------------------
# global used variables ...
# ---------------------------------------------------------------
$http_content_dir = "T:\GitHub\dBase2Many\srv"
$phpCgi           = "T:\Programme\PHP_8_5_5\php-cgi.exe"
$win_hosts        = "C:\Windows\System32\drivers\etc\hosts"
#
$certStore        = "Cert:\LocalMachine\My"
$trustedRootStore = "Cert:\LocalMachine\Root"
$caName           = "MeineTestCA"

$serverA = "serverA"
$serverB = "serverB"
$serverC = "serverC"
#
$client1 = "client1"
$client2 = "client2"
$client3 = "client3"

$client1a_host = "client1.servera"
$client2a_host = "client2.servera"
$client3a_host = "client3.servera"
#
$client1b_host = "client1.serverb"
$client2b_host = "client2.serverb"
$client3b_host = "client3.serverb"

$path_1  = ($http_content_dir + "\" + $serverA + "\" + $client1)
$path_2  = ($http_content_dir + "\" + $serverB + "\" + $client2)
$path_3  = ($http_content_dir + "\" + $serverC + "\" + $client3)
#

$prefix_str    = "Python"
$suffix_srva   = "Server A"
$suffix_srvb   = "Server B"

$filter_str    = "system.webServer/fastCgi/application"
$filter_defdoc = "system.webServer/defaultDocument/files"
$filter_errcod = "system.webServer/httpErrors"
$filter_handle = "system.webServer/handlers"
$filter_browse = "system.webServer/directoryBrowse"

$client_1srva  = "${prefix_str} Client1 $suffix_srva"
$client_2srva  = "${prefix_str} Client2 $suffix_srva"
$client_3srva  = "${prefix_str} Client3 $suffix_srva"

$client_1srvb  = "${prefix_str} Client1 $suffix_srvb"
$client_2srvb  = "${prefix_str} Client2 $suffix_srvb"
$client_3srvb  = "${prefix_str} Client3 $suffix_srvb"

$client_1srva_site  = ("IIS:\Sites\" + $client_1srva)
$client_2srva_site  = ("IIS:\Sites\" + $client_2srva)
$client_3srva_site  = ("IIS:\Sites\" + $client_3srva)

$client_1srvb_site  = ("IIS:\Sites\" + $client_1srvb)
$client_2srvb_site  = ("IIS:\Sites\" + $client_2srvb)
$client_3srvb_site  = ("IIS:\Sites\" + $client_3srvb)

$sites = @(
    @{ site = ${client_1srva_site}; name = $client_1srva; path = $path_1; cname = $client1; ip = "192.168.10.12"; host = $client1a_host },
    @{ site = ${client_2srva_site}; name = $client_2srva; path = $path_2; cname = $client2; ip = "192.168.10.14"; host = $client2a_host },
    @{ site = ${client_3srva_site}; name = $client_3srva; path = $path_3; cname = $client3; ip = "192.168.10.16"; host = $client3a_host },
    #
    @{ site = ${client_1srvb_site}; name = $client_1srvb; path = $path_1; cname = $client1; ip = "192.168.10.22"; host = $client1b_host },
    @{ site = ${client_2srvb_site}; name = $client_2srvb; path = $path_2; cname = $client2; ip = "192.168.10.24"; host = $client2b_host },
    @{ site = ${client_3srvb_site}; name = $client_3srvb; path = $path_3; cname = $client3; ip = "192.168.10.26"; host = $client3b_host }
)

# ---------------------------------------------------------------
# helper function to re-create the windows system file:
# C:\windows\system32\drivers\etc\hosts
# ---------------------------------------------------------------
function Check-HostsFile {
    try {
        @"
# -----------------------------------------------------------
# /etc/hosts
# created on 2026-05-01 (c) 2026 Jens Kallup - paule32
# all Rights reserved.
#
# We use this file as an alternative to the big DNS-Server
# that is shiped by Microsoft Windows Server Platform to make
# test cases much easier.
# -----------------------------------------------------------

# -------------------------------------------
# the Standard devices on local machiene
# -------------------------------------------
127.0.0.1 localhost
::1       localhost

# -------------------------------------------
# ipv6 Connection numbers
# -------------------------------------------
fd00::10  servera
fd00::20  serverb
fd00::30  serverc

fd00::12  client1.servera
fd00::14  client2.servera
fd00::16  client3.servera
fd00::18  client4.servera

fd00::22  client1.serverb
fd00::24  client2.serverb
fd00::26  client3.serverb
fd00::28  client4.serverb

fd00::32  client1.serverc
fd00::34  client2.serverc
fd00::36  client3.serverc
fd00::38  client4.serverc

# -------------------------------------------
# ipv4 Connection numbers
# -------------------------------------------
192.168.10.10 servera
192.168.10.20 serverb
192.168.10.30 serverc

192.168.10.12 client1.servera
192.168.10.14 client2.servera
192.168.10.16 client3.servera
192.168.10.18 client4.servera

192.168.10.22 client1.serverb
192.168.10.24 client2.serverb
192.168.10.26 client3.serverb
192.168.10.28 client4.serverb

192.168.10.32 client1.serverc
192.168.10.34 client2.serverc
192.168.10.36 client3.serverc
192.168.10.38 client4.serverc

"@ | Set-Content -Path $win_hosts -Force
        Write-Host "add new hosts to C:\Windows\System32\drivers\etc\hosts"
    }   catch {
        Write-Host "Error: $($_.Exception.Message)"
        return
    }
}

# ---------------------------------------------------------------
# helper function to get the thumbprint of a certificate
# ---------------------------------------------------------------
function Get-CertThumbprint($domain) {
    foreach ($store in @("Cert:\LocalMachine\My", "Cert:\CurrentUser\My")) {
        $cert = Get-ChildItem $store |
            Where-Object {
                $_.Subject -like "*CN=$domain*" -or
               ($_.DnsNameList | ForEach-Object { $_.Unicode }) -contains $domain
            } | Select-Object -First 1
        if ($cert) {
            if ($cert.Thumbprint) {
                return $cert.Thumbprint
            }   else {
                Write-Host "wrong cert"
                return $null
            }
        }
    }
    Write-Host "Error: no cert for: ${domain}."
    return $null
}

# ---------------------------------------------------------------
# helper function to set page errors content ...
# ---------------------------------------------------------------
function Set-IisErrorPages {
    param (
        [string]$PSPath
    )

    $errors = @(
        @{ code = 400; path = "/pageErrors/400.html" },
        @{ code = 403; path = "/pageErrors/403.html" },
        @{ code = 404; path = "/pageErrors/404.html" },
        @{ code = 500; path = "/pageErrors/500.html" }
    )

    foreach ($e in $errors) {
        $entry = Get-WebConfiguration `
            -PSPath $PSPath `
            -Filter "${filter_errcod}/error" |
            Where-Object {
                [int]$_.statusCode    -eq [int]$e.code -and
                [int]$_.subStatusCode -eq -1
            }

        if ($entry) {
            Set-WebConfigurationProperty `
                -PSPath $PSPath `
                -Filter "$filter_errcod/error[@statusCode='$($e.code)' and @subStatusCode='-1']" `
                -Name "path" `
                -Value $e.path

            Set-WebConfigurationProperty `
                -PSPath $PSPath `
                -Filter "$filter_errcod/error[@statusCode='$($e.code)' and @subStatusCode='-1']" `
                -Name "responseMode" `
                -Value "ExecuteURL"
        }
        else {
            Add-WebConfigurationProperty `
                -PSPath $PSPath `
                -Filter $filter_errcod `
                -Name "." `
                -Value @{ statusCode = $e.code; subStatusCode = -1; path = $e.path; responseMode = "ExecuteURL" }
        }
    }
}

# ---------------------------------------------------------------
# pre-tasks: create directories ...
# ---------------------------------------------------------------
function Check-Directories {
    try {
        Write-Host "add new directory: $path_1\pageErrors"
        New-Item -ItemType Directory -Path ($path_1 + "\pageErrors") -Force -ErrorAction Stop | Out-Null
        
        Write-Host "add new directory: $path_2\pageErrors"
        New-Item -ItemType Directory -Path ($path_2 + "\pageErrors") -Force -ErrorAction Stop | Out-Null
        
        Write-Host "add new directory: $path_3\pageErrors"
        New-Item -ItemType Directory -Path ($path_3 + "\pageErrors") -Force -ErrorAction Stop | Out-Null
        #
        Write-Host ""
        #
        Write-Host "add new directory: $path_1\pageLogs"
        New-Item -ItemType Directory -Path ($path_1 + "\pageLogs") -Force -ErrorAction Stop | Out-Null
        
        Write-Host "add new directory: $path_2\pageLogs"
        New-Item -ItemType Directory -Path ($path_2 + "\pageLogs") -Force -ErrorAction Stop | Out-Null
        
        Write-Host "add new directory: $path_3\pageLogs"
        New-Item -ItemType Directory -Path ($path_3 + "\pageLogs") -Force -ErrorAction Stop | Out-Null
        
    }   catch {
        Write-Host "Error: could not create directory: $($_.Exception.Message)"
        return
    }
}

# ---------------------------------------------------------------
# create or reuse root CA in CurrentUser\My
# IMPORTANT:
# The CA certificate must stay in CurrentUser\My because the private
# key is needed for signing. Do NOT Move-Item it away before signing.
# ---------------------------------------------------------------
function Check-CA {
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
    }   else {
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
    # create/reuse one cert per domain
    # ---------------------------------------------------------------
    foreach ($site in $sites) {
        $siteHost = $site.host
        $existing = Get-ChildItem $certStore |
            Where-Object { $_.Subject -eq "CN=${siteHost}" -and $_.Issuer -eq "CN=$caName" } |
            Sort-Object NotAfter -Descending |
            Select-Object -First 1

        if ($existing) {
            Write-Host "Cert exists:  $domain  $($existing.Thumbprint)"
            continue
        }

        $cert = New-SelfSignedCertificate `
            -Type SSLServerAuthentication `
            -DnsName $siteHost `
            -CertStoreLocation $certStore `
            -Signer $rootCert `
            -NotAfter (Get-Date).AddYears(2) `
            -KeyExportPolicy Exportable `
            -HashAlgorithm sha256

        Write-Host "Cert created: $domain  $($cert.Thumbprint)"
    }
}

function Check-WebSites {
    try {
        foreach ($site in $sites) {
            $sitePath = $site.site
            $siteName = $site.name
            $siteHost = $site.host
            $siteIP   = $site.ip
            
            if (test-Path $sitePath) {
                Write-Host ($siteName + " -> exists, will delete...")
                Remove-Website -Name $siteName
                Remove-Item ("IIS:\SslBindings\" + ${siteIP} + "!443!" + ${siteHost}) -ErrorAction SilentlyContinue
            }
        }
    }   catch {
        Write-Host "Error: $($_.Exception.Message)"
        return
    }

    Write-Host ""
    Write-Host "set ipV4, port: 80 ..."
    try {
        foreach ($site in $sites) {
            $siteName = $site.name
            $siteIP   = $site.ip
            $sitePath = $site.path
            $siteHost = $site.host
            
            New-Website -Name $siteName `
                -PhysicalPath $sitePath `
                -IPAddress $siteIP      `
                -Port 80                `
                -HostHeader $siteHost   `
                -Force                  `
                -ErrorAction Stop | Out-Null
            Write-Host "successfully add http  for: ${siteName}"
        }
    }   catch {
        Write-Host "Error: $($_.Exception.Message)"
        return
    }

    Write-Host ""
    Write-Host "set ipV6, port: 443 ..."
    try {
        foreach ($site in $sites) {
            $siteName = $site.name
            $siteIP   = $site.ip
            $siteHost = $site.host
            
            New-WebBinding -Name $siteName  `
                -Protocol "https"           `
                -IPAddress $siteIP          `
                -Port 443                   `
                -HostHeader $siteHost       `
                -ErrorAction Stop
            Write-Host "successfully add https for: ${siteName}"
        }
    }   catch {
        Write-Host "Error: $($_.Exception.Message)"
        return
    }
}

function Check-Handlers {
    #Enable-WindowsOptionalFeature -Online -FeatureName IIS-CGI -All

    $handlerName = "PHP_via_FastCGI"

    Write-Host ""
    try {
        foreach ($site in $sites) {
            $sitePath = $site.site
            $siteName = $site.name
            $siteClnt = $site.host.Replace(".", "_")
            
            $exists = Get-WebConfiguration `
                -PSPath $sitePath `
                -Filter ("${filter_handle}/add") | Where-Object {
                    $_.name -eq "${handlerName}_${siteClnt}"
                }
            if ($exists) {
                Remove-WebConfigurationProperty `
                    -PSPath $sitePath           `
                    -Filter "${filter_handle}"  `
                    -Name "."                   `
                    -AtElement @{ name = "${handlerName}_${siteClnt}" } `
                    -ErrorAction Stop | Out-Null
                Write-Host "del old handler assign for: ${siteName}: ${handlerName}_${siteClnt}"
            }
        }
    }   catch {
        Write-Host "Error: $($_.Exception.Message)"
        return
    }

    Write-Host ""
    try {
        foreach ($site in $sites) {
            $sitePath = $site.site
            $siteName = $site.name
            $siteClnt = $site.host.Replace(".", "_")
            
            $exists = Get-WebConfiguration `
                -PSPath $sitePath `
                -Filter ("${filter_handle}/add") | Where-Object {
                    $_.name -eq "${handlerName}_${siteClnt}"
                }
            if (-not $exists) {
                New-WebHandler          `
                    -PSPath $sitePath   `
                    -Name "${handlerName}_${siteClnt}" `
                    -Path "*.php"       `
                    -Verb "*"           `
                    -Modules "FastCgiModule" `
                    -ScriptProcessor $phpCgi `
                    -ResourceType "Either"
                Write-Host "add new handler assign for: ${siteName}: ${handlerName}_${siteClnt}"
            }
        }
    }   catch {
        Write-Host "Error: $($_.Exception.Message)"
        return
    }
}

# ---------------------------------------------------------------
# remove all default documents, and set new ones .php, and .html
# ---------------------------------------------------------------
function Check-Documents {
    try {
        foreach ($site in $sites) {
            $sitePath = $site.site
            $siteName = $site.name
            
            Clear-WebConfiguration -Filter ${filter_defdoc} -PSPath $sitePath
            Write-Host "clear default documents for: ${siteName}"
        }
    }   catch {
        Write-Host "Error: $($_.Exception.Message)"
        return
    }

    Write-Host ""
    try {
        $docs = @{
        }
        foreach ($site in $sites) {
            $sitePath = $site.site
            $siteName = $site.name

            $exists_php = Get-WebConfiguration -PSPath $sitePath -Filter "${filter_defdoc}/add" | Where-Object { $_.value -ieq "index.php"  }
            $exists_htm = Get-WebConfiguration -PSPath $sitePath -Filter "${filter_defdoc}/add" | Where-Object { $_.value -ieq "index.html" }

            if (-not $exists_php) {
                Add-WebConfiguration        `
                    -Filter $filter_defdoc  `
                    -PSPath $sitePath       `
                    -Value @{ value = "index.php"  }
            }
            if (-not $exists_htm) {
                Add-WebConfiguration        `
                    -Filter $filter_defdoc  `
                    -PSPath $sitePath       `
                    -Value @{ value = "index.html" }
            }
            Write-Host "set default documents for: ${siteName}: index.php, index.html"
        }
    }   catch {
        Write-Host "Error: $($_.Exception.Message)"
        return
    }
}

# ---------------------------------------------------------------
# SSL binding ...
# ---------------------------------------------------------------
function Check-SSLBindings {
    foreach ($site in $sites) {
        $siteHost   = $site.host
        $siteIP     = $site.ip

        $thumbprint = Get-CertThumbprint $siteHost
        
        if ([string]::IsNullOrWhiteSpace($thumbprint)) {
            Write-Host "Error: no cert for: $domain"
            return
        }
        
        $thumbprint = $thumbprint.Replace(" ", "").Trim()
        $sslPath = "IIS:\SslBindings\$siteIP!443!$siteHost"
        
        Write-Host ""
        Write-Host "thumb: $thumbprint"
        Write-Host "path : $sslPath"
        
        if (-not $sslPath) {
            New-Item `
              -Path $sslPath `
              -Thumbprint $thumbprint `
              -SSLFlags 1 `
              -ErrorAction Stop | Out-Null
              
            Write-Host "SSL binding created: $siteHost"
        }   else {
            Write-Host "SSL binding already exists: $siteHost"
        }
    }
}

# ---------------------------------------------------------------
# set website browse file system to true ...
# ---------------------------------------------------------------
function Check-DirectoryBrowse {
    foreach ($site in $sites) {
        $sitePath = $site.site
        $siteHost = $site.host
        
        Set-WebConfigurationProperty `
            -PSPath $sitePath        `
            -Filter $filter_Browse   `
            -Name "enabled"          `
            -Value "True"
        Write-Host "Host: ${siteHost} is browseable, now"
    }
}

# ---------------------------------------------------------------
# set error pages for each domain
# ---------------------------------------------------------------
function Check-ErrorPages {
    Write-Host "del old error code pages settings, please wait..."
    foreach ($site in $sites) {
        $sitePath = $site.site
        Set-IisErrorPages -PSPath $sitePath
    }

    # ---------------------------------------------------------------
    # set new error pages, and content ...
    # ---------------------------------------------------------------
    Write-Host "add new error code pages settings, please wait..."
    foreach ($site in $sites) {
        $sitePath = $site.site
        Set-IisErrorPages -PSPath $sitePath
    }

    Write-Host "add new error code pages content"
    foreach ($site in $sites) {
        $errorPath = Join-Path $site.path "pageErrors"
        New-Item -ItemType Directory -Path $errorPath -Force | Out-Null
        
        foreach ($code in @(400,403,404,500)) {
            Set-Content `
            -Path (Join-Path $errorPath "$code.html") `
            -Value "$code error"
        }
    }
}

function Check-Logging {
    Write-Host "add new page log files, please wait..."
    foreach ($site in $sites) {
        $siteName = $site.name
        $logPath  = Join-Path $site.path "pageLogs"

        New-Item -ItemType Directory -Path $logPath -Force | Out-Null

        Set-ItemProperty "IIS:\Sites\$siteName" `
            -Name "logFile.directory" `
            -Value $logPath

        Set-ItemProperty "IIS:\Sites\$siteName" `
            -Name "logFile.period" `
            -Value "Daily"

        Set-ItemProperty "IIS:\Sites\$siteName" `
            -Name "logFile.localTimeRollover" `
            -Value $true

        Set-ItemProperty "IIS:\Sites\$siteName" `
            -Name "logFile.truncateSize" `
            -Value 8388608

        Set-ItemProperty "IIS:\Sites\$siteName" `
            -Name "logFile.logFormat" `
            -Value "W3C"
    }
}

function Check-InfoPHP {
    Write-Host "add new php info pages content"
    foreach ($site in $sites) {
        $path = $site.path
        Set-Content ($path + "\info.php") "<?php phpinfo(); ?>"
    }
}

function Check-IISInstalled {
    try {
        Import-Module WebAdministration -ErrorAction Stop
        if (Test-Path "IIS:\") {
            return $true
        }
    } catch {
        return $false
    }
    return $false
}

# ---------------------------------------------------------------
# main part -> call structure ...
# ---------------------------------------------------------------
if (Check-IISInstalled) {
    Write-Host "IIS is installed..."
    
    $state = Get-Service W3SVC -ErrorAction SilentlyContinue

    if ($state.Status -eq "Running") {
        Write-Host "IIS is running"
    }   elseif ($state.Status -eq "Stopped") {
        Write-Host "IIS stopped"
    }
    Write-Host ""
    Check-HostsFile         ; Write-Host ""
    Check-CA                ; Write-Host ""
    Check-Directories       ; Write-Host ""
    Check-WebSites          ; Write-Host ""
    Check-Handlers          ; Write-Host ""
    Check-Documents         ; Write-Host ""
    Check-SSLBindings       ; Write-Host ""
    Check-DirectoryBrowse   ; Write-Host ""
    Check-ErrorPages        ; Write-Host ""
    Check-Logging           ; Write-Host ""
    Check-InfoPHP
}   else {
    Write-Host "IIS is NOT installed."
    return
}

# ---------------------------------------------------------------
# re-start IIS ...
# ---------------------------------------------------------------
iisreset

Write-Host "done."
