provider "aws" {
  profile = "default"
  region  = "us-east-1"
}

resource "aws_instance" "skylight_instance" {
  ami           = "ami-2757f631"
  instance_type = "t2.micro"
  key_name      = "skylight"

  #provisioner "remote-exec" {
  #inline = [
  #"sudo apt-get -y update",
  #"sudo apt-get install -y python",
  #]
  #connection {
  #type = "ssh"
  #user = "ubuntu"
  #}
  #}

}

resource "aws_security_group" "skylight_elb" {
  name = "skylight-elb"

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

resource "aws_elb" "skylight_lb" {
  name               = "skylight-lb"
  availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"]
  instances          = ["${aws_instance.skylight_instance.id}"]

  health_check {
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 3
    interval            = 30
    target              = "HTTP:80/"
  }

  listener {
    instance_port     = 80
    instance_protocol = "http"
    lb_port           = 80
    lb_protocol       = "http"
  }

  cross_zone_load_balancing   = true
  idle_timeout                = 400
  connection_draining         = true
  connection_draining_timeout = 4
}

output "instance_ips" {
  value = ["${aws_instance.skylight_instance.*.public_ip}"]
}
