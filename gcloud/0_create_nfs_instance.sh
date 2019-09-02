ZONE=us-east1-b

echo 'Update default-allow-internal firewall rule (source-ranges=0.0.0.0/0) ...'
gcloud compute firewall-rules update default-allow-internal --source-ranges=0.0.0.0/0 --rules=all

gcloud compute  instances create nfs-instance \
    --zone=$ZONE \
    --machine-type=n1-standard-1 \
    --image=debian-9-stretch-v20190124 \
    --image-project=debian-cloud \
    --boot-disk-size=10GB \
    --tags http-server,https-server \
    --deletion-protection \
    --metadata-from-file startup-script=startup-scripts/nfs.sh \
    --scopes compute-ro,default

gcloud compute  instances create example \
    --zone=$ZONE \
    --machine-type=n1-standard-1 \
    --image=debian-9-stretch-v20190124 \
    --image-project=debian-cloud \
    --boot-disk-size=10GB \
    --tags http-server,https-server \
    --metadata startup-script="apt-get update && apt-get install -y wget curl git nfs-common" \
    --scopes compute-ro,default

echo 'Sleep 180 seconds...'
sleep 180

gcloud compute ssh nfs-instance --zone $ZONE -- "\
    sudo exportfs -a; \
    sudo systemctl enable nfs-kernel-server; \
    sudo service nfs-kernel-server restart; \
    sudo service rpcbind restart; \
"

echo 'Sleep 30 seconds...'
sleep 30

echo 'NFS connection test...'
NFS_IP=`gcloud compute instances describe nfs-instance --zone=$ZONE --format='get(networkInterfaces[0].networkIP)'`
gcloud compute ssh example --zone $ZONE -- "\
    sudo apt-get install -y nfs-common; \
    sudo mkdir -p /mnt/nfs; \
    sudo mount -t nfs $NFS_IP:/var/nfs-export /mnt/nfs/; \
    sudo chmod o+w /mnt/nfs/; \
    echo \"$NFS_IP:/var/nfs-export /mnt/nfs/ nfs\" | sudo tee -a /etc/fstab; \
"
