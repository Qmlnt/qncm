## Qncm is Not a Config Manager
qncm uses rsync to copy files and preserve the tree with permissions.

Simple example: `sudo -k ./qncm.py -if list -ef exclude --to /root/Backup/`

Copies files and directories in `list` excluding ones in `exclude`, and preserving the tree from `/` to `/root/Backup/`.
