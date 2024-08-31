#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from imblearn.over_sampling import SMOTE
from sklearn.utils.class_weight import compute_class_weight
from catboost import CatBoostClassifier, Pool
file_path = '/home/user01/Data/roads/NNNPedestrian Accidents_translated-Yasir_Laptop.csv'   # Replace with the actual file path
data = pd.read_csv(file_path)

# Display the first few rows of the dataset
print(data.head())
print(data.info())
print(data.describe())
# %%
# Replace unknown values (9) with NaN
data = data.replace(9, np.nan)

# Check for missing values
print(data.isnull().sum())

# Fill missing values with mean (or choose another strategy)
data = data.fillna(1)#data.mean())

# Verify no more missing values
print(data.isnull().sum())
#%%
features = data.drop(columns=['Injury_Severity'])
target = data['Injury_Severity']
#%%
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
# Oversample the minority class
smote = SMOTE(random_state=42, k_neighbors=5)
X_resampled, y_resampled = smote.fit_resample(X_train, y_train)
#%%
# Compute class weights
class_weights = compute_class_weight(class_weight='balanced', classes=np.unique(y_train), y=y_train)
class_weights_dict = {i: class_weights[i] for i in range(len(class_weights))}
#%%

# eval_dataset = Pool(data=X_test, label=y_test)
# model = CatBoostClassifier(learning_rate=0.1, depth=6, n_estimators=600,
#                            class_weights=class_weights_dict, task_type='GPU', devices='0',
#                            custom_metric=['Logloss', 'F1',
#                                           'AUC:hints=skip_train~false']
#                            )


# model.fit(X_resampled, y_resampled, eval_set=eval_dataset, verbose=False)
# %%
model = CatBoostClassifier(class_weights=class_weights_dict, task_type='GPU', devices='0',
                           custom_metric=['Logloss',
                                          'AUC:hints=skip_train~false'])

grid = {'learning_rate': [0.01,0.05,0.1,0.15,0.2,0.25,0.3],
        'depth': [3,4,5, 6,7,8,9, 10],
        'n_estimators': list(range(100,800, 100))}

grid_search_result = model.grid_search(grid,
                                       X=features,
                                       y=target,
                                       cv=3,
                                       train_size=0.8,
                                       verbose=False,
                                       plot=False)

# %%
