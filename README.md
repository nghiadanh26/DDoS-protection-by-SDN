# DDoS-protection-by-SDN
#TODO: write the description

This is a big project of Future Internet Lab, guided by Assoc. Prof. Nguyen Huu Thanh. We use POX controller to excute SDN architecture. The main purpose of this project is how to detect DDoS attack(common attacks, such as: TCP SYN, ICMP Flood, UDP Flood) and mitigate them by policies. All algorithms we use in this project are machine leaning algorithms, written in PYTHON.

If you want to follow this project, read these steps carefully.

--------------> Step 1: What are the common DDoS attacks?

--------------> Step 2: Which features are used to detect common DDoS attacks?

--------------> Step 3: The idea of building matrix data

--------------> Step 4: Find the information from OVS

According to OpenFlow doccumentation 1.3 and pox_wiki, there are many kinds of statistic pair messages (request and respond), like flow_stats, port_stats, aggregate_stats,...

--------------> Step 5: Collect data from OVSes and build the matrix data

--------------> Step 6: Use Local Outlier Factor algorithm to detect DDoS attacks. Find the source attacks and destination victims.

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
  
  
  
