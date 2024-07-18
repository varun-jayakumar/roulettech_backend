#!/bin/bash

# Check if the correct number of arguments are provided
# if [ "$#" -ne 2 ]; then
#     echo "Usage: $0 path_to_private_key public_ip_of_ec2"
#     exit 1
# fi

# Assign command line arguments to variables
PRIVATE_KEY="path/to/your/private-key.pem"
PUBLIC_IP="<your-ec2-public-ip>"

# Install Docker on the EC2 instance
ssh -i $PRIVATE_KEY ec2-user@$PUBLIC_IP << 'EOF'
sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose version
sudo yum update -y
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user

# Verify the installation
docker-compose --version
exit
EOF


# Copy project files to the EC2 instance
rsync -avz --exclude 'venv' -e "ssh -i $PRIVATE_KEY" . ec2-user@$PUBLIC_IP:/home/ec2-user/app

# SSH into the EC2 instance and build/start the Docker containers
ssh -i $PRIVATE_KEY ec2-user@$PUBLIC_IP << 'EOF'
cd /home/ec2-user/app
docker-compose -f "docker-compose.yml" down
docker system prune --all --force
docker-compose build
docker-compose up -d
EOF

echo "Deployment completed. Your application should be accessible at http://$PUBLIC_IP"