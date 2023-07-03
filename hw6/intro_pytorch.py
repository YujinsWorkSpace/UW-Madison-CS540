import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
# from torch.utils.data import DataLoader
from torchvision import datasets, transforms


# Feel free to import other packages, if needed.
# As long as they are supported by CSL machines.


def get_data_loader(training=True):
    custom_transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])
    if training:
        dataset = datasets.FashionMNIST('./ data', train=True,
                                        download=True, transform=custom_transform)
        loader = torch.utils.data.DataLoader(dataset, batch_size=64)
    else:
        dataset = datasets.FashionMNIST('./ data', train=False,
                                        transform=custom_transform)
        loader = torch.utils.data.DataLoader(dataset, batch_size=64, shuffle=False)

    return loader


def build_model():
    model = nn.Sequential(
        nn.Flatten(),
        nn.Linear(784, 128),
        nn.ReLU(),
        nn.Linear(128, 64),
        nn.ReLU(),
        nn.Linear(64, 10)
    )
    return model


def train_model(model, train_loader, criterion, T):
    opt = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)

    for epoch in range(T):
        model.train()
        train_loss = 0
        correct = 0
        for inputs, targets in train_loader:
            opt.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            loss.backward()
            opt.step()
            train_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            correct += (predicted == targets).sum().item()

        accuracy = 100. * correct / len(train_loader.dataset)
        train_loss /= len(train_loader)

        print(
            f"Train Epoch: {epoch} Accuracy: {correct}/{len(train_loader.dataset)} ({accuracy:.2f}%) Loss: {train_loss:.3f}")


def evaluate_model(model, test_loader, criterion, show_loss=True):
    # function collaborated with Robbie Xu
    model.eval()
    correct = 0
    running_loss = 0.0
    total = 0
    with torch.no_grad():
        for data, labels in test_loader:
            outputs = model(data)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            running_loss += criterion(outputs, labels).item() * labels.size(0)

    accuracy = 100 * correct / total
    if show_loss:
        print('Average loss: {:.4f}'.format(running_loss / total))
    print('Accuracy: {:.2f}%'.format(accuracy))


def predict_label(model, test_images, index):
    with torch.no_grad():
        model.eval()
        logits = model(test_images[index])
        probs = F.softmax(logits, dim=1)[0]
        sorted_probs, indices = probs.sort(descending=True)
        classes = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag',
                   'Ankle boot']
        print(f'{classes[indices[0]]}: {sorted_probs[0] * 100:.2f}%')
        print(f'{classes[indices[1]]}: {sorted_probs[1] * 100:.2f}%')
        print(f'{classes[indices[2]]}: {sorted_probs[2] * 100:.2f}%')


if __name__ == '__main__':
    criterion = nn.CrossEntropyLoss()
    # get_data_loader
    train_loader = get_data_loader()
    print(type(train_loader))
    print(train_loader.dataset)
    test_loader = get_data_loader(False)
    # build model
    model = build_model()
    print(model)
    # train model
    train_model(model, train_loader, criterion, 5)
    # evaluate
    evaluate_model(model, test_loader, criterion, show_loss=False)
    evaluate_model(model, test_loader, criterion, show_loss=True)
    # predict
    data = iter(test_loader)
    test_images, labels = next(data)
    predict_label(model, test_images, 1)
