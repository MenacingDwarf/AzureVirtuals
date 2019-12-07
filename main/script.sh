#!/bin/bash
az vm start --name MyVm --no-wait --resource-group MyResourceGroup
ssh azureuser@13.90.157.122
python3 task_solution/task_solution.py
exit
az vm stop --resource-group MyResourceGroup --name MyVm