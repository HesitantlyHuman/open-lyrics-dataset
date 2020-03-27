# Lyrical Analysis By Popularity

### Contributors:
Tanner Sims: u1159642 tannerjeffreysims@gmail.com
Ethan Burrows: u1102916 ethandburrows@gmail.com
Lass Omar: u1179231 u1179231@utah.edu


## Project Progress as of 3/26/20

### Project Intro:
This project demonstrates a lower bound for the effect of lyrics on popularity (number of spotify listens) for a given song. To achieve this we utilized a transformer based NLP model on fine tuned word embeddings over a 118,466 word corpus.

### Data Aquisition:
To collect the data required for our analysis, we will be using two sources: Spotify and Genius. From Spotify, we will collect metrics about a song’s performance in the public sphere. As the service is very popular and widely used, we expect that the users on this platform are representative of the music consumer population as a whole. While Spotify is the best source for this data, we do recognize that the age of Spotify users is heavily skewed towards young people, and that young people will engage primarily with more recent music. 
Genius houses a large library of annotated lyrics, complete with genre tags. While the breadth of songs held on Genius is quite large (25 million) it is not as expansive as the Spotify library (30 million). We expect that most songs which can be found on Genius are also on the Spotify platform, but not necessarily the reverse. Therefore we will use Genius as our primary source of data.
(Update this to reflect the true process) The process will proceed as follows: First, we will select a song at random from all songs on Genius, and collect the song title, lyrics, and genres labels. Next, using the Genius API, we will get the Spotify song url, and proceed to collect the number of listens, and the Spotify hotness (a time weighted listens value). 
After repeating this process many times, we will have a database of approximately 100,000 songs with their genres, lyrics and popularity metrics. 

### Data Cleanup:
Once the complete dataframe of songs were obtained, in order to analyze the songs based on their lyrics, we needed to remove those that were either non-english or were simply instrumentals. Our model will be based off of english words, and including songs that either contain none nor have any actual lyrics will obviously affect the outcome. 
To check for english speaking songs, we used the package “Pychant” to check the lyrics within each song and got rid of those that were not english. This was done by using a for loop and using the lyrics column for each song to detect any different languages used. 
To check for instrumental songs, it is noted that on Spotify, any instrumental songs have their titles noted as, “Instrumental”. Similarly for checking a song’s language, we use a for loop and check the title within each song to see if it contains the word, “Instrumental”. Not only that, but we use a try block for each song to see if the lyrics feature any words or not, since a song may or may not contain any phrases or words whatsoever, which is what we want to avoid.
After that, we used str.replace() to help remove any unwanted punctuation marks such as exclamation marks, question marks, periods, and other symbols. Since we're gonna analyze each word within our corpus list of words used within every song, we want words like, “love!” and “love?” to be the same word. Once we have stripped the lyrics of any unwanted punctuation, we have finally cleaned all of the data.
(you can at some point talk about limiting the training load on the embedding)
Once the song and its data have been gathered, we will filter the songs to eliminate non-English songs and remove instrumental tracks. We are limiting our data to English lyrics to minimize the breadth of our final corpus for embedding training.

