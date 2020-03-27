# Lyrical Analysis By Popularity

### Contributors:
Tanner Sims: u1159642 tannerjeffreysims@gmail.com
Ethan Burrows: u1102916 ethandburrows@gmail.com
Lass Omar: u1179231 u1179231@utah.edu

### Project Intro:
This project demonstrates a lower bound for the effect of lyrics on popularity (number of spotify listens) for a given song. To achieve this we utilized a transformer based NLP model on fine tuned word embeddings over a 118,466 word corpus.

### Data Aquisition:
After obtaining all the scraped data from the API, we obtained about 51,000 (Hopefully 100,000) various songs. 

To collect the data required for our analysis, we will be using two sources: Spotify and Genius. From Spotify, we will collect metrics about a song’s performance in the public sphere. As the service is very popular and widely used, we expect that the users on this platform are representative of the music consumer population as a whole. While Spotify is the best source for this data, we do recognize that the age of Spotify users is heavily skewed towards young people, and that young people will engage primarily with more recent music. 
Genius houses a large library of annotated lyrics, complete with genre tags. While the breadth of songs held on Genius is quite large (25 million) it is not as expansive as the Spotify library (30 million). We expect that most songs which can be found on Genius are also on the Spotify platform, but not necessarily the reverse. Therefore we will use Genius as our primary source of data.
(Update this to reflect the true process) The process will proceed as follows: First, we will select a song at random from all songs on Genius, and collect the song title, lyrics, and genres labels. Next, using the Genius API, we will get the Spotify song url, and proceed to collect the number of listens, and the Spotify hotness (a time weighted listens value). 
After repeating this process many times, we will have a database of approximately 100,000 songs with their genres, lyrics and popularity metrics. 

