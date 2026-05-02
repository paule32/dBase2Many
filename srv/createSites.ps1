# ---------------------------------------------------------------
# file  : createSites.ps1
# author: (c) 2026 Jens Kallup - paule32
# note  : create IIS sites
# ---------------------------------------------------------------
Import-Module WebAdministration

# ---------------------------------------------------------------
# pre-tasks: create directories ...
# ---------------------------------------------------------------
$http_content_dir = "T:\GitHub\dBase2Many\srv"
$serverA = "serverA"
$serverB = "serverB"
$serverC = "serverC"
#
$client1 = "client1"
$client2 = "client2"
$client3 = "client3"
#
$path_1  = $http_content_dir + "\" + $serverA + "\" + §client1
$path_2  = $http_content_dir + "\" + $serverB + "\" + §client2
$path_3  = $http_content_dir + "\" + $serverC + "\" + §client3
#
New-Item -ItemType Directory -Path $path_1 -Force
New-Item -ItemType Directory -Path $path_2 -Force
New-Item -ItemType Directory -Path $path_3 -Force

# ---------------------------------------------------------------
# add PHP support per FastCGI ...
# ---------------------------------------------------------------
$phpCgi = "T:\Programme\PHP_8_5_5\php-cgi.exe"

Add-WebConfiguration -Filter "system.webServer/fastCgi" -Value @{ fullPath = $phpCgi }
Enable-WindowsOptionalFeature -Online -FeatureName IIS-CGI -All
New-WebHandler -Name "PHP_via_FastCGI" -Path "*.php" -Verb "*" -Modules "FastCgiModule" -ScriptProcessor $phpCgi -ResourceType "Either"

# ---------------------------------------------------------------
# add sites ...
# ---------------------------------------------------------------
New-WebBinding -Name "Python Client1 Server A" -Protocol "http" -IPAddress "192.168.10.12" -Port 80 -HostHeader "client1.servera"
New-WebBinding -Name "Python Client2 Server A" -Protocol "http" -IPAddress "192.168.10.14" -Port 80 -HostHeader "client1.servera"
New-WebBinding -Name "Python Client3 Server A" -Protocol "http" -IPAddress "192.168.10.16" -Port 80 -HostHeader "client1.servera"

New-WebBinding -Name "Python Client1 Server B" -Protocol "http" -IPAddress "192.168.10.22" -Port 80 -HostHeader "client1.servera"
New-WebBinding -Name "Python Client2 Server B" -Protocol "http" -IPAddress "192.168.10.24" -Port 80 -HostHeader "client1.servera"
New-WebBinding -Name "Python Client3 Server B" -Protocol "http" -IPAddress "192.168.10.26" -Port 80 -HostHeader "client1.servera"

$thumb_A1 = (Get-Item "IIS:\SslBindings\192.168.10.12!443!client1.servera").Thumbprint
$thumb_A2 = (Get-Item "IIS:\SslBindings\192.168.10.14!443!client2.servera").Thumbprint
$thumb_A3 = (Get-Item "IIS:\SslBindings\192.168.10.16!443!client3.servera").Thumbprint

$thumb_B1 = (Get-Item "IIS:\SslBindings\192.168.10.22!443!client1.serverb").Thumbprint
$thumb_B2 = (Get-Item "IIS:\SslBindings\192.168.10.24!443!client2.serverb").Thumbprint
$thumb_B3 = (Get-Item "IIS:\SslBindings\192.168.10.26!443!client3.serverb").Thumbprint

New-Item -Path "IIS:\SslBindings\192.168.10.12!443!client1.servera" -Thumbprint $thumb_A1 -SSLFlags 1
New-Item -Path "IIS:\SslBindings\192.168.10.14!443!client2.servera" -Thumbprint $thumb_A2 -SSLFlags 1
New-Item -Path "IIS:\SslBindings\192.168.10.16!443!client3.servera" -Thumbprint $thumb_A3 -SSLFlags 1

New-Item -Path "IIS:\SslBindings\192.168.10.22!443!client1.serverb" -Thumbprint $thumb_B1 -SSLFlags 1
New-Item -Path "IIS:\SslBindings\192.168.10.24!443!client2.serverb" -Thumbprint $thumb_B2 -SSLFlags 1
New-Item -Path "IIS:\SslBindings\192.168.10.26!443!client3.serverb" -Thumbprint $thumb_B3 -SSLFlags 1

# ---------------------------------------------------------------
# remove all default documents, and set new ones .php, and .html
# ---------------------------------------------------------------
Clear-WebConfiguration -Filter "system.webServer/defaultDocument/files" -PSPath "IIS:\Sites\Python Client1 Server A"
Clear-WebConfiguration -Filter "system.webServer/defaultDocument/files" -PSPath "IIS:\Sites\Python Client2 Server A"
Clear-WebConfiguration -Filter "system.webServer/defaultDocument/files" -PSPath "IIS:\Sites\Python Client3 Server A"
#
Clear-WebConfiguration -Filter "system.webServer/defaultDocument/files" -PSPath "IIS:\Sites\Python Client1 Server B"
Clear-WebConfiguration -Filter "system.webServer/defaultDocument/files" -PSPath "IIS:\Sites\Python Client2 Server B"
Clear-WebConfiguration -Filter "system.webServer/defaultDocument/files" -PSPath "IIS:\Sites\Python Client3 Server B"

Add-WebConfiguration   -Filter "system.webServer/defaultDocument/files" -PSPath "IIS:\Sites\Python Client1 Server A" -Value @{ value = "index.php" }
Add-WebConfiguration   -Filter "system.webServer/defaultDocument/files" -PSPath "IIS:\Sites\Python Client2 Server A" -Value @{ value = "index.php" }
Add-WebConfiguration   -Filter "system.webServer/defaultDocument/files" -PSPath "IIS:\Sites\Python Client3 Server A" -Value @{ value = "index.php" }

Add-WebConfiguration   -Filter "system.webServer/defaultDocument/files" -PSPath "IIS:\Sites\Python Client1 Server B" -Value @{ value = "index.php" }
Add-WebConfiguration   -Filter "system.webServer/defaultDocument/files" -PSPath "IIS:\Sites\Python Client2 Server B" -Value @{ value = "index.php" }
Add-WebConfiguration   -Filter "system.webServer/defaultDocument/files" -PSPath "IIS:\Sites\Python Client3 Server B" -Value @{ value = "index.php" }
#
Add-WebConfiguration   -Filter "system.webServer/defaultDocument/files" -PSPath "IIS:\Sites\Python Client1 Server A" -Value @{ value = "index.html" }
Add-WebConfiguration   -Filter "system.webServer/defaultDocument/files" -PSPath "IIS:\Sites\Python Client2 Server A" -Value @{ value = "index.html" }
Add-WebConfiguration   -Filter "system.webServer/defaultDocument/files" -PSPath "IIS:\Sites\Python Client3 Server A" -Value @{ value = "index.html" }

Add-WebConfiguration   -Filter "system.webServer/defaultDocument/files" -PSPath "IIS:\Sites\Python Client1 Server B" -Value @{ value = "index.html" }
Add-WebConfiguration   -Filter "system.webServer/defaultDocument/files" -PSPath "IIS:\Sites\Python Client2 Server B" -Value @{ value = "index.html" }
Add-WebConfiguration   -Filter "system.webServer/defaultDocument/files" -PSPath "IIS:\Sites\Python Client3 Server B" -Value @{ value = "index.html" }

# ---------------------------------------------------------------
# set website file system to true ...
# ---------------------------------------------------------------
Set-WebConfigurationProperty -PSPath "IIS:\Sites\Python Client1 Server A" -Filter "system.webServer/directoryBrowse" -Name "enabled" -Value "True"
Set-WebConfigurationProperty -PSPath "IIS:\Sites\Python Client2 Server A" -Filter "system.webServer/directoryBrowse" -Name "enabled" -Value "True"
Set-WebConfigurationProperty -PSPath "IIS:\Sites\Python Client3 Server A" -Filter "system.webServer/directoryBrowse" -Name "enabled" -Value "True"

Set-WebConfigurationProperty -PSPath "IIS:\Sites\Python Client1 Server B" -Filter "system.webServer/directoryBrowse" -Name "enabled" -Value "True"
Set-WebConfigurationProperty -PSPath "IIS:\Sites\Python Client2 Server B" -Filter "system.webServer/directoryBrowse" -Name "enabled" -Value "True"
Set-WebConfigurationProperty -PSPath "IIS:\Sites\Python Client3 Server B" -Filter "system.webServer/directoryBrowse" -Name "enabled" -Value "True"

# ---------------------------------------------------------------
# set error pages for each domain
# ---------------------------------------------------------------
$errors = @(
    @{ code = 400; path = "/errors/400.html" },
    @{ code = 403; path = "/errors/403.html" },
    @{ code = 404; path = "/errors/404.html" },
    @{ code = 500; path = "/errors/500.html" }
)
foreach ($e in $errors) {
    Remove-WebConfigurationProperty -PSPath "IIS:\Sites\Python Client1 Server A" -Filter "system.webServer/httpErrors" -Name "." -AtElement @{ statusCode = $e.code } -ErrorAction SilentlyContinue
    Remove-WebConfigurationProperty -PSPath "IIS:\Sites\Python Client2 Server A" -Filter "system.webServer/httpErrors" -Name "." -AtElement @{ statusCode = $e.code } -ErrorAction SilentlyContinue
    Remove-WebConfigurationProperty -PSPath "IIS:\Sites\Python Client3 Server A" -Filter "system.webServer/httpErrors" -Name "." -AtElement @{ statusCode = $e.code } -ErrorAction SilentlyContinue
    
    Remove-WebConfigurationProperty -PSPath "IIS:\Sites\Python Client1 Server B" -Filter "system.webServer/httpErrors" -Name "." -AtElement @{ statusCode = $e.code } -ErrorAction SilentlyContinue
    Remove-WebConfigurationProperty -PSPath "IIS:\Sites\Python Client2 Server B" -Filter "system.webServer/httpErrors" -Name "." -AtElement @{ statusCode = $e.code } -ErrorAction SilentlyContinue
    Remove-WebConfigurationProperty -PSPath "IIS:\Sites\Python Client3 Server B" -Filter "system.webServer/httpErrors" -Name "." -AtElement @{ statusCode = $e.code } -ErrorAction SilentlyContinue
    
    Add-WebConfigurationProperty    -PSPath "IIS:\Sites\Python Client1 Server A" -Filter "system.webServer/httpErrors" -Name "." -Value @{ statusCode = $e.code path = $e.path responseMode = "ExecuteURL"}
    Add-WebConfigurationProperty    -PSPath "IIS:\Sites\Python Client2 Server A" -Filter "system.webServer/httpErrors" -Name "." -Value @{ statusCode = $e.code path = $e.path responseMode = "ExecuteURL"}
    Add-WebConfigurationProperty    -PSPath "IIS:\Sites\Python Client3 Server A" -Filter "system.webServer/httpErrors" -Name "." -Value @{ statusCode = $e.code path = $e.path responseMode = "ExecuteURL"}
    
    Add-WebConfigurationProperty    -PSPath "IIS:\Sites\Python Client1 Server B" -Filter "system.webServer/httpErrors" -Name "." -Value @{ statusCode = $e.code path = $e.path responseMode = "ExecuteURL"}
    Add-WebConfigurationProperty    -PSPath "IIS:\Sites\Python Client2 Server B" -Filter "system.webServer/httpErrors" -Name "." -Value @{ statusCode = $e.code path = $e.path responseMode = "ExecuteURL"}
    Add-WebConfigurationProperty    -PSPath "IIS:\Sites\Python Client3 Server B" -Filter "system.webServer/httpErrors" -Name "." -Value @{ statusCode = $e.code path = $e.path responseMode = "ExecuteURL"}
}

# ---------------------------------------------------------------
# set new content ...
# ---------------------------------------------------------------
Set-Content $path_1 + "\info.php" "<?php phpinfo(); ?>"
Set-Content $path_2 + "\info.php" "<?php phpinfo(); ?>"
Set-Content $path_3 + "\info.php" "<?php phpinfo(); ?>"

# ---------------------------------------------------------------
# re-start IIS ...
# ---------------------------------------------------------------
iisreset
