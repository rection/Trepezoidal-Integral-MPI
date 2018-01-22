#!/bin/python
#SAFA BAYAR  Ogrenci No: 161906001
#calistirmak icin :  'mpiexec -n 4 python olas.py 0.0 1.0 10000' 
import numpy
from math import sin,pi
from mpi4py import MPI			#Kutuphane tanimlamalari
import sys

comm = MPI.COMM_WORLD
rank = comm.Get_rank()			#Paralellestirmek icin kutuphanedekileri degisken olarak ataniyor.
size = comm.Get_size()

a = float(sys.argv[1])
b = float(sys.argv[2])			#sys.argv[] amaci degisken olarak surekli icerigi degisebilen degerler atanmasini saglayan araclardir.
n = int(sys.argv[3])			#Burada a degeri 1 boyutunda float degeri tasiyan dinamik bir array olusturmasini saglamistir.

def f(x):
        return x*x			#hesaplanacak f(x) degerinin fonksiyonu atanmistir.


def integral(a, b, n):			#integralin formulu olan fonksiyon tanimlanmistir. 3 tane parametreye sahiptir.
	integrals = -(f(a)+f(b))/2.0	#integrals adinda bir degisken tanimlanan a ve b degiskenlerinin f(x) fonksiyonu icinde x*x uygulanip toplanip 2'ye bolunmesi 						#sonrasinda negatif degeri atanmaktadir.
	for x in numpy.linspace(a,b,n+1): #linspace a ve b araliginda n+1 kadar bosluk acmasina yaramaktadir. Array uzerinde dusunursek.
		integrals = integrals + f(x) #sonucta cikan degerlerinde integrals degiskeni sonucunda f(x)'in gercek degeriyle toplanmasidir.f(1) gibi. Formulden geldi
	integrals = integrals * (b-a)/n	   #integrals degiskeni sonucunda gelen deger b ile a cikarilmasi ve n'e bolunmesi sonucunun carpilmasidir. 
	return integrals		#integrals degiskenini dondurmektedir. Yani cagirilmasi sonucu integrals sonucunu vermesi istenecektir.


h = (b-a)/n				#Formulde fonksiyonun kucuk parcalara bolunmesini, kac parcaya bolunecegini hesaplar.

local_n = n/size			#local_n adinda degiskene kac adimda yapilacaginu belirler girilen adim sayisinin cekirdek sayisina bolumudur. Eger tam bolunmez 					#ise sonuc dogru cikmaz.

local_a = a + rank * local_n * h	#local_a degerinde a degeri orjinden ne kadar uzakta baslayacak onu belirtir. rank * local_n * h kisimi fonksiyonun adim sayisi 					#kadar olmasinin local_a degiskenine atanmasini saglar.
local_b = local_a + local_n *h		#local_b degerinde y ekseni olarak dusunursek adim sayisi ile bolunecek cekirdek sayisinin local_a ile toplamidir.
					#Burada ki asil amac bolunmesi sonucu olusan kesitlerin yamuk gibi alinip alanin bulunmasini saglar. Sonucunda cekirdek sayisina					#bolunen islemlerin her cekirdekte ayni sayida islem yapmasini saglar.

integrals = numpy.zeros(1)		#integrals degiskenine, icerisi 0 olan bir diziye sahip ve 1 boyutuna sahip bir dizi olusturulup atanir.
total = numpy.zeros(1)			#total degiskenine, icerisi sifir olan bir diziye sahip ve 1 boyutuna sahip bir dizi olusturulup atanir.

integrals[0] = integral(local_a, local_b, local_n) #integrals dizisi tanimlanir. Fonksiyonun icindeki integrals degeriyle alakasizdir suan boyutu 1 dir. karsidaki fonks						   #fonksiyonun tanimlanmasi ve parametreleri atanmistir. ve bu fonksiyon cagirilmasi sonucu integrals dizisinin icine a						   #atilir. dizi olmasinin sebebi parametrelerden kaynaklanmaktadir.

comm.Reduce(integrals, total, op=MPI.SUM, root=0)  #MPI'in icinde olan basitlestirme yani hepsini bir araya toplamadir. Olmasaydi hepsini cekirdekler icin ayri ayri    						   #tekrar yazmak zorunda kalirdik. integrals bir yukarida tanimli olan degiskendir. total 1 boyutunda dizidir ve 							   #dinamiktir. op degiskenine cekirdeklerden gelen sonuclarin toplanmasini saglayan MPI.SUM kullanilmistir. root 							   # degiskeni ise main olarak atanacak cekirdegi belirler.

if comm.rank == 0:				   #sifirinci  yani main cekirdek atatigimiz degere gelince asagidakini uygula anlamina geliyor. 

	print "n\'nin degeri " ,n , "a nin degeri " , a ," b\'nin degeri",b,"toplami ",total #n hangi bolumlemede oldugunu gostermeke, a ve b degerinde girilen parametl						   #parametreler sonucunda olan cikan sonucu ise total degiskenidir. Sonucu bastirmaktadir.


