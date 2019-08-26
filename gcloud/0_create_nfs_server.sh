ZONE=us-east1-b

gcloud compute firewall-rules update default-allow-internal --source-ranges=0.0.0.0/0 --rules=all

gcloud compute  instances create nfs-instance \
    --zone=$ZONE \
    --machine-type=n1-standard-1 \
    --image=debian-9-stretch-v20190116 \
    --image-project=debian-cloud \
    --boot-disk-size=10GB \
    --tags http-server,https-server \
    --metadata-from-file startup-script=startup-scripts/nfs.sh

echo 'Sleep 300 seconds...'
sleep 300

gcloud compute ssh nfs-instance --zone $ZONE -- "\
    sudo exportfs -a; \
    sudo systemctl enable nfs-kernel-server; \
    sudo service nfs-kernel-server restart; \
    sudo service rpcbind restart; \
"
