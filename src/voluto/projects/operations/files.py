################################################################
# Voluto - Volunteering Computing Administration & Organization
# Copyright (C) 2015 Ioannis Charalampidis
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
################################################################

import os
import uuid

from django.conf import settings
from voluto.projects.models import ProjectFiles

class UploadError(Exception):
	"""
	An exception thrown if an error occurs
	"""
	def __init__(self, message):
		super(UploadError, self).__init__(message)

def handle_repository_upload( project, repository_type, url, tag ):
	"""
	Handle the fact that the user requested the upload of a project file by a repository
	"""

	# Find last project record
	version = 1
	last_record = None
	try:
		last_record = ProjectFiles.objects.filter(project=project).order_by('-number')[0]
		version = last_record.number + 1
	except IndexError:
		pass

	# Create a new file information
	files_record = ProjectFiles( project=project, src="%s:%s:%s" % ( repository_type, url, tag ), number=version )

	# Test repository
	

	# Save record
	files_record.save()

def handle_tarball_upload( project, uploaded_file ):
	"""
	Handle the fact that the user has uploaded a new tarball to the project
	"""

	# Find the staging directory for this project
	stage_dir = os.path.join( settings.PROJECT_TEMP_DIR, project.uuid )

	# Make sure stage dir exists
	if not os.path.exists(stage_dir):
		os.mkdir(stage_dir)

	# Calculate upload file name
	upload_file = os.path.join( stage_dir, uuid.uuid4().hex )

	# Find last project record
	version = 1
	last_record = None
	try:
		last_record = ProjectFiles.objects.filter(project=project).order_by('-number')[0]
		version = last_record.number + 1
	except IndexError:
		pass

	# Create a new file information
	files_record = ProjectFiles( project=project, src="file:%s" % upload_file, number=version )

	# Discard unsupported archive types
	if uploaded_file.content_type == "application/zip":
		files_record.filetype = "zip"
	elif uploaded_file.content_type == "application/x-gzip":
		if ('.tar' in uploaded_file.name) or ('.tgz' in uploaded_file.name):
			files_record.filetype = ProjectFiles.TARGZ
		else:
			raise UploadError("The uploaded file is not in one of the supported file formats!")
	elif uploaded_file.content_type == "application/x-bzip2":
		if ('.tar' in uploaded_file.name) or ('.tbz2' in uploaded_file.name):
			files_record.filetype = ProjectFiles.TARBZ2
		else:
			raise UploadError("The uploaded file is not in one of the supported file formats!")
	elif uploaded_file.content_type == "application/x-xz":
		if ('.tar' in uploaded_file.name) or ('.txz' in uploaded_file.name):
			files_record.filetype = ProjectFiles.TARXZ
		else:
			raise UploadError("The uploaded file is not in one of the supported file formats!")
	elif uploaded_file.content_type == "application/octet-stream":
		if ('.gz' in uploaded_file.name) or ('.tgz' in uploaded_file.name):
			files_record.filetype = ProjectFiles.TARGZ
		elif ('.bz2' in uploaded_file.name) or ('.tbz2' in uploaded_file.name):
			files_record.filetype = ProjectFiles.TARBZ2
		elif ('.tar' in uploaded_file.name) or ('.txz' in uploaded_file.name):
			files_record.filetype = ProjectFiles.TARXZ
		else:
			raise UploadError("The uploaded file is not in one of the supported file formats!")
	else:
		raise UploadError("The uploaded file is not in one of the supported file formats!")


	# Write down the chunks
	size = 0
	with open(upload_file, 'wb+') as destination:
		for chunk in uploaded_file.chunks():
			destination.write(chunk)
			size += len(chunk)

	# Save record
	files_record.save()
