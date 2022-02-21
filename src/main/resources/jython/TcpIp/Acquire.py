"""
This script demonstrates how to acquire images via the Java API from an external application. 
By default the acquire command is designed for the acquisition of Z-stacks. Single images can also be acquired by specifying the number of slice to 1.
For the acquire command, like for the autofocus command, the objective and camera settings are defined beforehand via the dedicated commands (see previous tutorial scripts).

The acquire commands can be called with an optional path argument to specify where the images should be saved.
If not specified, the images are saved in a subdirectory of the project directory.
The project directory can be defined using the command setDefaultProjectFolder or via the Imaging Machine software.
The images are saved in a subdirectory of the project directory, named using the user-defined PlateId and a unique timestamp.
Use setPlateId to define the plate id.

The images are named following the Imaging Machine naming syntax.
The values of the metadata tags in the filename can be updated using the set of setMetadata commands.
These commands should be called before the corresponding acquire command to update the well ID, subposition and timepoint tags.
Indeed contrary to running an experiment in the GUI, there is no way for the software to know what well, timepoint or subposition the next acquire command corresponds to.

NOTE about script/live mode
The acquire commands always switches the software to script mode.
If the software is in live mode before the acquire command is sent, the software will switch to script mode, acquire the images and return to live mode.
Switching between script and live mode takes a few seconds. Therefore for successive acquire commands, it is advised to switch to script mode once for all, before calling the acquire command,
using the setMode("script") command.
"""
from acquifer.core import TcpIp

myIM = TcpIp()

myIM.setObjective(1)
myIM.resetCamera() # use default setting, use setCamera functions to update ROI and/or binning

# Update metadata fields such as wellID, subposition (within a given well), timepoint
myIM.setMetadataWellId("C002") # this should be a 4-character string : a character and 3 digits 
myIM.setMetadataSubposition(1) # to specify if we are acquiring subpositions within a well
myIM.setMetadataTimepoint(1)   # for timelapse

# OPTION1 : acquire with full set of arguments including custom directory to save the images
channelNumber = 1 # this is for filenaming (the CO tag)
lightSource = "brightfield"
detectionFilter = 2 # between 1 and 4
intensity = 50 # relative intensity of the lightsource in %
exposure = 100 # exposure in ms
zStackCenter = 18000 # in µm
nSlices = 20
zStepSize = 10 # µm
lightConstantOn = False

# For saveDirectory we pass a raw string (r prefix) so that backslashes are not interpreted as special characters
# one can also use normal string with double backslashes as separators \\ or forward slash /
# if the directory does not exist, it is automatically created
# if "" or None is passed as argument to acquire, the images are saved in the default project folder within a plate-specific directory (see below) 
saveDirectory = r"C:\Users\Default\Desktop\MyDataset"

myIM.acquire(channelNumber, 
			 lightSource, 
			 detectionFilter, 
			 intensity, 
			 exposure, 
			 zStackCenter,
			 nSlices, 
			 zStepSize, 
			 lightConstantOn, 
			 saveDirectory)



# OPTION2 : Using default project folder and plate ID
# This avoids the need to specify the image directory for every new acquire command
#
# This will assure the following acquire commands are saved in the same subdirectory
# Indeed when switching to script mode, a timestamp is created that is used as part of the plate directory
myIM.setDefaultProjectFolder(r"C:\Users\Default\Desktop\MyDataset")
myIM.setPlateId("test")

# Switch to script mode before calling successive acquire commands
# otherwise each acquire command will switch back to live mode after execution (time consuming)
myIM.setMode("script")


# Define channel settings
detectionFilter = 2 # here we use the same detection filter between brightfield and fluo bu we could use different ones for each

intensityBF = 50  # relative intensity of the lightsource in %
exposureBF  = 100 # exposure in ms

intensityFluo = 80  # relative intensity of the lightsource in %
exposureFluo  = 150 # exposure in ms

# Stack settings (identical for brigtfield and fluo)
zStackCenter = 18000 # in µm
nSlices = 20
zStepSize = 10 # µm

# Acquire brightfield channel
myIM.setMetadataWellId("A001")
myIM.acquire(1, # here we set channel number for brightfield to 1, this defines the value for the tag "CO" in the filename
			 "brightfield", 
			 detectionFilter,
			 intensityBF, 
			 exposureBF, 
			 zStackCenter, 
			 nSlices, 
			 zStepSize) # here we set channel number for brightfield to 1
						# here we dont specify the output directory so images will be saved in the dfault projectDirectory/timestamp_plateID. lightConstantOn is not specified neither and default to False

# Acquire fluo channel
myIM.acquire(2, # here we set channel number for this fluo channel to 2, this defines the value for the tag "CO" in the filename
			 "100000", # use the 1st fluo light source, see the "LightSource" example script
			 detectionFilter, 
			 intensityFluo, 
			 exposureFluo, 
			 zStackCenter,
			 nSlices, 
			 zStepSize,
			 True, # here we specifiy lightConstantOn to true, so fluo light source is not blinking 
			 None) # set the saveDirectory to None, in this case the images are saved to the default project directory as above

myIM.closeConnection() # closing the connection will automatically switch back to live mode