import torch
from torchvision import transforms, models
from PIL import Image
import torch.nn.functional as F

class Resnet():
    def __init__(self, model_path, device=None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.class_map = [
            'A', 'B', 'C', 'CLEAR', 'D', 'DEL', 'E', 'F', 'G', 'H', 'I', 'K', 'L',
            'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'SPACE', 'T', 'U', 'V', 'W', 'X', 'Y'
        ]
        self.num_classes = len(self.class_map)
        self.model = models.resnet18(pretrained=False)
        self.model.fc = torch.nn.Linear(self.model.fc.in_features, self.num_classes)
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.to(self.device)
        self.model.eval()
        self.transform = transforms.Compose([
            transforms.Resize((224,224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485,0.456,0.406], std=[0.229,0.224,0.225])
        ])

    def preprocess(self, frame):
        img = Image.fromarray(frame)
        return self.transform(img).unsqueeze(0).to(self.device)

    def predict(self, frame):
        tensor = self.preprocess(frame)
        with torch.no_grad():
            out = self.model(tensor)
            probs = F.softmax(out, dim=1)
            conf, idx = torch.max(probs, 1)
        return self.class_map[idx.item()], conf.item()
