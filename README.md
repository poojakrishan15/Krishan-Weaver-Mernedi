## Cooperative Exploration for Multi-Agent Deep Reinforcement Learning #
### ICML 2021
#### [[Project Website]](https://ioujenliu.github.io/CMAE/) [[PDF]](http://proceedings.mlr.press/v139/liu21j/liu21j.pdf)

[Iou-Jen Liu](https://ioujenliu.github.io/), [Unnat Jain](https://unnat.github.io/), [Raymond A. Yeh](http://raymondyeh07.github.io/), [Alexander G. Schwing](http://www.alexander-schwing.de/) <br/>
University of Illinois at Urbana-Champaign<br/>


The repository contains Python implementation of Cooperative Exploration for Multi-Agent Deep Reinforcement Learning (CMAE) with Q-Learning on the discrete multi-agent particle environments (MPE).

If you used this code for your experiments or found it helpful, please consider citing the following paper:

<pre>
@inproceedings{LiuICML2021,
  author = {I.-J. Liu and U. Jain and R.~A. Yeh and A.~G. Schwing},
  title = {{Cooperative Exploration for Multi-Agent Deep Reinforcement Learning}},
  booktitle = {Proc. ICML},
  year = {2021},
}
</pre>

### Platform and Dependencies:
* Platform: Ubuntu 16.04
* Conda 4.8.3
* Python 3.6.3
* Numpy 1.19.2

### Training
    cd script
    sh run_came_push_box.sh
    sh run_came_room.sh
    sh run_came_secret_room.sh
Training log will be dumped to `log/CMAE/`.

### How to run a particular environment?
To run the a particular environment say secret_room mention the same in the "ENV" variable in the bash script file. env_factory.py file has list of environments we can run in a dict called as ENV_MAP. The keys which contain ckpt at end are the dense reward variation of the particular environment.
Ex: To run a pushbox in dense reward system. we would run the bash script file with ENV variable with push_box_ckpt.

- To run in CMAE mode: mention the exp_mode as active_cen along with --mixed_explore tag.
- To run Q learning: mention the exp_mode as epsilon without --mixed_explore tag.

### Generating Graphs
#### For Pass:
- cd to log and run python generate_graphs_dense.py and python generate_graphs_sparse.py to generate graphs for dense and sparse reward tasks of Room / Pass environment.

#### For Pushbox, RWARE, DERK
- cd to CMAEDERKandRWARE Mention the path of the 2 data.csv files which were logged during training in the `log/CMAE/` as df and df1. Next run the plot.py file.

### License
CMAE is licensed under the MIT License