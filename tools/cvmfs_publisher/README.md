# CVMFS Publisher

This utility is used for programmatically updating the files of a particular voluto project in the CVMFS server.

This utility is meant to be deployed on the CVMFS repository manager. It provides the mechanism to send a batch of files over SSH directly to the CVMFS repository.

## Usage

The `cvmfs_publisher.sh` utility has the following syntax:

```
cvmfs_publisher.sh publish <project> <revision> [activate]
cvmfs_publisher.sh select <project> <revision>
cvmfs_publisher.sh delete <project> <revision>
```

* The __publish__ option expects a gzip tarball stream through STDIN end extracts it's contents in the appropriate project directory in the CVMFS repository. If the `activate` parameter is specified, that revision will be selected as the 'latest'.
* The __select__ option selects a previous revision of the specified project and marks it as the 'latest'.
* The __delete__ option deletes a previous revision of the specified project. This operation cannot be performed if that revision is the 'latest'.

## Example

Let's say that you have a couple of files that you want to publish through CVMFS.

```shell
~$ ls 
img/        index.html  src/
```

Also we assume that you already have generated an SSH keypair for logging into our example repository manager in `cvmfs.example.com`, for the user `user`. To upload that files to the cvmfs repository, use:

```shell
tar -zc * | ssh -i id_rsa user@cvmfs.example.com cvmfs_publisher.sh publish project 2 activate
```

This will do the following:

1. Create a gzipped tarball on-the-fly with the files you want to commit
2. Log-in to the CVMFS repository and run the `cvmfs_publisher.sh` helper utility
3. The utility will begin a transaction and extract the tarball directly on the appropriate location in CVMFS
4. Upon completion, it will mark the revision `2` as the latest and commit the transaction.

## Setting up 

You should first create an SSH keypair that you will use for password-less log-in to the CVMFS repository manager.

1. Generate an SSH keypair using the command `ssh-keygen -t rsa -b 4096`
2. Append the public key to the `/home/cvmfs_user/.ssh/authorized_keys`
3. Deploy `cvmfs_publisher.sh` to the CVMFS repository machine (ex. copy it in `/usr/local/bin`)
4. Edit the first two lines of the `cvmfs_publisher.sh`:

```bash
# Change this to point to your base directory:
BASE_DIRECTORY="/cvmfs/myrepo.cern.ch/path/to/base"
# Change this to the name of the CVMFS repository:
CVMFS_REPOS="sft.cern.ch"
```

Youa re now ready!

### Files Versioning

This utility uploads the tarball contents to a project directory using a versioning scheme. Each tarball is extracted into a versioned sub-directory and then it's linked to the `latest` symlink.

For example:

```
total 14
drwxrwxr-x. 3 voluto voluto 4096 Sep 23 15:13 1
drwxrwxr-x. 3 voluto voluto 4096 Sep 23 15:20 2
drwxrwxr-x. 3 voluto voluto 4096 Sep 23 15:21 3
lrwxrwxrwx. 1 voluto voluto    1 Sep 23 15:21 latest -> 3
```
