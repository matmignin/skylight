#variable "public_key_path" {
#default     = "~/.ssh/aws-rsa.pub"
#description = "public key path"
#}

#variable "private_key" {
#default = "~/.ssh/skylight.pem"
#}

variable "server_instance_type" {
  default     = "t2.micro"
  description = "instance_type"
}

variable "region" {
  default     = "us-east-1"
  description = "AWS Region"
}
