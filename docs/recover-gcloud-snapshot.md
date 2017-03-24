# Recover Data From Snapshots

1. Locate the user's PVC:
 ```
kubectl --namespace={NAMESPACE} describe pod {POD} | grep ClaimName
```

1. Locate the volume assocated with the PVC:
  ```
kubectl --namespace={NAMESPACE} describe pvc {CLAIM} | grep Volume:
```

1. Locate the snapshots associated with the volume:
  ```
gcloud compute snapshots list | grep {VOLUME}
```

1. Create recovery disks for each volume:
  ```
gcloud compute disks create recovery-{USERNAME}-1 --source-snapshot {SNAPSHOT1}
gcloud compute disks create recovery-{USERNAME}-2 --source-snapshot {SNAPSHOT2}
...
```

1. Attach recovery disks:
  ```
gcloud compute instances attach-disk provisioner-01 --disk recovery-{USERNAME}-1
gcloud compute instances attach-disk provisioner-01 --disk recovery-{USERNAME}-2
...
```

1. Create mount path:
  ```
sudo -i mkdir /mnt/disks/recovery-{USERNAME}-1
sudo -i mkdir /mnt/disks/recovery-{USERNAME}-2
...
```

1. Mount disks:
  ```
sudo -i mount /dev/{blockdevice1} /mnt/disks/recovery-{USERNAME}-1
sudo -i mount /dev/{blockdevice2} /mnt/disks/recovery-{USERNAME}-2
...
```

1. Recover data:
  ```
cp /mnt/disks/recovery-{USERNAME}-1/some/file/1 /somewhere/else/
cp /mnt/disks/recovery-{USERNAME}-2/some/file/2 /somewhere/else/
...
```

1. Unmount disks:
  ```
sudo -i umount /mnt/disks/recovery-{USERNAME}-1
sudo -i umount /mnt/disks/recovery-{USERNAME}-2
...
```

1. Detach recovery disks:
  ```
gcloud compute instances detach-disk provisioner-01 --disk recovery-{USERNAME}-1
gcloud compute instances detach-disk provisioner-01 --disk recovery-{USERNAME}-2
...
```

1. Delete recovery disks:
  ```
gcloud compute disks delete recovery-{USERNAME}-1
gcloud compute disks delete recovery-{USERNAME}-2
...
```

