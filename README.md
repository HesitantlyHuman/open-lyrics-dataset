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
To collect the data required for our analysis, we have been using two sources: Spotify and Genius. From Spotify, we collected metrics about a song’s performance in the public sphere. As the service is very popular and widely used, we expected that the users on this platform are representative of the music consumer population as a whole. While Spotify is the best source for this data, we do recognize that the age of Spotify users is heavily skewed towards young people, and that young people will engage primarily with more recent music. 
Genius houses a large library of annotated lyrics, complete with genre tags. While the breadth of songs held on Genius is quite large (25 million) it is not as expansive as the Spotify library (30 million). We expected that most songs which can be found on Genius are also on the Spotify platform, but not necessarily the reverse. This ended up being the case on a variety of songs (14391). Therefore we will use Genius as our primary source of data.
(Update this to reflect the true process) The process will proceed as follows: First, we will select a song at random from all songs on Genius, and collect the song title, lyrics, and genres labels. Next, using the Genius API, we will get the Spotify song url, and proceed to collect the number of listens, and the Spotify hotness (a time weighted listens value). 
After repeating this process many times, we will have a database of approximately 100,000 songs with their genres, lyrics and popularity metrics. 

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


