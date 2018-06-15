# flask-ansible

## Usage
First you need to create an SSH key pair, copy the public key on remote hosts and copy the private key to the empty ```id_rsa``` file in this project.
Build and run the sample application on your workstation:
```
docker build -t flask-ansible .
sudo docker run -p 80:80/tcp flask-ansible
```

Now open http://localhost on your browser, or just use ```curl``` to call the only method on the sample application:
```
curl 'localhost/?host=srvX.example,srvY.example'
```

That command uses Ansible to run these two tasks on ```srvX.example``` and ```srvY.example``` hosts:
```
27 ...
28 dict(action=dict(module='shell', args="hostname -f")),
29 dict(action=dict(module='yum', args="name=nano, state=latest"))
30 ...
```

This is a sample JSON response from the application:
```
{
  "msg": [
    {
      "host": "srvX.example", 
      "msg": "", 
      "result": {
        "_ansible_no_log": true, 
        "_ansible_parsed": true, 
        "changed": true, 
        "cmd": "hostname -f", 
        "delta": "0:00:00.005304", 
        "end": "2018-01-13 18:54:59.392896", 
        "invocation": {
          "module_args": {
            "_raw_params": "hostname -f", 
            "_uses_shell": true, 
            "chdir": null, 
            "creates": null, 
            "executable": null, 
            "removes": null, 
            "warn": true
          }
        }, 
        "rc": 0, 
        "start": "2018-01-13 18:54:59.387592", 
        "stderr": "", 
        "stderr_lines": [], 
        "stdout": "srvX.example", 
        "stdout_lines": [
          "srvX.example"
        ]
      }, 
      "success": true
    }, 
    {
      "host": "srvY.example", 
      "msg": "", 
      "result": {
        "_ansible_no_log": true, 
        "_ansible_parsed": true, 
        "changed": true, 
        "cmd": "hostname -f", 
        "delta": "0:00:00.010413", 
        "end": "2018-01-13 18:55:02.548078", 
        "invocation": {
          "module_args": {
            "_raw_params": "hostname -f", 
            "_uses_shell": true, 
            "chdir": null, 
            "creates": null, 
            "executable": null, 
            "removes": null, 
            "warn": true
          }
        }, 
        "rc": 0, 
        "start": "2018-01-13 18:55:02.537665", 
        "stderr": "", 
        "stderr_lines": [], 
        "stdout": "srvY.example", 
        "stdout_lines": [
          "srvY.example"
        ]
      }, 
      "success": true
    }, 
    {
      "host": "srvX.example", 
      "msg": "failed", 
      "result": {
        "_ansible_no_log": true, 
        "_ansible_parsed": true, 
        "changed": false, 
        "failed": true, 
        "invocation": {
          "module_args": {
            "conf_file": null, 
            "disable_gpg_check": false, 
            "disablerepo": null, 
            "enablerepo": null, 
            "exclude": null, 
            "install_repoquery": true, 
            "installroot": "/", 
            "list": null, 
            "name": [
              "nano", 
              ""
            ], 
            "skip_broken": false, 
            "state": "latest", 
            "update_cache": false, 
            "validate_certs": true
          }
        }, 
        "msg": "No package matching '' found available, installed or updated", 
        "rc": 126, 
        "results": [
          "All packages providing nano are up to date", 
          "No package matching '' found available, installed or updated"
        ]
      }, 
      "success": false
    }, 
    {
      "host": "srvY.example", 
      "msg": "failed", 
      "result": {
        "_ansible_no_log": true, 
        "_ansible_parsed": true, 
        "changed": false, 
        "failed": true, 
        "invocation": {
          "module_args": {
            "conf_file": null, 
            "disable_gpg_check": false, 
            "disablerepo": null, 
            "enablerepo": null, 
            "exclude": null, 
            "install_repoquery": true, 
            "installroot": "/", 
            "list": null, 
            "name": [
              "nano", 
              ""
            ], 
            "skip_broken": false, 
            "state": "latest", 
            "update_cache": false, 
            "validate_certs": true
          }
        }, 
        "msg": "No package matching '' found available, installed or updated", 
        "rc": 126, 
        "results": [
          "All packages providing nano are up to date", 
          "No package matching '' found available, installed or updated"
        ]
      }, 
      "success": false
    }
  ], 
  "success": true
}
```

## Development
Use [Flask documentation](http://flask.pocoo.org/docs/) for more information on developing Flask applications.
You can use any [Ansible module](http://docs.ansible.com/ansible/latest/modules_by_category.html) to write tasks in your application.
If you [develop new Ansible modules](http://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html) just put them in ```application/library``` directory in this project and start using them in the application.

## License
MIT License

Copyright (c) 2018 @rmin
