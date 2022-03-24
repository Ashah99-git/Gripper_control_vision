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



# Project Flow 

<img width="296" alt="image" src="https://user-images.githubusercontent.com/102171203/159884461-d54718ee-d5f7-4202-8dc6-4a73e7010306.png">

PointCloud Preprocessing : Convert Point Cloud --> Mesh --> Depth Image.



<img width="150" alt="image" src="https://user-images.githubusercontent.com/102171203/159885395-75aead31-178f-41c3-8c7e-63d293655aa9.png">  <img width="117" alt="image" src="https://user-images.githubusercontent.com/102171203/159885436-6df99a0e-15fa-4a1d-bc83-936d293d0e43.png"> 
<img width="132" alt="image" src="https://user-images.githubusercontent.com/102171203/159885476-465fa151-20eb-440d-9814-494e8e861ae9.png">


Detection from Depth Image and Camera Image :

<img width="344" alt="image" src="https://user-images.githubusercontent.com/102171203/159886562-fff3bc26-536b-4e8c-80e6-d5fb7ef85aca.png">	<img width="344" alt="image" src="https://user-images.githubusercontent.com/102171203/159886734-18f5a4b1-6bd6-4129-96e2-00a5b62c6410.png">





	
