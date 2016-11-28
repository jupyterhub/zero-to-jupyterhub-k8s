# Google Drive
As of Fall 2016, Data8's Jupyterhub deployment uses an NFS to store and manage all of its students resources that are intended to persist through the lifetime of the course they are taking. Data sets, notebooks, and other miscellaneous files that students create or modify and their respective changes must still be stored and preserved when we eventually migrate to our Kubernetes Jupyterhub deployment.

The goal of the Data Science Initiative is that eventually, students who continue to take Data Science courses and their various connector classes will begin to build a portfolio of projects and work that they can take with them by the time they graduate into academia or industry. In order to do so, we must support a means of persisting a student's data for a course even after they are done with it. 

## Purpose

All UC Berkeley students automatically own their own Google Drive account, with 1 TB worth of storage space. Because these accounts are automatically provisioned and are frequently used by students throughout their years, they are the natural option for storing files associated with their classes for the long term. Additionally, Google drive provides an open API and a robust ecosystem for tools that we can leverage to manage, upload, and sync a student's files.

## Goal

Our short term goal after switching to our Kubernetes Jupyterhub deployment is to ensure that students can continue to work on their assignments without fear of their data being lost of corrupted. From their end, they should not feel like managing their files is any different from our old Ansible deployment. Our long term goal is to allow students to have access to their files for as long as possible.

By persisting a student's files across the lifetime of the specific classes they take, they will have the opportunity to review old materials and use the work they've done in their classes as a portfolio for their future endeavors. Additionally, we will expose a few extra tools for students such as allowing them to manually sync their files to their Drive accounts whenever they please.

## Background Syncing

With the Kubernetes deployment, a student should even without Google Drive in their picture have access to persistent storage. We dynamically allocate Google Cloud disks for each student that follows them specifically, ensuring they will always have access to their own data.

With background syncing, we will occasionally run a service that will pull all the relevant files from their active classes during minimal service times (likely early in the morning) and sync them with their Drive accounts to ensure that they are always as up to date as possible without disturbing the student's ability to work or access their data.

## Implementation

Currently, we intend on using [Drive](https://github.com/prasmussen/gdrive) as our command line interface to managing Google Drive accounts. After having our students authenticate the service, we will run a script daily using Drive's interface to upload all the files from that student's class directory to their Drive account. On a more granular level, we will first:

1. Using a nbextension, send first time users a link to authenticate their Google Drive account.
2. Each single user has their `/home` directory mounted to a persistent disk, and we will sync this directory with a Google Drive directory named `/home/{username}`.
3. Each day, running this script will allow Drive to identify any changes made to the `/home` directory and sync those changes to the ones on drive. 
4. We will also expose an extension to allow users to manually upload their files to Drive.

## Conflicting Writes

There are a few conflicting issues that we must define a policy on to avoid data loss. Firstly, we push on a daily basis from each single user's mounted directory to Drive. We justify that the latest write will be the correct one, meaning that intermediate changes that a user makes directly on their Drive files will not be synced to their persistent disks.

Additionally, it is necessary for users to have a correctly synced Drive directory as multiple pushes of the same file without syncing to a directory will push multiple copies of a file without updating the original one.
