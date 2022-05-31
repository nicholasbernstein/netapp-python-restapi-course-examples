#!pwsh
 
# prior to running this, you should install powershell-core (7)
# choco install powershell-core
# you can then use the pwsh.exe command to open a powershell 7 command run the script
# or you can use the #!pwsh syntax which seems to work.
# This allows for the much simpler "-SkipCertificateCheck" option
 
 
$header =  @{"accept" = "application/json"; "authorization" = "Basic YWRtaW46TmV0YXBwMSE="}
$uri = "https://cluster2.demo.netapp.com/api/storage/volumes"
$body = '{"name": "vol3", "aggregates": [{"name": "aggr2"}], "nas.path": "/vol3", "size": 100000000, "svm.name": "VServer2"}'
$result = Invoke-RestMethod -SkipCertificateCheck -method POST –uri $uri  –header $header –body $body
$result
$uri = 'https://cluster2.demo.netapp.com/api/storage/volumes/?name=vol1&return_records=true&return_timeout=15'
$result = Invoke-RestMethod –header $header -Method Get -Uri $uri -SkipCertificateCheck
$result
