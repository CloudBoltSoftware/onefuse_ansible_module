# onefuse_ansible_module
Ansible module for consuming OneFuse integration within Ansible Core and Ansible Tower

# Installation

Place the contents of the modules folder in your Ansible Modules Folder:

## Ansible Tower Typical Modules Folder Path
```
/usr/share/ansible/plugins/modules
```
## Ansible Core Typical Modules Folder Path
```
/{ansible_root_folder}/lib/ansible/modules
```
Edit the contents of the config.py file located in the module_utils/onefuse folder and place in the Ansible Module_Utils folder.  It must reside in a /module_utils/onefuse/config.py

## Ansible Tower Typical Module_Utils Folder Path
```
/usr/share/ansible/plugins/module_utils
```
## Ansible Core Typical Module_Utils Folder Path
```
/{ansible_root_folder}/lib/ansible/module_utils
```
# Usage

Please see the contents of the examples folder for usage examples.