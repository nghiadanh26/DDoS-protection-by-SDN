# DDoS-protection-by-SDN
## About the project
Hello, I am N.D. Nghia from Future Internet Lab. I have main responsibility to run this project from the beginning. You can contact me for more detail via nghiadanh.fil@gmail.com.

This is a big project of Future Internet Lab, guided by Assoc. Prof. Nguyen Huu Thanh. We use POX controller to excute SDN architecture. The main purpose of this project is how to detect DDoS attack(common attacks, such as: TCP SYN, ICMP Flood, UDP Flood) and mitigate them by policies. All algorithms we use in this project are machine leaning algorithms, written in PYTHON.


## How does this project procedure?
If you want to follow this project, read these steps carefully.

    Step 1: What are the common DDoS attacks?

    Step 2: Which features are used to detect common DDoS attacks?

    Step 3: The idea of building matrix data

    Step 4: Find the information from OVS

According to OpenFlow doccumentation 1.3 and pox_wiki, there are many kinds of statistic pair messages (request and respond), like flow_stats, port_stats, aggregate_stats,...

    Step 5: Collect data from OVSes and build the matrix data

    Step 6: Use Local Outlier Factor algorithm to detect DDoS attacks. Find the source attacks and destination victims.

      Step 6.1: Collect matrix data and normalize them before saving to csv file
  
      Step 6.2: Create local_outlier_factor_matrix class for LOF algorithm
  
      Step 6.3: Write the function read_data to read data from csv file and convert them to 6x6 matrix
  
      Step 6.4: Write the function to calculate matrix_distance
  
      Step 6.5: Write the function to calculate k-distance
  
      Step 6.6: Calculate reachability distance for each component of matrix data
  
      Step 6.7: Calculate lrd (local reachability density) for each component of matrix data
  
      Step 6.8: Write LOF_predict function based on k nearest neighboors
  
      Step 6.9: Run this algorithm on Mininet.
  
  Reference for LOF is following https://towardsdatascience.com/local-outlier-factor-for-anomaly-detection-cc0c770d2ebe
  
  #### Sorry, at the last meeting, we have discussed about LOF, how to make LOF on matrix faster. That is solution! We will remove Step 6 and move on Step 7! (1/4/2019)
  
        Step 7: Faster LOF on matrix.

The idea of this solution is cutting off unexisted link. By this way we can reduce from 36 to 10 times to calculate LOF. This following some substeps:

     Step 7.1: Rebuild topology, the new topology file named 6sw_v3.py
  
     Step 7.2: Modify the code to collect data from OVSes
  
     Step 7.3: Collect matrix data (10 instead of 36 points)
  
     Step 7.4: Normalize data and save in csv file
  
     Step 7.5: Write LOF
  
     Step 7.6: Training LOF
  
     Step 7.7: Run demontration on Mininet.
  
  ## How to understand this project
  
  First, everything in this project is written in algorithm_v2.py file, including:
  
    + How to collect data from OVSs
    + Collect data
    + Normalize data
    + Collect data for training
    + Training with LOF
    + Dectect anomal point real time
    
 Second, LOF algorithm is contained in local_outlier_factor_v2.py
 
 ## How to run simulation
 ##### Step 1: Run topology on Mininet
   
 
    $ cd DDoS-protection-by-SDN
 
    $ sudo python 6sw_v3.py
 
 ##### Step 2: Run pox controller
 
 Open another terminal, and run python file:
 
    $ cd DDoS-protection-by-SDN/pox
 
    $ ./pox.py algorithm_v2 forwarding.l2_learning
  
