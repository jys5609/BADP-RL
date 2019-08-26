ZONE=us-east1-b

function create_instance(){
    gcloud compute  instances create $1-template \
        --zone=$ZONE \
        --machine-type=n1-standard-1 \
        --image=debian-9-stretch-v20181011 \
        --image-project=debian-cloud \
        --boot-disk-size=10GB \
        --metadata-from-file startup-script=startup-scripts/$1.sh
}

function install_custom_packages(){
    # Insatll custom packages
    gcloud compute ssh $1-template --zone $ZONE -- '\
	    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh; \
	    bash Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda; \
	    rm Miniconda3-latest-Linux-x86_64.sh; \
	    eval "$($HOME/miniconda/bin/conda shell.bash hook)"; \
	    conda init; \
	    git clone https://github.com/jys5609/BAMCP_negotiation.git; \
        cd BAMCP_negotiation; \
        conda env create -f environment.yml; \
    '
}

function stop_instance(){
    gcloud compute instances stop --zone=$ZONE $1-template
}

function create_image(){
    gcloud compute images create $1 \
	     --source-disk $1-template \
	     --source-disk-zone $ZONE \
	     --family htcondor-debian
}

function delete_instance(){
    gcloud compute instances delete --quiet --zone=$ZONE $1-template
}

create_instance condor-compute
create_instance condor-submit
create_instance condor-master

echo 'Sleep for a while... (30 seconds)'
sleep 30

echo 'Install custom packages...'
install_custom_packages condor-compute
install_custom_packages condor-submit

echo 'Stop instances...'
stop_instance condor-master
stop_instance condor-compute
stop_instance condor-submit

echo 'Create images...'
create_image condor-master
create_image condor-compute
create_image condor-submit

echo 'Delete instances...'
delete_instance condor-master
delete_instance condor-compute
delete_instance condor-submit