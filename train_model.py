import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

df = pd.read_csv("training/output.csv")

# Remove strings out of features since the features should only contain numbers, and booleans
features = df[["Number.of.posts", "Number.of.people.they.follow", "Number.of.followers", "has_profile_picture", "Private.account", "has_number", "has_number_at_end", "alpha_numeric_ratio", "following_followers_ratio", "following_posts_ratio", "followers_posts_ratio"]]
label = df["rating"]

# split the dataset
features_train, features_test, label_train, label_test = train_test_split(features, label, test_size=0.30, random_state=0)

# Apply Random Forest Classifier
clf = RandomForestClassifier(n_estimators=30)
clf.fit(features_train, label_train)

# Test it
label_prediction = clf.predict(features_test)
print("Accuracy on test split: ", metrics.accuracy_score(label_test, label_prediction))

