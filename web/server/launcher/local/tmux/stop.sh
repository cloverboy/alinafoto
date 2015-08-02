#! /bin/bash
# Author: Roman Ruskov
# Date: 2014-07-28
# Usage: sudo ./tmux/stop.sh

SESSION_NAME="wyse_media"

tmux select-window -t "$SESSION_NAME:0"
tmux select-pane -t 0

tmux send-keys -t 2 PageUp
tmux send-keys -t 2 Down
tmux send-keys -t 2 F9
tmux send-keys -t 2 15
tmux send-keys -t 2 Enter

tmux attach-session -t "$SESSION_NAME"