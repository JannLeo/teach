set val(chan) Channel/WirelessChannel;
set val(prop) Propagation/TwoRayGround;
set val(netif) Phy/WirelessPhy;
set val(mac) Mac/802_11;
set val(ifq) Queue/DropTail/PriQueue;
set val(ll) LL;
set val(ant) Antenna/OmniAntenna;
set val(ifqlen) 50;
set val(rp) AODV;
set val(nn) 10;
set val(x) 600;
set val(y) 600;
set val(stop) 1000;

#You do not need the energy level of nodes in your Coursework
set val(energymodel) EnergyModel;
set val(initialenergy) 1000;

set ns [new Simulator]


set tf [open try.tr w]
$ns trace-all $tf

set nf [open try.nam w]
$ns namtrace-all-wireless $nf $val(x) $val(y)

#$ns use-newtrace

set topo [new Topography]
$topo load_flatgrid $val(x) $val(y)

create-god $val(nn)

set chan_1_ [new $val(chan)]

$ns node-config -adhocRouting $val(rp) \
	-llType $val(ll) \
	-macType $val(mac) \
	-ifqType $val(ifq) \
	-ifqLen $val(ifqlen) \
	-antType $val(ant) \
	-propType $val(prop) \
	-phyType $val(netif) \
	-channel $chan_1_ \
	-topoInstance $topo \
	-agentTrace ON \
	-routerTrace ON \
	-macTrace OFF \
	-movementTrace ON \
	-energyModel $val(energymodel) \
	-initialEnergy $val(initialenergy) \
	-rxPower 0.4 \
	-txPower 1.0 \
	-idlePower 0.6 \
	-sleepPower 0.1 \
	-transitionPower 0.4 \
	-transitionTime 0.1


for {set i 0} {$i < $val(nn)} {incr i} { 
	set node_($i) [$ns node]
	$node_($i) set X_ [expr 200 + 250 * cos(2*$i*3.1415926535897/$val(nn))] 
	$node_($i) set Y_ [expr 200 + 250 * sin(2*$i*3.1415926535897/$val(nn))] 
	$node_($i) set Z_ 0.0
}
#$ns duplex-link $node_(5) $node_(2) 2Mb 10ms DropTail

set udp [new Agent/UDP]
#$udp set class_ 1
$ns attach-agent $node_(9) $udp
set null [new Agent/Null]
$ns attach-agent $node_(3) $null
set cbr [new Application/Traffic/CBR]
$cbr attach-agent $udp
$cbr set packetSize_ 512
$cbr set interval_ 0.1
$cbr set rate_ 0.2mb
$ns connect $udp $null
$ns at 0.1 "$cbr start"

 
set tcp [new Agent/TCP]
#$tcp set class_ 2
set sink [new Agent/TCPSink]
$ns attach-agent $node_(4) $tcp
$ns attach-agent $node_(6) $sink
$ns connect $tcp $sink
set ftp [new Application/FTP]
$ftp attach-agent $tcp
$ftp set packetSize_ 512
$ftp set interval_ 0.1
$ftp set rate_ 0.2mb
$ns at 0.1 "$ftp start"



for {set i 0} {$i < $val(nn)} {incr i} {
        $ns initial_node_pos $node_($i) 30
}

for {set i 0} {$i < $val(nn)} {incr i} {
	$ns at $val(stop) "$node_($i) reset";
}

$ns at $val(stop) "$ns nam-end-wireless $val(stop)"
$ns at $val(stop) "finish"
$ns at $val(stop)+0.1  "puts \"end simulation\"; $ns halt"

proc finish {} {
        global ns tf nf
        $ns flush-trace
        close $tf
        close $nf
        exec nam try.nam &
        exit 0
}

puts "CBR packet size = [$cbr set packetSize_]"
puts "CBR interval = [$cbr set interval_]"

$ns run

