# PNP
### Запуск
#####* Для того чтобы скачать твиты
python main.py tw save_period_seconds path_to_folder 

где: save_period_seconds - время, через которое информация о твиттах будет сохраняться в path_to_folder/Y_D_M_h_m

например 

python main.py tw 3600 data/twitter



#####* Для того чтобы скачать новости
main.py news sleep_time iter_to_save folder_path

где: 
sleep_time - время, через которое новости будут скачиваться, iter_to_save - количество скачиваний до того, как оно будет сохранено в path_to_folder/Y_D_M_h_m

например
news 3600 4 data/news

