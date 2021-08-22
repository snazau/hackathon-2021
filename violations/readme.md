# Выявление несвоевременного или досрочного гашения ВСД
Для работы программы необходимы библиотека pandas и два файла: ‘/data/Certificate_2020_ds_0.txt’ и ‘/data/labels_pretty.csv’. labels_pretty представляет собой обработанный “Разметка_обезличенная.xlsx”.

Файлы можно выкачать по ссылкам:
1. https://hakaton-rosselhoznadzor-2021.s3.eu-central-1.amazonaws.com/data/labels_pretty.csv
2. https://hakaton-rosselhoznadzor-2021.s3.eu-central-1.amazonaws.com/data/Certificate_2020_ds_0.txt

Алгоритм проверяет файл ‘/data/Certificate_2020_ds_0.txt’ и ищет один из следующих вариантов:
1.	repaid_cert_date равняется nan
2.	repaid_cert_date - cert_date сильно отличается от transit_time_hour
3.	repaid_cert_date - cert_date больше определенного значения
4.	repaid_cert_date - cert_date меньше определенного значения
5.	Если id транзакции уже помечен в labels_pretty как нарушитель сроков, то эта транзакция игнорируется. Ищутся только новые нарушения.

Пример вывода программы - список эВСД с нарушениями: 

![time_anomaly](readme_stuff/Screenshot_114.png)