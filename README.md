# DP-means

The primary goal of this work is to identify clusters of students exhibiting similar knowledge patterns.

Paper:

@inproceedings{Khayi2019ClusteringSB,
  title={Clustering Students Based on Their Prior Knowledge},
  author={Nisrine Ait Khayi and V. Rus},
  booktitle={EDM},
  year={2019}
}

Algorithm:  DP-means :

Input: x_1,…,x_(n ): input data, α∶ cluster penalty parameter
Output:  Clustering l_1,…,l_k and number of clusters k
	Init.  k=1,l_1={x_1,…,x_n } and μ_1 the global mean.
	Init. Cluster indicators z_i=1 for all i=1,…,n
	Repeat until convergence 
	For each point x_i
	Compute d_ic= ‖x_i- μ_c ‖^2 for
          c=1,…,k
	If d_ic> α , set k=k+1,z_i=k,and  μ_k= x_i
	Otherwise, set   z_i= 〖argmin〗_c  d_ic

	Generate clusters l_1,…,l_k based on  z_1,…,z_k ∶ l_j={x_i  | z_i=j }
	For each cluster l_j , compute μ_(j = 1/|l_j | )  ∑_(x ∈l_j)▒x .


