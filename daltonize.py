# -*- coding: iso-8859-1 -*-

import os.path

def daltonize(im, color_deficit='deuteranope', operation='daltonize'):
    import numpy
    from PIL import Image

    # Get image data
    if im.mode in ['1', 'L']: # Don't process black/white or grayscale images
        return (filename, fpath)
    im = im.copy() 
    im = im.convert('RGB') 
    RGB = numpy.asarray(im, dtype=float)

    # Transformation matrix for Deuteranope (a form of red/green color deficit)
    lms2lmsd = numpy.array([[1.5,0,0],[0.7413105,0,1.872405],[0,0,1.5]])
    # Transformation matrix for Protanope (another form of red/green color deficit)
    lms2lmsp = numpy.array([[0,2.02344,-2.52581],[0,1,0],[0,0,1]])
    # Transformation matrix for Tritanope (a blue/yellow deficit - very rare)
    lms2lmst = numpy.array([[1,0,0],[0,1,0],[-0.395913,0.801109,0]])
    # Colorspace transformation matrices
    rgb2lms = numpy.array([[17.8824,43.5161,4.11935],[3.45565,27.1554,3.86714],[0.0299566,0.184309,1.46709]])
    lms2rgb = numpy.linalg.inv(rgb2lms)
    # Daltonize image correction matrix
    err2mod = numpy.array([[0,0,0],[0.7,1,0],[0.7,0,1]])

    # Get the requested image correction
    if color_deficit == 'deuteranope':
        lms2lms_deficit = lms2lmsd
    elif color_deficit == 'protanope':
        lms2lms_deficit = lms2lmsp
    elif color_deficit == 'tritanope':
        lms2lms_deficit = lms2lmst
    else:
        return (filename, fpath)
    
    # Transform to LMS space
    LMS = numpy.zeros_like(RGB)               
    for i in range(RGB.shape[0]):
        for j in range(RGB.shape[1]):
            rgb = RGB[i,j,:3]
            LMS[i,j,:3] = numpy.dot(rgb2lms, rgb)

    #Calculate image as seen by the color blind
    _LMS = numpy.zeros_like(RGB)  
    for i in range(RGB.shape[0]):
        for j in range(RGB.shape[1]):
            lms = LMS[i,j,:3]
            _LMS[i,j,:3] = numpy.dot(lms2lms_deficit, lms)

    _RGB = numpy.zeros_like(RGB) 
    for i in range(RGB.shape[0]):
        for j in range(RGB.shape[1]):
            _lms = _LMS[i,j,:3]
            _RGB[i,j,:3] = numpy.dot(lms2rgb, _lms)

   # Save simulation how image is perceived by a color blind
    if operation == "simulate" :
        for i in range(RGB.shape[0]):
            for j in range(RGB.shape[1]):
                _RGB[i,j,0] = max(0, _RGB[i,j,0])
                _RGB[i,j,0] = min(255, _RGB[i,j,0])
                _RGB[i,j,1] = max(0, _RGB[i,j,1])
                _RGB[i,j,1] = min(255, _RGB[i,j,1])
                _RGB[i,j,2] = max(0, _RGB[i,j,2])
                _RGB[i,j,2] = min(255, _RGB[i,j,2])
        simulation = _RGB.astype('uint8')
        im_simulation = Image.fromarray(simulation, mode='RGB')
        return im_simulation


    if operation == "daltonize" :
        # Calculate error between images
        error = (RGB-_RGB)

        # Daltonize
        ERR = numpy.zeros_like(RGB) 
        for i in range(RGB.shape[0]):
            for j in range(RGB.shape[1]):
                err = error[i,j,:3]
                ERR[i,j,:3] = numpy.dot(err2mod, err)

        dtpn = ERR + RGB
        
        for i in range(RGB.shape[0]):
            for j in range(RGB.shape[1]):
                dtpn[i,j,0] = max(0, dtpn[i,j,0])
                dtpn[i,j,0] = min(255, dtpn[i,j,0])
                dtpn[i,j,1] = max(0, dtpn[i,j,1])
                dtpn[i,j,1] = min(255, dtpn[i,j,1])
                dtpn[i,j,2] = max(0, dtpn[i,j,2])
                dtpn[i,j,2] = min(255, dtpn[i,j,2])

        result = dtpn.astype('uint8')
        
        # Save daltonized image
        im_converted = Image.fromarray(result, mode='RGB')
        #im_converted.save(modified_fpath)
        #return (modified_filename, modified_fpath)
        return im_converted





