# movie_recommender
Movie recommender system using collaborative filtering in Python. Project for BIL 441.

Clone the project and run `python program.py` in the directory which has `program.py`.

# Seçenekler
## Kullanıcıya En Çok Benzeyen Kullanıcıların Listesi
  Bir hedef kullanıcı ID'si ve k-NN derecesi girildiğinde, seçimleri hedef kullanıcının seçimlerine en çok benzeyen k kullanıcıyı ekrana basar. 
  Dönen listenin formatı: `[kullanıcı ID'si] -> [cosine distance]`
## Kullanıcının Bir Filme Vereceği Reyting Tahmini
  Bir hedef kullanıcı ID'si, bir film ID'si ve hesaplama yapılırken kullanılacak k-NN derecesi girildiğinde, ekrana kullanıcının filme vereceği tahmini reytingi basar. 
  Dönen sonucun formatı: `[kullanıcı ID] ID'li kullanıcının [film ID] ID'li filme vereceği tahmini reyting: [tahmini reyting]`
## Film Önerileri
  Bir hedef kullanıcı ID'si, k-NN derecesi ve önerilmesi istenen film sayısı girildiğinde, ekrana kullanıcıya önerilecek filmlerin listesini basar. 
  Dönen listenin formatı: `[film ID] -> [film adı]`
## Test
  k-NN derecesi ve bir veri seti numarası girildiğinde, o veri setinde yapılan testin MSE değerini ekrana basar. 
  Dönen sonucun formatı: `MSE(kNN =  [k-NN derecesi] , dataset # [veri seti] ): [MSE değeri]`
