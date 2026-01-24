# Домашнее задание №6
## Инфраструктурные паттерны (Работа с Helm'ом)

### Вариант 1 (С КОДОМ)

#### Сделать дашборд в Графане, в котором были бы метрики с разбивкой по API методам:

#### Latency (response time) с квантилями по 0.5, 0.95, 0.99, max
#### RPS
#### Error Rate - количество 500ых ответов

#### Добавить в дашборд графики с метрикам в целом по сервису, взятые с nginx-ingress-controller:

#### Latency (response time) с квантилями по 0.5, 0.95, 0.99, max
#### RPS
#### Error Rate - количество 500ых ответов

#### Настроить алертинг в графане на Error Rate и Latency.


#### На выходе должно быть:

#### 0) скриншоты дашборды с графиками в момент стресс-тестирования сервиса. Например, после 5-10 минут нагрузки.

#### 1) json-дашборды.


#### Задание со звездочкой

#### Используя существующие системные метрики из кубернетеса, добавить на дашборд графики с метриками:

#### Потребление подами приложения памяти
#### Потребление подами приолжения CPU

#### Инструментировать базу данных с помощью экспортера для prometheus для этой БД.

#### Добавить в общий дашборд графики с метриками работы БД.

### ПОДГОТОВКА
#### в /etc/hosts прописываем
```
127.0.0.1 arch.homework 
```

#### Запускаем docker
```
любым вариантом, у меня docker desktop с виртуализацией VT-d
```

#### Запускаем minikube
```
minikube start --driver=docker
```

#### Устанавливаем чарт, содержащий Прометея + Графану (и ещё пачку всего, на самом деле...)
```
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install kube-prometheus-stack prometheus-community/kube-prometheus-stack -n monitoring --create-namespace
```

#### Надо обновить конфигу nginx - включить метрики (если они не были включены по умолчанию)
#### Для полной уверенности я бы его переустановил...
##### Сносим старый релиз (если он никуда не делся с прошлых домашек)
```
helm uninstall nginx -n m
```
##### Обновляем репу
```
helm repo update
```
##### Ставим по-новой с обновленным файлом values (и в другой namespace)
```
helm install nginx ingress-nginx/ingress-nginx -n nginx -f ./nginx/nginx_ingress.yaml --create-namespace
```

### СТАВИМ ПРИЛОЖЕНИЕ
##### "Внешняя" поставка секрета в кластер
```
kubectl apply -f ./secret/secret.yaml
```

##### Переходим в директорию с чартом
```
cd ./users-app
```

##### Качаем зависимости
```
helm dependency update
```

##### Возвращаемся в корень
```
cd ../
```

##### Ставимся и ждем, пока установка закончится
```
helm install <имя релиза> users-app
```

##### Включаем (и не закрываем терминал)
```
minikube tunnel
```

##### Проверяем health-check (в новом окне терминала)
```
curl http://arch.homework/health/
```
```
curl http://arch.homework/health
```


### КАК УДАЛИТЬ ПРИЛОЖЕНИЕ
#### Сносим чарт и БД
```
helm uninstall <имя релиза>
```

#### Сносим прометея и графану (при желании)
```
helm uninstall kube-prometheus-stack -n monitoring
```

#### Сносим secret
```
kubectl delete secret users-db-secret
```

#### Сносим PVC, оставшиеся от БД
```
kubectl delete pvc -l app.kubernetes.io/name=users-postgresql,app.kubernetes.io/instance=<имя релиза>
```

#### Сносим PV, оставшиеся от БД (если reclaimPolicy: Retain)
```
kubectl get pv
```
Смотрим вывод, узнаем <имя PV> (к сожалению, меток у него не будет - я проверил)
```
kubectl delete pv <имя PV>
```

#### Удалять мониторинг и Nginx смысла как бы нет

#### Готово!

### GRAFANA
#### Открыть страницу графана
#### Импортировать дашборд из файла HW5_Dashboard-1768658495921.json
#### Импортировать правила алерта из файла alert-rules-1768659201558.json