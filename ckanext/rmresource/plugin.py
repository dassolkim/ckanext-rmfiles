import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.common import config

import ckan.lib.uploader as uploader
import os
import logging
import requests
import json

log = logging.getLogger(__name__)

def dsfile_remove(id):

    # id = data_dict.get('id')

    # your ckan host url + apiname

    url = 'ckan_host_url'

    # fill in your platform information
    headers = {'Content-Type': 'application/json', 'Authorization': 'apikey'}
    data = {'resource_id': id, 'force': True}
    response = requests.post(url=url, headers=headers, data=json.dumps(data))
    log.debug('Delete {0} resource in Datastore'.format(id))


def file_remove(resource_id):

    # resource_id = data_dict.get('resource_id')
    storage_path = uploader.get_storage_path()
    directory = os.path.join(storage_path, 'resources', resource_id[0:3], resource_id[3:6])
    filepath = os.path.join(directory, resource_id[6:])

    try:
        os.remove(filepath)
        log.info('remove filepath {0}'.format(filepath))
        os.removedirs(directory)
        log.info('remove directory {0}'.format(directory))
        log.debug('Delete {0} resource in Filestore'.format(resource_id))

    except OSError, e:
        log.debug(u'Error: %s - %s.' % (e.filename, e.strerror))
        pass

class RmresourcePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IResourceController, inherit=True)

    def before_delete(context, data_dict, resource, resources):
        file_remove(resource['id'])
        dsfile_remove(resource['id'])

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'rmresource')