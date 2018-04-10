import spotipy
import spotipy.util as util
import random
#from ConfigParser import SafeConfigParser

class User():
	def __init__(self):
		#parser = SafeConfigParser() #Reads config.ini file for API keys
		#parser.read("config.ini")
		self.CLIENT_ID = '7e7adeea0cb14c149c605989a61259a7'
		self.CLIENT_SECRET = '98e1ab5c21774f64babdd62383d98e98'
		self.REDIRECT_URI = 'http://localhost:8888/callback'
		self.SCOPE = "playlist-read-private playlist-modify-private playlist-read-collaborative playlist-modify-public" #Allows program to access/edit private and public playlists
		self.sp = self.getUser() #Creates Spotify Instance
		self.id = self.sp.me()['id'] #Gets ID of authenticating user

	def getUser(self):
		"""Creates Spotify instance for Authenticating User"""
		token = self.getUserToken()
		sp = spotipy.Spotify(auth=token)
		sp.trace = False
		return sp

	def getFeatures(self, trackID):
		"""Retrieves Audio features for a track"""
		features = self.sp.audio_features(track)
		return features

	def getPlaylist(self):
		"""Retrieves all playlists from user, then allows user to select one"""
		results = self.sp.current_user_playlists()
		for i, item in enumerate(results['items']):
			print ("{number} {name}".format(number=i, name=item['name'].encode('utf8'))) #Prints out the name of each playlist, preceded by a number

		choice = input("Please choose a playlist number: ")
		return results['items'][int(choice)]['id']

	def getSongs(self, playlistID):
		"""Gets all songs from a chosen playlist, returns a lsit of all song ids"""
		results = self.sp.user_playlist_tracks(self.id,playlist_id)
		tracks = results['items']
		song_ids = []
		while results['next']:
			results = self.sp.next(results)
			tracks.extend(results['items'])
		for song in tracks:
			song_ids.append(song['track']['id'])
		return song_ids

	def getUserToken(self):
		"""Gets authentication token from user"""
		name = input("Please enter your username: ")
		token = util.prompt_for_user_token(username=name,scope=self.SCOPE, client_id=self.CLIENT_ID, client_secret=self.CLIENT_SECRET, redirect_uri=self.REDIRECT_URI)
		return token

	def getRelatedArtistsIDs(self, artistID):
    '''Gets IDs for artists related to the user's chosen artist'''
		allArtists=[artistID]
		items=self.sp.artist_related_artists(artistID)
		artists=items['artists']
		for i in range(len(artists)):
			allArtists.append(artists[i]['uri'])
		return allArtists
		
	def getAlbumsByArtist(self, artistID):
  '''Gets all albums by the input artist'''
		items=self.sp.artist_albums(artistID,album_type='album', country=None, limit=20, offset=0)
		albums=items['items']
		return albums

	def getTracksByAlbum(self,albumID):
  '''Gets all tracks on the input album'''
		items=self.sp.album_tracks(albumID,limit=50,offset=0)
		tracks=items['items']
		return tracks
	
	def getRandomSongs(self,tracksIDs):
		pass


	def createPlaylist(self, title, tracks):
		playlist = self.sp.user_playlist_create(self.id, title, False)
		for track in tracks:
			self.sp.user_playlist_add_tracks(self.id, playlist['id'], [track])


	def main(self):
		#playlist = self.getPlaylist()
		searchedArtist=input("Pick an artist:")
		artistsIDs = self.sp.search(q='artist:' + searchedArtist, type='artist')
		artist=artistsIDs['artists']['items']
		relatedArtistsIDs=self.getRelatedArtistsIDs(artist[0]['uri'])
		#albumsIDs=self.getAlbumsByArtist(relatedArtistsIDs[0])
		#tracks=self.getTracksByAlbum(albumsIDs[0]['uri'])

		for i in range(len(relatedArtistsIDs)):
			albumsIDs=self.getAlbumsByArtist(relatedArtistsIDs[i])
			for k in range(len(albumsIDs)):
				tracks=self.getTracksByAlbum(albumsIDs[k]['uri'])
				for j in range(len(tracks)):
					print(tracks[j]['name'])
		


#ask for artist, check artists discogrophy
#find related artists, check related discogrophy

if __name__ == "__main__":
	SpotifyUser = User()
	SpotifyUser.main()




