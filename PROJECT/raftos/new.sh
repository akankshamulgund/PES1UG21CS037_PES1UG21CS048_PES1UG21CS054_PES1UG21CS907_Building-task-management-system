#!/bin/bash

# Clean up existing log, state_machine, and storage files
rm *.log
rm *.state_machine
rm *.storage

# Create log files for each node
touch node1_CUSTOMLOG.log node2_CUSTOMLOG.log node3_CUSTOMLOG.log 

# Create a new tmux session named PES1UG21CS054
tmux new-session -d -s task_management

# Split the window horizontally
tmux split-window -h

# Split the top pane vertically into two panes (66% and 33%)
tmux split-window -v -p 66
tmux split-window -v

# Select the left-top pane
tmux select-pane -t 0

# Split the left-top pane vertically into two panes (66% and 33%)
tmux split-window -v -p 66
tmux split-window -v

# Attach to the tmux session
tmux attach-session -t task_management
