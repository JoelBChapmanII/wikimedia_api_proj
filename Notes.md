Internet

Cloudflare <- DNS, WAF, Caching, Some security

AWS Application LB <- SSL

Kubernetes <- Helm chart, Ingress, Deployment, AZA, AZB, AZC, EKS

Monitoring <- Node based monitoring (CPU, Memory, Storage), Latency, Status code, Pod upness,

Looking into latency <- Internet to AWS LB, Inside aws to EKS ingress, Exec into the ingress pod try to hit the pod's service,
exec into the specific application pod and test locally, check external APIs for latency, maybe bring some aspects of the outside API inside the app with caching
