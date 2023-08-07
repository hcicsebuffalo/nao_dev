# Importing libraries
from torch.utils.data import DataLoader, Dataset
import torch.nn as nn
import torch
import matplotlib.pyplot as plt
import numpy as np
import random
from PIL import Image
import PIL.ImageOps    
import pathlib
import torchvision
import torchvision.datasets as datasets
import torchvision.transforms as transforms
import torchvision.utils
from torch.autograd import Variable
from torch import optim
import torch.nn.functional as F
import os
# from pytorch_lightning import Trainer
# from pytorch_lightning.callbacks import EarlyStopping

# Showing images
def imshow(img, text=None):
    npimg = img.numpy()
    plt.axis("off")
    if text:
        plt.text(75, 8, text, style='italic',fontweight='bold',
            bbox={'facecolor':'white', 'alpha':0.8, 'pad':10})
        
    plt.imshow(np.transpose(npimg, (1, 2, 0)))
    plt.show()    

# Plotting data
def show_plot(xpoints,ypoints, text):
    title = 'Epochs v/s '+ text
    plt.title(title) 
    plt.plot(xpoints,ypoints)
    plt.show()

# Siamese Function
class SiameseNetworkDataset(Dataset):
    def __init__(self,imageFolderDataset,transform=None):
        self.imageFolderDataset = imageFolderDataset    
        self.transform = transform

    # for reference check 
    # https://www.geeksforgeeks.org/__getitem__-in-python/#:~:text=__getitem__()%20is%20a%20magic,equivalent%20to%20type(x).    
    def __getitem__(self,index):
        img0_tuple = random.choice(self.imageFolderDataset.imgs)

        #We need to approximately 50% of images to be in the same class
        should_get_same_class = random.randint(0,1) 
        if should_get_same_class:
            while True:
                #Look until the same class image is found
                img1_tuple = random.choice(self.imageFolderDataset.imgs) 
                if img0_tuple[1] == img1_tuple[1]:
                    break
        else:
            while True:
                #Look until a different class image is found
                img1_tuple = random.choice(self.imageFolderDataset.imgs) 
                if img0_tuple[1] != img1_tuple[1]:
                    break

        img0 = Image.open(img0_tuple[0])
        img1 = Image.open(img1_tuple[0])

        # Transforms image to grayscale (probably)
        img0 = img0.convert("L")
        img1 = img1.convert("L")

        # this self.transform does the transformation defined in 
        # the .ipynb file when this class is called 
        if self.transform is not None:
            img0 = self.transform(img0)
            img1 = self.transform(img1)
        
        # torch.from_numpy() or torch.Tensor() is used to construct a tensor from an ndarray
        # 3rd parameter in the return statement used as LABEL 
        return img0, img1, torch.from_numpy(np.array([int(img1_tuple[1] != img0_tuple[1])], dtype=np.float32))
    
    def __len__(self):
        return len(self.imageFolderDataset.imgs)

# Save best model (need to check whether it is required)
class SaveBestModel:
    def __init__(
        self, best_test_acc=0.0 #, best_valid_loss=float('inf'),
    ):
        # self.best_valid_loss = best_valid_loss
        self.best_test_acc = best_test_acc
        
    def __call__(
        self, current_test_acc, #current_valid_loss, 
        epoch, model, optimizer, criterion
    ):
        # if current_valid_loss < self.best_valid_loss:
        if current_test_acc > self.best_test_acc:
            # self.best_valid_loss = current_valid_loss
            self.best_test_acc = current_test_acc
            # print(f"\nBest validation loss: {self.best_valid_loss}")
            print(f"\n: {self.best_test_acc}")
            print(f"\nSaving best model for epoch: {epoch+1}\n")
            torch.save({
                'epoch': epoch+1,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'loss': criterion,
                # 'accuracy': test_accuracy
                }, './saved_models/best_siamese_model.pth')

# Function to save the trained model to disk wrt loss
def save_model(epochs, model, optimizer, criterion, test_loss, path):
    # print(f"Saving final model...")
    torch.save({
                'epoch': epochs,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'loss': criterion,
                'present_loss': test_loss,
                }, path)

# Function to save the trained model to disk wrt accuracy
def save_model_wrt_accr(epochs, model, optimizer, criterion, test_accuracy, path):
    # print(f"Saving final model...")
    torch.save({
                'epoch': epochs,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'loss': criterion,
                'present_accruracy': test_accuracy,
                }, path)
# Function for loading the model 
def load_model(model,path):
    optimizer = optim.Adam(model.parameters(), lr = 0.001 )
    checkpoint = torch.load(path)
    model.load_state_dict(checkpoint['model_state_dict'])
    optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    epoch = checkpoint['epoch']
    criterion = checkpoint['loss']
    prev_loss = checkpoint['present_loss']
    return model, optimizer, epoch, criterion, prev_loss

def save_plots(train_acc, valid_acc, train_loss, valid_loss):
    """
    Function to save the loss and accuracy plots to disk.
    """
    # accuracy plots
    plt.figure(figsize=(10, 7))
    plt.plot(
        train_acc, color='green', linestyle='-', 
        label='train accuracy'
    )
    plt.plot(
        valid_acc, color='blue', linestyle='-', 
        label='validataion accuracy'
    )
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.savefig('./plots/accuracy.png')
    
    # loss plots
    plt.figure(figsize=(10, 7))
    plt.plot(
        train_loss, color='orange', linestyle='-', 
        label='train loss'
    )
    plt.plot(
        valid_loss, color='red', linestyle='-', 
        label='validataion loss'
    )
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.savefig('./plots/loss.png')

# Define the Siamese Neural Network
class SiameseNetwork(nn.Module):

    def __init__(self):
        super(SiameseNetwork, self).__init__()

        # Setting up the Sequential of CNN Layers
        self.cnn1 = nn.Sequential(
            nn.Conv2d(1,96, kernel_size=11,stride=4),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(3, stride=2),
            
            nn.Conv2d(96, 256, kernel_size=5, stride=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, stride=2),

            nn.Conv2d(256, 384, kernel_size=3,stride=1),
            nn.ReLU(inplace=True)
        )

        # Setting up the Fully Connected Layers
        self.fc1 = nn.Sequential(
            nn.Linear(31104, 1024),
            nn.ReLU(inplace=True),
            
            nn.Linear(1024, 256),
            nn.ReLU(inplace=True),
            
            nn.Linear(256,2)
        )
        
    def forward_once(self, x):
        # This function will be called for both images
        # Its output is used to determine the similiarity
        output = self.cnn1(x)
        output = output.view(output.size()[0], -1)
        output = self.fc1(output)
        return output

    def forward(self, input1, input2):
        # In this function we pass in both images and obtain both vectors
        # which are returned
        output1 = self.forward_once(input1)
        output2 = self.forward_once(input2)

        return output1, output2
        
# Define the Contrastive Loss Function
class ContrastiveLoss(torch.nn.Module):
    def __init__(self, margin=2.0):
        super(ContrastiveLoss, self).__init__()
        self.margin = margin

    def forward(self, output1, output2, label):
      # Calculate the euclidean distance and calculate the contrastive loss
      euclidean_distance = F.pairwise_distance(output1, output2, keepdim = True)

      loss_contrastive = torch.mean((1-label) * torch.pow(euclidean_distance, 2) +
                                    (label) * torch.pow(torch.clamp(self.margin - euclidean_distance, min=0.0), 2))

      return loss_contrastive

# torch.clamp example
# a = tensor([ 1.0941,  0.9940, -1.2605,  1.0354, -0.0059,  0.1327])
# out = torch.clamp(a, min = 0.0)
# then out will be tensor([1.0941, 0.9940, 0.0000, 1.0354, 0.0000, 0.1327])
# basically here torch.clamp did set the lower bound. 

# Old training loop modified 
# for understanding python enumerate better, refer to the link below.
# https://www.geeksforgeeks.org/enumerate-in-python/
def train_siamese(dataloader,model,criterion,optimizer,epoch,counter,loss_history, iteration_number,acc_arr):
    size = len(dataloader.dataset)
    train_running_correct = 0
    # Iterate over batches
    for i, (img0, img1, label) in enumerate(dataloader, 0):
        # Send the images and labels to CUDA
        img0, img1, label = img0.cuda(), img1.cuda(), label.cuda()
        # Zero the gradients
        optimizer.zero_grad()
        # Pass in the two images into the network and obtain two outputs
        output1, output2 = model(img0, img1)
        # Pass the outputs of the networks and label into the loss function
        loss_contrastive = criterion(output1, output2, label)
        # Calculate the backpropagation
        loss_contrastive.backward()
        # Optimize
        optimizer.step()
        # Every 10 batches print out the loss
        if i % 10 == 0 :
            # print(f'Epoch {epoch+1}\n-----------------------------')
            # print(f"Current loss {loss_contrastive.item()}\n")
            iteration_number += 10
            counter.append(iteration_number)
            loss_history.append(loss_contrastive.item())
        # Calculate the train accuracy 
        euclidean_distance = F.pairwise_distance(output1, output2, keepdim = True)
        # print("euclidean_distance - ",euclidean_distance)
        pred = []
        for x in euclidean_distance:
            if x < 0.05:
                pred.append(0.) 
                # why is a .present here? to signify float 
                # example 0.0
            else: 
                pred.append(1.)
                
        pred = torch.FloatTensor(pred)
        pred = torch.reshape(pred,label.shape).cuda()
        train_running_correct += (pred == label).sum().item()    
    
    accuracy = 100. * (train_running_correct / size)    
    acc_arr.append(accuracy)
    # we must also return train_accuracy after calculating
    return model, counter, loss_history, iteration_number, accuracy, acc_arr, loss_contrastive.item()

def test_siamese(dataloader,model,test_acc_arr):
    size = len(dataloader.dataset)
    test_running_correct = 0
    # here in need a constant img0 and only 
    for i, (img0, img1, label) in enumerate(dataloader, 0):
        # Send the images and labels to CUDA
        img0, img1, label = img0.cuda(), img1.cuda(), label.cuda()
        # Pass in the two images into the network and obtain two outputs
        output1, output2 = model(img0, img1)
        # Calculate the test accuracy 
        euclidean_distance = F.pairwise_distance(output1, output2, keepdim = True)
        pred = []
        for x in euclidean_distance:
            if x < 0.05:
                pred.append(0.) # why is a .present here?
            else: 
                pred.append(1.)

        pred = torch.FloatTensor(pred)
        pred = torch.reshape(pred,label.shape).cuda()
        test_running_correct += (pred == label).sum().item()  
    
    accuracy = 100. * (test_running_correct / size)    
    test_acc_arr.append(accuracy)
    return accuracy, test_acc_arr




# WRT LOSS

def test_siamese_wrt_loss(dataloader,model,test_loss_arr,criterion):
    size = len(dataloader.dataset)
    test_running_correct = 0
    # here in need a constant img0 and only 
    for i, (img0, img1, label) in enumerate(dataloader, 0):
        # Send the images and labels to CUDA
        img0, img1, label = img0.cuda(), img1.cuda(), label.cuda()
        # Pass in the two images into the network and obtain two outputs
        output1, output2 = model(img0, img1)
        # Pass the outputs of the networks and label into the loss function
        loss_contrastive = criterion(output1, output2, label)
  
    test_loss_arr.append(loss_contrastive.item())
    return loss_contrastive.item(), test_loss_arr


def train_siamese_wrt_loss(dataloader,model,criterion,optimizer,epoch,counter,loss_history, iteration_number):
    size = len(dataloader.dataset)
    train_running_correct = 0
    # Iterate over batches
    for i, (img0, img1, label) in enumerate(dataloader, 0):
        # Send the images and labels to CUDA
        img0, img1, label = img0.cuda(), img1.cuda(), label.cuda()
        # Zero the gradients
        optimizer.zero_grad()
        # Pass in the two images into the network and obtain two outputs
        output1, output2 = model(img0, img1)
        # Pass the outputs of the networks and label into the loss function
        loss_contrastive = criterion(output1, output2, label)
        # Calculate the backpropagation
        loss_contrastive.backward()
        # Optimize
        optimizer.step()
        # Every 10 batches print out the loss
        if i % 10 == 0 :
            # print(f'Epoch {epoch+1}\n-----------------------------')
            # print(f"Current loss {loss_contrastive.item()}\n")
            iteration_number += 10
            counter.append(iteration_number)
            loss_history.append(loss_contrastive.item())
    # we must also return train_accuracy after calculating
    return model, counter, loss_history, iteration_number, loss_contrastive.item()

# Need to check this function. Maybe its accuracy part is not working correct
def train(dataloader,model,criterion,optimizer):
    size = len(dataloader.dataset)
    model.train()
    train_running_loss = 0.0
    train_running_correct = 0
    counter = 0
    for i, (img0,img1,label) in enumerate(dataloader,0):
        counter += 1
        img0, img1, label = img0.cuda(), img1.cuda(), label.cuda()
        
        optimizer.zero_grad()
        # 2 outputs
        output1, output2 = model(img0, img1)
        # loss function
        loss_contrastive = criterion(output1, output2, label)
        train_running_loss += loss_contrastive.item()
        
        euclidean_distance = F.pairwise_distance(output1, output2, keepdim = True)
        print("euclidean_distance = ",euclidean_distance)
        pred = []
        for x in euclidean_distance:
            if x < 0.05:
                pred.append(0.)
            else: 
                pred.append(1.)
                
        pred = torch.FloatTensor(pred)
        pred = torch.reshape(pred,label.shape).cuda()
        train_running_correct += (pred == label).sum().item()
        
        loss_contrastive.backward()
        optimizer.step()        
#         if i % 10 == 0 :
#             print(f"Current loss {loss_contrastive.item()}\n")
#             loss_history.append(loss_contrastive.item())
    epoch_loss = train_running_loss / counter
    epoch_acc = 100. * (train_running_correct / size)
    return epoch_acc,epoch_loss

## xxxxxxxxxxxxxxxxxx----References----xxxxxxxxxxxxxxxxxx 
# Python program to illustrate
# enumerate function
# l1 = ["eat", "sleep", "repeat"]
# s1 = "geek"
  
# # creating enumerate objects
# obj1 = enumerate(l1)
# obj2 = enumerate(s1)
  
# print ("Return type:", type(obj1))
# print (list(enumerate(l1)))
  
# # changing start index to 2 from 0
# print (list(enumerate(s1, 2)))

# Output:
# Return type: 
# [(0, 'eat'), (1, 'sleep'), (2, 'repeat')]
# [(2, 'g'), (3, 'e'), (4, 'e'), (5, 'k')]
## xxxxxxxxxxxxxxxxxx----References----xxxxxxxxxxxxxxxxxx 