$vms = Get-VM | Sort-Object VMName
Enable-VMResourceMetering $vms
$measure = Measure-VM $vms | Sort-Object VMName
$count = 0
$output = New-Object -TypeName 'System.Object[,]' -ArgumentList $vms.Count, 3
$out = New-Object -TypeName 'System.Object[]' -ArgumentList $vms.Count

foreach ($vmname in $measure.VMName){
    $output[$count, 0] = $vmname
    $traffic = $measure[$count].NetworkMeteredTrafficReport
    foreach ($addr in $traffic){
        if ($addr.Direction -eq "Inbound"){
            $output[$count, 1] += $addr.TotalTraffic
        }
        elseif ($addr.Direction -eq "Outbound"){
            $output[$count, 2] += $addr.TotalTraffic
        }
    }
    $count++
}

for ($i = 0; $i -lt $count; $i++){
    $out[$i] = [PSCustomObject]@{
        "VMName" = $output[$i, 0];
        "Inbound(M)" = $output[$i, 1];
        "Outbound(M)" = $output[$i, 2]
    }
}

$retVal = $out | ConvertTo-Json

$retVal | Out-file OutFiles\netstats.json -Encoding ascii -Force