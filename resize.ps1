#!pwsh
 
# prior to running this, you should install powershell-core (7)
# choco install powershell-core
# you can then use the pwsh.exe command to open a powershell 7 command run the script
# or you can use the #!pwsh syntax which seems to work.
# This allows for the much simpler "-SkipCertificateCheck" option
 
 
$header =  @{"accept" = "application/json"; "authorization" = "Basic YWRtaW46TmV0YXBwMSE="}
# Example, you would get your own uuid from the previous step
$uuid="6632a01e-e09c-11ec-9545-005056950301"
$uri = "https://cluster2.demo.netapp.com/api/storage/volumes/"+$uuid
#Write-Output $uri

$body = '{"name": "vol3",  "size": "400M"}'
$result = Invoke-RestMethod -SkipCertificateCheck -method PATCH –uri $uri  –header $header –body $body
$result

