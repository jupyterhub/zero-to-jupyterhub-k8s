# Shared Disks

1. Create the shared disk. In your jupyterhub-k8s working directory, run `./make-disk.bash {course_name}`. For example `./make-disk.bash cogneuro88`. This creates the disk, attaches it to the provisioner node, and mounts it to the filesystem.
1. Copy data into the disk. The course will have a script in the disks/ subdirectory of jupyterhub-k8s. Change to the mount location and run the script.
  ```
cd /mnt/disks/{disk_name}
sudo /path/to/jupyterhub-k8s/disks/{course_name}.bash
```

1. Detach the disk:
  ```
cd /somewhere/else/
sudo umount /mnt/disks/{disk_name}
gcloud compute instances detach-disk provisioner-01 --disk {disk_name}
```
1. Update the chart by editing the disk name in dev.yaml.
