ZONE=us-east1-b

gcloud compute  instances create nfs \
    --zone=$ZONE \
    --machine-type=n1-standard-1 \
    --image=debian-9-stretch-v20181011 \
    --image-project=debian-cloud \
    --boot-disk-size=10GB \
    --metadata-from-file startup-script=startup-scripts/nfs.sh
