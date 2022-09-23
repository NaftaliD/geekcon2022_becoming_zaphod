from os import path as osp

import torch
from PIL import Image
from torchvision import transforms as transforms

from mobilenet import MobileNet

FACIAL_ATTRIBUTES = ['5_o_Clock_Shadow', 'Arched_Eyebrows', 'Attractive', 'Bags_Under_Eyes', 'Bald', 'Bangs', 'Big_Lips',
              'Big_Nose', 'Black_Hair', 'Blond_Hair', 'Blurry', 'Brown_Hair', 'Bushy_Eyebrows', 'Chubby',
              'Double_Chin', 'Eyeglasses', 'Goatee', 'Gray_Hair', 'Heavy_Makeup', 'High_Cheekbones', 'Male',
              'Mouth_Slightly_Open', 'Mustache', 'Narrow_Eyes', 'No_Beard', 'Oval_Face', 'Pale_Skin', 'Pointy_Nose',
              'Receding_Hairline', 'Rosy_Cheeks', 'Sideburns', 'Smiling', 'Straight_Hair', 'Wavy_Hair',
              'Wearing_Earrings', 'Wearing_Hat', 'Wearing_Lipstick', 'Wearing_Necklace', 'Wearing_Necktie', 'Young']


def find_attributes_of_face(face_crop, model, device="cpu"):
    image_tensor = np_array_to_tensor(face_crop)

    image = torch.unsqueeze(image_tensor, 0)
    image = image.to(device)
    output = model(image)
    result = output > 0.5
    result = result.cpu().numpy()
    results_dict = {FACIAL_ATTRIBUTES[t]: result[0][t] for t in range(len(FACIAL_ATTRIBUTES))}
    return result, results_dict


def load_attribute_model(device):
    checkpoint_path = osp.join(osp.dirname(__file__), "model_checkpoint.pth")
    # instantiate Net class
    mobilenet = MobileNet()
    # use cuda to train the network
    mobilenet.to(device)
    # loss function and optimizer
    learning_rate = 1e-3
    optimizer = torch.optim.Adam(mobilenet.parameters(), lr=learning_rate, betas=(0.9, 0.999))
    model = MobileNet().to(device)
    checkpoint = torch.load(checkpoint_path, map_location=torch.device('cpu'))
    print("model load successfully.")
    model.load_state_dict(checkpoint['model_state_dict'])
    optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    model.eval()
    return model


def np_array_to_tensor(face_crop):
    transform = transforms.Compose(
        [transforms.Resize(224),
         transforms.ToTensor(),
         transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

    image_tensor = transform(Image.fromarray(face_crop))
    return image_tensor
