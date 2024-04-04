#!/bin/bash

# Clear previous log, state_machine, and storage files
rm *.log
rm *.state_machine
rm *.storage

# Create log files for each node
touch node1_CUSTOMLOG.log node2_CUSTOMLOG.log node3_CUSTOMLOG.log node4_CUSTOMLOG.log node5_CUSTOMLOG.log

# Create a new tmux session named cc_project
tmux new-session -d -s cc_project

# Split the window horizontally
tmux split-window -h

# Split the top pane vertically into two panes (50% and 50%)
tmux split-window -v

# Split the second pane vertically into four panes (25% each)
tmux split-window -v
tmux split-window -v
tmux split-window -v

# Select the left-top pane
tmux select-pane -t 0

# Split the left-top pane vertically into two panes (50% and 50%)
tmux split-window -v

# Select the second pane from the left-top
tmux select-pane -t 1

# Split the selected pane horizontally into two panes (50% and 50%)
tmux split-window -h

# Select the third pane from the left-top
tmux select-pane -t 2

# Split the selected pane horizontally into two panes (50% and 50%)
tmux split-window -h

# Select the fourth pane from the left-top
tmux select-pane -t 3

# Split the selected pane horizontally into two panes (50% and 50%)
tmux split-window -h

# Attach to the tmux session
tmux attach-session -t cc_project

