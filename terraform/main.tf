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
      "sudo apt-get -y update",
      "sudo apt-get install -y python3 python3-pip python3-venv"
    ]
    connection {
      type = "ssh"
      user = "ubuntu"
      host = self.public_ip
    }
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
