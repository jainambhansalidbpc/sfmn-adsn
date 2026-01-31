import numpy as np
import pandas as pd

def pca_from_scratch(X, num_components):
    X_mean = X - np.mean(X, axis=0)
    
    cov_matrix = np.cov(X_mean, rowvar=False)
    
    eigen_values, eigen_vectors = np.linalg.eigh(cov_matrix)
    
    sorted_index = np.argsort(eigen_values)[::-1]
    sorted_eigenvectors = eigen_vectors[:, sorted_index]
    
    eigenvector_subset = sorted_eigenvectors[:, 0:num_components]
    
    X_reduced = np.dot(X_mean, eigenvector_subset)
    
    return X_reduced

if __name__ == "__main__":
    data = np.random.rand(100, 5) 
    df = pd.DataFrame(data, columns=['A', 'B', 'C', 'D', 'E'])
    
    reduced_data = pca_from_scratch(df.values, 2)
    print("Original Shape:", df.shape)
    print("Reduced Shape:", reduced_data.shape)