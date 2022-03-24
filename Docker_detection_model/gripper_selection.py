import cv2 as cv
import open3d as o3d

i = 0

while i < 1:
    new_tray = 1
    Rank_final = []

    # get new try info using ZMQ protocol and write to new tray variable

    if new_tray == 1:

        file_in = open("pcd.txt", "rt")
        file_out = open("pcd_0.txt", "wt")

        for line in file_in:
            file_out.write(line.replace(';', ' '))
        file_in.close()
        file_out.close()

        read_points = o3d.io.read_point_cloud("pcd_0.txt", format="xyzn")
        read_points.estimate_normals()
        reference = o3d.geometry.TriangleMesh.create_coordinate_frame()  # reference frame for rotation
        read_points.rotate(reference.get_rotation_matrix_from_xyz((3.14 / 2, 0, 0)))  # rotate

        ###################################### Alpha shapes ###########################################
        Alpha_mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(read_points, alpha = 9)
        Alpha_mesh.compute_vertex_normals()
        o3d.io.write_triangle_mesh("mesh.ply", Alpha_mesh) # Alpha shapes
        # o3d.visualization.draw_geometries([Alpha_mesh])
        #############################################################################################



        read_mesh = o3d.io.read_triangle_mesh("mesh.ply")
        sample_points = read_mesh.sample_points_uniformly(number_of_points=1000000)
        # o3d.visualization.draw_geometries([sample_points])
        vis = o3d.visualization.Visualizer()
        vis.create_window()
        vis.get_render_option().point_color_option = o3d.visualization.PointColorOption.ZCoordinate
        vis.get_render_option().point_size = 4.0
        vis.add_geometry(sample_points)
        vis.capture_screen_image("depth_image.jpg", do_render=True)
        vis.destroy_window()


        classes = ['Three Jaw Gripper', 'Inner Gripper','Vacuum Gripper','Two Jaw Gripper']

        #Model Trained for PCD
        net_pcd = cv.dnn.readNetFromDarknet('yolov4_custom_pcd.cfg','yolov4_pcd.weights')

        #Model Trained for RGB
        net_rgb = cv.dnn.readNetFromDarknet('yolov4_custom_rgb.cfg','yolov4_rgb.weights')


        img_pcd = cv.imread('depth_image.jpg')
        img_rgb = cv.imread('rgb_image.jpg')

        # Function to rank the detected gripper 

        def rankfunc(img,net):

            img = cv.resize(img, (1370, 749))
            height, width, _ = img.shape
            blob = cv.dnn.blobFromImage(img, 1 / 255, (416, 416), (0, 0, 0), swapRB=True, crop=False)

            net.setInput(blob)

            output_layers_name = net.getUnconnectedOutLayersNames()

            layerOutputs = net.forward(output_layers_name)

            boxes0,boxes1,boxes2,boxes3 = [],[],[],[]
            confidences0,confidences1,confidences2,confidences3 = [],[],[],[]

        # loop to identify the accuracy of the same detected object for each class

            for output in layerOutputs:
                for detection in output:
                    score = detection[5:]

                    if score[0] or score[1] or score[2] or score[3] > 0.5:
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)

                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)

                        
                        boxes0.append([x, y, w, h])
                        confidences0.append((float(score[0])))

                        
                        boxes1.append([x, y, w, h])
                        confidences1.append((float(score[1])))
                        
                        boxes2.append([x, y, w, h])
                        confidences2.append((float(score[2])))
                        
                        boxes3.append([x, y, w, h])
                        confidences3.append((float(score[3])))
                            


            indexes0 = cv.dnn.NMSBoxes(boxes0, confidences0, .8, .4)
            indexes1 = cv.dnn.NMSBoxes(boxes1, confidences1, .8, .4)
            indexes2 = cv.dnn.NMSBoxes(boxes2, confidences2, .8, .4)
            indexes3 = cv.dnn.NMSBoxes(boxes3, confidences3, .8, .4)

            item = (len(indexes0) + len(indexes1) + len(indexes2) + len(indexes3))
            index = [indexes0 , indexes1 , indexes2 , indexes3]
            confidence = [confidences0 , confidences1 ,confidences2 ,confidences3]

            Rank = []

            if len(index[0]) > 0:
                sum = 0
                for i in index[0].flatten():
                    sum += confidences0[i]
                Rank.append((round(sum/item, 2),0))
            else:
                Rank.append((0,0))
                
            if len(index[1]) > 0:
                sum = 0
                for i in index[1].flatten():
                    sum += confidences1[i]
                Rank.append((round(sum/item, 2),1))
            else:
                Rank.append((0,1))

            if len(index[2]) > 0:
                sum = 0
                for i in index[2].flatten():
                    sum += confidences2[i]
                Rank.append((round(sum/item, 2),2))
            else:
                Rank.append((0,2))

            if len(index[3]) > 0:
                sum = 0
                for i in index[3].flatten():
                    sum += confidences3[i]
                Rank.append((round(sum/item, 2),3))
            else:
                Rank.append((0,3))
            
            Rank.sort()

            return Rank

        # Output based on rank

        Rank_pcd = rankfunc(img_pcd,net_pcd)

        Rank_rgb = rankfunc(img_rgb,net_rgb)
        print("Gripper ranking from PointCloud")
        print(Rank_pcd)
        print("Gripper ranking from RGB image")
        print(Rank_rgb)

        # final gripper Ranking Algorithm 

        if Rank_pcd[3][1] == 1:
            Rank_final = Rank_pcd
        elif Rank_rgb[3][1] == 2:
            Rank_final = Rank_rgb
        else :
            for i in range(0,4):
                for j in range(0,4):
                    if Rank_pcd[i][1] == Rank_rgb[j][1]:
                        Rank_final.append(((Rank_pcd[i][0] + Rank_rgb[j][0])/2,Rank_pcd[i][1]))
        Rank_final.sort()
        print("Final gripper ranking ")
        print(Rank_final)
        print("Selected Gripper : ")
        print(classes[Rank_final[3][1]])
        i = 3 


