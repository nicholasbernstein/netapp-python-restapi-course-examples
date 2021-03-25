python3.7 rest.py   -c cluster1 -v Vol1 -vs VServer1 -a aggr1 -n cluster1-01 -d 5 -s 30000000 -u admin -p Netapp1!

python3.7 volume.py -c cluster1 -v Vol2 -vs VServer1 -a aggr1 -ma aggr2 -rs 40000000 -s 30000000 -u admin -p Netapp1!

python3.7 snap.py -c cluster1 -v Vol1 -vs VServer1 -s Snap1 -sp SnapPolicy1 -sc NewWeek -u admin -p Netapp1!
-------------------------------------------------------
python3.7 qtree.py -c cluster1 -v Vol1 -vs VServer1 -q QTree1 -qos QoS_Policy1 -sh 1000000 -fh 1000 -un admin -u admin -p Netapp1!
-------------------------------------------------------------------
python3.7 cifs.py -c cluster1 -n cluster1-01 -a aggr1_cluster1_01_data -vs nas_svm_02 -v nas_svm_02_cifs_02 -ip 192.168.0.210 -nm 255.255.255.0 -g 192.168.0.1 -d demo.netapp.com -s 192.168.0.253 -se nas_svm_02 -sh share_02 -pa /nas_svm_02_cifs_02 -u admin -p Netapp1!
---------------------------------------------------------------------
python3.7 nfs.py -c cluster1 -n cluster1-01 -a aggr1_cluster1_01_data -vs nas_svm_03 -v nas_svm_03_nfs_03 -ip 192.168.0.215 -nm 255.255.255.0 -g 192.168.0.1 -d demo.netapp.com -s 192.168.0.253 -se nas_svm_03 -sh /nas_svm_03_nfs_03 -u admin -p Netapp1!
---------------------------------------------------------
