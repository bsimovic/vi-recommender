class Film:
	def __init__(self, id_, naziv, tagovi):
		self.id_ = id_
		self.naziv = naziv
		self.tagovi = tagovi

class Korisnik:
	def __init__(self, username, likes, tagovi):
		self.username = username
		self.likes = likes
		self.tagovi = tagovi

class Recommender:
	def __init__(self, filmovi, korisnici):
		self.filmovi = filmovi
		self.korisnici = korisnici
		
	def _slicnost(self, u1, u2):
		return len(u1.likes & u2.likes) # velicina preseka skupova lajkova

	def _brojLikes(self, film, slicnosti):
		n = 0
		for s in slicnosti:
			if film.id_ in s[0].likes:
				n += 1
		return n
	
	def _normalizuj(self, preporuke):
		norm = list()
		minimum = min(preporuke, key = lambda x: x[1])
		maksimum = max(preporuke, key = lambda x: x[1])
		
		for i in preporuke:
			if minimum == maksimum:
				norm.append((i[0], 0))
			else:
				norm.append((i[0], (i[1] - minimum[1]) / (maksimum[1] - minimum[1]))) # normalizacija na [0, 1]
		return norm


	def _kolabFilter(self, u, k, n):
		# izracunamo slicnosti
		slicnosti = list()
		for korisnik in self.korisnici:
			if korisnik is not u:
				slicnosti.append((korisnik, self._slicnost(u, korisnik)))
		slicnosti.sort(key = lambda x: x[1], reverse = True)
		slicnosti = slicnosti[:k]

		# nadjemo preporuke
		preporuke = list()
		for film in self.filmovi:
			if film.id_ not in u.likes:
				preporuke.append((film, self._brojLikes(film, slicnosti)))
		preporuke.sort(key = lambda x: x[1], reverse = True)
		
		#--- debug ---
		# for s in slicnosti:
		# 	print(s[0].username + " " + str(s[1]))
		# for p in preporuke[:n]:
		# 	print(p[0].naziv + " " + str(p[1]))
		#-------------

		return preporuke[:n]
	
	def _sadrzajFilter(self, u, n):
		preporuke = list()
		for film in self.filmovi:
			if film.id_ not in u.likes:
				s = 0
				for tag in film.tagovi:
					if tag in u.tagovi:
						s += 1
				# preporuci samo ako se poklapa bar jedan tag
				if s > 0:
					preporuke.append((film, s))
		preporuke.sort(key = lambda x: x[1], reverse = True)

		#--- debug ---
		# for p in preporuke[:n]:
		# 	print(p[0].naziv + " " + str(p[1]))
		#-------------

		return preporuke[:n]


	def recommend(self, username, k, n):
		# nadji korisnika sa datim username
		u = None
		for kor in self.korisnici:
			if kor.username == username:
				u = kor

		if u is None:
			return []

		kolab = self._kolabFilter(u, k, n * 2)
		sadrzaj = self._sadrzajFilter(u, n * 2)

		kombinacija = self._normalizuj(kolab + sadrzaj)
		kombinacija.sort(key = lambda x: x[1], reverse = True)

		# izbacimo duplikate
		preporuke = list()
		for i in kombinacija:
			preporuke.append(i[0])
		preporuke = list(dict.fromkeys(preporuke)) 

		return preporuke[:n]