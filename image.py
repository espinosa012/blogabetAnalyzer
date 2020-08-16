import 	numpy 				as 		np
import 	matplotlib.image 	as 		mpimg
import 	matplotlib.pylab 	as 		plt

from 	PIL 				import 	Image

from 	skimage.io 			import	imread 	
from 	skimage.color 		import 	rgb2lab, lab2rgb, rgb2gray
from 	skimage.util 		import 	crop
from 	copy 				import 	deepcopy



chart_path 	=	'./profit_charts/soccermister.png'



def imshow(img, figsize=None):
	plt.figure(figsize=figsize)
	plt.imshow(img)
	plt.show()




def rgb2gray_(img_path):
	#	Read original image (rgb, no alpha channel)
	im 			=	imread(img_path)
	
	#	Transform from rgb to lab space color
	im1 		=	rgb2lab(im)
	#	Set color channel values (second and third channels) to zeros
	im1[...,1] 	=	im1[..., 2] 	=	0
	#	Obtenemos la imagen en escala de grises volviendo al espacio rgb después de haber anulado las componentes de color
	#	Get grayscale image imga by transforming back to rgb (without color informatio)
	return 	lab2rgb(im1)




def get_img_channels(img):
	#	Muestra los 3 canales de color de rgb en grayscale, al estilo Matlab
	if img.shape[-1] == 1:
		#	La imagen ya está en escala de grises
		pass

	img_r 	=	deepcopy(img)
	img_g 	=	deepcopy(img)
	img_b 	=	deepcopy(img)

	img_r[...,1] 	=	img_r[...,2]	=	0
	img_g[...,0] 	=	img_g[...,2]	=	0
	img_b[...,0] 	=	img_b[...,1]	=	0

	img_r_ 			=	rgb2lab(img_r)
	img_r_[...,1] 	=	img_r_[...,2]	=	0
	img_r 			=	lab2rgb(img_r_)

	img_g_ 			=	rgb2lab(img_g)
	img_g_[...,1] 	=	img_g_[...,2]	=	0
	img_g 			=	lab2rgb(img_g_)

	img_b_ 			=	rgb2lab(img_b)
	img_b_[...,1] 	=	img_b_[...,2]	=	0
	img_b 			=	lab2rgb(img_b_)

	plt.figure()
	plt.subplot(411), plt.imshow(img), plt.title('Original image'), plt.axis('off')
	plt.subplot(412), plt.imshow(img_r), plt.title('Red channel'), plt.axis('off')
	plt.subplot(413), plt.imshow(img_g), plt.title('Green channel'), plt.axis('off')
	plt.subplot(414), plt.imshow(img_b), plt.title('Blue channel'), plt.axis('off')

	plt.show()



def crop_chart(img, x1=81, x2=337, y1=205, y2=81):
	#	Return cropped chart from image (in image format)

	cropped 	= 	crop(img, ((50, 100), (50, 50), (0,0)), copy=False)



def crop_test(img):
	x1	=	83
	y1	=	83
	x2	=	205
	y2	=	336

	cropped 	=	img[x1:x2,y1:y2]

	plt.figure()
	plt.subplot(121), plt.imshow(img), plt.title('Original')
	plt.subplot(122), plt.imshow(cropped), plt.title('Cropped')
	plt.show()





img 	=	imread(chart_path)
crop_test(img)
#imshow(img)
#imshow(img[81:337, 81:205])
#imshow(img[x1:x2, y1:y2])


#crop_chart(imread(chart_path))

#get_img_channels(imread(chart_path))