provider "aws" {
  profile = "default"
  region  = "us-east-1"
}

resource "aws_instance" "skylight_instance" {
  ami                    = "ami-2757f631"
  instance_type          = "t2.micro"
  key_name               = "skylight"
  vpc_security_group_ids = [aws_security_group.skylight_sg.id]

  provisioner "remote-exec" {
    inline = [
      "sudo apt-get -y update",
      "sudo apt-get install -y python",
    ]
    connection {
      type = "ssh"
      user = "ubuntu"
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
