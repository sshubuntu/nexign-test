# Задание 2

## Текст задания

> Легенда:  
> Представьте, что нам нужно перенести устаревшее решение с Docker Swarm на современный Kubernetes. В продакшене у нас есть цепочка микросервисов (App1 -> App2 -> App3 -> App4), которые общаются асинхронно через очередь сообщений (Message Broker). Ваша задача — воспроизвести упрощенную версию этой архитектуры в Kubernetes, запустив её локально.
> 
> **Цель задания:**  
> Развернуть в Kubernetes (локальный кластер, например, Minikube, Kind, K3s или MicroK8s) пайплайн из 4 приложений и брокера сообщений, который обрабатывает простое JSON-сообщение.
> 
> **Описание работы**  
> 1. В кластер "внешним образом" отправляется JSON-сообщение: `{"message": "hello, world"}` (например, через kubectl port-forward и curl или через отдельный Pod-отправитель).  
> 2. App1 забирает это сообщение из очереди, логирует факт получения и отправляет его дальше в следующую очередь (для App2).  
> 3. App2 забирает сообщение от App1, логирует и отправляет дальше.  
> 4. App3 и App4 делают то же самое.  
> 5. После прохождения всех 4 приложений факт успешной обработки должен быть где-то зафиксирован (логи конечного приложения или отдельный служебный топик).
> 
> Важно: Сами приложения могут быть максимально простыми (на Python, Go, Node.js или даже bash-скрипты в контейнерах). Сложная бизнес-логика не нужна. Главное — корректная передача сообщения между сервисами через брокер.
> 
> **Технические требования и ограничения**  
> - Инфраструктура: Вся работа должна выполняться локально. Допускается использование Minikube, Kind, K3d или встроенного Kubernetes в Docker Desktop.  
> - Брокер сообщений: На ваш выбор (NATS, RabbitMQ, Kafka, ValKey Pub/Sub). Выбор нужно обосновать.  
> - Приложения: Это могут быть Docker-образы, собранные вами, или вы можете использовать готовые образы с публичных реестров...  
> - Манифесты: Все ресурсы Kubernetes должны быть описаны в манифестах (Deployment, Service, ConfigMap и т.д.). Использование kubectl create "на лету" без сохранения конфигов не допускается.  
> - Хранение: Stateful-компоненты (брокер сообщений) должны использовать PersistentVolume (или emptyDir для упрощения, но знание разницы — плюс).

# Сборка и загрузка образа
```bash
docker build -t app:1.0.3 .
minikube image load app:1.0.3
kubectl create namespace nexign-test
kubectl apply -f ./manifests
```

# Отправить сообщение:
```bash
# Пробросить RabbitMQ Management UI на отдельном терминале
kubectl port-forward -n nexign-test svc/rabbitmq 15672:15672
```
### Через ui
- Открыть в браузере: http://localhost:15672 
- Ввести credits guest, guest
- Открыть start-queue 
- Publish message -> Payload:  {"message":"hello, world"}
### Через curl
```bash
curl -u guest:guest -X POST \
  -H "Content-Type: application/json" \
  -d '{"properties":{},"routing_key":"start-queue","payload":"{\"message\":\"hello, world\"}","payload_encoding":"string"}' \
  http://localhost:15672/api/exchanges/%2F/amq.default/publish
```

# Проверка
```bash
kubectl logs  deployment.apps/app4 -n nexign-test
```

