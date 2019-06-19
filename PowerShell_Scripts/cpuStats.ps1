$vms = Get-VM | Sort-Object VMName
Enable-VMResourceMetering $vms
$measure = Measure-VM $vms | Sort-Object VMName
$count = 0
$output = New-Object -TypeName 'System.Object[,]' -ArgumentList $vms.Count, 3
$out = New-Object -TypeName 'System.Object[]' -ArgumentList $vms.Count

foreach ($vmname in $measure.VMName){
    $output[$count, 0] = $vmname
    $output[$count, 1] = $vms[$count].CPUUsage
    $output[$count, 2] = $measure[$count].AverageProcessorUsage

    $count++
}

for ($i = 0; $i -lt $count; $i++){
    $out[$i] = [PSCustomObject]@{
        "VMName" = $output[$i, 0];
        "Current CPU Usage(%)" = $output[$i, 1];
        "Average CPU Usage(MHz)" = $output[$i, 2];
    }
}

$retVal = $out | ConvertTo-Json

$retVal | Out-file OutFiles\cpustats.json -Encoding ascii 