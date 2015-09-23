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

from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render

from voluto.common.decorators import render_to
from voluto.ui.views.project_forms import *

from voluto.projects.operations import files
from voluto.projects.models import ProjectFiles, Project

##################################
# Forms
##################################

from django import forms

class ProjectFilesForm(forms.Form):
	tarball = forms.forms.FileField(label='Upload files')

class OpenstackForm(forms.Form):
	enabled = forms.BooleanField(initial=False)
	api_key = forms.CharField(label='API Key', help_text="ex. API")
	api_secret = forms.CharField(label='API Secret', help_text="ex. Secret")

class DatabridgeForm(forms.Form):
	enabled = forms.BooleanField(initial=False)
	domain = forms.CharField(label='Queue Domain', help_text="ex. text4theory.cern.ch")
	username = forms.CharField(label='Username', help_text="ex. user")
	password = forms.CharField(label='Password', help_text="ex. secret")

class ScriptInitForm(forms.Form):
	enabled = forms.BooleanField(initial=False)
	script = forms.CharField(label='Script to run', help_text="ex. init.sh")

class ScriptTeardownForm(forms.Form):
	enabled = forms.BooleanField(initial=False)
	script = forms.CharField(label='Script to run', help_text="ex. teardown.sh")

class NoQueueForm(forms.Form):
	enabled = forms.BooleanField(initial=True)

class DatabridgeQueueForm(forms.Form):
	enabled = forms.BooleanField(initial=False)
	script = forms.CharField(label='Handler to run', help_text="ex. handler.sh")
	args = forms.ChoiceField(label='How to pass the job description', choices=(
			('stdin', 'Via STDIN'),
			('arg', 'As a Command-Line argument'),
			('env', 'As an Environment Variable'),
		))

class CopilotQueueForm(forms.Form):
	enabled = forms.BooleanField(initial=False)
	server = forms.CharField(label='The XMPP server to connect to', help_text="ex. handler.sh")


##################################
# URL Handlers
##################################

@render_to("ui/project/list.html")
def list(request):
	"""
	The project listing interface
	"""
	return { }

def manage_publish(request, project, revision):
	"""
	Publish project's files
	"""

	# Lookup project
	try:
		project = Project.objects.get(uuid=project)
	except Project.DoesNotExist:
		return render(request, 'ui/error.html', { "message": "The specified project does not exist" })

	# Get file set
	try:
		fileset = ProjectFiles.objects.get(id=revision)
	except ProjectFiles.DoesNotExist:
		return render(request, 'ui/error.html', { "message": "The specified fileset does not exist" })

	# Validate fileset
	if fileset.project != project:
		return render(request, 'ui/error.html', { "message": "The specified fileset does belong to your project" })

	# Update
	fileset.status = ProjectFiles.STAGING
	fileset.save()

	# Redirect to project management
	return redirect(reverse("project.manage", kwargs={ 'project': project.uuid }))

def manage(request, project):
	"""
	The project management interface
	"""

	# In-page error message
	error = ""

	# Lookup project
	try:
		project = Project.objects.get(uuid=project)
	except Project.DoesNotExist:
		return render(request, 'ui/error.html', { "message": "The specified project does not exist" })
	
	# If we have a POST request, update the appropriate form	
	if request.method == 'POST':

		# Check the form to initialize
		file_name = request.GET.get('form', None)

		# Handle Upload
		if (file_name == "import-upload") and ('file' in request.FILES):

			# Handle file upload to the voluto project
			try:
				files.handle_tarball_upload( project, request.FILES['file'] )
			except files.UploadError as e:
				error = e.message

		# Hangle GIT
		elif file_name == "import-git":
			pass


	# Update 
	return render(request, 'ui/project/manage.html', 
		{
			'error': error,

			# Project and it's files
			'project': project,
			'files': ProjectFiles.objects.filter(project=project).order_by('-number'),

			# Feedback forms
			'forms': {
			},

			# Groups
			'groups': [

				{
					'id': 'databridge',
					'title': '<i class="fa fa-rocket"></i> Databridge API',
					'color': 1,
					'form': DatabridgeForm(),
					'link_enable': 'queue-databridge',
					'environment': [
						{ 'name': 'DB_DOMAIN', 'description': 'The databridge domain.' },
						{ 'name': 'DB_USER', 'description': 'The username for the databridge queue.' },
						{ 'name': 'DB_PASSWORD', 'description': 'The password for te databridge queue.' },
					]
				},
				{
					'id': 'creditpiggy',
					'title': '<i class="fa fa-rocket"></i> CreditPiggy API',
					'color': 1,
					'form': OpenstackForm(),
					'environment': [
						{ 'name': 'DB_DOMAIN', 'description': 'The databridge domain.' },
						{ 'name': 'DB_USER', 'description': 'The username for the databridge queue.' },
						{ 'name': 'DB_PASSWORD', 'description': 'The password for te databridge queue.' },
					]
				},

				{
					'id': 'script-init',
					'title': '<i class="fa fa fa-cog"></i> Initialization Script',
					'color': 2,
					'description': 'This sript is executed after the job environment is initialized and ready to start.',
					'form': ScriptInitForm(),
				},

				{
					'id': 'queue-none',
					'title': '<i class="fa fa-hourglass-half"></i> No Queue Logic',
					'color': 3,
					'form': NoQueueForm(),
					'radiogroup': 'queue'
				},

				{
					'id': 'queue-databridge',
					'title': '<i class="fa fa-hourglass-half"></i> Databridge Queue Logic',
					'color': 3,
					'description': 'The databridge queue logic will call the specified handling application when a new job arrives. The job should exit upon successful completion of it\'s task.',
					'form': DatabridgeQueueForm(),
					'radiogroup': 'queue',
					'environment': [
						{ 'name': 'DB_JOB', 'description': 'The full path to a file containing the contents of the incoming job description.' },
					]
				},

				{
					'id': 'queue-copilot',
					'title': '<i class="fa fa-hourglass-half"></i> Co-Pilot Queue Logic',
					'color': 3,
					'description': 'The co-pilot will set-up and run a co-pilot agent that will be responsible for downloading and executing the jobs.',
					'form': CopilotQueueForm(),
					'radiogroup': 'queue',
				},

				{
					'id': 'script-teardown',
					'title': '<i class="fa fa fa-cog"></i> Teardown Script',
					'color': 2,
					'description': 'This sript is executed when the job is completed and it is about to cleanup.',
					'form': ScriptTeardownForm(),
				},

			]
		}
	)
