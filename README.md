set up:
  - install conda -> conda create -n yourenv python=3.9 -> conda activate yourenv (recommended)
  - git clone https://github.com/baochi0212/Optimization
  -  pip install -r requirements.txt
  
  
  
usage:
  - cd Optimization 
  - python gen_input.py
  - python youralgo.py --input filename.json
  - python gen_input.py
  - python main.py

  
  
algo:
  -  IP (ORtools)
  -  CP model (ORtools)
  -  heuristic:
     -  greedy
     -  simulated annealing
     -  K-means + simulated annealing
     -  genetic algorithm
     -  hill climbing
     -  TS - LNS 

dataset:
  - sample0.json: N = 6, k = 3 
  - sample1.json: N = 99, k = 9
  - sample2.json: N = 999, k = 99
  - sample3.json: N = 9999, k = 999
  - out.csv (converted to sample2d.json for heurisitcs): N = 535, k = 3 
Code Contribution:
  - Hoang Van An
  - Tran Bao Chi
  - Nguyen Cong Dat
  - Nguyen Hoang Dang 
ite10
