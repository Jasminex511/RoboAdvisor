#!/bin/bash

export PATH=$PATH:/Applications/MATLAB/MATLAB_R2023b.app/bin

# Run Streamlit file
streamlit run main.py &

STREAMLIT_PID=$!

# Run MATLAB script
matlab -batch "run('RoboAdvisor_BacktestingWorkflow.mlx')"

wait $STREAMLIT_PID
