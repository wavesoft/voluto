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

from django.conf.urls import patterns, include, url
from voluto.ui.views import home, project

urlpatterns = patterns('',

	# Landing page
	url(r'^$', 											home.landing, 			name="home.landing"),

	# Project management
	url(r'^project/list$', 								
		project.list, 			name="project.list"),
	url(r'^project/manage/(?P<project>[^/]+)/$', 		
		project.manage, 		name="project.manage"),
	url(r'^project/manage/(?P<project>[^/]+)/publish/(?P<revision>[^/]+)/$',
		project.manage_publish,	name="project.manage.publish"),

)
