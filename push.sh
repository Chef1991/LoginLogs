#!/bin/bash

yes | rm -r /mnt/it-nas/share1/LoginLogs
scp -r /Users/tylercook/IdeaProjects/LoginLogs/ nas:/shares/share1/LoginLogs
mv /mnt/it-nas/share1/LoginLogs/LoginLogs/* /mnt/it-nas/share1/LoginLogs/
rm -r /mnt/it-nas/share1/LoginLogs/LoginLogs