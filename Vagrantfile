# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "generic/ubuntu1804"
  config.vm.provider "virtualbox" do |vb|
     vb.memory = "3072"
     vb.cpus = 2
  end

  config.vm.provider :libvirt do |lv|
    lv.memory = 3072
    lv.cpus = 2
  end if Vagrant.has_plugin?('vagrant-libvirt')

  config.vm.network "forwarded_port", guest: 8080, host: 8080

  config.vm.provision "shell", path: "vagrant-vm-root-setup.sh"
  config.vm.synced_folder ".", "/home/vagrant/zero-to-jupyterhub-k8s"
end
