set up:
  - install conda -> conda create -n yourenv python=3.9 -> conda activate yourenv (recommended)
  - git clone https://github.com/baochi0212/Optimization
  -  pip install -r requirements.txt
  -  Colab on browser 
  
  
  
usage:
- python files running local
  - cd Optimization 
  - python gen_input.py
  - python youralgo.py --input filename.json
  - python gen_input.py
  - python main.py
- Colab: use 2 colab files added in repo

  
  
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
  - sample0,5.json N = 18, k = 3
  - sample1.json: N = 99, k = 9
  - sample1,5.json: N = 99, k = 3
  - sample2.json: N = 999, k = 99
  - sample2,5.json: N = 9999, k = 9
  - sample3.json: N = 9999, k = 999
  - out.csv (converted to sample2d.json for heurisitcs): N = 535, k = 3 


Code Contribution:
  - Hoang Van An
  - Tran Bao Chi
  - Nguyen Cong Dat
  - Nguyen Hoang Dang 



ite10
