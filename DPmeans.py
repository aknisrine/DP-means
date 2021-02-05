import pandas as pd
import numpy as np
from sklearn.decomposition import PCA

class DPMEANS:
    def __init__(self, londa, max_iter=1):
        self.londa = londa
        self.max_iter = max_iter

    def fit(self, data):

        self.u = {}
        self.z = {}
        self.k = 1
        self.data_index = {}
        for i in range(len(data)):
                self.z[i] = 1

        self.u[0] = np.mean(data, axis=0)


        for i in range(1, self.max_iter+1):

                self.l = {}
                self.s_l = {}
                for index in range(len(data)):
                    self.data_index[index] = data[index]
                    #euclidian distance
                    distances = [np.linalg.norm(data[index]-self.u[c]) for c in range(self.k)]
                    distances_array = np.array(distances)

                    if min(distances) > self.londa:

                        self.k = self.k+1
                        self.z[index] = self.k
                        self.u[self.k-1] = data[index]

                    else:
                        self.z[index] = distances_array.argmin()+1

                    distances.clear()

                # the output  here is k and the clusters indexes
                # Generate the clusters
                for j in range(1, self.k+1):
                    list = []
                    list_s = []
                    for i in range(len(data)):
                        if self.z[i] == j:
                            list.append(data[i])
                            list_s.append(i)

                    self.l[j] = list
                    self.s_l[j] = list_s

                #Compute the centroids of the results clusters:

                self.u[j-1] = 1/len(self.l[j]) * sum(self.l[j], 0)


if __name__ == '__main__':

    # Read data from the excel file
    df = pd.read_excel('DPmeans_input.xlsx')
    df_text = pd.read_csv("input.txt",delimiter="\t")
    df_text = df_text[['Anon Student Id','Duration (sec)','Outcome']]
    df_text.loc[df_text.Outcome != 'CORRECT','CORRECT'] = 0
    df_text.loc[df_text.Outcome == 'CORRECT', 'CORRECT'] = 1


    ids = pd.read_excel('DPmeans_input.xlsx', usecols = "A")

    student_ids=ids.values.tolist()



    data = df.iloc[:,1:36].values

    data_txt = df_text.values



    df_score =df.Posttest
    data_score = df_score.values

    students_ids = {}
    students_posttest = {}
    student_pretest = {}
    scores_index = {}

    for i in range(len(data_score)):


        students_posttest[i] = data_score[i]

    df_pretest =df.Prestest
    pretest_score = df_pretest.values


    for i in range(len(pretest_score)):
        student_pretest[i]=pretest_score[i]

   #Perform the PCA analysis to reduce the dimentionality
    pca = PCA(n_components=24).fit(data)
    X = pca.transform(data)

    pca1= PCA(n_components=3).fit_transform(data_txt)
    X_txt = pca.transform(data_txt)



    DF = DPMEANS(5, 10)
    DF.fit(X)

    DF1= DPMEANS(4,10)
    DF1.fit(X_txt)

    for item in DF1.s_l :
        print(item)

    scores1 = []

    for item in DF.s_l[1] :

        scores1.append(students_posttest[item])

    scores_1_index={}
    for j in range(1, len(DF.s_l)+1):
        scores = []
        scores_1=[]
        for item in DF.s_l[j]:
           scores.append(students_posttest[item])
           scores_1.append(student_pretest[item])
        scores_index[j] = np.mean(scores)
        scores_1_index[j]=np.mean(scores_1)

    students_clusters = {}
    for item in DF.s_l:

       for s in DF.s_l[item] :
           students_clusters[s]=item

    data_res=[]
    for i in range(len(student_ids)):
         l=[]
         l.append(student_ids[i])
         l.append(students_clusters[i])
         l.append(students_posttest[i])
         l.append(student_pretest[i])
         data_res.append(l)

    df = pd.DataFrame(data_res, columns=['ID', 'Cluster','Posttest','Pretest'])

    #Save the result in a chosen directory
    df.to_csv('C:\\Users\\nisri\\Documents\\DPmeans_vr\\clusters.txt', header=True, index=False, sep='\t', mode='a')