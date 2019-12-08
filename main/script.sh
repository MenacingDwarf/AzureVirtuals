#!/bin/bash
sudo az vm start --name MyVm --resource-group MyResourceGroup
ssh azureuser@13.90.157.122 python3 task_solution/task_solution.py
sudo az vm stop --resource-group MyResourceGroup --name MyVm