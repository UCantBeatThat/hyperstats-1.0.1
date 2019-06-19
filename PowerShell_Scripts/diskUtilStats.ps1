$vms = Get-VM | Sort-Object VMName
Enable-VMResourceMetering $vms
$measure = Measure-VM $vms | Sort-Object VMName
$count = 0
$output = New-Object -TypeName 'System.Object[,]' -ArgumentList $vms.Count, 5
$out = New-Object -TypeName 'System.Object[]' -ArgumentList $vms.Count

foreach ($vmname in $measure.VMName){
    $output[$count, 0] = $vmname
    $output[$count, 1] = $measure[$count].TotalDiskAllocation
    $output[$count, 2] = $measure[$count].AggregatedDiskDataRead
    $output[$count, 3] = $measure[$count].AggregatedDiskDataWritten
    $output[$count, 4] = $measure[$count].AggregatedAverageLatency

    $count++
}

for ($i = 0;$i -lt $count; $i++){
    $out[$i] = [PSCustomObject]@{
        "VMName" = $output[$i, 0];
        "Total Disk Allocated" = $output[$i, 1];
        "Aggregated Disk Data Read" = $output[$i, 2];
        "Aggregated Disk Data Written" = $output[$i, 3];
        "Aggregated Average Latency" = $output[$i, 4]
    }
}

$retVal = $out | ConvertTo-Json

$retVal | Out-file OutFiles\diskstats.json -Encoding ascii 