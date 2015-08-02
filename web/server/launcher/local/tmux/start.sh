#! /bin/bash
# Author: Roman Ruskov
# Date: 2014-07-28
# Usage: sudo ./tmux/start.sh
# Docs: http://www.openbsd.org/cgi-bin/man.cgi/OpenBSD-current/man1/tmux.1?query=tmux&sec=1

#----------------------Common-Settings--------------------#

PROJECT_NAME="wyse_media"
ENVIRONMENT="local"
BASE_PATH="/home/roman/projects/$PROJECT_NAME/web"
LAUNCHER_PATH="${BASE_PATH}/server/launcher/${ENVIRONMENT}"
VIRTUALENV_PATH="/home/roman/projects/virtualenv/${PROJECT_NAME}/bin/activate"
LOGS_PATH="${BASE_PATH}/logs"
SESSION_NAME=$PROJECT_NAME
WINDOW_0_NAME="startup"
WINDOW_1_NAME="logs"

#----------------------End-of-Settings------------------#

tmux start-server
tmux new-session -d -s "$SESSION_NAME" -n "$WINDOW_0_NAME"
tmux new-window -t "$SESSION_NAME:1" -n "$WINDOW_1_NAME"

#--------------------------------
tmux select-window -t "$SESSION_NAME:0"

tmux split-window -v
tmux split-window -v

tmux resize-pane -t 0 -y 2
tmux resize-pane -t 1 -y 7
tmux resize-pane -t 2 -y 35

tmux send-keys -t 0 "cd $LAUNCHER_PATH"
tmux send-keys -t 0 Enter
tmux send-keys -t 0 "source $VIRTUALENV_PATH"
tmux send-keys -t 0 Enter
tmux send-keys -t 0 C-l
tmux send-keys -t 0 "sh ./start_server.sh"
tmux send-keys -t 0 Enter

tmux send-keys -t 1 "cd $LOGS_PATH"
tmux send-keys -t 1 Enter
tmux send-keys -t 1 C-l
tmux send-keys -t 1 "tail -f server.log"
tmux send-keys -t 1 Enter

tmux send-keys -t 2 "htop"
tmux send-keys -t 2 Enter
tmux send-keys -t 2 F4
tmux send-keys -t 2 $PROJECT_NAME
tmux send-keys -t 2 Enter
tmux send-keys -t 2 F5

#--------------------------------
tmux select-window -t "$SESSION_NAME:1"

tmux split-window -v
tmux split-window -v
tmux split-window -v
tmux split-window -v

tmux select-layout even-vertical

tmux send-keys -t 0 "cd $LOGS_PATH"
tmux send-keys -t 0 Enter
tmux send-keys -t 0 C-l
tmux send-keys -t 0 "tail -f tornado.application.log"
tmux send-keys -t 0 Enter

tmux send-keys -t 1 "cd $LOGS_PATH"
tmux send-keys -t 1 Enter
tmux send-keys -t 1 C-l
tmux send-keys -t 1 "tail -f tornado.general.log"
tmux send-keys -t 1 Enter

tmux send-keys -t 2 "cd $LOGS_PATH"
tmux send-keys -t 2 Enter
tmux send-keys -t 2 C-l
tmux send-keys -t 2 "tail -f nginx_error.log"
tmux send-keys -t 2 Enter

#--------------------------------
tmux select-window -t "$SESSION_NAME:0"
tmux select-pane -t 2

tmux attach-session -t "$SESSION_NAME"