# Домашнее задание №6
## Backend for frontends. Apigateway

### Вариант 1 (С КОДОМ)

#### Добавить в приложение аутентификацию и регистрацию пользователей.

### Здесь у нас сервис профилей (бывший сервис пользователей из прошлых ДЗ)


### ПОДГОТОВКА
#### в /etc/hosts прописываем
```
127.0.0.1 arch.homework 
```

#### Запускаем docker
любым вариантом, у меня docker desktop с виртуализацией VT-d

#### Запускаем minikube
```
minikube start --driver=docker
```

#### NGINX
Считам, что с прошлой домашки никуда не ушел из кластеа

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
curl http://arch.homework/health
```


### КАК УДАЛИТЬ ПРИЛОЖЕНИЕ
#### Сносим чарт и БД
```
helm uninstall <имя релиза>
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

#### Готово!
