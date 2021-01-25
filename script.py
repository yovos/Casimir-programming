import test
import matplotlib.pyplot as plt

print('Hello world')
print('The circumference of a circule with radius 3 is: {}'.format(test.circumference(3)))
print('The area of a circle with radius 3 is: {}'.format(test.area(3))) 


figure, axes = plt.subplots()
draw_circle = plt.Circle((0.5, 0.5), 0.3)

axes.set_aspect(1)
axes.add_artist(draw_circle)

plt.title('Circle')

plt.savefig('plotted_circle.png', bbox_inches='tight')
plt.show()
