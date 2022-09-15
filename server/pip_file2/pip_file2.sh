yum update
yum install -y epel-release
yum install -y python3-pip
pip3 install --no-index --find-links="./" -r requirements.txt