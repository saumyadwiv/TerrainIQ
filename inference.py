import torch
import numpy as np
import segmentation_models_pytorch as smp
from torchvision import transforms
import cv2

NUM_CLASSES = 10


def load_model():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = smp.Unet(
        encoder_name="resnet34",
        encoder_weights=None,
        in_channels=3,
        classes=NUM_CLASSES,
    )

    state_dict = torch.load("model/model.pth", map_location=device)
    model.load_state_dict(state_dict)

    model.to(device)
    model.eval()

    return model


def predict(model, image, device):

    original_h, original_w = image.shape[:2]

    transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((320, 320)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])

    input_tensor = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(input_tensor)
        mask = torch.argmax(output, dim=1).squeeze().cpu().numpy()

    # Resize mask back to original resolution
    mask = cv2.resize(
        mask.astype(np.uint8),
        (original_w, original_h),
        interpolation=cv2.INTER_NEAREST
    )

    return mask