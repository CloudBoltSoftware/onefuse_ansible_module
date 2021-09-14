#!/usr/bin/python

DOCUMENTATION = '''
---
module: version_change
short_description: bump semantic version numbers
'''
EXAMPLES = '''
- hosts: localhost
  tasks:
  - name: Test that my module works
    version_change: 
      version_name: "Before"
      version_no:  1.1.1 
      unchanged_value: "This will pass through"
    register: result
  - debug: var=result    
'''


import json
from ansible.module_utils.basic import *
from ansible.module_utils.onefuse.admin import OneFuseManager
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
  else:
    print("A OneFuse Module with the name " + module.params['module'] + " does not exists!")

# OneFuse Naming Module

def naming(module, ofm, onefuse_inputs, resource_path, unique_field):

  def present(module, ofm, onefuse_inputs):
 
    try:
      response_json = ofm.provision_naming(policy_name=module.params['policy_name'], template_properties=module.params['template_properties'], 
                tracking_id=module.params['tracking_id'])
    except:
      create_exception(module, onefuse_inputs)

    ansible_facts={ "onefuse_name": response_json, 
            "name": response_json["name"], "fqdn": f'{response_json["name"]}.{response_json["dnsSuffix"]}', "tracking_id":response_json["trackingId"], 
            "onefuse_name_id": response_json["id"], "name_suffix": response_json["dnsSuffix"] }
    
    create_success(module, onefuse_inputs, response_json, ansible_facts)

  def absent(module, ofm, onefuse_inputs, resource_path, unique_field):

    try:
      onefuse_object = ofm.get_object_by_unique_field(resource_path=resource_path, field_value=module.params["object_name"], field=unique_field)  
    except:
      remove_exception(module, onefuse_inputs)    

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

  def present(module, ofm, onefuse_inputs):

    response_json = ofm.provision_ipam(policy_name=module.params['policy_name'], template_properties=module.params['template_properties'], 
            hostname=module.params['name'], tracking_id=module.params['tracking_id'])

    
    ansible_facts={ "onefuse_ipam": response_json, 
                  "ip_address": response_json["ipAddress"], "netmask": response_json["netmask"], 
                  "gateway": response_json["gateway"], "subnet": response_json["subnet"], 
                  "network": response_json["network"], "dns_suffix": response_json["dnsSuffix"], 
                  "primary_dns": response_json["primaryDns"], "secondary_dns": response_json["secondaryDns"], 
                  "nic_label": response_json["nicLabel"], "dns_search_suffixes": response_json["dnsSearchSuffixes"], 
                  "onefuse_ipam_id": response_json["id"], "tracking_id": response_json['trackingId'] }
    
    create_success(module, onefuse_inputs, response_json, ansible_facts)

  def absent(module, ofm, onefuse_inputs, resource_path, unique_field):

    try:
      onefuse_object = ofm.get_object_by_unique_field(resource_path=resource_path, field_value=module.params["object_name"], field=unique_field)  
    except:
      remove_exception(module, onefuse_inputs)    
    
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

  def present(module, ofm, onefuse_inputs):
    try:
      response_json = ofm.provision_dns(policy_name=module.params['policy_name'], template_properties=module.params['template_properties'], 
            name=module.params['name'], value=module.params['value'], zones=module.params['zones'], tracking_id=module.params['tracking_id'])
    except:
      create_exception(module, onefuse_inputs)

    ansible_facts={ "onefuse_dns": response_json, 
          "onefuse_dns_id":response_json['id'], "tracking_id": response_json['trackingId'] }

    create_success(module, onefuse_inputs, response_json, ansible_facts)
    
  def absent(module, ofm, onefuse_inputs, resource_path, unique_field):

    try:
       onefuse_object = ofm.get_object_by_unique_field(resource_path="dnsReservations", field_value=module.params["object_name"], field=unique_field)  
    except:
      remove_exception(module, onefuse_inputs)    
    
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

  def present(module, ofm, onefuse_inputs):

    try:
      response_json = ofm.provision_ad(policy_name=module.params['policy_name'], template_properties=module.params['template_properties'], 
              name=module.params['name'], tracking_id=module.params['tracking_id'])
    except:
      create_exception(module, onefuse_inputs)

    ansible_facts={ "onefuse_ad": response_json, 
                    "onefuse_ad_id": response_json['id'], "tracking_id": response_json['trackingId'] }

    create_success(module, onefuse_inputs, response_json, ansible_facts)

  def absent(module, ofm, onefuse_inputs, resource_path, unique_field):

    try:
      onefuse_object = ofm.get_object_by_unique_field(resource_path="microsoftADComputerAccounts", field_value=module.params["object_name"], field=unique_field)  
    except:
      remove_exception(module, onefuse_inputs)    
    
    remove_success(module, ofm, onefuse_inputs, resource_path, onefuse_object)
    
  try:
    if module.params['state'] == 'absent':
      absent(module, ofm, onefuse_inputs, resource_path, unique_field)
    else:  
      present(module, ofm, onefuse_inputs)
    module.exit_json(changed=True, path=path)
  except Exception as e:
      module.fail_json(msg=to_native(e), exception="exception")

# OneFuse Scripting Module

def scripting(module, ofm, onefuse_inputs, resource_path, unique_field):

  def present(module, ofm, onefuse_inputs):

    try:
      response_json = ofm.provision_scripting(policy_name=module.params['policy_name'], template_properties=module.params['template_properties'], 
              tracking_id=module.params['tracking_id'])
    except:
      create_exception(module, onefuse_inputs)

    ansible_facts={ "onefuse_script": response_json, 
            "onefuse_script_id": response_json["id"], "tracking_id": response_json['trackingId'] }
    
    create_success(module, onefuse_inputs, response_json, ansible_facts)

  def absent(module, ofm, onefuse_inputs, resource_path, unique_field):

    try:
      onefuse_object = ofm.get_object_by_unique_field(resource_path="scriptingDeployments", field_value=module.params["object_name"], field=unique_field)  
    except:
      remove_exception(module, onefuse_inputs)    
    
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

  def present(module, ofm, onefuse_inputs):

    try:
      response_json = ofm.provision_cmdb(policy_name=module.params['policy_name'], template_properties=module.params['template_properties'], 
              tracking_id=module.params['tracking_id'])
    except:
      create_exception(module, onefuse_inputs)

    ansible_facts={ "onefuse_cmdb": response_json, 
            "onefuse_cmdb_id": response_json["id"], "tracking_id": response_json['trackingId'] }

    create_success(module, onefuse_inputs, response_json, ansible_facts)

  def absent(module, ofm, onefuse_inputs, resource_path, unique_field):

    try:
      onefuse_object = ofm.get_object_by_unique_field(resource_path="servicenowCMDBDeployments", field_value=module.params["object_name"], field=unique_field)  
    except:
      remove_exception(module, onefuse_inputs)    
    
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

  def present(module, ofm, onefuse_inputs):

    try:
      response_json = ofm.provision_ansible_tower(policy_name=module.params['policy_name'], 
          template_properties=module.params['template_properties'], hosts=module.params['hosts'], 
          limit=module.params['limit'], tracking_id=module.params['tracking_id'])
    except:
      create_exception(module, onefuse_inputs)

    ansible_facts={ "onefuse_ansible_tower": response_json, 
                "onefuse_ansible_tower_id": response_json["id"], "tracking_id": response_json['trackingId'] }
    
    create_success(module, onefuse_inputs, response_json, ansible_facts)

  def absent(module, ofm, onefuse_inputs, resource_path, unique_field):

    try:
      onefuse_object = ofm.get_object_by_unique_field(resource_path="ansibleTowerDeployments", field_value=module.params["object_name"], field=unique_field)  
    except:
      remove_exception(module, onefuse_inputs)    
    
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

  def present(module, ofm, onefuse_inputs):

    try:
      response_json = ofm.provision_vra(policy_name=module.params['policy_name'], template_properties=module.params['template_properties'], 
              deployment_name=module.params['deployment_name'], tracking_id=module.params['tracking_id'])
    except:
      create_exception(module, onefuse_inputs)

    ansible_facts={ "onefuse_vra": response_json, 
              "onefuse_vra_id": response_json["id"], "tracking_id": response_json['trackingId'] }
    
    create_success(module, onefuse_inputs, response_json, ansible_facts)

  def absent(module, ofm, onefuse_inputs, resource_path, unique_field):

    try:
      onefuse_object = ofm.get_object_by_unique_field(policy_path="vraDeployments", field_value=module.params["object_name"], field=unique_field)  
    except:
      remove_exception(module, onefuse_inputs)    
    
    remove_success(module, ofm, onefuse_inputs, resource_path, onefuse_object)
    
  try:
    if module.params['state'] == 'absent':
      absent(module, ofm, onefuse_inputs, resource_path, unique_field)
    else:  
      present(module, ofm, onefuse_inputs)
    module.exit_json(changed=True, path=path)
  except Exception as e:
      module.fail_json(msg=to_native(e), exception="vRA State Error")

# OneFuse Managed object for module does not exists

def remove_exception(module, onefuse_inputs):
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
  module.exit_json(changed=False, response=result)

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

def create_exception(module, onefuse_inputs):
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
  module.exit_json(changed=False, response=result)

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

  module.exit_json(changed=changed, response=response, ansible_facts=ansible_facts)

if __name__ == "__main__":
    main()