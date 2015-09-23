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

import uuid

from django.db import models
from django.contrib.auth.models import User

###################################################################
# Utlity Functions
###################################################################

def new_uuid():
	"""
	UUID Generator
	"""
	return uuid.uuid4().hex

###################################################################
# Database Models
###################################################################

class Project(models.Model):
	"""
	Base configuration for every voluto project
	"""

	#: The UUID of this project
	uuid = models.CharField(max_length=32, default=new_uuid, unique=True, db_index=True, 
		help_text="Project identification string")
	
	#: The owner of this project
	owner = models.ForeignKey(User)

	#: The name of this project
	name = models.CharField(max_length=1024, default="",
		help_text="The name of this project")

	#: Current project's files record
	files = models.ForeignKey('ProjectFiles', default=None, blank=True, null=True, related_name='projectfiles')

	def __unicode__(self):
		"""
		Return project name in unicode
		"""
		return self.name

class ProjectFiles(models.Model):
	"""
	Revisioning project files
	"""

	PENDING = 'PE'
	STAGING = 'ST'
	PUBLISHED = 'PU'
	RETIRED = 'RE'
	FILE_STATUS_CHOICES = (
		(PENDING, 'Pending'),		# Pending staging
		(STAGING, 'Staging'),		# Staging (to CVMFS)
		(PUBLISHED, 'Published'),	# Published (in CVMFS)
		(RETIRED, 'Retired'),		# Retired
	)

	ZIP = 'zip'
	TARGZ = 'tgz'
	TARBZ2 = 'tbz2'
	TARXZ = 'txz'
	LZMA = 'lzma'
	GIT = 'git'
	SVN = 'svn'
	CVMFS = 'cvmfs'
	FILE_TYPE_CHOICES = (
		(ZIP, '.zip file'),			# A zipball
		(TARGZ, '.tar.gz file'),	# A tarball with GZ compression
		(TARBZ2, '.tar.bz2 file'),	# A tarball with BZ2 compression
		(TARXZ, '.tar.xz file'),	# A tarball with XZ compression
		(LZMA, '.7z (LZMA) file'),	# A zeven-zip (LZMA) archive
		(GIT, 'GIT Repository'),	# A link to a GIT repository
		(SVN, 'SVN Repository'),	# A link to an SVN repository
		(CVMFS, 'CVMFS Link'),		# A link to an SVN repository
	)

	#: The relevant project
	project = models.ForeignKey(Project)

	#: The revision number
	number = models.IntegerField(default=1,
		help_text="Project files revision number")

	#: The time the user uploaded the files
	date = models.DateTimeField(auto_now_add=True)

	#: Files status
	status = models.CharField(max_length=2, choices=FILE_STATUS_CHOICES, default=PENDING,
		help_text="Current status of the project files")

	#: The type of this file
	filetype = models.CharField(max_length=5, choices=FILE_TYPE_CHOICES, default="",
		help_text="The type of the project files")

	#: The URL where the files can be obtained from
	src = models.CharField(max_length=4096, default="", 
		help_text="The URL where the files can be obtained from")

	#: The URL where the files are available at
	url = models.CharField(max_length=4096, default=None, blank=True, null=True,
		help_text="The URL where the files are available at")

class ProjectLog(models.Model):
	"""
	A log of actions performed in a particular project
	"""

	INFO = 0
	WARNING = 1
	ERROR = 2
	CRITICAL = 3
	LOG_LEVELS = (
		(INFO, 'Info'),			# An informational message
		(WARNING, 'Warning'),	# A warning
		(ERROR, 'Error'),		# An error
		(CRITICAL, 'Critical'),	# A critical error
	)

	#: The relevant project
	project = models.ForeignKey(Project)

	#: Who triggered this action
	user = models.ForeignKey(User)

	#: The the action was scheduled
	date = models.DateTimeField(auto_now_add=True)

	#: Log level
	level = models.IntegerField(choices=LOG_LEVELS, default=0)

	#: Visual description of the action
	text = models.CharField(max_length=1024, default="")

class ProjectActions(models.Model):
	"""
	Project actions stack
	"""

	#: The relevant project
	project = models.ForeignKey(Project)

	#: The action data
	data = models.TextField(default="{}")

