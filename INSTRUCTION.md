# Setup 1 Client VM
- Update the VM and install Ansible and configure it 
    - Install [Ansible](https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-ansible-on-ubuntu-20-04)
        - Enable SSH agent forwarding towards ansible host, [see](https://theusmanhaider.medium.com/ansible-clone-private-git-repository-c8a2c9ec8a61)
            - `[ssh_connection]` is now renamed to `[connection]`
    - Configure SSH agent forwarding for connection to Client VM
        - needed to add config below to `~/.ssh/config`
        - also needed to run `ssh-add <PRIVATE-GIT-KEY>`
        - test connection via `ssh -T git@github.com`
```
Host hostname / ip of host
  ForwardAgent yes
```

