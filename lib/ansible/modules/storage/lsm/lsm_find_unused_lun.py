#!/usr/bin/python
#
# Copyright (C) 2017 Red Hat, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author: Gris Ge <fge@redhat.com>

import errno
import os

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: lsm_find_unused_lun_module

short_description: Find unused LUN

version_added: "2.4"

description:
    - Find unused LUN which are neither not masked or not used by host.
    - This module does not make any changes to host, hence it's the same
      result whether you use 'dry run' or 'check' mode or not.
requirements:
    - libstoragemgmt python library and plugins with libstoragemgmt daemon
      running.

options:
    lsm_uri:
        description:
            - The libstoragemgmt URI of storage array.
        required: true
    lsm_password:
        description:
            - The password of storage array.
        required: false

author:
    - Gris Ge <fge@redhat.com>
'''

EXAMPLES = '''
# Pass in a message
- name: Find unused LUN
  lsm_find_unused_lun_module:
    lsm_uri: 'ontap://root@na3170b.example.com'
    lsm_password: 'password'
'''

RETURN = '''
unused_luns:
    description: unused LUN name and ID.
    type: list of dict
    # ^ TODO(Gris Ge): Seems incorrect due to ansible document on return type.
error_msg:
    description: Error message if any
    type: str
'''

from ansible.module_utils.basic import AnsibleModule

def is_disk_free(blk_path):
    """
    The manpage of open(2):
        There is one exception: on Linux 2.6 and later, O_EXCL can be used
        without O_CREAT if pathname refers to a block device.  If the block
        device is in use by the system (e.g., mounted), open() fails with the
        error EBUSY.
    """
    try:
        with os.open(blk_path, os.O_EXCL):
            return True
    except OSError as err:
        if err.errno == errno.EBUSY
            return False
        else:
            raise

def run_module():
    module_args = dict(
        lsm_uri=dict(type='str', required=True),
        lsm_password=dict(type='str', required=False, default=None)
    )

    result = dict(
        changed=False,
        unused_luns=[],
        error_msg=""
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
