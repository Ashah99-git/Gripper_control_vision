# gripper_control_vision
Smart Gripper selection for Pick and Place robot using Vision Input



# 1.Docker_detection_model : 
This is for showcasing the working of the algorithm of gripper selection.
which can be run by building the Dockerfile .

open terminal inside the path containing dockerfile
 
	$ docker build –t gripper_selection . // include the '.'
	$ docker run gripper_selection
	
to check with different dataset replace the pcd.txt and rgb_image.jpg 

# 2.Docker_with_communication : 
This is for deployment in the target device which has connection established with the pcd and image generators publishing the pointcloud and rgb data in pub-sub messaging method. also assuming the all the dependent controllers are connected on the same network .

To run the dockerfile follow the steps in 1.

	User input is required for the following attributes of ZMQ communication: 

	Example IP addresses and ports to be used by the containers: 
	New tray Detector - IP address:  127.0.0.1 Port: 5000
	Image generator - IP address:  127.0.0.2 Port: 2002
	PCD generator - IP address:  127.0.0.3 Port: 2002

The Subscribers of the gripper selection controller should  connect to IP address:  127.0.0.1  Port: 5001 in pub-sub method .

The build of dockerfile will take apprx 1-2 hr depending on the system capabilities and will be of 5GB .The dockerfile is written to be compatible with arm64 devices since the target device (Jetson nano) is arm64. Hence the above methods will work only on arm64 architecture device.


	
