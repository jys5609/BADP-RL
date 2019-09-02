source load_parse_yaml.sh
eval $(parse_yaml config.yaml)
GPU_INSTANCE_NAME=gpu-instance
GPU_ZONE=us-east1-c

# preemtible option?
gcloud compute  instances create $GPU_INSTANCE_NAME \
    --zone=$GPU_ZONE \
    --machine-type=n1-standard-4 \
    --accelerator type=nvidia-tesla-k80,count=1 \
    --image-family ubuntu-1604-lts --image-project ubuntu-os-cloud \
    --maintenance-policy TERMINATE --restart-on-failure \
    --preemptible \
    --metadata-from-file startup-script=startup-scripts/gpu.sh \
    --boot-disk-size=20GB \
    --scopes compute-ro,default

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
