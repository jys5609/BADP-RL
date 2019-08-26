apt-get update && apt-get install -y wget curl net-tools git nfs-kernel-server nfs-common portmap

echo "rpcbind mountd nfsd statd lockd rquotad : 127.0.0.1 : allow" >> /etc/hosts.allow
echo "rpcbind mountd nfsd statd lockd rquotad : ALL : allow" >> /etc/hosts.allow

mkdir /var/nfsroot
chown nobody:nogroup /var/nfsroot/

echo "/var/nfsroot     *.*.*.*/17(rw,root_squash,subtree_check)" >> /etc/exports
exportfs -ra
systemctl restart nfs-kernel-server
