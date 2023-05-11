## Qncm is Not a Config Manager
qncm uses rsync to copy files and preserve the tree with permissions.

Simple example: `sudo -k ./qncm.py -if list -ef exclude_main --to /root/Backup/`

Will copy from `/` to `/root/Backup/` files and directories in `list` excluding ones listed in `exclude_main`.
