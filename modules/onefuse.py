#!/usr/bin/python

DOCUMENTATION = '''
---
module: OneFuse
short_description: OneFuse module for Ansible.  This module enables consumption of OneFuse integrations by Ansible.
'''
EXAMPLES = '''
- name: OneFuse Get Name
  hosts: localhost
  gather_facts: false
   tasks:
  - name: Get Machine Name
    onefuse:
      policy_name: '{{ policy_name }}'
      module: naming
      state: present
      tracking_id: '{{ tracking_id  | default(omit) }}'
      template_properties: '{{ template_properties }}'
    delegate_to: localhost
    register: output
  - name: Output Results
    debug:
      msg: '{{ output }}'

- name: OneFuse Release Name
  hosts: '{{ ansible_hosts }}'
  gather_facts: false
  tasks:
  - name: Deprovision Name
    onefuse:
      object_name: '{{ onefuse_name_id | default(omit) }}'
      module: naming
      state: absent
    delegate_to: localhost
    register: output
  - name: Output Results
    debug:
      msg: '{{ output }}'

- name: OneFuse Get IPAM
    hosts: localhost
    gather_facts: false
    tasks:
  - name: Get IP Address
    onefuse:
      policy_name: '{{ policy_name }}'
      module: ipam
      state: present
      name: '{{ name }}'
      tracking_id: '{{ tracking_id | default(omit) }}'
      template_properties: '{{ template_properties }}'
    register: output
  - name: Output Results
    debug:
      msg: '{{ output }}'

- name: OneFuse Release IPAM
    hosts: '{{ ansible_hosts }}'
    gather_facts: false
    tasks:
    - name: Reclaim IP Address
      onefuse:
        object_name: '{{ onefuse_ipam_id | default(omit) }}'
        module: ipam
        state: absent
      delegate_to: localhost
      register: output
    - name: Output Results
      debug:
        msg: '{{ output }}'

- name: OneFuse Create DNS Record
    hosts: localhost
    gather_facts: false
    tasks:
    - name: Register DNS
        onefuse:
          policy_name: '{{ policy_name }}'
          module: dns
          state: present
          name: '{{ name }}'
          value: '{{ ip_address }}'
          zones: '{{ name_suffix }}'
          tracking_id: '{{ tracking_id | default(omit) }}'
          template_properties: '{{ template_properties }}'
        delegate_to: localhost
        register: output
        - name: Output Results
        debug:
          msg: '{{ output }}'

- name: OneFuse Release DNS Record
    hosts: '{{ ansible_hosts }}'
    gather_facts: false
    tasks:
    - name: Remove DNS Record
      onefuse:
        object_name: '{{ onefuse_dns_id | default(omit) }}'
        module: dns
        state: absent
      delegate_to: localhost
      register: output
      - name: Output Results
        debug:
          msg: '{{ output }}'

    - name: AD Create
      hosts: localhost
      gather_facts: false
      tasks:
      - name: Create AD Record
        onefuse:
          policy_name: '{{ policy_name }}'
          module: ad
          state: present
          name: '{{ name }}'
          tracking_id: '{{ tracking_id  | default(omit) }}'
          template_properties: '{{ template_properties }}'
        register: output
      - name: Output Results
        debug:
          msg: '{{ output }}'

    - name: AD
      hosts: '{{ ansible_hosts }}'
      gather_facts: false
      tasks:
      - name: Deprovision Ad Computer Object
        onefuse:
          object_name: '{{ onefuse_ad_id | default(omit) }}'
          module: ad
          state: absent
        delegate_to: localhost
        register: output
      - name: Output Results
        debug:
          msg: '{{ output }}'

- name: OneFuse Scripting provision
    hosts: localhost
    gather_facts: false
    tasks:
      - name: Execute Script
        onefuse:
          policy_name: '{{ policy_name }}'
          module: scripting
          state: present
          tracking_id: '{{ tracking_id  | default(omit) }}'
          template_properties: {{ template_properties }}
        delegate_to: localhost
        register: output
      - name: Output Results
        debug:
          msg: '{{ output }}'

- name: OneFuse Scripting desprovision
    hosts: '{{ ansible_host }}'
    gather_facts: false
    tasks:
    - name: Deprovision Script Deployment
      onefuse:
        object_name: '{{ onefuse_script_id | default(omit) }}'
        module: scripting
        state: absent
      delegate_to: localhost
      register: output
    - name: Output Results
      debug:
        msg: '{{ output }}'

- name: Create ServiceNow CMDB Record
    hosts: localhost
    gather_facts: false
    tasks:
    - name: Create CMDB CI Record
      onefuse:
      policy_name: '{{ policy_name }}'
      module: cmdb
      state: present
      tracking_id: '{{ tracking_id  | default(omit) }}'
      template_properties: {{ template_properties }}
      delegate_to: localhost
      register: output
    - name: Output Results
      debug:
        msg: '{{ output }}'

- name: Remove ServiceNow CMDB Record
    hosts: '{{ ansible_hosts }}'
    gather_facts: false
    tasks:
    - name: Remove CMDB Record
      onefuse:
        object_name: '{{ onefuse_cmdb_id | default(omit) }}'
        module: cmdb
        state: absent
      delegate_to: localhost
      register: output
    - name: Output Results
      debug:
      msg: '{{ output }}'

- name: OneFuse Ansible Tower Provision
  hosts: localhost
  gather_facts: false
  tasks:
  - name: Run Ansible Tower Playbook
    onefuse:
      policy_name: '{{ policy_name }}'
      module: ansible_tower
      state: present
      limit: ''
      hosts: ''
      tracking_id: '{{ tracking_id  | default(omit) }}'
      template_properties: {{ template_properties }}
    delegate_to: localhost
    register: output
  - name: Output Results
    debug:
      msg: '{{ output }}'

- name: OneFuse Ansible Tower Deprovision
  hosts: '{{ ansible_hosts }}'
  gather_facts: false
  tasks:
  - name: Remove Ansible Tower Object
    onefuse:
      object_name: '{{ onefuse_ansible_id | default(omit) }}'
      module: ansible_tower
      state: absent
    delegate_to: localhost
    register: output
  - name: Output Results
    debug:
      msg: '{{ output }}'      

- name: Deploy vRA Blueprint
    hosts: localhost
    gather_facts: false
    tasks:
    - name: Deploy vRA Blueprint
      onefuse:
        policy_name: '{{ policy_name }}'
        deployment_name: '{{ deployment_name }}'
        module: vra
        state: present
        tracking_id: '{{ tracking_id  | default(omit) }}'
        template_properties: {{ template_properties }}
      register: output
    - name: Output Results
      debug:
        msg: '{{ output }}'

- name: Destroy vRA Blueprint
    hosts: '{{ ansible_host }}'
    gather_facts: false
    tasks:
  - name: Deprovision vRA Deployment
    onefuse:
      object_name: '{{ onefuse_vra_id | default(omit) }}'
      module: vra
      state: absent
    delegate_to: localhost
    register: output
  - name: Output Results
    debug:
      msg: '{{ output }}'

'''


import json
from ansible.module_utils.basic import *
from onefuse.admin import OneFuseManager
from ansible.module_utils.onefuse.config import username, password, host
import sys
from os import path
ROOT_PATH = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
sys.path.append(ROOT_PATH)

#OneFuse Module main function

def main():

  onefuse_inputs = {
    "policy_name": {"required": False, "type": "str"},
    "template_properties": {"required": False, "type": "dict"},
    "tracking_id": {"required": False, "type": "str"},
    "object_name": {"required": False, "type": "str"},
    "object_id": {"required": False, "type": "int"},
    "module": {"required": False, "type": "str"},
    "value": {"required": False, "type": "str"},
    "name": {"required": False, "type": "str"},
    "zones": {"required": False, "type": "list"},
    "limit": {"required": False, "type": "str"},
    "hosts": {"required": False, "type": "str"},
    "deployment_name": {"required": False, "type": "str"},    
    "state": {"required": False, "type": "str"}
  }

  module = AnsibleModule(argument_spec=onefuse_inputs)
  ofm = OneFuseManager(username, password, host, source='Ansible')

  if module.params['module'] == 'ipam':
    ipam(module, ofm, onefuse_inputs, resource_path="ipamReservations", unique_field="id")
  elif module.params['module'] == 'naming':
    naming(module, ofm, onefuse_inputs, resource_path="customNames", unique_field="id")
  elif module.params['module'] == 'dns':
    dns(module, ofm, onefuse_inputs, resource_path="dnsReservations", unique_field="id")
  elif module.params['module'] == 'ad':
    ad(module, ofm, onefuse_inputs, resource_path="microsoftADComputerAccounts", unique_field="id")
  elif module.params['module'] == 'scripting':
    scripting(module, ofm, onefuse_inputs, resource_path="scriptingDeployments", unique_field="id")
  elif module.params['module'] == 'cmdb':
    cmdb(module, ofm, onefuse_inputs, resource_path="servicenowCMDBDeployments", unique_field="id")
  elif module.params['module'] == 'ansible_tower':
    ansible_tower(module, ofm, onefuse_inputs, resource_path="ansibleTowerDeployments", unique_field="id")
  elif module.params['module'] == 'vra':
    vra(module, ofm, onefuse_inputs, resource_path="vraDeployments", unique_field="id")
  elif module.params['module'] == 'pluggable':
    pluggable_module(module, ofm, onefuse_inputs, resource_path="moduleManagedObjects", unique_field="id")
  elif module.params['module'] == 'property_toolkit':
    property_toolkit(module, ofm, onefuse_inputs)
  else:
    print("A OneFuse Module with the name " + module.params['module'] + " does not exists!")

# OneFuse Naming Module

def naming(module, ofm, onefuse_inputs, resource_path, unique_field):
  """
  - name: OneFuse Get Name
    hosts: localhost
    gather_facts: false
    tasks:
    - name: Get Machine Name
      onefuse:
        policy_name: '{{ policy_name }}'
        module: naming
        state: present
        tracking_id: '{{ tracking_id  | default(omit) }}'
        template_properties: '{{ template_properties }}'
      delegate_to: localhost
      register: output
    - name: Output Results
      debug:
        msg: '{{ output }}'


    - name: OneFuse Release Name
      hosts: '{{ ansible_hosts }}'
      gather_facts: false
      tasks:
      - name: Deprovision Name
      onefuse:
        object_name: '{{ onefuse_name_id | default(omit) }}'
        module: naming
        state: absent
      delegate_to: localhost
      register: output
    - name: Output Results
      debug:
        msg: '{{ output }}'
  """
  def present(module, ofm, onefuse_inputs):
 
    try:
      response_json = ofm.provision_naming(policy_name=module.params['policy_name'], template_properties=module.params['template_properties'], 
                tracking_id=module.params['tracking_id'])
    except Exception as err:
      create_exception(module, onefuse_inputs, err)

    ansible_facts={ "onefuse_name": response_json }
    
    create_success(module, onefuse_inputs, response_json, ansible_facts)

  def absent(module, ofm, onefuse_inputs, resource_path, unique_field):

    try:
      onefuse_object = ofm.get_object_by_unique_field(resource_path=resource_path, field_value=module.params["object_name"], field=unique_field)  
    except Exception as err:
      remove_exception(module, onefuse_inputs, err)

    remove_success(module, ofm, onefuse_inputs, resource_path, onefuse_object)

  try:
    if module.params['state'] == 'absent':
      absent(module, ofm, onefuse_inputs, resource_path, unique_field)
    else:  
      present(module, ofm, onefuse_inputs)
      module.exit_json(changed=True, path=path)
  except Exception as e:
    module.fail_json(msg=to_native(e), exception="exception")  

# OneFuse IPAM Module

def ipam(module, ofm, onefuse_inputs, resource_path, unique_field):
  """
  - name: OneFuse Get IPAM
    hosts: localhost
    gather_facts: false
    tasks:
  - name: Get IP Address
    onefuse:
      policy_name: '{{ policy_name }}'
      module: ipam
      state: present
      name: '{{ name }}'
      tracking_id: '{{ tracking_id | default(omit) }}'
      template_properties: '{{ template_properties }}'
    register: output
  - name: Output Results
    debug:
      msg: '{{ output }}'


  - name: OneFuse Release IPAM
    hosts: '{{ ansible_hosts }}'
    gather_facts: false
    tasks:
    - name: Reclaim IP Address
      onefuse:
        object_name: '{{ onefuse_ipam_id | default(omit) }}'
        module: ipam
        state: absent
      delegate_to: localhost
      register: output
    - name: Output Results
      debug:
        msg: '{{ output }}'
  """

  def present(module, ofm, onefuse_inputs):
    try:
      response_json = ofm.provision_ipam(policy_name=module.params['policy_name'], template_properties=module.params['template_properties'], 
            hostname=module.params['name'], tracking_id=module.params['tracking_id'])
    except Exception as err:
      create_exception(module, onefuse_inputs, err)

    ansible_facts={ "onefuse_ipam": response_json }


    create_success(module, onefuse_inputs, response_json, ansible_facts)

  def absent(module, ofm, onefuse_inputs, resource_path, unique_field):

    try:
      onefuse_object = ofm.get_object_by_unique_field(resource_path=resource_path, field_value=module.params["object_name"], field=unique_field)  
    except Exception as err:
      remove_exception(module, onefuse_inputs, err)    
    
    remove_success(module, ofm, onefuse_inputs, resource_path, onefuse_object)
    
  try:
    if module.params['state'] == 'absent':
      absent(module, ofm, onefuse_inputs, resource_path, unique_field)
    else:  
      present(module, ofm, onefuse_inputs)
    module.exit_json(changed=True, path=path)
  except Exception as e:
      module.fail_json(msg=to_native(e), exception="exception")

# OneFuse DNS Module

def dns(module, ofm, onefuse_inputs, resource_path, unique_field):
  """
  - name: OneFuse Create DNS Record
    hosts: localhost
    gather_facts: false
    tasks:
  -   name: Register DNS
      onefuse:
        policy_name: '{{ policy_name }}'
        module: dns
        state: present
        name: '{{ name }}'
        value: '{{ ip_address }}'
        zones: '{{ name_suffix }}'
        tracking_id: '{{ tracking_id | default(omit) }}'
        template_properties: '{{ template_properties }}'
      delegate_to: localhost
      register: output
      - name: Output Results
        debug:
          msg: '{{ output }}'


  - name: OneFuse Release DNS Record
    hosts: '{{ ansible_hosts }}'
    gather_facts: false
    tasks:
    - name: Remove DNS Record
      onefuse:
        object_name: '{{ onefuse_dns_id | default(omit) }}'
        module: dns
        state: absent
      delegate_to: localhost
      register: output
      - name: Output Results
        debug:
          msg: '{{ output }}'
  """

  def present(module, ofm, onefuse_inputs):
    try:
      response_json = ofm.provision_dns(policy_name=module.params['policy_name'], template_properties=module.params['template_properties'], 
            name=module.params['name'], value=module.params['value'], zones=module.params['zones'], tracking_id=module.params['tracking_id'])
    except Exception as err:
      create_exception(module, onefuse_inputs, err)

    ansible_facts={ "onefuse_dns": response_json }

    create_success(module, onefuse_inputs, response_json, ansible_facts)
    
  def absent(module, ofm, onefuse_inputs, resource_path, unique_field):

    try:
       onefuse_object = ofm.get_object_by_unique_field(resource_path=resource_path, field_value=module.params["object_name"], field=unique_field)  
    except Exception as err:
      remove_exception(module, onefuse_inputs, err)    
    
    remove_success(module, ofm, onefuse_inputs, resource_path, onefuse_object)

  try:
    if module.params['state'] == 'absent':
      absent(module, ofm, onefuse_inputs, resource_path, unique_field)
    else:  
      present(module, ofm, onefuse_inputs)
    module.exit_json(changed=True, path=path)
  except Exception as e:
      module.fail_json(msg=to_native(e), exception="DNS State Failure")

# OneFuse AD Module

def ad(module, ofm, onefuse_inputs, resource_path, unique_field):

  """
    - name: AD Create
      hosts: localhost
      gather_facts: false
      tasks:
      - name: Create AD Record
        onefuse:
          policy_name: '{{ policy_name }}'
          module: ad
          state: present
          name: '{{ name }}'
          tracking_id: '{{ tracking_id  | default(omit) }}'
          template_properties: '{{ template_properties }}'
        register: output
      - name: Output Results
        debug:
          msg: '{{ output }}'

    - name: AD
      hosts: '{{ ansible_hosts }}'
      gather_facts: false
      tasks:
      - name: Deprovision Ad Computer Object
        onefuse:
          object_name: '{{ onefuse_ad_id | default(omit) }}'
          module: ad
          state: absent
        delegate_to: localhost
        register: output
      - name: Output Results
        debug:
          msg: '{{ output }}'
  """

  def present(module, ofm, onefuse_inputs):

    try:
      response_json = ofm.provision_ad(policy_name=module.params['policy_name'], template_properties=module.params['template_properties'], 
              name=module.params['name'], tracking_id=module.params['tracking_id'])
    except Exception as err:
      create_exception(module, onefuse_inputs, err)

    ansible_facts={ "onefuse_ad": response_json }

    create_success(module, onefuse_inputs, response_json, ansible_facts)

  def absent(module, ofm, onefuse_inputs, resource_path, unique_field):

    try:
      onefuse_object = ofm.get_object_by_unique_field(resource_path=resource_path, field_value=module.params["object_name"], field=unique_field)  
    except Exception as err:
      remove_exception(module, onefuse_inputs, err)    
    
    remove_success(module, ofm, onefuse_inputs, resource_path, onefuse_object)
  
  def final_ou(module, ofm, onefuse_inputs):

    try:
      response_json = ofm.move_ou(module.params["object_id"])
    except Exception as err:
      create_exception(module, onefuse_inputs, err)

    ansible_facts={ "ad_ou": response_json}

    create_success(module, onefuse_inputs, response_json, ansible_facts)

  try:
    if module.params['state'] == 'absent':
      absent(module, ofm, onefuse_inputs, resource_path, unique_field)
    elif module.params['state'] == 'present':
      present(module, ofm, onefuse_inputs)
    elif module.params['state'] == 'final_ou':
      final_ou(module, ofm, onefuse_inputs)
    else:
      print("A OneFuse State with the name " + module.params['module'] + " does not exists!")
    module.exit_json(changed=True, path=path)
  except Exception as e:
      module.fail_json(msg=to_native(e), exception="exception")

# OneFuse Scripting Module

def scripting(module, ofm, onefuse_inputs, resource_path, unique_field):

  """
  - name: OneFuse Scripting provision
    hosts: localhost
    gather_facts: false
    tasks:
      - name: Execute Script
        onefuse:
          policy_name: '{{ policy_name }}'
          module: scripting
          state: present
          tracking_id: '{{ tracking_id  | default(omit) }}'
          template_properties: {{ template_properties }}
        delegate_to: localhost
        register: output
      - name: Output Results
        debug:
          msg: '{{ output }}'

  - name: OneFuse Scripting desprovision
    hosts: '{{ ansible_host }}'
    gather_facts: false
    tasks:
    - name: Deprovision Script Deployment
      onefuse:
        object_name: '{{ onefuse_script_id | default(omit) }}'
        module: scripting
        state: absent
      delegate_to: localhost
      register: output
    - name: Output Results
      debug:
        msg: '{{ output }}'
  """

  def present(module, ofm, onefuse_inputs):

    try:
      response_json = ofm.provision_scripting(policy_name=module.params['policy_name'], template_properties=module.params['template_properties'], 
              tracking_id=module.params['tracking_id'])
    except Exception as err:
      create_exception(module, onefuse_inputs, err)

    ansible_facts={ "onefuse_script": response_json }
    
    create_success(module, onefuse_inputs, response_json, ansible_facts)

  def absent(module, ofm, onefuse_inputs, resource_path, unique_field):

    try:
      onefuse_object = ofm.get_object_by_unique_field(resource_path=resource_path, field_value=module.params["object_name"], field=unique_field)  
    except Exception as err:
      remove_exception(module, onefuse_inputs, err)    
    
    remove_success(module, ofm, onefuse_inputs, resource_path, onefuse_object)
    
  try:
    if module.params['state'] == 'absent':
      absent(module, ofm, onefuse_inputs, resource_path, unique_field)
    else:  
      present(module, ofm, onefuse_inputs)
    module.exit_json(changed=True, path=path)
  except Exception as e:
      module.fail_json(msg=to_native(e), exception="exception")

# OneFuse CMDB Module

def cmdb(module, ofm, onefuse_inputs, resource_path, unique_field):

  """
  - name: Create ServiceNow CMDB Record
    hosts: localhost
    gather_facts: false
    tasks:
  - name: Create CMDB CI Record
    onefuse:
     policy_name: '{{ policy_name }}'
     module: cmdb
     state: present
     tracking_id: '{{ tracking_id  | default(omit) }}'
     template_properties: {{ template_properties }}
    delegate_to: localhost
    register: output
  - name: Output Results
    debug:
      msg: '{{ output }}'

  - name: OneFuse CMDB
  hosts: '{{ ansible_hosts }}'
  gather_facts: false
  tasks:
  - name: Remove CMDB Record
    onefuse:
      object_name: '{{ onefuse_cmdb_id | default(omit) }}'
      module: cmdb
      state: absent
    delegate_to: localhost
    register: output
  - name: Output Results
    debug:
      msg: '{{ output }}'
  """
  def present(module, ofm, onefuse_inputs):

    try:
      response_json = ofm.provision_cmdb(policy_name=module.params['policy_name'], template_properties=module.params['template_properties'], 
              tracking_id=module.params['tracking_id'])
    except Exception as err:
      create_exception(module, onefuse_inputs, err)

    ansible_facts={ "onefuse_cmdb": response_json }

    create_success(module, onefuse_inputs, response_json, ansible_facts)

  def absent(module, ofm, onefuse_inputs, resource_path, unique_field):

    try:
      onefuse_object = ofm.get_object_by_unique_field(resource_path=resource_path, field_value=module.params["object_name"], field=unique_field)  
    except Exception as err:
      remove_exception(module, onefuse_inputs, err)    
    
    remove_success(module, ofm, onefuse_inputs, resource_path, onefuse_object)
    
  try:
    if module.params['state'] == 'absent':
      absent(module, ofm, onefuse_inputs, resource_path, unique_field)
    else:  
      present(module, ofm, onefuse_inputs)
  except Exception as e:
      module.fail_json(msg=to_native(e), exception="CMDB State Error")

# OneFuse Ansible Module

def ansible_tower(module, ofm, onefuse_inputs, resource_path, unique_field):

  """
  - name: OneFuse Ansible Tower Provision
  hosts: localhost
  gather_facts: false
  tasks:
  - name: Run Ansible Tower Playbook
    onefuse:
      policy_name: '{{ policy_name }}'
      module: ansible_tower
      state: present
      limit: ''
      hosts: ''
      tracking_id: '{{ tracking_id  | default(omit) }}'
      template_properties: {{ template_properties }}
    delegate_to: localhost
    register: output
  - name: Output Results
    debug:
      msg: '{{ output }}'

  - name: OneFuse Ansible Tower Deprovision
  hosts: '{{ ansible_hosts }}'
  gather_facts: false
  tasks:
  - name: Remove Ansible Tower Object
    onefuse:
      object_name: '{{ onefuse_ansible_id | default(omit) }}'
      module: ansible_tower
      state: absent
    delegate_to: localhost
    register: output
  - name: Output Results
    debug:
      msg: '{{ output }}'
  """

  def present(module, ofm, onefuse_inputs):

    try:
      response_json = ofm.provision_ansible_tower(policy_name=module.params['policy_name'], 
          template_properties=module.params['template_properties'], hosts=module.params['hosts'], 
          limit=module.params['limit'], tracking_id=module.params['tracking_id'])
    except Exception as err:
      create_exception(module, onefuse_inputs, err)

    ansible_facts={ "onefuse_ansible_tower": response_json }
    
    create_success(module, onefuse_inputs, response_json, ansible_facts)

  def absent(module, ofm, onefuse_inputs, resource_path, unique_field):

    try:
      onefuse_object = ofm.get_object_by_unique_field(resource_path=resource_path, field_value=module.params["object_name"], field=unique_field)  
    except Exception as err:
      remove_exception(module, onefuse_inputs, err)    
    
    remove_success(module, ofm, onefuse_inputs, resource_path, onefuse_object)
    
  try:
    if module.params['state'] == 'absent':
      absent(module, ofm, onefuse_inputs, resource_path, unique_field)
    else:  
      present(module, ofm, onefuse_inputs)
    module.exit_json(changed=True, path=path)
  except Exception as e:
      module.fail_json(msg=to_native(e), exception="Ansible State Error")

# OneFuse VRA Module

def vra(module, ofm, onefuse_inputs, resource_path, unique_field):

  """
  - name: Deploy vRA Blueprint
    hosts: localhost
    gather_facts: false
    tasks:
    - name: Deploy vRA Blueprint
      onefuse:
        policy_name: '{{ policy_name }}'
        deployment_name: '{{ deployment_name }}'
        module: vra
        state: present
        tracking_id: '{{ tracking_id  | default(omit) }}'
        template_properties: {{ template_properties }}
      register: output
    - name: Output Results
      debug:
        msg: '{{ output }}'

  - name: Destroy vRA Blueprint
    hosts: '{{ ansible_host }}'
    gather_facts: false
    tasks:
  - name: Deprovision vRA Deployment
    onefuse:
      object_name: '{{ onefuse_vra_id | default(omit) }}'
      module: vra
      state: absent
    delegate_to: localhost
    register: output
  - name: Output Results
    debug:
      msg: '{{ output }}'
  """

  def present(module, ofm, onefuse_inputs):

    try:
      response_json = ofm.provision_vra(policy_name=module.params['policy_name'], template_properties=module.params['template_properties'], 
              deployment_name=module.params['deployment_name'], tracking_id=module.params['tracking_id'])
    except Exception as err:
      create_exception(module, onefuse_inputs, err)

    ansible_facts={ "onefuse_vra": response_json }
    
    create_success(module, onefuse_inputs, response_json, ansible_facts)

  def absent(module, ofm, onefuse_inputs, resource_path, unique_field):

    try:
      onefuse_object = ofm.get_object_by_unique_field(policy_path=resource_path, field_value=module.params["object_name"], field=unique_field)  
    except Exception as err:
      remove_exception(module, onefuse_inputs, err)    
    
    remove_success(module, ofm, onefuse_inputs, resource_path, onefuse_object)
    
  try:
    if module.params['state'] == 'absent':
      absent(module, ofm, onefuse_inputs, resource_path, unique_field)
    else:  
      present(module, ofm, onefuse_inputs)
    module.exit_json(changed=True, path=path)
  except Exception as e:
      module.fail_json(msg=to_native(e), exception="vRA State Error")

# OneFuse Pluggable Module

def pluggable_module(module, ofm, onefuse_inputs, resource_path, unique_field):

  def present(module, ofm, onefuse_inputs):
 
    try:
      response_json = ofm.provision_module(policy_name=module.params['policy_name'], template_properties=module.params['template_properties'], 
                tracking_id=module.params['tracking_id'])
    except Exception as err:
      create_exception(module, onefuse_inputs, err)

    ansible_facts={ "onefuse_pluggable": response_json }
    
    create_success(module, onefuse_inputs, response_json, ansible_facts)

  def absent(module, ofm, onefuse_inputs, resource_path, unique_field):

    try:
      onefuse_object = ofm.get_object_by_unique_field(resource_path=resource_path, field_value=module.params["object_name"], field=unique_field)  
    except Exception as err:
      remove_exception(module, onefuse_inputs, err)    

    remove_success(module, ofm, onefuse_inputs, resource_path, onefuse_object)

  try:
    if module.params['state'] == 'absent':
      absent(module, ofm, onefuse_inputs, resource_path, unique_field)
    else:  
      present(module, ofm, onefuse_inputs)
      module.exit_json(changed=True, path=path)
  except Exception as e:
    module.fail_json(msg=to_native(e), exception="exception")

# Create Tracking ID

def create_tracking_id(module, ofm):

  """
  - name: Deploy vRA Blueprint
    hosts: localhost
    gather_facts: false
    tasks:
    - name: Deploy vRA Blueprint
      onefuse:
        policy_name: '{{ policy_name }}'
        deployment_name: '{{ deployment_name }}'
        module: vra
        state: present
        tracking_id: '{{ tracking_id  | default(omit) }}'
        template_properties: {{ template_properties }}
      register: output
    - name: Output Results
      debug:
        msg: '{{ output }}'

  - name: Destroy vRA Blueprint
    hosts: '{{ ansible_host }}'
    gather_facts: false
    tasks:
  - name: Deprovision vRA Deployment
    onefuse:
      object_name: '{{ onefuse_vra_id | default(omit) }}'
      module: vra
      state: absent
    delegate_to: localhost
    register: output
  - name: Output Results
    debug:
      msg: '{{ output }}'
  """

  def present(module, ofm):

    tracking_id = ofm.create_tracking_id()
 

    ansible_facts={ "tracking_id": tracking_id }
    
    create_success(module, onefuse_inputs, response_json, ansible_facts)

  def absent(module, ofm, onefuse_inputs, resource_path, unique_field):

    try:
      onefuse_object = ofm.get_object_by_unique_field(policy_path=resource_path, field_value=module.params["object_name"], field=unique_field)  
    except Exception as err:
      remove_exception(module, onefuse_inputs, err)    
    
    remove_success(module, ofm, onefuse_inputs, resource_path, onefuse_object)
    
  try:
    if module.params['state'] == 'absent':
      absent(module, ofm)
    else:  
      present(module, ofm)
    module.exit_json(changed=True, path=path)
  except Exception as e:
      module.fail_json(msg=to_native(e), exception="exception")

#Render OneFuse Property Sets

def property_toolkit(module, ofm, onefuse_inputs):
 
    try:
      response_json = ofm.resolve_properties(module.params['template_properties'])
    except Exception as err:
      create_exception(module, onefuse_inputs, err)

    ansible_facts={ "rendered_properties": response_json }
    
    response=response_json
    changed = True

    result = dict(
      changed=changed,
      original_message='',
      message='No Change'
    )

    module = AnsibleModule(
      argument_spec=onefuse_inputs,
      supports_check_mode=True
    )

    if module.check_mode:
      module.exit_json(**result)

    result['original_message'] = ''
    result['message'] = f' OneFuse {module.params["module"]} properties rendered {response_json}'

    if response_json:
      result['changed'] = changed

    module.exit_json(changed=changed, response=result, ansible_facts=ansible_facts)

# OneFuse Managed object for module does not exists

def remove_exception(module, onefuse_inputs, error):
  result = dict(
  changed=False,
  original_message='',
  message='No Change'
  )

  module = AnsibleModule(
  argument_spec=onefuse_inputs,
  supports_check_mode=True
  )

  if module.check_mode:
    module.exit_json(**result)

  result['original_message'] = ""
  result['message'] = f'OneFuse {module.params["module"]} object with id {module.params["object_name"]} does not exist'
  result['changed'] = False
  module.fail_json(msg=to_native(error), exception="exception")

# OneFuse Managed object successfully removed

def remove_success(module, ofm, onefuse_inputs, resource_path, onefuse_object):
  path = f'/{resource_path}/{onefuse_object["id"]}/'
  response_json = ofm.deprovision_mo(path)
  print(f'response: {response_json}')

  result = dict(
    changed=False,
    original_message='',
    message='Changed'
  )

  module = AnsibleModule(
    argument_spec=onefuse_inputs,
    supports_check_mode=True
  )

  if module.check_mode:
    module.exit_json(**result)

  result['original_message'] = ""
  result['message'] = f'OneFuse {module.params["module"]} object with ID {module.params["object_name"]} Removed'
  result['changed'] = True

  module.exit_json(changed=True, response=result)

# OneFuse Managed object for module could not be created

def create_exception(module, onefuse_inputs, error):
  result = dict(
  changed=False,
  original_message='',
  message='No Change'
  )

  module = AnsibleModule(
  argument_spec=onefuse_inputs,
  supports_check_mode=True
  )

  if module.check_mode:
    module.exit_json(**result)

  result['original_message'] = ""
  result['message'] = f'OneFuse {module.params["module"]} could not create object.'
  result['changed'] = False
  module.fail_json(msg=to_native(error), exception="exception")

# OneFuse Managed object for module created successfully

def create_success(module, onefuse_inputs, response_json, ansible_facts):
  response=response_json
  changed = True

  result = dict(
    changed=changed,
    original_message='',
    message='No Change'
  )

  module = AnsibleModule(
    argument_spec=onefuse_inputs,
    supports_check_mode=True
  )

  if module.check_mode:
    module.exit_json(**result)

  result['original_message'] = ''
  result['message'] = f' OneFuse {module.params["module"]} object created {response_json}'

  if response_json["id"]:
    result['changed'] = changed

  module.exit_json(changed=changed, response=result, ansible_facts=ansible_facts)

if __name__ == "__main__":
    main()