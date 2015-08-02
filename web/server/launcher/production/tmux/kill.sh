#! /usr/local/bin/bash
# Author: Roman Ruskov
# Date: 2014-07-28
# Usage: sudo ./tmux/kill.sh

SESSION_NAME="wyse_media"

tmux kill-session -t "$SESSION_NAME"