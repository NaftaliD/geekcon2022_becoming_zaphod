
import cv2
import numpy as np
from facenet_pytorch import MTCNN

from attributes import FACIAL_ATTRIBUTES, find_attributes_of_face, load_attribute_model
from face_detection.track_faces import detect_faces_in_frame



def main():
    device = "cpu"  # torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    # model = MTCNN(keep_all=True, device=device)
    model = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    frame = cv2.imread("C:/Users/Ragit/Desktop/Yohai/Zafhodize/face_images/yohai.jpg")

    face, relative_x_center, frame = detect_faces_in_frame(frame, model)
    print(f'location: {relative_x_center}')

    # plt.clf()
    # plt.imshow(frame[:, :, ::-1])
    # plt.gca().add_patch(Rectangle((face[0], face[1]), face[2] - face[0], face[3] - face[1], alpha=0.5))
    # plt.show()
    # ##

    new_h = 10

    res_str = detection_as_ascii(new_h, frame.shape, face)
    print(res_str)

    ##
    # label_path = "C:/Users/Ragit/Downloads/list_attr_celeba.txt"

    # attributes = open(label_path).readlines()[1].split()
    model = load_attribute_model(device)
    face_crop = crop_face_from_frame(face, frame)
    result, results_dict = find_attributes_of_face(face_crop, model)

    for t in range(len(FACIAL_ATTRIBUTES)):
        if result[0][t] == True:
            print("Attribute: \033[1;35m%s \033[0m, \033[1;35m%s \033[0m" % (FACIAL_ATTRIBUTES[t], result[0][t]))
        else:
            print("Attribute: %s, %s" % (FACIAL_ATTRIBUTES[t], result[0][t]))


if __name__ == '__main__':
    main()
