from scipy.stats import randint,uniform


# Define the parameter grid for Random Forest
LIGHTGM_PARAMS = {
    'n_estimators': randint(100, 500),
    'max_depth': randint(5, 15),
    'learning_rate': uniform(0.01, 0.2),
    'num_leaves': randint(20, 59),
    'boosting_type': ['gbdt', 'dart'],

}


RANDOM_SEARCH_PARAMS = {
    'n_iter': 100,
    'cv': 2,
    'n_jobs': -1,
    'verbose': 2,
    'random_state': 42,
    'scoring': 'accuracy',
}