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

import json
from voluto.projects.models import *

def push( project, data, log=None, user=None, level=ProjectLog.INFO ):
	"""
	Push some data and optionally create a log entry
	"""

	# Create action
	action = ProjectActions(data=json.dumps(data), project=project)
	action.save()

	# Create log entry
	if (not user is None) and (not log is None):
		log_entry = ProjectLog(project=project, user=user, text=log, level=level)
		log_entry.save()

def pop():
	"""
	Pop a data entry from the database and reurn a (project, data) tuple
	"""

	# Get next 
	try:
		action = ProjectActions.objects.all().order_by('id')[0]
	except IndexError:
		return None

	# Decode and return
	return (
		'project': action.project,
		'data': json.loads(action.data)
	)
