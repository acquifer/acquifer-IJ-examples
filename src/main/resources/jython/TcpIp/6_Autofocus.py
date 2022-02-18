"""
This script demonstrate how to run autofocus via an external application like python.
The runHardwareAutofocus / runSoftwareAutofocus commands can be called both in "live" and "script" mode.
"""
from acquifer.core import TcpIp
from java.lang import Thread

myIM = TcpIp() # open the communication port with the IM


# SOFTWARE AUTOFOCUS
"""
Software autofocus is run with the current objective and camera settings.
To use a different objective or to use different camera settings (ROI acquisition or binning), you would need to first call one of this function
"""
#myIM.setObjective(index) # with index in range 1-4
#myIM.setCamera(x,y,width,height,binning)


lightSource = "bf" # as in setLightSource, here using brightfield, for fluo use a 6-digit code such as "001000" as in setFluoChannel 
detectionFilter = 2
intensity = 80
exposure = 100
zStackCenter = 18000 # center of the stack (in µm) imaged to evaluate the focus
nSlices = 11         # this means we measure the focus for 5 slices above and 5 below the center slice -> 5 + 1 (center) + 5 = 11
zStepSize = 10       # distance in µm between slices in the "autofocus stack"

"""
you might want to check the light parameters using setLight before running the autofocus to make sure the parameters allow to distinguish sometzing from the image 
The search range along the Z-axis is always (nSlices - 1) x zStepSize
Here 11 slices x 10 makes 110 µm
"""

print "Starting software autofocus, focus value will be printed once the focus search is done."
zFocus = myIM.runSoftwareAutoFocus(lightSource, 
								   detectionFilter, 
								   intensity, 
							       exposure, 
							       zStackCenter,
							       nSlices, 
							       zStepSize)

print u"Z-Focus = {} µm".format(zFocus)




# HARDWARE AUTOFOCUS
# Hardware autofocus use its own light source and detector so you dont need to choose an intensity/exposure
# You only have to choose the objective, detectionFilter and starting Z position
print "Starting hardware autofocus, focus value will be printed once the focus search is done."
objective = 1
detectionFilter = 1
zStart = 18500 # starting Z-coordinate for the autofocus search, in µm

zFocus = myIM.runHardwareAutoFocus(1,1,18500)

print u"Z-Focus = {} µm".format(zFocus)