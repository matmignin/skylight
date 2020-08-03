#variable "public_key_path" {
#default = "us-east-1"
#}

variable "private_key" {
  default = "skylight2"
}

variable "ami_id" {
  default = "ami-2757f631"
}

variable "server_instance_type" {
  default     = "t2.micro"
  description = "instance_type"
}

variable "region" {
  default     = "us-east-1"
  description = "AWS Region"
}
