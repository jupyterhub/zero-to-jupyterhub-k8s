# Recover Data From Snapshots

1. Locate the user's PVC:
 ```
kubectl --namespace={NAMESPACE} describe pod {POD} | grep ClaimName
```

2. Locate the volume assocated with the PVC:
  ```
kubectl --namespace={NAMESPACE} describe pvc {CLAIM} | grep Volume:
```

3. Locate the snapshots associated with the volume:
  ```
gcloud compute snapshots list | grep {VOLUME}
```

4. Create recovery disks for each volume:
  ```
gcloud compute disks create recovery-{USERNAME}-1 --source-snapshot {SNAPSHOT1}
gcloud compute disks create recovery-{USERNAME}-2 --source-snapshot {SNAPSHOT2}
...
```

5. Attach recovery disks:
  ```
gcloud compute instances attach-disk provisioner-01 --disk recovery-{USERNAME}-1
gcloud compute instances attach-disk provisioner-01 --disk recovery-{USERNAME}-2
...
```

6. Create mount path:
  ```
sudo mkdir /mnt/disks/recovery-{USERNAME}-1
sudo mkdir /mnt/disks/recovery-{USERNAME}-2
...
```

7. Mount disks:
  ```
sudo mount /dev/{blockdevice1} /mnt/disks/recovery-{USERNAME}-1
sudo mount /dev/{blockdevice2} /mnt/disks/recovery-{USERNAME}-2
...
```

8. Recover data:
  ```
cp /mnt/disks/recovery-{USERNAME}-1/some/file/1 /somewhere/else/
cp /mnt/disks/recovery-{USERNAME}-2/some/file/2 /somewhere/else/
...
```

9. Unmount disks:
  ```
sudo umount /mnt/disks/recovery-{USERNAME}-1
sudo umount /mnt/disks/recovery-{USERNAME}-2
...
```

10. Detach recovery disks:
  ```
gcloud compute instances detach-disk provisioner-01 --disk recovery-{USERNAME}-1
gcloud compute instances detach-disk provisioner-01 --disk recovery-{USERNAME}-2
...
```

11. Delete recovery disks:
  ```
gcloud compute disks delete recovery-{USERNAME}-1
gcloud compute disks delete recovery-{USERNAME}-2
...
```
