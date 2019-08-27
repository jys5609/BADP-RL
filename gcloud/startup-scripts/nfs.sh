apt-get update && apt-get install -y wget curl net-tools git nfs-kernel-server nfs-common portmap

mkdir -p /var/nfs-export
chmod o+w /var/nfs-export

echo "rpcbind mountd nfsd statd lockd rquotad : 127.0.0.1 : allow" > /etc/hosts.allow
echo "rpcbind mountd nfsd statd lockd rquotad : ALL : allow" >> /etc/hosts.allow
echo "/var/nfs-export *(rw,sync,no_subtree_check,no_root_squash)" > /etc/exports

exportfs -a
systemctl enable nfs-kernel-server
service nfs-kernel-server restart
service rpcbind restart

echo "Hello world" >> /var/nfs-export/file.txt
