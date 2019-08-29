"""

"""
import numpy as np
import pandas as pd
import unidecode


def myHash(s):
	d = dict()
	s2 = standardizeString(s)

	for c in s2:
		if c in d:
			d[c] += 1
		else:
			d[c] = 1

	l = []
	for k, v in d.items():
		for i in range(v):
			l.append(k)

	return hash(tuple(sorted(l)))


def standardizeString(s):
	sb = ""
	sa = unidecode.unidecode(s)

	for c in sa:
		if c in ('-', "'", ' '):
			c = ""
		sb += c

	return sb.upper()


class Person(object):
	def __init__(self, name, surname, mail):
		self.name = str(name)
		self.surname = str(surname)
		self.mail = str(mail)

	def __hash__(self):
		if type(self.surname) != str or type(self.name) != str or type(self.mail) != str:
			return -1
		return myHash(self.name + self.surname)

	def __eq__(self, other):
		# return self.name == other.name and self.surname == other.surname and self.mail == other.mail # For dict
		return self.__hash__() == other.__hash__()

	def __str__(self):
		if self.mail is not None:
			return "{} {} : {}".format(self.surname, self.name, self.mail)
		return "{} {}".format(self.surname, self.name)

	def __repr__(self):
		return self.__str__()


class All(object):
	def __init__(self, persons=None, mails=None, name=None):
		self.persons = dict() if persons is None else persons
		self.mails = set() if mails is None else set(mails)
		self.name = "" if name is None else name
		self.untraited = []

	def add(self, person):
		if person in self.persons:
			self.persons[person].append(person)
		else:
			self.persons[person] = [person]

	def remove(self, mails):
		toDel = []
		for k, vs in self.persons.items():
			for i in range(len(vs)-1, -1, -1):
				if vs[i].mail in mails:
					self.persons[k].pop(i)

					if len(self.persons[k]) == 0:
						toDel.append(k)

		for k in toDel:
			del self.persons[k]

		for mail in mails:
			if mail in self.mails:
				self.mails.remove(mail)

	def loadAlice(self, file, name=19, surname=20, mail=13, condi=None):
		parsed = pd.ExcelFile(file).parse()

		for row in parsed.itertuples(index=False):
			if (condi is None) or (condi is not None and condi(row)):

				if row[name] is not np.nan and row[surname] is not np.nan and row[mail] is not np.nan:
					self.add(Person(row[name], row[surname], row[mail]))

				elif row[mail] is not np.nan:
					self.mails.add(row[mail])

				else:
					self.untraited.append(list(row))
			else:
				self.untraited.append(list(row))

	def loadTxt(self, file, mailOnly=False):
		with open(file, "r") as r:
			data = r.read()

		if mailOnly:
			self.mails = set(data.split("\n"))

		else:
			for row in data.split("\n"):

				if ":::" in row:
					self.add(Person(*row.split(":::")))

				else:
					self.mails.add(row)

	def toDF(self):
		return pd.DataFrame([(p.name, p.surname, p.mail) for p in self.persons], columns=[
			"Name",
			"Surname",
			"Mail"
		])

	def toXl(self, filename):
		if not filename.endswith(".xlsx"):
			filename += ".xlsx"

		writer = pd.ExcelWriter(filename, engine='xlsxwriter')
		self.toDF().to_excel(writer, "Feuille 1")
		sheet = writer.sheets["Feuille 1"]

		for letter in ("A", "B", "C"):
			sheet.set_column("{}:{}".format(letter, letter), 30)

		writer.save()

	def toTxt(self, filename, mailOnly=False):
		if not filename.endswith(".txt"):
			filename += ".txt"

		l = []

		if mailOnly:
			for k in self.persons:
				for person in self.persons[k]:
					l.append(person.mail)

		else:
			for k in self.persons:
				for person in self.persons[k]:
					l.append(person.name + ":::" + person.surname + ":::" + person.mail)

		l += self.mails

		with open(filename, "w") as w:
			w.write("\n".join(l))

	def countP(self):
		i = 0
		for v in self.persons.values():
			i += len(v)
		return i

	def countM(self):
		return len(self.mails)

	def countU(self):
		return len(self.untraited)

	def __contains__(self, item):
		if type(item) == str:
			for m in self.mails:
				if m == item:
					return True

			for vs in self.persons.values():
				for v in vs:
					if v.mail == item:
						return True

			return False

		return item in self.persons

	def __eq__(self, other):
		return self.persons == other.persons and self.mails == other.mails

	def __str__(self):
		c = self.count()
		return "Personnes : {} ; Mails Seuls : {} ; Lignes Non Traitees : {} ; Total : {}".format(*c, sum(c))

	def __repr__(self):
		return self.__str__()

	def count(self):
		return self.countP(), self.countM(), self.countU()

	def et(self, other):
		persons = dict()

		for k1, v1 in self.persons.items():
			persons[k1] = list(v1)

		toDel = []

		for k, v in persons.items():
			if k not in other.persons:
				toDel.append(k)

			else:
				vTemp = other.persons[k]

				for i in range(len(persons[k])-1, -1, -1):
					if persons[k][i] not in vTemp:
						persons[k].pop(i)

				if len(persons[k]) == 0:
					toDel.append(k)

		for k in toDel:
			del persons[k]

		return All(persons, self.mails & other.mails)

	def __add__(self, other):
		persons = dict()

		for k1, v1 in self.persons.items():
			persons[k1] = list(v1)

		for k2, v2 in other.persons.items():
			if k2 in persons:
				persons[k2].extend([x for x in v2 if x not in persons[k2]])
			else:
				persons[k2] = v2

		return All(persons, self.mails.union(other.mails))

	def __sub__(self, other):
		persons = dict()

		for k1, v1 in self.persons.items():
			persons[k1] = list(v1)

		for k2, v2 in other.persons.items():

			if k2 in persons:
				for v in v2:
					for i in range(len(persons[k2])-1, -1, -1):
						if persons[k2][i] == v:
							persons[k2].pop(i)

				if len(persons[k2]) == 0:
					del persons[k2]

		return All(persons, self.mails - other.mails)


################ Concret #################
COMPANIES = {
	0 : "Compagnie des experts judiciaires près la Cour d'appel d'Angers",
    1 : "Compagnie des Experts de Justice près la Cour d'Appel de Basse-Terre",
    2 : "Compagnie des experts judiciaires près la Cour d'appel de Besançon",
    3 : "Compagnie d'experts de justice près la Cour d'appel de Bordeaux ",
    4 : "Compagnie des Experts Judiciaires près la Cour d'Appel de Bourges",
    5 : "Compagnie des experts judiciaires près la Cour d'appel de Caen",
    6 : "Compagnie d'experts de justice près la Cour d'appel de Colmar",
    7 : "Compagnie des experts judiciaires près la Cour d'appel de Dijon",
    8 : "Compagnie des experts près la Cour administrative de Douai",
    9 : "Compagnie des experts près la Cour d'appel de Fort-de-France",
    10 : "Compagnie des experts judiciaires près la Cour d'appel de Grenoble",
    11 : "Compagnie des Experts Judiciaires près la Cour d'Appel de Limoges",
    12 : "Compagnie des Experts de Justice de Lyon ",
    13 : "Compagnie des experts de justice près la Cour d'appel de Metz",
    14 : "Compagnie des experts judiciaires près la Cour d'appel de Montpellier",
    15 : "Compagnie des experts judiciaires près la Cour d'appel de Nancy",
    16 : "Compagnie des experts judiciaires près la Cour d'appel de Nîmes",
    17 : "Compagnie des experts judiciaires près la Cour d'appel d'Orléans",
    18 : "Compagnie des experts judiciaires près la Cour d'appel de Pau",
    19 : "Compagnie des experts judiciaires près la Cour d'appel de Poitiers",
    20 : "Compagnie des experts de justice près la Cour d'appel de Reims",
    21 : "Compagnie des experts de justice près la Cour d'appel de Rennes et les tribunaux de son ressort",
    22 : "Compagnie des experts près la Cour d'appel de Rouen",
    23 : "Compagnie des experts judiciaires près la Cour d'appel de Toulouse",
    24 : "Compagnie des experts judiciaires près la Cour d'appel de Versailles",
    25 : "Compagnie Nationale des Experts de Justice Automobile",
    26 : "Compagnie des ingénieurs experts près la Cour d'appel de Paris",
    27 : "Compagnie nationale des ingénieurs diplômés experts près les Cours judiciaires et administratives d'appel",
    28 : "Union des Compagnies d'experts de justice des Alpes Maritimes et du sud-est",
}



def test():
	a = All()
	a.loadAlice("xlToDict/test.xlsx")

	b = All()
	b.loadAlice("xlToDict/m.xlsx", 2, 4, 5, lambda x : x[12] not in COMPANIES.values())

	c = a.et(b)

	return a, b, c


