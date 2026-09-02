# =============================================================================
# Terraform — Aprovisionamiento del VPS Linode (IaaS)
# Provider oficial: linode/linode
# =============================================================================

terraform {
  required_version = ">= 1.5"
  required_providers {
    linode = {
      source  = "linode/linode"
      version = "~> 2.0"
    }
  }
}

provider "linode" {
  token = var.linode_token
}

# --- Firewall (sin costo adicional) ------------------------------------------
resource "linode_firewall" "sirh_firewall" {
  label = "sirh-nomina-fw"

  # Permitir HTTP
  inbound {
    label    = "allow-http"
    action   = "ACCEPT"
    protocol = "TCP"
    ports    = "80"
    ipv4     = ["0.0.0.0/0"]
    ipv6     = ["::/0"]
  }

  # Permitir HTTPS
  inbound {
    label    = "allow-https"
    action   = "ACCEPT"
    protocol = "TCP"
    ports    = "443"
    ipv4     = ["0.0.0.0/0"]
    ipv6     = ["::/0"]
  }

  # SSH solo desde IPs administrativas
  inbound {
    label    = "allow-ssh-admin"
    action   = "ACCEPT"
    protocol = "TCP"
    ports    = "22"
    ipv4     = var.admin_ips
  }

  # Denegar todo lo demás
  inbound_policy  = "DROP"
  outbound_policy = "ACCEPT"

  linodes = [linode_instance.sirh_server.id]
}

# --- VPS Nanode 1 GB ---------------------------------------------------------
resource "linode_instance" "sirh_server" {
  label           = "sirh-nomina-prod"
  region          = var.region
  type            = "g6-nanode-1"  # Nanode 1GB — $5/mes
  image           = "linode/ubuntu24.04"
  authorized_keys = [var.ssh_public_key]

  metadata {
    user_data = base64encode(file("${path.module}/cloud-init.yaml"))
  }

  tags = ["produccion", "sirh-nomina"]
}

# --- Backups ($2/mes) --------------------------------------------------------
resource "linode_instance_config" "sirh_config" {
  linode_id = linode_instance.sirh_server.id
  label     = "sirh-boot-config"

  devices {
    sda {
      disk_id = linode_instance.sirh_server.disk[0].id
    }
  }

  booted = true
}

# --- Outputs -----------------------------------------------------------------
output "server_ip" {
  description = "IP pública del VPS"
  value       = linode_instance.sirh_server.ip_address
}

output "server_status" {
  description = "Estado del VPS"
  value       = linode_instance.sirh_server.status
}
