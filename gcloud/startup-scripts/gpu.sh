#!/bin/bash
NFS_ZONE=us-east1-b

userdel -r ubuntu
groupdel ubuntu
groupmod -g 1000 google-sudoers
usermod -u 1000 starjongmin
groupmod -g 1001 starjongmin

NFS_IP=`gcloud compute instances describe nfs-instance --zone=$NFS_ZONE --format='get(networkInterfaces[0].networkIP)'`
sudo apt-get install -y nfs-common; \
sudo mkdir -p /mnt/nfs; \
sudo mount -t nfs $NFS_IP:/var/nfs-export /mnt/nfs/; \
sudo chmod o+w /mnt/nfs/; \
echo \"$NFS_IP:/var/nfs-export /mnt/nfs/ nfs\" | sudo tee -a /etc/fstab; \

echo "Checking for CUDA and installing."
# Check for CUDA and try to install.
if ! dpkg-query -W cuda-10-0; then
    curl -O http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/cuda-repo-ubuntu1604_10.0.130-1_amd64.deb
    dpkg -i ./cuda-repo-ubuntu1604_10.0.130-1_amd64.deb
    apt-key adv --fetch-keys http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/7fa2af80.pub
    apt-get update
    apt-get install cuda-10-0 -y
fi
