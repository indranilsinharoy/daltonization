Daltonization
=============

Python daltonization module

How to use it
=============
```python
from PIL import Image
import daltonization
original = Image.open("original.png") #Load the original image via PIL
sim = daltonize.simulate(original) #Simulate the effect of colourblindness on the original image
dalt = daltonize.daltonize(original) #Daltonize the original image
dalt.save("dalt.png") #Save the daltonized image
```

Requirements
============
1. python2
2. PIL 
3. numpy

