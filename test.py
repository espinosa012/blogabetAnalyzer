import 	numpy 				as 	np
import 	matplotlib.image 	as 	mpimg
import 	matplotlib.pyplot 	as 	plt
from 	PIL 										import 	Image

cart_path 	=	'./profit_charts/soccermister.png'
#im 			= 	Image.open(cart_path)
im 			=	mpimg.imread(cart_path)

print(im)

plt.figure()
plt.imshow(im)
#plt.imshow(im)
plt.show()

