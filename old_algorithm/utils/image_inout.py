from PIL import Image
import torchvision.transforms as transforms

loader = transforms.ToTensor()
unloader = transforms.ToPILImage()

def image_to_tensor(image_name):
    image = Image.open(image_name)
    image_tensor = loader(image)
    return image_tensor#将图片转化为tensor

def tensor_to_PIL(image_tensor):
    image = unloader(image_tensor)
    return image#将图片转化为PIL

