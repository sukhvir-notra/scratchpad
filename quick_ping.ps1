Write-Host "`n`n**** WARNING : Running a ping sweep will produce a lot of noice on your network. Please advice CPT members before commencing to avoid blue on blue ****`n`n" -ForegroundColor Red

[string]$range=Read-Host -Prompt "Provide the first three octets of the IP range"
[int]$start=Read-Host -Prompt "What is the starting address?"
[int]$end=Read-Host -Prompt "What is the last address?"

$timestamp=$(((get-date).ToUniversalTime()).ToString("yyyyMMdd_hh_mm_ss_Z"))
mkdir $timestamp -ErrorAction SilentlyContinue
cd $timestamp
$pwd=(pwd).Path

$total=0
$joblist = @(256)

while($start -le $end){
    $ip=[string]$start
    $job=Test-Connection -ComputerName "$range.$ip" -count 1 -AsJob
    $joblist+=$job
    $start+=1
}

Start-Sleep -Seconds 2

for($i=0;$i -le $joblist.Count;$i++){
    if($joblist[$i].state -eq "Completed"){
        $results = Receive-Job -Job $joblist[$i] -Keep
        if($results.statuscode -eq 0){
            $address=$results.Address
            if($results.ResponseTimeToLive -eq 128){
                Write-Output "$address - Windows" >> "$pwd\Windows_$timestamp.txt"
            }elseif($results.ResponseTimeToLive -eq 64){
                Write-Output "$address - Linux/Unix" >> "$pwd\Linux_$timestamp.txt"
            }elseif($results.ResponseTimeToLive -eq 254){
                Write-Output "$address - Layer 3 device" >> "$pwd\layer3_$timestamp.txt"
            }
            Write-Output $address >> "$pwd\live_hosts_$timestamp.txt"
            $total+=1
        }
    }
}

write-host "`n$total hosts found" -ForegroundColor Green
stop-job *
Remove-Job *