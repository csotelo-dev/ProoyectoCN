# =============================================================================
# Variables de Terraform
# Valores sensibles se pasan via terraform.tfvars o variables de entorno
# =============================================================================

variable "linode_token" {
  description = "Token de API de Linode (alcance mínimo y con expiración)"
  type        = string
  sensitive   = true
}

variable "region" {
  description = "Región del VPS Linode"
  type        = string
  default     = "us-east"  # Norteamérica
}

variable "ssh_public_key" {
  description = "Llave pública SSH ed25519 para acceso al VPS"
  type        = string
}

variable "admin_ips" {
  description = "IPs permitidas para acceso SSH (CIDR)"
  type        = list(string)
  default     = ["0.0.0.0/0"]  # Restringir en producción
}
