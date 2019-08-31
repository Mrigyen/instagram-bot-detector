import insta_api
import train_model

# Train the RF classifier
print()
print("Training results: ")
train_model.train()
print()

# Driver
while(True):
    username = input("Enter username of user you want to verify whether they are a bot or not: ")
    if(username):
        features = insta_api.features(username)
        if features:
            print(train_model.predict(features))

