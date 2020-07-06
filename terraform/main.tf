provider "aws" {
  profile = "default"
  region  = var.region
  #version = "~> 2.0"
}


resource "aws_instance" "skylight_instance" {
  key_name               = "skylight"
  ami                    = "ami-2757f631"
  instance_type          = var.server_instance_type
  vpc_security_group_ids = [aws_security_group.skylight_sg.id]

  tags = {
    name = "skylight-tag"
  }

  provisioner "remote-exec" {
    inline = [
      "sudo apt-get -y update",
      "sudo apt-get install -y python",
    ]
    connection {
      type = "ssh"
      user = "ubuntu"
      #private_key = file("~/.ssh/skylight.pem")
      host = self.public_ip
    }
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

  ingress { # http port
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress { # https port
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }


  ingress { #ssh port
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


output "instance_ips" {
  value = [aws_instance.skylight_instance.public_ip]
}


