# Climbing Locals Recommendation System

## The problem

1. Create a recommendation system which analysis a local informed by the user, the grade and type of climb desired, and using this informations, select and shows the results of near climbing spots to be explored.

2. Climbing is practiced in two main modalities, Lead and Boulder. The main difference between both styles is that the first one requires equipments such as rope and harness, and the second one, only a crash pad, which is basically an outdoor matress. Therefore the type of climbing is a very important information to consider when recommending climbing spots.

3. Also, the climbing grade is as important as the type of climbing, because the climber may be not stronger enoght to climb a grade that is higher than the one he is used to. A lower grade, by the other side, may be not challenging enought to the climber. So it is very important to recommend a similar grade than the informed by the user.

## The Dataset

Dataset: A dataset from [8a.nu Beta site](https://www.kaggle.com/dcohen21/8anu-climbing-logbook) is used. Provided by [David Cohen](https://www.kaggle.com/dcohen21) in a sqlite database, it contains information of several Routes (the name used to refer a lead line climbed and which has a register) and Boulders (The name used to refer a boulder line is identic to the type of climbing).
The database has 4 tables, but for this project it was only used two of then, the ascent and the grade tables to create the two datasets needed.

## Data Preparation

The data was prepared according the following steps:

1. Import the tables from sqlit database.

2. Identify and remove the routes and bouders named with a question mark "?".

3. Removed the duplicated itens.

4. To recommend locations, the information of latitude and longitude from each Route or Boulder is needed. The data found on the dataset contains only the city or the country of the climbing spot. These information were used to do a Web Scraping, with a French website, [climbingaway](https://climbingaway.fr/fr/)

5. In the dataset, a climbing type classified with a "0" is related to the routes (lead climbing), and the climbing type classified with a "1" is a boulder. With this information, along with the grade_id of the ascent, is possible to define the grade in a reference system on the grade_results dataset.

6. Two final datasets were saved: The first one with the ascents, grades and locations, and the second one with the grades and reference system for each type of climbing.

The complete process, along with all steps description, may be found on [climb_dataset_cleaning](https://github.com/tiagotakeshi/climb-project/blob/366666ca5b7b974286e3c1e907b927c3ff2a3ebb/files/climb_dataset_cleaning.ipynb)

## Exploratory analysis

The [Sweetviz](https://pypi.org/project/sweetviz/) library is used for the exploratory analysis. It is very useful for a first data analysis, as the Sweetviz generates a report containg some informations and correlations from the dataset. Using this tools it was identified that the dataset has registers with no names, and the results still had names containing "?". Some important characteristics of the dataset were identified:

1. It is an unbalanced dataset, which is expected. The quantity of register in each location, countries and cities is different. Also, there are less spots with hardests grades, and a average grade of difficult will predominant.

2. The unbalanced dataset will affect the result of the recommendation system. It will recommend more precisely climbing spots with more registers and a high variety of grade. So, if the machine learn algorithm uses the best parameters from this location, it will not work for locations with a lower amount of registers and vice versa. It is then necessary to find the best set of parameters that allows the algorithm to recommend climbing spots at locations with higher or at least a minimum quantity of registers.

The complete file with the analysis can be checked as [exploratory_analysis](https://github.com/tiagotakeshi/climb-project/blob/443c2feda1506ffd916955aa58f95cbf2bbdb2cf/files/exploratory_analysis.ipynb).

## Definition of Algorithm Parameters

1. For the idea of a system recommendation based on the grade, location (latitude and longitude) and type of climbing (0 or 1), it was necessary to use a density based algorithm. In this project it was used the [DBSCAN](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html), which consists on the minimum distance between elements (eps parameter) to be considered a neighbor, different of other algorithms that defines a possible center of a cluster and analyse the distance to the points to classify then.   

2. In the analysis, differents sets of eps and minimum samples were tested and analysed by the clusters defined by the algorithm. Two considerations needed to be analysed in this step:
	- If the eps was less than 0.3 the clusters were more precise in the latitude and longitude, but the grade in each cluster were the same for all elements.
	- The minimum samples can not solve the conflict between geo location precision and the limition of the grade in the same cluster.

3. Due this conflict, the parameters chosen were defined by a wide geo location range, in order to get a range of grades 1 or 2 degrees lower and 1 or 2 degrees higher than the informed grade.

To analyze the clusters in a visual way, it was used the [T-SNE](https://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html) tool, which is a dimensional reduction tool.
This tools has a main parameter, the perplexity, that defines the number of nearest neighbors used in other manifold learning algorithms. And it affects the way of the dimensional reduction groups the clusters.
For a better visualization, some sets of perplexity were tested with different numbers of iterations. With this visualization, it was noted that the correct number of iterations  was needed to correctly visualize the clusters.

This process can be check on the [dbscan_cluster](https://github.com/tiagotakeshi/climb-project/blob/8373caa334e6ecf01a74b7430bb583049bbdeb41/files/dbscan_clusters.ipynb).

## The interface and deploy

After the definition of the algorithm parameters, all the information necessary to create the recommendation system was prepared. The interface was made using the [streamlit](https://streamlit.io/#install) and the deploy using [heroku](https://www.heroku.com/about) platform.
The recommendation includes a map, showing the location of the recommendations, the location informed by the user, some statistics about the results and a dataframe with the list of all results. Everything working interactively with the user.

The complete code can be checked [here](https://github.com/tiagotakeshi/climb-project/blob/dfe79661a277c9b462889aa16208a35836ceb3b6/main.py).

This is a initial study of a climbing recommendation system, some of improvements for a future modification includes:
- A larger dataset to include more location and grades results around the world.
- A more precise location reccomendation with variable grades.
- Filters to allow the user to choose between grade and location, with an interactive update on statistics, map and list of results.
- Creation of a checkbox to the algorithm be more accurated to recommend a a specific difficult grade, or a list of grades (the way it works now)
