source load_parse_yaml.sh
eval $(parse_yaml config.yaml)
GPU_INSTANCE_NAME=gpu-instance
GPU_ZONE=us-east1-c
NFS_ZONE=us-east1-b
USER=`whoami`
NFS_IP=`gcloud compute instances describe nfs-instance --zone=$NFS_ZONE --format='get(networkInterfaces[0].networkIP)'`

# preemtible option?
gcloud compute  instances create $GPU_INSTANCE_NAME \
    --zone=$GPU_ZONE \
    --machine-type=n1-standard-4 \
    --accelerator type=nvidia-tesla-p100,count=1 \
    --image-family ubuntu-1604-lts --image-project ubuntu-os-cloud \
    --maintenance-policy TERMINATE --restart-on-failure \
    --preemptible \
    --boot-disk-size=20GB \
    --scopes compute-ro,default \
    --metadata startup-script="#! /bin/bash
userdel -r ubuntu
groupdel ubuntu
groupmod -g 1000 google-sudoers
usermod -u 1000 $USER
groupmod -g 1001 $USER

sudo apt-get install -y nfs-common; \
sudo mkdir -p /mnt/nfs; \
sudo mount -t nfs $NFS_IP:/var/nfs-export /mnt/nfs/; \
sudo chmod o+w /mnt/nfs/; \
echo \"$NFS_IP:/var/nfs-export /mnt/nfs/ nfs\" | sudo tee -a /etc/fstab; \

echo \"Checking for CUDA and installing.\"
# Check for CUDA and try to install.
if ! dpkg-query -W cuda-10-0; then
    curl -O http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/cuda-repo-ubuntu1604_10.0.130-1_amd64.deb
    dpkg -i ./cuda-repo-ubuntu1604_10.0.130-1_amd64.deb
    apt-key adv --fetch-keys http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/7fa2af80.pub
    apt-get update
    apt-get install cuda-10-0 -y
fi
"

echo 'Sleep 700 seconds...'
sleep 700

echo 'install anaconda...'
gcloud compute ssh $GPU_INSTANCE_NAME --zone $GPU_ZONE -- "
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh;
    bash Miniconda3-latest-Linux-x86_64.sh -b -p \$HOME/miniconda;
    rm Miniconda3-latest-Linux-x86_64.sh;
    eval \"\$(\$HOME/miniconda/bin/conda shell.bash hook)\";
    conda init;
    git clone https://$GITHUB_USERNAME:$GITHUB_PASSWORD@github.com/jys5609/BAMCP_negotiation.git;
    cd BAMCP_negotiation;
    conda env create -f environment.yml;
    cd \$HOME; rm BAMCP_negotiation -rf;
"
