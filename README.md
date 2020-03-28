# Lyrical Analysis By Popularity

### Contributors:
Tanner Sims: u1159642 tannerjeffreysims@gmail.com,
Ethan Burrows: u1102916 ethandburrows@gmail.com,
Lass Omar: u1179231 u1179231@utah.edu


## Project Progress as of 3/26/20

### Project Intro:
Our interest in this project stems from our love of music. Each of us is a musician, and we have wondered why certain song lyrics are so much better than others. We would like to know how important lyrics are in a song, and gain insight into how one might write better lyrics. Thus, our project revolves around a fundamental question, “Do lyrics matter in a song?”.
Our primary purpose is to investigate the relationship between lyrical content and engagement with a song in the popular sphere. To do this, we will use RNNS and transform models on embedded word features to explore how the popularity of a song correlates with the contextual interdependency of the lyrics. Further, we will attempt to generate specific models which predict the popularity of a song by lyrics within genres. By analyzing genres and their lyrics, we can make predictions about the importance of lyrics within that genre.

### Ethical Considerations:
While we are not utilizing private or sensitive data outside of the public sphere, there are still some ethical implications which arise from the application of such techniques to judge the quality of an individual’s effort, especially when the product is art. Such a tool which evaluates the ‘quality’ of lyrical work and its predictions is not necessarily representative of a song’s artistic merit. If such a tool, geared to increase a raw and speculative metric like the number of Spotify listens, were to be used for measuring the worth of an Artist’s work or career, it might cause unjust devaluing of otherwise capable individuals. If those who manage such artists, such as Record Labels, feel that they should rely on these types of metrics and suggestions entirely, they may require conformity to those standards on the part of the musicians, hampering the diversity of music which they produce.

## DATA:
### Data Aquisition: NEEDS EDIT
To perform the analysis, we need two primary pieces of information for each song in our eventual data set. First, the lyrics, and secondly, we need a measure of the song’s popularity. Since we will be performing a regression it’s important that the measure we use is quantitative, and as continuous as possible. This means measures like top Billboard position are out of the question. While we can kind of interpret ordered data like this as quantitative, there is no information about how much more popular the best song is relative to the second best. In fact, if those songs were released at different times, both of them would have hit the top. We chose the number of listens a song has on the streaming platform Spotify, since this data was available to the general public, and is reasonably continuous. Although you can’t have anything in between integer value numbers of listens, since the numbers tend to be very large, the data is granular relative to its range, and it is very unlikely that two songs have the same number of listens. Spotify also contains a measure called hotness, which their documentation explains is a time weighted measure of listens, among other things. (Read more here) While this could have also been a valid choice, there are two reservations to be had using this measure. Firstly, the method by which they are calculating the hotness is not exposed, so it’s unclear if there are other factors we wouldn’t want to consider. Secondly, since hotness is time weighted, the release date of a song is introduced as a confounding factor. Older songs will naturally suffer, where this might not be reflected in their lyrical content. We believe the model has a greater chance of explaining variability in the number of listens using the lyrics instead.

Unfortunately, Spotify does not contain the lyrics for a song, and so we need an alternate source for that data. To obtain the song lyrics, we chose to use the site Genius, since it houses a large library of various songs and lyrics. Ideally, the larger our source of data, the more it begins to resemble songs as a whole. This is important for maintaining the generalizability of our final model and results.

Beyond those two critical attributes, we would also like to know the title of the song, the artist, as well as the track’s genres. Luckily for us, Genius also contains genre tags for every song, so those can be grabbed along with the lyrics, all in one go.
Both Genius and Spotify are large companies, with large databases and large services. Naturally, they both have extensive and very well documented APIs. Our initial hope was that all of the necessary data could be obtained by querying each API. As it turns out, the data that we wanted to collect, was not exposed in the API: for both services. Genius does not give lyrics or genre, and Spotify does not provide listens. So naturally, we had to turn to scraping.

Genius is relatively easy to scrape. Their service is hosted entirely in html, and every song has its own page. The lyrics are available immediately, and the genre tags are hidden away in some metadata json.
Spotify however, is not that simple. It functions more like an application, and even the web listening service they do have requires a login, and is entirely JavaScript, which is far more difficult to extract data from. Luckily, there is a github user by the name of ___ who has already solved this problem. His project interfaces with the spotify client application, and exposes the number of listens, returning a json file with the data. For more information, please visit his repo here.

At this point, we have all of the components which are required, but we also need a way to ensure that our data set is representative of the music industry as a whole. Beyond collecting as large a dataset as is feasible, we need to select our data points randomly. Luckily for us, Genius uses integers between 0 and 4,000,000 to identify each of the songs in their database. Thus, to select a song, we can generate a random Genius ID between those values. Using the Genius API, we can find the song and scrape its lyrics and genre. Finally, we use the Spotify search API to find the same song within the Spotify database, and then scrape the number of listens and hotness.

This is done by a standalone python script which was run in the command line. The full process is described in more detail in the jupyter notebook found here, and scraping script found here. In total, we collected -- number of unique song data points. The scraping was done over the course of about 2 weeks, off and on, at a rate of about 1200 songs per hour.

### Data Cleanup:
Once the complete dataframe of songs were obtained, in order to analyze the songs based on their lyrics, we needed to remove those that were either non-english or were simply instrumentals. Our model will be based off of english words, and including songs that either contain none nor have any actual lyrics will obviously affect the outcome. To check for english speaking songs, we used the package “langdetect” to check the lyrics within each song and got rid of those that were not english. This was done by using a for loop and using the lyrics column for each song to detect any different languages used. To check for instrumental songs, it is noted that on Spotify, any instrumental songs have their titles noted as, “Instrumental”. 

Similarly for checking a song’s language, we use a for loop and check the title within each song to see if it contains the word, “Instrumental”. Not only that, but we use a try block for each song to see if the lyrics feature any words or not, since a song may or may not contain any phrases or words whatsoever, which is what we want to avoid. After that, we used str.replace() to help remove any unwanted punctuation marks such as exclamation marks, question marks, periods, and other symbols. Since we're gonna analyze each word within our corpus list of words used within every song, we want words like, “love!” and “love?” to be the same word. 

Finally, we needed to remove the words, “Genius” from our genres columns as the various types of music contained the word, “Genius”, which of course sounds really weird to say(R&B Genius doesn’t sound like a popular genre). Thus we once again used str.replace()to remove all the “Genius”’s from the column. Once we had all that done, we had finally cleaned all of the data.


### Exploratory Analysis: NEEDS EDIT
Some Exploratory Statistics include:
- Total number of unique words: 118,466
- Total number of genre/genre combinations: 4,369
- Total number of rejected music songs: 14,391
- Total number of words in the corpus: 9,591,976
- Sample list of genre/genre combinations: ['UK Rap', 'UK', 'Rap Genius'], ['Heavy Metal', 'Thrash Metal', 'Rock Genius', 'Death Metal'], ['Atlanta', 'Trap', 'Rap Genius'], etc..
- Scatter plot of listens by hotness:

## TRAINING:
### Corpus and Embeddings:
While it is standard to use a pre trained embedding without modification in many language tasks, we will be fine tuning our embedding to the dataset. We believe that the use of the English language within songs varies from general use. Within a song, a word can be chosen not just for its meaning, but also its rhythm or cadence. Sometimes a word is chosen with complete disregard for meaning. We expect that fine tuning the embeddings on a corpus of songs will lead to an increased performance in the final model.

Our initial collected corpus consists of a mass amount of song lyrics. This raw corpus introduces issues of special characters in the data set, these special characters have the potential to cause issues with collecting things like a unique word count and word indexing. For example, we do not want two different numeric indexes for “love!” and “love?” because both are composed of the same unique word but in this form will be counted as two seperate unique words. This issue can also be found in similar words where one is capitalized and the other is lower case, to address this problem we made sure to convert the words the corpus to lower case.We proceeded to limit these unique words, as well as splitting the corpus by dashes in order to format our numeric list. This new list maps our refined unique words to a unique numeric value that can be used later in our embedding process and allow for efficient indexing. 

There are many ways to generate an embedding, but most stem from defining a task to be performed, and then training the embedding on that task. For our embedding training we will be using a process called “Continuous Bag of Words” or (CBOW). This method is used by the Word2Vec model, and has proven to result in meaningful embeddings. (For more information, see the bottom of the page) This model predicts our target word by taking in pairs of context and target words. This is then embedded and an average is taken in order to find a target word, this result is then compared to the actual target word and the process continues training. Training however, takes a substantial amount of computing power that our own individual laptops are not capable of. Due to the easy accessibility of the University of Utah’s computing resources we have decided to use the Center for High Performance Computing (for more information, see the bottom of the page) the University of Utah provides to train our embeddings. 

### Analysis:
NOTE: NO analysis has been preformed yet.
The primary model which we will utilize is a Transformer network. This network has excelled experimentally at natural language tasks, and trains quickly in parallel processing situations (read GPU). (Decide whether we will be using multi-headed attention or not)
Additionally, we will train a simple recurrent neural network (RNN) and an long-short-term memory (LSTM) on the dataset, as these will provide a baseline performance for the more complicated Transformer network. The size and parameters of the networks are yet to be determined.
In addition to the recurrent models, we will perform the regression task using even simpler fully connected models. For those which cannot handle data of variable length, we will attempt padding or truncating the lyrical embeddings.

We expect that the main model we will be training for this regression task will be a transformer structure with a fully connected regression head. The training on such a model will be the most time consuming portion of the project. We have chosen the U of U Center for High Performance Computing to undertake this task. Additionally, we will explore utilizing transfer learning from GPT-2 (OpenAI) or BERT (Google), since this would reduce the learning time for our model.

Once the models have been trained on the data, we will cross-validate with a testing set of data to select the most performant model for our regression task. This will become the broad model. We will then refit the model to five selected genres, looking at the performance of these models as an indicator of how important lyrics are within that genre as compared to the general market.

Finally, as an extension of the project, we aim to create the lyric analysis tool described previously. This tool will be able to utilize the general and genre specific models which we will train to identify which lyrics have the greatest negative impact on the final score given by the model. Further, if the genre of the lyrics is one of the five which we select, then a specific model for that genre will be used in place of the general model

### What haven’t we done yet? when?:
As of the Project Milestone benchmark we have collected and cleaned the data, performed preliminary analysis on the song data and we are currently training the embeddings. Our next steps include choosing our pretrained model, this going to be a transformer and a RNN as stated in the intro of this paper. Below is a project schedule for the rest of the semester:

- March 27th: All data collected,  progress embeddings
- March 29th - April 1st: Have clean and explored data, complete embeddings, model types chosen.
- April 2nd: Models created and training of the main model in progress.
- April 9th: Training completed and models evaluated. Begin creating project video.
- April 19th (Entire Project): *Can identify the problematic areas of lyrics using models


