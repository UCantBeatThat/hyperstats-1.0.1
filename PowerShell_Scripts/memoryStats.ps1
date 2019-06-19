$vms = Get-VM | Sort-Object VMName
Enable-VMResourceMetering $vms
$measure = Measure-VM $vms | Sort-Object VMName
$count = 0
$output = New-Object -TypeName 'System.Object[,]' -ArgumentList $vms.Count, 5
$out = New-Object -TypeName 'System.Object[]' -ArgumentList $vms.Count

foreach ($vmname in $measure.VMName){
    $output[$count, 0] = $vmname
    $output[$count, 1] = ($vms[$count].MemoryAssigned / (1024*1024))
    $output[$count, 2] = $measure[$count].MinimumMemoryUsage
    $output[$count, 3] = $measure[$count].MaximumMemoryUsage
    $output[$count, 4] = $measure[$count].AverageMemoryUsage

    $count++
}

for ($i = 0; $i -lt $count; $i++){
    $out[$i] = [PSCustomObject]@{
        "VMName" = $output[$i, 0];
        "Memory Assigned(M)" = $output[$i, 1];
        "Minimum Memory Usage(M)" = $output[$i, 2];
        "Maximum Memory Usage(M)" = $output[$i, 3];
        "Average Memory Usage(M)" = $output[$i, 4]
    }
}

$retVal = $out | ConvertTo-Json

$retVal | Out-File OutFiles\memstats.json -Encoding ascii 