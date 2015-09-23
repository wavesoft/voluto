#!/bin/bash

#####################################################

# Configurable base CVMFS directory
BASE_DIRECTORY="/cvmfs/sft.cern.ch/lcg/external/experimental/vcprojects"

# Configurable CVMFS project
CVMFS_REPOS="sft.cern.ch"

#####################################################

# Help screen
function help_and_exit {
	echo "Usage: $0 [publish|select|delete] <project> [<revision>] [activate]"
	echo ""
	echo " publish : Extracts a tarball streamed through STDIN to the project's folder,"
	echo "           under the specified revision. If 'activate' is also specified, this"
	echo "           revision will become the latest active."
	echo " select  : Activate the specified revision."
	echo " delete  : Delete an archived revision."
	echo ""
	exit 1
}

# Enter a CVMFS transaction
function cvmfs_start {
	# echo "Entering CVMFS transaction"
	cvmfs_server transaction ${CVMFS_REPOS}
	if [ $? -ne 0 ]; then
		return 1
	fi
	return 0
}

# Discard a CVMFS transaction
function cvmfs_discard {
	# echo "Discarding CVMFS transaction"
	cvmfs_server abort -f ${CVMFS_REPOS}
	if [ $? -ne 0 ]; then
		return 1
	fi
	return 0
}

# Exit a CVMFS transaction
function cvmfs_commit {
	# echo "Committing CVMFS transaction"
	cvmfs_server publish ${CVMFS_REPOS}
	if [ $? -ne 0 ]; then
		return 1
	fi
	return 0
}

# Validate input
P_ACTION="$1"
P_PROJECT="$2"
P_REVISION="$3"
[ -z "$P_ACTION" ] && echo "ERROR: Please specify a publish action!" && help_and_exit
[ -z "$P_PROJECT" ] && echo "ERROR: Please specify a project name!" && help_and_exit
[ ! -d "${BASE_DIRECTORY}" ] && echo "ERROR: The base directory ($BASE_DIRECTORY) is missing!" && exit 2
[ -z "$(which cvmfs_server)" ] && echo "ERROR: Missing cvmfs_server utility!" && exit 2

# Sanitize project name
P_PROJECT=${P_PROJECT//_/}
P_PROJECT=${P_PROJECT// /_}
P_PROJECT=${P_PROJECT//[^a-zA-Z0-9_]/}
P_PROJECT=`echo -n $P_PROJECT | tr A-Z a-z`

# Sanitize revision (keep only numbers)
P_REVISION=${P_REVISION//[^0-9]/}

# Handle actions
case $P_ACTION in
	publish)
	
		# Prepare paths
		UPLOAD_TARGET="${BASE_DIRECTORY}/${P_PROJECT}/${P_REVISION}"
		LINK_FILE="${BASE_DIRECTORY}/${P_PROJECT}/latest"

		# Perform sanity checks
		[ -z "$P_REVISION" ] && echo "ERROR: Missing revision number (use only numbers!)" && help_and_exit
		[ -d "${UPLOAD_TARGET}" ] && echo "ERROR: This revision already exists!" && exit 2
		[[ -e "${LINK_FILE}" && ! -L "${LINK_FILE}" ]] && echo "ERROR: The 'latest' link is improperly configured!" && exit 3

		# Enter CVMFS transaction
		cvmfs_start
		if [ $? -ne 0 ]; then
			echo "ERROR: Unable to start a CVMFS transaction!"
			exit 4
		fi

		# Make directories
		mkdir -p "${UPLOAD_TARGET}"

		# Expand stdin
		cat | tar -xz --no-same-owner --no-selinux --no-xattrs -C "${UPLOAD_TARGET}"
		ANS=$?

		# Exit on expand errors
		if [ $ANS -ne 0 ]; then
			echo "ERROR: Unable to extract archive from STDIN"
			cvmfs_discard
			exit 5
		fi

		# Create 'latest' target if missing
		if [ ! -L "${LINK_FILE}" ]; then
			ln -s "${P_REVISION}" "${LINK_FILE}"

		# Update 'latest' target if asked to do so
		elif [ "$4" == "activate" ]; then
			[ -L "${LINK_FILE}" ] && rm "${LINK_FILE}"
			ln -s "${P_REVISION}" "${LINK_FILE}"
		fi

		# Exit CVMFS transaction
		cvmfs_commit
		if [ $? -ne 0 ]; then
			echo "ERROR: Unable to commit a CVMFS transaction!"
			cvmfs_discard
			exit 4
		fi

		;;

	select)
		
		# Calculate target and link file
		LINK_TARGET="${BASE_DIRECTORY}/${P_PROJECT}/${P_REVISION}"
		LINK_FILE="${BASE_DIRECTORY}/${P_PROJECT}/latest"

		# Check for errors
		[ ! -d "${LINK_TARGET}" ] && echo "ERROR: The specified revision and/or project does not exist!" && exit 2
		[[ -e "${LINK_FILE}" && ! -L "${LINK_FILE}" ]] && echo "ERROR: The 'latest' link is improperly configured!" && exit 3

		# Enter CVMFS transaction
		cvmfs_start
		if [ $? -ne 0 ]; then
			echo "ERROR: Unable to start a CVMFS transaction!"
			exit 4
		fi

		# Replace 'latest' link
		rm "${LINK_FILE}"
		ln -s "${P_REVISION}" "${LINK_FILE}"

		# Exit CVMFS transaction
		cvmfs_commit
		if [ $? -ne 0 ]; then
			echo "ERROR: Unable to commit a CVMFS transaction!"
			cvmfs_discard
			exit 4
		fi

	  ;;

	delete)
		
		# Delete an inactive link
		DELETE_TARGET="${BASE_DIRECTORY}/${P_PROJECT}/${P_REVISION}"
		LINK_FILE="${BASE_DIRECTORY}/${P_PROJECT}/latest"

		# Check for errors
		[ ! -d "${DELETE_TARGET}" ] && echo "ERROR: The specified revision and/or project does not exist!" && exit 2
		[[ -e "${LINK_FILE}" && ! -L "${LINK_FILE}" ]] && echo "ERROR: The 'latest' link is improperly configured!" && exit 3

		# Check for deleting an active revision
		if [ -L "${LINK_FILE}" ]; then
			LINK_TARGET=$(readlink "${LINK_FILE}")
			if [ "$LINK_TARGET" == "${P_REVISION}" ]; then
				echo "ERROR: You are trying to delete an active revision!"
				exit 2
			fi
		fi

		# Enter CVMFS transaction
		cvmfs_start
		if [ $? -ne 0 ]; then
			echo "ERROR: Unable to start a CVMFS transaction!"
			exit 4
		fi

		# Delete folder
		rm -rf "${DELETE_TARGET}"

		# Exit CVMFS transaction
		cvmfs_commit
		if [ $? -ne 0 ]; then
			echo "ERROR: Unable to commit a CVMFS transaction!"
			cvmfs_discard
			exit 4
		fi

	  ;;
	*)
	  echo "ERROR: Unknown action ($P_ACTION) specified!" && help_and_exit
	  ;;
esac

