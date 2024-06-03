kubectl apply -n default -f client.yaml
n=1
while [ $n -lt 60 ]
do
sleep 5
n=`expr $n + 3`
kubectl get deployment -n default tcp-test-client-deployment
kubectl get pods -n default | grep ago
kubectl scale deployment -n default tcp-test-client-deployment --replicas=$n
done
while true
do
kubectl get deployment -n default tcp-test-client-deployment
kubectl get pods -n default | grep ago
sleep 5
done
