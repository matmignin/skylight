provider "aws" {
  profile = "default"
  region  = var.region

}


resource "aws_instance" "skylight_instance" {
  ami                    = var.ami_id
  instance_type          = var.server_instance_type
  key_name               = var.private_key
  vpc_security_group_ids = [aws_security_group.skylight_sg.id]

  provisioner "remote-exec" {
    inline = [
      #"sudo apt -y update && sudo apt -y upgrade",
      "sudo apt -y update && sudo apt install -y python3 python3-pip python3-venv",
      #"sudo apt install -y python3 python3-venv python3-pip",
      #"python3 -m venv venv",
      "sudo pip3 install --upgrade pip"
    ]
    connection {
      type = "ssh"
      user = "ubuntu"
      host = self.public_ip
    }
  }

  provisioner "local-exec" {
    command = "sed -i '' -e '$ d' ../ansible/inventory/hosts; echo ${self.public_ip} >> ../ansible/inventory/hosts"
  }
  tags = {
    name = "skylight-tag"
  }
}

resource "aws_security_group" "skylight_sg" {
  name = "skylight-sg"

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }


  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


output "instance_ips" {
  value = [aws_instance.skylight_instance.public_ip]
}
