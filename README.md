<!-- Header -->
# MDP Planning

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#adding-a-new-algorithm">Adding a new algorithm</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

Implemented different algorithms to compute an optimal policy for a given MDP.

Using the algorithms we have built a maze solver which finds the shortest path in the given maze.

### Algorithms
The algorithms implemented are:
* Value Iteration
* Howard's Policy Iteration
* Linear Programming

### Built With

Code is in python. It uses the following libraries:
* [NumPy](https://numpy.org/)
* [PuLP](https://pypi.org/project/PuLP/)

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

* NumPy

  ```sh
  $ pip3 install numpy
  $ pip3 install pulp
  ```

### Installation

1. Clone the repo
   
   ```sh
   $ git clone https://github.com/rishiagarwal2000/mdp-planning.git 
   ```

<!-- USAGE EXAMPLES -->
## Usage

* To use MDP planning algorithms:
    ```sh
    $ python3 planner.py --mdp MDP --algorithm ALGORITHM 
    ```
    Here is an example:
    ```sh
    $ python3 planner.py --mdp ../data/mdp/continuing-mdp-10-5.txt --algorithm vi
    ```
    Refer [Algorithms](#algorithms) to see the list of implemented algorithms.

* To solve a maze:
    1. Encode the maze into an MDP
    
    ```sh
    $ python3 encoder.py --grid GRID > MDPFILE
    ```
    Here is an example:
    ```sh
    $ python3 encoder.py --grid ../data/maze/grid10.txt > mdpFile
    ```
    2. Solve the MDP using one of the mentioned algorithms

    ```sh
    $ python3 planner.py --mdp mdpFile --algorithm vi > VALUE_AND_POLICY_FILE
    ```
    Here is an example:
    ```sh
    $ python3 planner.py --mdp mdpFile --algorithm vi > value_and_policy_file
    ```
    3. Decode the output policy to print the optimal path

    ```sh
    $ python3 decoder.py --grid GRID --value_policy VALUE_AND_POLICY_FILE
    ```
    Here is an example:
    ```sh
    $ python3 decoder.py --grid ../data/maze/grid10.txt --value_policy value_and_policy_file
    ```

<!-- Adding a new algorithm -->
## Adding a new algorithm
Add your algorithm in the following section:
```python
def plan(f, algo):
	S,A,T,R,gamma,st,end = readMDP(f)
	#print('{}, {}, {}, {}, {}, {}, {}'.format(S,A,T,R,gamma,st,end))
	v,p = [],[]
	if algo == 'vi':
		v,p = vi(S,A,T,R,gamma)
	elif algo == 'hpi':
		v, p = hpi(S,A,T,R,gamma)
	elif algo == 'lp':
		v, p = lp(S,A,T,R,gamma)	
	else:
		print("Algo not found")
		return
	
	for value,action in zip(v,p):
		print("{:.6f} {}".format(value, action))

	return
```
### I/O specification:

* Inputs of the algorithm:
    * _S_ is the number of states in the MDP
    * _A_ is the number of actions in the action space
    * _T_ is a 3-d array of transition probabilities
    * _R_ is a 3-d array of rewards
    * _gamma_ is the discount factor

* The algorithm should output a tuple of optimal value function and optimal policy


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Rishi Agarwal - rishiapril2000@gmail.com

Project Link: [https://github.com/rishiagarwal2000/mdp-planning.git](https://github.com/rishiagarwal2000/mdp-planning.git)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [Professor Shivaram Kalyanakrishnan, IIT Bombay](https://www.cse.iitb.ac.in/~shivaram/)
* Santhosh Kumar G., IIT Bombay