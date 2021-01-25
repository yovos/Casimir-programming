import test
import matplotlib.pyplot as plt

print('Hello world')
print('The circumference of a circule with radius 3 is: {}'.format(test.circumference(3)))
print('The area of a circle with radius 3 is: {}'.format(test.area(3))) 


figure, axes = plt.subplots()
draw_circle = plt.Circle((0.5, 0.5), 0.3)

axes.set_facecolor('Black')
axes.set_xlabel(r'$x$', size=15)
axes.set_ylabel(r'$y$', size=15)
axes.set_title('Circle', size=20)
axes.set_aspect(1)
axes.add_artist(draw_circle)
axes.legend(loc=1)
plt.show()
