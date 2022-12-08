## Cooperative Exploration for Multi-Agent Deep Reinforcement Learning Evaluation #

The repository contains code used to evaluate the Python implementation of Cooperative Exploration for Multi-Agent Deep Reinforcement Learning (CMAE) with Q-Learning on the discrete multi-agent particle environments (MPE) provided by [[1]](https://ioujenliu.github.io/CMAE/).

### Platform and Dependencies provided by [[1]](https://ioujenliu.github.io/CMAE/):
* Platform: Ubuntu 16.04
* Conda 4.8.3
* Python 3.6.3
* Numpy 1.19.2

### Training for environments developed by [[1]](https://ioujenliu.github.io/CMAE/):
    cd script
    sh run_cmae_push_box.sh
    sh run_cmae_room.sh
    sh run_cmae_secret_room.sh
Training log will be dumped to `log/CMAE/`.

### Training for Pressure Plate evironments, base Pressure Plate environment developed by [[2]](https://github.com/uoe-agents/pressureplate)
  #### For Greedy Pressure Plate:
  - cd into greedyPressurePlate and run main.py, this will create a greedyData.txt file in the same folder. The file that is used to generate graph in the tech report has been provided.
  #### For CMAE Pressure Plate:
  - cd into CMAEPressurePlate/CMAE/script then run sh run_cmae_pressure_plate.sh. This will run the simulation and display the updated count table and current errors.
 
### Generating Graphs
#### For Pass:
- cd to log and run python generate_graphs_dense.py and python generate_graphs_sparse.py to generate graphs for dense and sparse reward tasks of Room / Pass environment.
#### For Secret Room:
- For Sparse graphs: cd to log and edit the file name on line 5 to "CMAE/CMAE_SECRET_ROOM_0_0/data1.csv" and on line 7 change the file name to "CMAE/CMAE_SECRET_ROOM_1_1/data2.csv" the generate_graphs_sparse.py
- For Dense graphs: cd to log and edit the file name on line 5 to "CMAE/CMAE_SECRET_ROOM_2_2/data3.csv" and on line 7 change the file name to "CMAE/CMAE_ROOM_3_3/data4.csv" the generate_graphs_dense.py
- Then follow the steps for generating the graphs for the Pass environment
#### For Greedy Pressure Plate:
- cd into greedyPressurePlate and run graphGen.py to generate the graph for the Pressure Plate environment.

### License
CMAE is licensed under the MIT License

### References
### 1. Cooperative Exploration for Multi-Agent Deep Reinforcement Learning, ICML 2021
#### [[Project Website]](https://ioujenliu.github.io/CMAE/) [[PDF]](http://proceedings.mlr.press/v139/liu21j/liu21j.pdf)
<pre>
@inproceedings{LiuICML2021,
  author = {I.-J. Liu and U. Jain and R.~A. Yeh and A.~G. Schwing},
  title = {{Cooperative Exploration for Multi-Agent Deep Reinforcement Learning}},
  booktitle = {Proc. ICML},
  year = {2021},
}
</pre>

### 2. PressurePlate Multi-Agent Environment
#### [[Project Website]](https://github.com/uoe-agents/pressureplate)

