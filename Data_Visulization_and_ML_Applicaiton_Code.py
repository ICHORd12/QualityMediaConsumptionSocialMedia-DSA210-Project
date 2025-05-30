import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display




#get the data from csv files


def loadData():
    # Load all CSV files
    #Holiday df
    holiday = pd.read_csv('./DATA/Holiday_Workday.csv')

    #Quality Media df's
    ipad_chunky = pd.read_csv('./DATA/Ipad_Chunky_Usage.csv')
    imdb = pd.read_csv('./DATA/IMDB_Ratings.csv')
    story_games = pd.read_csv('./DATA/StoryDriven_Playtime.csv')

    #Social Media df's
    iphone_insta = pd.read_csv('./DATA/Iphone_Instagram_Usage.csv')
    iphone_reddit = pd.read_csv('./DATA/Iphone_Reddit_Usage.csv')
    iphone_yt = pd.read_csv('./DATA/Iphone_Youtube_Usage.csv')
    ipad_yt = pd.read_csv('./DATA/Ipad_Youtube_Usage.csv')
    
    return holiday, imdb, story_games, iphone_insta, iphone_reddit, iphone_yt, ipad_chunky, ipad_yt
#Load the data
holiday, imdb, story_games, iphone_insta, iphone_reddit, iphone_yt, ipad_chunky, ipad_yt = loadData()


#Functions for prcessing csv df's

#Convert special A.BB format to minutes
def convertMin(time_str):
    """
    Convert 'hours.minutes' string (A.BB) to total minutes
    Examples:
        1.30 = 90 minutes (1 hour 30 mins)
        Same explained at README.md
    
    """
    #Convert it to string then split
    time_str = f"{time_str:.2f}"
    hours, minutes = time_str.split('.')
    
    # Pad minutes to 2 digits if needed (e.g., '1.5' -> '1.05', mine csv does not contain this)
    minutes = minutes.ljust(2, '0')[:2]
    
    # A.BB Calculation 
    return int(hours) * 60 + int(minutes)

# Process social media data
#With Given data frames, apply convertMin function to convert A.BB format to minutes. and make a app_name_mins column
def SocialProcess(df, app_name):

    df = df.copy()
    # Find the usage(hours.minutes) column and apply
    if 'usage(hours.minutes)' in df.columns:
        df['minutes'] = df['usage(hours.minutes)'].apply(convertMin)
    return df[['date', 'minutes']].rename(columns={'minutes': f'{app_name}_mins'})

# Process quality media data
#Same as social media, but but handles game playtime diffrently
def QualityProcess(df, media_name):
    df = df.copy()
    # Find the usage(hours.minutes) column and apply
    if 'usage(hours.minutes)' in df.columns:
        df['minutes'] = df['usage(hours.minutes)'].apply(convertMin)
    elif 'playtime(hours.minutes)' in df.columns:
        df['minutes'] = df['playtime(hours.minutes)'].apply(convertMin)
    return df[['date', 'minutes']].rename(columns={'minutes': f'{media_name}_mins'})

# Process IMDB data (films) 
#Needs diffrent handling as it has a diffrent  minutes and date format
def IMDBProcess(imdb):
    # Discard rows with NaN in 'Runtime (mins)'
    imdb = imdb[imdb['Runtime (mins)'].notna()].copy()
    #Change DATE format to dd-mm-yyyy 
    imdb['date'] = pd.to_datetime(imdb['Date Rated']).dt.strftime('%d-%m-%Y')

    #Films that watched same day grouped by date
    films = imdb.groupby('date')['Runtime (mins)'].sum().reset_index()
    films.columns = ['date', 'films_mins']
    return films


#combine all data to a single df


def CombineDATA():
    # Process social media using functions
    social_dfs = [SocialProcess(iphone_yt, 'youtube_phone'), SocialProcess(ipad_yt, 'youtube_ipad'),SocialProcess(iphone_insta, 'instagram'),SocialProcess(iphone_reddit, 'reddit')]
    
    # Merge all social media
    social = social_dfs[0]
    for df in social_dfs[1:]:

        # Merge on 'date' and fill NaN with 0
        social = social.merge(df, on='date', how='outer')
    social = social.fillna(0)
    
    # Calculate socşak total column
    social['social_mins'] = (social['youtube_phone_mins'] + social['youtube_ipad_mins'] + social['instagram_mins'] + social['reddit_mins'])
    
    # Process quality mediab (Same process as social media)
    quality_dfs = [QualityProcess(ipad_chunky, 'comics'),QualityProcess(story_games, 'games'),IMDBProcess(imdb)]
    
    # Merge all quality media with same date
    quality = quality_dfs[0]
    for df in quality_dfs[1:]:
        quality = quality.merge(df, on='date', how='outer')
    quality = quality.fillna(0)
    
    # Calculate totals
    quality['quality_mins'] = quality['comics_mins'] + quality['games_mins'] + quality['films_mins']
    
    # ADD Holiday data to DF
    final_df = social.merge(quality, on='date', how='outer').fillna(0)
    final_df = final_df.merge(holiday, on='date', how='left')
    
    # Convert minutes to hours for readability. !! Conventional hour format not A.BB format !!
    final_df['social_hours'] = final_df['social_mins'] / 60
    final_df['quality_hours'] = final_df['quality_mins'] / 60
    final_df['day_type'] = final_df['holiday'].map({1: 'Holiday', 0: 'Workday'})
    
    return final_df

#Using the Function
df = CombineDATA() 

# Save processed data as CSV to ./DATA folder
df.to_csv('./DATA/processed_media_data.csv', index=False)
print("Data processing complete. Saved to 'processed_media_data.csv'")

# Display Frame
print("\nProcessed Data Frame")
display(df)


#Visulize Combined Dataframe
#Discard holiday column for visualization
numeric_cols = df.select_dtypes(include=[np.number]).columns.drop(['holiday'])

#Diffrent color pallete for diffrent day types
day_palette = {'Holiday': '#FF7F0E', 'Workday': '#1F77B4'}

plt.figure(figsize=(15, 5))

#Group the data by day type
Df_mean = df.groupby('day_type')[numeric_cols].mean().T.reset_index()

#  Arranged 
Df_mean = Df_mean.melt(id_vars='index', var_name='day_type', value_name='mean')

#Create double bar plot
sns.barplot(x='index', y='mean', hue='day_type', data=Df_mean,palette=day_palette)
plt.title("Mean Values by Day Type")
plt.xlabel("")
plt.ylabel("Mean Value")
plt.xticks(rotation=45)
plt.legend(title="Day Type")
plt.tight_layout()
plt.show()


print(
'''
First Hypothesis Test: 

Null Hypothesis (H₀): There is no meaningfull connection between my Quality Media Consumption and Social media consumption (X₀ = Xₐ)
Alternative Hypothesis (Hₐ): There is a meaningfull connection between Quality Media consumption and Social media consumption (X₀ != Xₐ)

Default signifigance level: 0.05 (For All Hypothesis Tests)
''')
#Create Dataframes Based on total social and quality media usage
social_hours = df['social_hours']
quality_hours = df['quality_hours']

#Display general statistics
print("\nSocial Media Consumption analysis throughout 21 days")
display(social_hours.describe())
print("\nQuality Media Consumption analysis throughout 21 days")
display(quality_hours.describe())

#Visulization of Dataframes
print("\nTotal Hours Visiualize:")

#Create a Boxplot to visualize the distribution of social and quality media hours
plt.figure(figsize=(15, 5))
sns.boxplot(data=pd.DataFrame({'Social': social_hours, 'Quality': quality_hours}))
plt.title("Overall Distribution")
plt.ylabel("Hours")
plt.show()

#Correlation Analysis and hypothesis test
corr, p_val = stats.pearsonr(social_hours, quality_hours)

print(f"Pearson r: {corr:.3f}")
print(f"p-value: {p_val:.4f}")

#Print appropriate message based on p-value
if p_val < 0.05:
  print("Reject the null hypothesis (H₀): There is a significant correlation between social and quality media consumption.") 
else:  
  print("Fail to reject the null hypothesis (H₀): No significant correlation between social and quality media consumption.")



#Visualization Regplot
plt.figure(figsize=(15, 5))
plt.subplot(1, 2, 1)
sns.regplot(x='social_hours', y='quality_hours', data=df, scatter_kws={'alpha':0.5}, line_kws={'color':'red'})
plt.title(f"r = {corr:.2f}, p = {p_val:.3f}")
plt.xlabel("Social Media Hours")
plt.ylabel("Quality Media Hours")



#Randomization distribution
#Randomization List calculate pearson for shuffled then append 
rando_list = []
for i in range(1000):
    shuffled = df['quality_hours'].sample(frac=1).reset_index(drop=True)
    x, i = stats.pearsonr(df['social_hours'], shuffled)
    rando_list.append(x)
    
#randomization distribution visualization histogram with a line 
plt.subplot(1, 2, 2)
sns.histplot(rando_list, kde=True)
#Highlight the observed correlation
plt.axvline(x=corr, color='red', linestyle='--')
plt.title("Randomization Distribution (H₀)")
plt.xlabel("Correlation Coefficient")
plt.tight_layout()
plt.show()

#Format dat column
df['date1'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
print('''
Second Hypothesis Test:

Null Hypothesis (H₀): There is no meaningfull connection between my Quality Media Consumption and Day Type (X₀ = Xₐ)
Alternative Hypothesis (Hₐ): There is a meaningfull connection between Quality Media consumption and Day Type (X₀ != Xₐ)

''')

#Create Dataframes Based on Day Type
holiday_quality = df[df['day_type'] == 'Holiday']['quality_hours']
workday_quality = df[df['day_type'] == 'Workday']['quality_hours']
#Display general statistics
print("Holiday Quality Media Consumption analysis throughout 21 days")
display(holiday_quality.describe())
print("Workday Quality Media Consumption analysis throughout 21 days")
display(workday_quality.describe())





# T-test 
t_stat, p_val = stats.ttest_ind(holiday_quality, workday_quality)
print("T-test results:")
print(f"p-value: {p_val:.4f}")

if p_val < 0.05:
  print("\nReject the null hypothesis (H₀): There is a meaningfull connection between Quality Media consumption and Day Type (X₀ != Xₐ)") 
else:  
  print("\nFail to reject the null hypothesis (H₀):There is no meaningfull connection between Quality Media consumption and Day Type (X₀ = Xₐ)")


print("\nSecond Hypothesis Visualization:")
#Visulization of second Hypothesis's Dataframe boxplot and barplot
plt.figure(figsize=(15, 5))
plt.subplot(1, 2, 1)
sns.boxplot(x='day_type', y='quality_hours', data=df, order=['Holiday', 'Workday'])
plt.title("Quality Media by Day Type")
plt.xlabel("")
plt.ylabel("Hours")

plt.subplot(1, 2, 2)
day_order = df.sort_values('date1')['date1'].dt.strftime('%d-%m')
sns.barplot(x=day_order, y='quality_hours', hue='day_type', data=df, dodge=False, palette=['#1f77b4', '#ff7f0e'])
plt.title("Daily Quality Media Hours by Day Type")
plt.xlabel("Date")
plt.ylabel("Hours")
plt.xticks(rotation=45)
plt.legend(title="Day Type")

plt.tight_layout()
plt.show()

#T-test visulization 
print("\nT-test Visualization:")
plt.figure(figsize=(15, 5))

degreesOfreedom = len(holiday_quality) + len(workday_quality) - 2  # Degrees of freedom
x = np.linspace(-4, 4, 500)
# T-distribution 
y = stats.t.pdf(x, degreesOfreedom)
plt.plot(x, y, label='t-distribution')

# Critical region
# Two-tailed at α=0.05
critical = stats.t.ppf(0.975, degreesOfreedom)  
# Fill the critical region
plt.fill_between(x[x > critical], y[x > critical], color='red', alpha=0.3, label='Critical Region')
plt.fill_between(x[x < -critical], y[x < -critical], color='red', alpha=0.3)
# Highlight the observed t-statistic
plt.axvline(t_stat, color='black', linestyle='--', label=f'Observed t = {t_stat:.2f}')
plt.title(f"T-distribution (df={degreesOfreedom})\np-value = {p_val:.4f}")
plt.xlabel("t-value")
plt.ylabel("Density")
plt.legend()
plt.tight_layout()
plt.show()

print('''
Third Hypothesis Test:

Null Hypothesis (H₀): There is no meaningfull connection between my Social Media Consumption and Day Type (X₀ = Xₐ)
Alternative Hypothesis (Hₐ): There is a meaningfull connection between Social Media consumption and Day Type (X₀ != Xₐ)

''')
#Create Dataframes Based on Day Type and social hours
holiday_social = df[df['day_type'] == 'Holiday']['social_hours']
workday_social = df[df['day_type'] == 'Workday']['social_hours']

print("Holiday Social Media Consumption analysis throughout 21 days")
display(holiday_social.describe())
print("Workday Social Media Consumption analysis throughout 21 days")
display(workday_social.describe())
##DF Visulization boxplot and barplot
plt.figure(figsize=(15, 5))
plt.subplot(1, 2, 1)
sns.boxplot(x='day_type', y='social_hours', data=df, order=['Holiday', 'Workday'])
plt.title("Social Media by Day Type")
plt.xlabel("")
plt.ylabel("Hours")


plt.subplot(1, 2, 2)
day_order = df.sort_values('date1')['date1'].dt.strftime('%d-%m')
sns.barplot(x=day_order, y='social_hours', hue='day_type', data=df,dodge=False, palette=['#1f77b4', '#ff7f0e'])
plt.title("Daily Social Media Hours by Day Type")
plt.xlabel("Date")
plt.ylabel("Hours")
plt.xticks(rotation=45)
plt.legend(title="Day Type")

plt.tight_layout()
plt.show()


# T-test
t_stat, p_val = stats.ttest_ind(holiday_social, workday_social)

print("T-test results:")
print(f"p-value: {p_val:.4f}")

if p_val < 0.05:
  print("\nReject the null hypothesis (H₀): There is a meaningfull connection between Social Media consumption and Day Type (X₀ != Xₐ)") 
else:  
  print("\nFail to reject the null hypothesis (H₀):There is no meaningfull connection between Social Media consumption and Day Type (X₀ = Xₐ)")

#Third Hypothesis visulization
#T-Distrubution same as second hypothesis just with difrent observed data
print("\nT-test Visualization for Social Media:")
plt.figure(figsize=(15, 5))
degreesOfreedom = len(holiday_social) + len(workday_social) - 2  
x = np.linspace(-4, 4, 500)
y = stats.t.pdf(x, degreesOfreedom)
plt.plot(x, y, label='t-distribution')

#
critical = stats.t.ppf(0.975, degreesOfreedom)  
plt.fill_between(x[x > critical], y[x > critical], color='red', alpha=0.3, label='Critical Region (p<0.05)')
plt.fill_between(x[x < -critical], y[x < -critical], color='red', alpha=0.3)
plt.axvline(t_stat, color='black', linestyle='--', label=f'Observed t = {t_stat:.2f}')
plt.title(f"T-test Results (df={degreesOfreedom})\np-value = {p_val:.4f}")
plt.xlabel("t-value")
plt.ylabel("Probability Density")
plt.legend()

plt.tight_layout()
plt.show()

print('''
Fourth Hypothesis Test:

Null Hypothesis (H₀): Difrent platforms does not effect quality media usage (U1 = U2 = U3 )
Alternative Hypothesis (Hₐ): Diffrent platforms does effect quality media usage (Any diffrent)

''')
# Prepare platform data 
platforms = pd.melt(df,id_vars=['date', 'quality_hours'],value_vars=['youtube_phone_mins', 'youtube_ipad_mins', 'instagram_mins', 'reddit_mins'],var_name='platform',value_name='usage_mins')

platforms['usage_hours'] = platforms['usage_mins'] / 60

# Discard Days without usage 
platforms = platforms[platforms['usage_hours'] > 0]

groups = [platforms[platforms['platform'] == 'youtube_phone_mins']['quality_hours'],platforms[platforms['platform'] == 'youtube_ipad_mins']['quality_hours'],platforms[platforms['platform'] == 'instagram_mins']['quality_hours'],platforms[platforms['platform'] == 'reddit_mins']['quality_hours']] 

# ANOVA Test
anova_result= stats.f_oneway(*groups) # Use * to unpack the list into arguments
print(f"p-value: {anova_result.pvalue}")

if p_val < 0.05:
  print("\nReject the null hypothesis (H₀): Diffrent platforms does effect quality media usage") 
else:  
  print("\nFail to reject the null hypothesis (H₀):Difrent platforms does not effect quality media usage")


# Visualization
print("\nFourth Hypothesis Visualization:")

plt.figure(figsize=(15, 5))
platform_order = ['youtube_phone_mins', 'youtube_ipad_mins', 'instagram_mins', 'reddit_mins']
sns.boxplot(x='platform', y='quality_hours', data=platforms, order=platform_order)
plt.title("Quality Media Hours by Platform")
plt.xlabel("Platform")
plt.ylabel("Quality Media Hours")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#ML Methods application
print("\n ML Method applications")

# Import required ML libraries
from sklearn.preprocessing import StandardScaler #scaling countinous ones
from sklearn.model_selection import cross_val_score, KFold, cross_val_predict
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# encode with day type binary encoding used due to having binary classification
df['day_type_encoded'] = df['day_type'].map({'Workday': 0, 'Holiday': 1})

#scaling the numerical features 
num_features = ['youtube_phone_mins', 'instagram_mins', 'reddit_mins', 'comics_mins', 'games_mins']
scaler = StandardScaler()
df[num_features] = scaler.fit_transform(df[num_features])


#Define features and targets
features = ['day_type_encoded'] + num_features

# Verify all features exist
X = df[features]
y_social = df['social_hours']
y_quality = df['quality_hours']

#Setup Cross validation 

cv = KFold(n_splits=5, shuffle=True, random_state=42)

#KNN parameter tuning 
print("\nTuning k for kNN models")

k_values = range(1, 16)

# Find best k for social hours
knn_cv_scores_social = []
print("Tuning for social hours")
for k in k_values:
    
  model = KNeighborsRegressor(n_neighbors=k)
  scores = cross_val_score(model, X, y_social, cv=cv, scoring='neg_mean_squared_error')
  knn_cv_scores_social.append(-np.mean(scores))
    

# Find best k for quality hours
knn_cv_scores_quality = []
print("Tuning for quality hours")
for k in k_values:
    
  model = KNeighborsRegressor(n_neighbors=k)
  scores = cross_val_score(model, X, y_quality, cv=cv, scoring='neg_mean_squared_error')
  knn_cv_scores_quality.append(-np.mean(scores))


best_k_social = k_values[np.nanargmin(knn_cv_scores_social)] 
best_k_quality = k_values[np.nanargmin(knn_cv_scores_quality)]

print(f"\nOptimal k for social hours: {best_k_social}")
print(f"Optimal k for quality hours: {best_k_quality}")

# Plot results
plt.figure(figsize=(15, 6))

# Social hours plot
plt.subplot(1, 2, 1)
plt.plot(k_values, knn_cv_scores_social, 'bo-')
plt.axvline(x=best_k_social, color='r', linestyle='--')
plt.xlabel('Number of Neighbors (k)')
plt.ylabel('Mean Squared Error')
plt.title(f'kNN Tuning for Social Hours (Best k={best_k_social})')
plt.grid(True)

# Quality hours plot
plt.subplot(1, 2, 2)
plt.plot(k_values, knn_cv_scores_quality, 'go-')
plt.axvline(x=best_k_quality, color='r', linestyle='--')
plt.xlabel('Number of Neighbors (k)')
plt.ylabel('Mean Squared Error')
plt.title(f'kNN Tuning for Quality Hours (Best k={best_k_quality})')
plt.grid(True)

plt.tight_layout()
plt.show()

#Random Forest Parameter Tuning

print("\nTuning Random Forest for Social Hours")
rf_depths = [3, 5, 7, 10]
n_estimators = [50, 100, 150]
results_social = {}

for d in rf_depths:
    for n in n_estimators:
        rf = RandomForestRegressor(max_depth=d, n_estimators=n, random_state=42)
        score = cross_val_score(rf, X, y_social, cv=cv, scoring='neg_mean_squared_error').mean()
        results_social[(d, n)] = -score

#Find best combination for social hours
best_rf_social = min(results_social, key=results_social.get)
print(f"Best RF for Social: depth={best_rf_social[0]}, n_est={best_rf_social[1]} Best CV MSE: {results_social[best_rf_social]:.2f}")

#Tune Random Forest for Quality Hours
print("Tuning Random Forest for Quality Hours")
results_quality = {}

for d in rf_depths:
    for n in n_estimators:
        rf = RandomForestRegressor(max_depth=d, n_estimators=n, random_state=42)
        score = cross_val_score(rf, X, y_quality, cv=cv, scoring='neg_mean_squared_error').mean()
        results_quality[(d, n)] = -score
        

# Find best combination for quality hours
best_rf_quality = min(results_quality, key=results_quality.get)
print(f"Best RF for Social: depth={best_rf_quality[0]}, n_est={best_rf_quality[1]} Best CV MSE: {results_quality[best_rf_quality]:.2f}")

####
#Initialize models
models = {
    "Linear Regression": LinearRegression(),
    "k-Nearest Neighbors (Social)": KNeighborsRegressor(n_neighbors=best_k_social),
    "k-Nearest Neighbors (Quality)": KNeighborsRegressor(n_neighbors=best_k_quality),
    
    "Random Forest (Social)": RandomForestRegressor(max_depth=best_rf_social[0] ,n_estimators= best_rf_social[1], random_state=42),
    "Random Forest (Quality)": RandomForestRegressor(max_depth=best_rf_quality[0] ,n_estimators= best_rf_quality[1], random_state=42)
}

#Evaluate models for both targets
results = []
for model_name, model in models.items():
    model_results = {'Model': model_name}
    
    # Evaluate for social hours
    
    social_preds = cross_val_predict(model, X, y_social, cv=cv)
    social_rmse = np.sqrt(mean_squared_error(y_social, social_preds))
    model_results.update({
        'Social RMSE': f"{social_rmse:.2f} hours"
    })
    
    # Evaluate for quality hours
    
    quality_preds = cross_val_predict(model, X, y_quality, cv=cv)
    quality_rmse = np.sqrt(mean_squared_error(y_quality, quality_preds))
    model_results.update({
        'Quality RMSE': f"{quality_rmse:.2f} hours"
    })
    
    results.append(model_results)

#Print results table
results_df = pd.DataFrame(results)
display(results_df)


#Visualize predictions (Linear Regression)

print("\nVisualizing Linear Regression predictions")
model = LinearRegression()
model.fit(X, y_social)
y_social_pred = model.predict(X)

model.fit(X, y_quality)
y_quality_pred = model.predict(X)

plt.figure(figsize=(15, 6))

# Social hours plot
plt.subplot(1, 2, 1)
plt.scatter(y_social, y_social_pred, alpha=0.6, color='blue')
plt.plot([0, y_social.max()], [0, y_social.max()], 'k--', lw=2)
plt.xlabel("Actual Social Hours", fontsize=12)
plt.ylabel("Predicted Social Hours", fontsize=12)
plt.title("Social Hours Prediction (Linear Regression)", fontsize=14)

# Quality hours plot
plt.subplot(1, 2, 2)
plt.scatter(y_quality, y_quality_pred, alpha=0.6, color='green')
plt.plot([0, y_quality.max()], [0, y_quality.max()], 'k--', lw=2)
plt.xlabel("Actual Quality Hours", fontsize=12)
plt.ylabel("Predicted Quality Hours", fontsize=12)
plt.title("Quality Hours Prediction (Linear Regression)", fontsize=14)

plt.tight_layout()
plt.show()

#Visualize Random Forest

print("\nVisualizing Random Forest predictions")

#Create and fit models using the best parameters
rf_social = RandomForestRegressor(max_depth=best_rf_social[0],n_estimators=best_rf_social[1],random_state=42)
rf_social.fit(X, y_social)
y_social_pred_rf = rf_social.predict(X)

rf_quality = RandomForestRegressor(max_depth=best_rf_quality[0],n_estimators=best_rf_quality[1],random_state=42)
rf_quality.fit(X, y_quality)
y_quality_pred_rf = rf_quality.predict(X)


plt.figure(figsize=(15, 6))

# Social hours plot
plt.subplot(1, 2, 1)
plt.scatter(y_social, y_social_pred_rf, alpha=0.6, color='blue')
plt.plot([0, y_social.max()], [0, y_social.max()], 'k--', lw=2)
plt.xlabel("Actual Social Hours", fontsize=12)
plt.ylabel("Predicted Social Hours", fontsize=12)
plt.title(f"Social Hours Prediction (Random Forest)\ndepth={best_rf_social[0]}, trees={best_rf_social[1]}", fontsize=14)

# Quality hours plot
plt.subplot(1, 2, 2)
plt.scatter(y_quality, y_quality_pred_rf, alpha=0.6, color='green')
plt.plot([0, y_quality.max()], [0, y_quality.max()], 'k--', lw=2)
plt.xlabel("Actual Quality Hours", fontsize=12)
plt.ylabel("Predicted Quality Hours", fontsize=12)
plt.title(f"Quality Hours Prediction (Random Forest)\ndepth={best_rf_quality[0]}, trees={best_rf_quality[1]}", fontsize=14)

plt.tight_layout()
plt.show()
