import matplotlib.pyplot as plt
import matplotlib
import numpy as np

def get_color(matrix):

	cmap = plt.cm.get_cmap('inferno')



	#normalize item number values to colormap
	min_val = np.amin(matrix)
	max_val = np.amax(matrix)

	print(min_val, max_val)
	norm = matplotlib.colors.Normalize(vmin=min_val, vmax=max_val)



	hexa = np.array([[ matplotlib.colors.rgb2hex(cmap(norm(matrix[i, j]))[:3]) for j in range(len(matrix[0]))] for i in range(len(matrix))])
	return hexa

m = np.array([[1,2],[2,3],[4,5]])
print(m.shape)
print(get_color(m).shape)
print(get_color(m))
plt.imshow(get_color(m))
plt.show()



