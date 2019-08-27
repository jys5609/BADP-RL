ZONE=us-east1-b

gcloud compute firewall-rules update default-allow-internal --source-ranges=0.0.0.0/0 --rules=all

gcloud compute  instances create nfs-instance \
    --zone=$ZONE \
    --machine-type=n1-standard-1 \
    --image=debian-9-stretch-v20190124 \
    --image-project=debian-cloud \
    --boot-disk-size=10GB \
    --tags http-server,https-server \
    --deletion-protection \
    --metadata-from-file startup-script=startup-scripts/nfs.sh

gcloud compute  instances create example \
    --zone=$ZONE \
    --machine-type=n1-standard-1 \
    --image=debian-9-stretch-v20190124 \
    --image-project=debian-cloud \
    --boot-disk-size=10GB \
    --tags http-server,https-server \
    --metadata startup-script="apt-get update && apt-get install -y wget curl git nfs-common"

echo 'Sleep 300 seconds...'
sleep 300

gcloud compute ssh nfs-instance --zone $ZONE -- "\
    sudo exportfs -a; \
    sudo systemctl enable nfs-kernel-server; \
    sudo service nfs-kernel-server restart; \
    sudo service rpcbind restart; \
"

echo 'NFS connection test...'
NFS_IP=`gcloud compute instances describe nfs-instance --zone=$ZONE --format='get(networkInterfaces[0].networkIP)'`
gcloud compute ssh example --zone $ZONE -- "\
    sudo apt-get install -y nfs-common; \
    sudo mkdir -p /mnt/nfs; \
    sudo mount -t nfs $NFS_IP:/var/nfs-export /mnt/nfs/; \
    sudo chmod o+w /mnt/nfs/; \
    echo \"$NFS_IP:/var/nfs-export /mnt/nfs/ nfs\" | sudo tee -a /etc/fstab; \
"
