# Disparity-Between-Customer-Ratings-and-Reviews
This is a project to study if the reviews given by the customers on yelp match are consistent with their numerical ratings and the the ratings the respective hotels are given on websites like Expedia.com, TripAdvisor, etc

Customer reviews have a lot more information about their experience than categorical ratings(Value, Rooms, Cleanliness, Service, etc.), so we intended to study the disparity between caegorical numerical ratings and the sentiment analysis of the customer reviews.

## Data Source
http://times.cs.uiuc.edu/~wang296/Data/

## Work performed in the project
* Obtained Yelp reviews of 200 hotels and performed their sentiment analysis using Semantria for Excel.
* Determined their hotel ids and extracted data from their Yelp profiles to store in MySQL according to the normalized Entity Relationship Model.
* Wrote a Python script to transform the reviews and their sentiment scores into Mongo DB insert statements, then inserted them into Mongo DB using Robo 3T.
* Compared the numerical ratings of hotels with the categorical ratings and sentiment scores of the reviews.

## Conclusion
* Even though most of the hotels have a similar User Rating and Expedia Rating, the sentiments of the reviews often say otherwise.
* Its easier to express the customer experience through reviews, than through ratings, so hotels should focus more on analyzing and responding to reviews for better insights.
