#!/bin/bash
# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
apt-get update && apt-get install -y wget curl net-tools vm python-pandas python-numpy git
echo "deb http://research.cs.wisc.edu/htcondor/debian/stable/ jessie contrib" >> /etc/apt/sources.list
wget -qO - http://research.cs.wisc.edu/htcondor/debian/HTCondor-Release.gpg.key | apt-key add -
apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y condor=8.4.11~dfsg.1-1
if  dpkg -s condor >& /dev/null; then echo "yes"; else sleep 10; DEBIAN_FRONTEND=noninteractive apt-get install -y condor=8.4.11~dfsg.1-1; fi;

mkdir -p /etc/condor/config.d/

cat <<EOF > condor_config.local
DISCARD_SESSION_KEYRING_ON_STARTUP=False
CONDOR_ADMIN = EMAIL
DAEMON_LIST = MASTER, SCHEDD
CONDOR_HOST = condor-master
ALLOW_READ = *
ALLOW_WRITE = *
UID_DOMAIN = condor-master
TRUST_UID_DOMAIN = TRUE
EOF

mv condor_config.local /etc/condor/config.d/

/etc/init.d/condor start
update-rc.d condor defaults
update-rc.d condor enable

# # gcsfuse
# export GCSFUSE_REPO=gcsfuse-`lsb_release -c -s`
# echo "deb http://packages.cloud.google.com/apt $GCSFUSE_REPO main" | sudo tee /etc/apt/sources.list.d/gcsfuse.list
# curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
# apt-get update
# apt-get install -y gcsfuse
