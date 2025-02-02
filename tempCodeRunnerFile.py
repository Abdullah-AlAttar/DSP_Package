import matplotlib.pyplot as plt
# plot a line, implicitly creating a subplot(111)
plt.plot([1, 2, 3])
# now create a subplot which represents the top plot of a grid
# with 2 rows and 1 column. Since this subplot will overlap the
# first, the plot (and its axes) previously created, will be removed
plt.subplot(221)
plt.plot(range(12))
plt.subplot(222, facecolor='y')  # creates 2nd subplot with yellow background
plt.plot(range(33))
plt.show()
