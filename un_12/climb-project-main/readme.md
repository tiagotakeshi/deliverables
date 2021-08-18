# Climbing Locals Recommendation System

## The problem

1. Create a recommendation system which analysis a local informed by the user, the grade and type of climb desired, and using this informations, select and shows the results of near climbing spots to be explored.

2. First of all, the Climbing is a sport that is practiced in two main modalities, Sport and Boulder, and the main difference is that one requires equipments to use a rope and the other a crash pad, that is similar to a matress. So, the information of the type of climbing is very important to recommend the location to the user.

3. Second, the difficult grade is so important as the type of climbing is, because the climber may be not stronger enoght to finish a higher grade than it is used to and otherwise a low grade may be not challenging enought to the climber. So it is very important to recommend a similar Grade informed.

## The Dataset

For this recommendation system is was used a dataset from [8a.nu Beta site](https://www.kaggle.com/dcohen21/8anu-climbing-logbook) provided by [David Cohen](https://www.kaggle.com/dcohen21) who collect information of many Routes (the name used to refer a sport line climbed and which has a register) and Boulders (The name used to refer a boulder line is identic to the type of climbing) and provided in this sqlite database.
The database has 4 tables, but for this project we only used two of then, the ascent and the grade tables to create the two databases needed.

## Data Preparation

The data preparation was made in some steps listed below:

1. Import the tables from sqlit database and saved then.

2. Identify and remove the routes and boulders which has a "?" as the name.

3. Removed the duplicate itens.

4. To recommend locations the dataset needs the information of latitude and longitude from each Route or Boulder, so the dataset only has the information of the route or boulder name and the crag, sometimes the country. With this informations it was possible to do a Web Scraping using a French site to identfy the city and country where each register is located.

5. It was possible to identify that the climb type equal 0 is related to the routes, and the climb type equal 1 is used for boulder, with this information and the grade_id of ascent it is possible to define the grade in a reference system on the grade_results dataset.

6. With all the analysis of necessary columns and itens. It was saved the two final datasets, one with the ascents, grade and location and another with the grades and the reference system os graduation used for each modality.

All the steps are described and the complete process is on [climb_dataset_cleaning](https://github.com/tiagotakeshi/climb-project/blob/366666ca5b7b974286e3c1e907b927c3ff2a3ebb/files/climb_dataset_cleaning.ipynb)

## Exploratory analysis

For the exploratory analysis i used, in my opinion, a library which is really useful for a first impression of the data, the [Sweetviz](https://pypi.org/project/sweetviz/). The Sweetviz can generate a report containg some informations and correlations in the dataset.
Using this tools it was possible to identify that the dataset has registers with no names, and the results still had names containing "?".
After the report it was possible to identify some important characteristics in the dataset:

1. It is a unbalanced dataset, which is expected. The quantity of register in each location, countries and cities will be diffenrent. Not only the location, the grades will be lower for the hardests grades and a mid grade of difficult will be de mean.

2. The unbalenced dataset will affect the result of the recommendation system because, the location with more register, and a larger variaty of grades, will recommend more precisely the results, so if the machine learn algorithm uses the best parameters for this location, it will not work for the location with a lower quantity of register, and the logical is valid for the opposity consideration. So it is necessary to find the best set of parameters for being capable to recommend location with high or at least a minimum quantity of registers.

The complete file with the analysis can be checked as [exploratory_analysis](https://github.com/tiagotakeshi/climb-project/blob/443c2feda1506ffd916955aa58f95cbf2bbdb2cf/files/exploratory_analysis.ipynb).

## Definition of Algorithm Parameters

1. For the idea of a system recommendation based on the grade, location (latitude and longitude) and type of climbing (0 or 1), it was necessary to use a density based algorithm. In this project it was used the [DBSCAN](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html), which consists on the minimum distance between each elements (eps parameter) to be considered a neighbor, different of another algorithms that defines a possible center of a cluster and analyse the distance to the points to classify then.   

2. In the analysis, differents sets of eps and minimum samples was tested and analysed by the clusters defined by the algorithm. Two considerations needed to be analysed in this step:
	- If the eps was less than 0.3 the clusters were more precise in the latitude and longitude, but the grade in each cluster were the same for all elements.
	- The minimum samples can not solve the conflict between geo location precision and the limition of the grade in the same cluster.

3. Due the conflict the parameters chosen were defined by a wide geo location range to be able to get a range of grades and be possible for the climber chose one more difficult or an easier one than the informed grade.

To analyze the clusters in a visual way, it was used the [T-SNE](https://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html) tool, which is a dimensional reduction tool.
This tools has a principal parameter (the perplexity) that defines the number of nearest neighbors used in other manifold learning algorithms. And it affects the way of the dimensional reduction group the clusters.
For a better visualization it was tested some sets of perplexity with different numbers of iterations, with this visualization was possible to noticy that the correct number of iteration was needed to be possible the correct visualization of the cluster.

This process can be check on the [dbscan_cluster](https://github.com/tiagotakeshi/climb-project/blob/8373caa334e6ecf01a74b7430bb583049bbdeb41/files/dbscan_clusters.ipynb).