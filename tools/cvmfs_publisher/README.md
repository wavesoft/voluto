# CVMFS Publisher

This utility is used for programmatically updating the files of a particular voluto project in the CVMFS server.

This utility is meant to be deployed on the CVMFS repository manager. It provides the mechanism to send a batch of files over SSH directly to the CVMFS repository.

## Usage

In order to publish a batch of files use the following syntax:

```shell
tar -zc <files> | ssh -i <private_key> <user>@<repository> cvmfs_publisher.sh publish <project> <revision> activate
```

In order to use this utility you are going to need an SSH key for password-less login to your CVMFS repository. Check the setting-up guide below.

## Setting up 

You should first create an SSH keypair that you will use for password-less log-in to the CVMFS repository manager.

1. Generate an SSH key using the command `ssh-keygen -t rsa -b 4096`
2. Append your public key to the `/home/cvmfs_user/.ssh/authorized_keys`
3. Deploy `cvmfs_publisher.sh` to the CVMFS repository machine (ex. copy it in `/usr/local/bin`)
4. Edit the first two lines of the `cvmfs_publisher.sh`:

```bash
# Change this to point to your base directory:
BASE_DIRECTORY="/cvmfs/myrepo.cern.ch/path/to/base"
# Change this to the name of the CVMFS repository:
CVMFS_REPOS="sft.cern.ch"
```
