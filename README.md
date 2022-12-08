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

### How to run a particular environment?
To run the a particular environment say secret_room mention the same in the "ENV" variable in the bash script file. env_factory.py file has list of environments we can run in a dict called as ENV_MAP. The keys which contain ckpt at end are the dense reward variation of the particular environment.
Ex: To run a pushbox in dense reward system. we would run the bash script file with ENV variable with push_box_ckpt.

- To run in CMAE mode: mention the exp_mode as active_cen along with --mixed_explore tag.
- To run Q learning: mention the exp_mode as epsilon without --mixed_explore tag.

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
#### For Pushbox, RWARE, DERK
- cd to CMAEDERKandRWARE Mention the path of the 2 data.csv files which were logged during training in the `log/CMAE/` as df and df1. Next run the plot.py file.

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
<pre>
@article{PressurePlate,
    author = {Mcinroe, Trevor},
    title = {{UOE-Agents/Pressureplate: Repo for the Multi-Agent Pressureplate Environment.}},
    year = {2021},
    note = {\url{https://github.com/IouJenLiu/CMAE.}},
}
</pre>

### 3. Derk’s Gym 1.1.1
#### [[Project Website]](http://docs.gym.derkgame.com/)
<pre>
@misc{gym_derk,
   author = {John Fredrik Wilhelm Norén},
   title = {Derk Gym Environment},
   year = {2020},
   publisher = {Mount Rouke},
   journal = {Mount Rouke},
   howpublished = {\url{https://gym.derkgame.com}},
}
</pre>

### 4. Robotic-Warehouse
#### [[Project Website]](https://github.com/uoe-agents/robotic-warehouse)
<pre>
@article{RWARE,
    author = {Christianos, Filippos and Sch\"{a}fer, Lukas and Albrecht, Stefano},
    title = {{Shared Experience Actor-Critic for Multi-Agent Reinforcement Learning}},
    year = {2020},
    note = {\url{https://github.com/uoe-agents/robotic-warehouse}},
}
</pre>
