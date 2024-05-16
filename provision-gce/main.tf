resource "google_compute_firewall" "allow-k3s" {
	name = "allow-k3s"
	network = "default"
	allow {
		protocol = "tcp"
		ports = ["6443"]
	}
    source_ranges = ["0.0.0.0/0"]
	target_tags = ["k3s"]
}

resource "google_compute_instance" "gce-cluster" {
  name         = "gce-cluster"
  zone         = "us-west1-a"
  machine_type = "n1-highcpu-32"
  tags         = ["k3s"]

  boot_disk {
    initialize_params {
      image = "debian-12"
    }
  }

  network_interface {
    network = "default"

    access_config {}
  }

  depends_on = [
    google_compute_firewall.allow-k3s,
  ]
}

resource "google_compute_instance" "client" {
  name         = "client"
  zone         = "us-west1-a"
  machine_type = "e2-standard-4"

  boot_disk {
    initialize_params {
      image = "debian-12"
    }
  }

  network_interface {
    network = "default"

    access_config {}
  }

  metadata_startup_script = "echo hi > /test.txt"
}