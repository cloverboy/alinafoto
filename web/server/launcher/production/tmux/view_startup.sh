#! /usr/local/bin/bash
# Author: Roman Ruskov
# Date: 2014-07-28
# Usage: sudo ./tmux/view_logs.sh

SESSION_NAME="wyse_media"

tmux select-window -t "$SESSION_NAME:0"
tmux attach-session -t "$SESSION_NAME"