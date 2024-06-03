kubectl apply -f rmqtest.yaml
#kubectl apply -f rmqtest_external.yaml
n=1
while [ $n -lt 80 ]
do
sleep 5
n=`expr $n + 3`
kubectl get deployment -n default rmqtest
kubectl get pods -n default|grep ago
kubectl scale deployment -n default rmqtest --replicas=$n
done
while true
do
kubectl get deployment -n default rmqtest
kubectl get pods -n default|grep ago
sleep 5
done
