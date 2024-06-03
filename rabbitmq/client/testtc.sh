#kubectl apply -f rmqtest.yaml
#kubectl apply -f rmqtest_external.yaml
n=1
while [ $n -lt 60 ]
do
sleep 5
n=`expr $n + 3`
kubectl get deployment -n tc-a transcontainer-0.0.0-cde1aa4
kubectl get pods -n tc-a|grep transcontainer-0.0.0-cde1aa4|grep ago
kubectl scale deployment -n tc-a transcontainer-0.0.0-cde1aa4 --replicas=$n
done
while true
do
kubectl get deployment -n tc-a transcontainer-0.0.0-cde1aa4
kubectl get pods -n tc-a|grep transcontainer-0.0.0-cde1aa4|grep ago
sleep 5
done
